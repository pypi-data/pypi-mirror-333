"""Functions and utilities to produce features"""

from pathlib import Path
from typing import Dict, Tuple, Union

import geopandas as gpd
import numpy as np
import xarray as xr
from rasterio.crs import CRS
from satio.collections import FolderCollection
from shapely.geometry import Point
from skimage.transform import resize

from veg_workflows.aws import (
    RIO_GDAL_OPTIONS,
    get_bucket_client,
)
from veg_workflows.composite import (
    LoiAnnualCompositesProcessor,
    coords_from_bounds,
    get_loi_weights_params,
    smooth_nan_rescale,
)
from veg_workflows.errors import NoAcquisitionsError
from veg_workflows.io import save_geotiff
from veg_workflows.products import (
    Loi60Collection,
    LsfAnnualCollection,
)


def get_dem(tile, bounds, epsg):
    class DEMCollection(FolderCollection):
        def _filename(self, tile, *args, **kwargs):
            utm = tile[:2]
            return self.folder / utm / f"dem_{tile}.tif"

    dem_path = "/vitodata/vegteam/auxdata/dem/s2grid/20m/"
    dem_coll = DEMCollection(dem_path)
    dem_alt = dem_coll.filter_tile(tile).filter_bounds(bounds, epsg).load()

    return dem_alt


def get_latlon(bounds, epsg, resolution=10, steps=5):
    """
    Returns a lat, lon feature from the given bounds/epsg.

    This provide a coarse (but relatively fast) approximation to generate
    lat lon layers for each pixel.

    'steps' specifies how many points per axis should be use to perform
    the mesh approximation of the canvas
    """

    xmin, ymin, xmax, ymax = bounds
    out_shape = (
        int(np.floor((ymax - ymin) / resolution)),
        int(np.floor((xmax - xmin) / resolution)),
    )

    xx = np.linspace(xmin + resolution / 2, xmax - resolution / 2, steps)
    yy = np.linspace(ymax - resolution / 2, ymin + resolution / 2, steps)

    xx = np.broadcast_to(xx, [steps, steps]).reshape(-1)
    yy = np.broadcast_to(yy, [steps, steps]).T.reshape(-1)

    points = [Point(x0, y0) for x0, y0 in zip(xx, yy)]

    gs = gpd.GeoSeries(points, crs=CRS.from_epsg(epsg))
    gs = gs.to_crs(epsg=4326)

    lon_mesh = gs.apply(lambda p: p.x).values.reshape((steps, steps))
    lat_mesh = gs.apply(lambda p: p.y).values.reshape((steps, steps))

    lon = resize(lon_mesh, out_shape, order=1, mode="edge")
    lat = resize(lat_mesh, out_shape, order=1, mode="edge")

    return lat, lon


def band_composite(
    lcp_annual: LoiAnnualCompositesProcessor,
    band: str,
    resolution: int,
    interpolate: bool = True,
    interpolation_params: Dict = None,
    chunks: Tuple[int, int, int, int] = (-1, -1, 256, 256),
    cache_path: str = ".",
):
    lcp_annual.timer.compositing.start()
    composite = lcp_annual.composites(
        bands=[band],
        resolution=resolution,
    )
    lcp_annual.timer.compositing.stop()

    if interpolate:
        interpolate_params = interpolation_params or {}
        composite = lcp_annual.interpolate(
            composite,
            **interpolate_params,
        )

    if resolution == 20:
        composites_10 = smooth_nan_rescale(
            composite.data,
            src_resolution=resolution,
            dst_resolution=10,
            order=1,
            sigma=0,
        )
        bounds = lcp_annual.bounds
        y, x = coords_from_bounds(bounds, 10)
        composites_10 = xr.DataArray(
            composites_10,
            dims=["time", "band", "y", "x"],
            coords={
                "time": composite.time,
                "band": composite.band,
                "y": y,
                "x": x,
            },
        )
        composite = composites_10
    return composite.satio.cache(chunks=chunks, tempdir=cache_path)


def filter_satio_collection(s2_coll, year, tile, bounds, epsg):
    from loguru import logger  # noqa

    logger.debug(f"Filtering S2 collection for tile {tile}")
    logger.debug(f"N Products before: {s2_coll.df.shape[0]}")
    tile_coll = s2_coll.filter_tiles(tile)
    tile_coll = tile_coll.filter_dates(f"{year}-01-01", f"{year + 1}-01-01")
    tile_coll = tile_coll.filter_bounds(bounds, epsg)

    n_products = tile_coll.df.shape[0]

    logger.debug(f"N Products after: {n_products}")
    if n_products == 0:
        raise NoAcquisitionsError("No products after filtering collection")

    return tile_coll


def save_features_tif(
    percentiles: xr.DataArray,
    out_fn: Union[str, Path],
    tile: str,
    block_id: int,
    bounds: Tuple[float, float, float, float],
    epsg: int,
    lcp_annual: LoiAnnualCompositesProcessor,
    add_quality_score: bool = False,
    add_dem: bool = False,
    add_obs: bool = False,
):
    from loguru import logger  # noqa

    percentiles.name = f"L2A-{tile}_{block_id:03d}"

    logger.info("Computing percentiles")
    percentiles = percentiles.compute()

    if add_quality_score:
        logger.info("Adding quality score")
        quality_score = lcp_annual.get_quality_score(resolution=10)
        percentiles = percentiles.satio.add_band(
            quality_score.isel(band=0).data, name="LOI-QUALITY-MEAN"
        )
        percentiles = percentiles.satio.add_band(
            quality_score.isel(band=1).data, name="LOI-QUALITY-MAX"
        )

    if add_obs:
        logger.info("Adding number of observations")
        obs_l2a = (lcp_annual.weights > 0).sum(dim="time")
        percentiles = percentiles.satio.add_band(obs_l2a, name="L2A-OBS-NB")

    if add_dem:
        logger.info("Adding DEM altitude")
        dem_alt = get_dem(tile, bounds, epsg)
        dem_alt = smooth_nan_rescale(
            dem_alt, src_resolution=20, dst_resolution=10, order=1, sigma=0
        )
        percentiles = percentiles.satio.add_band(dem_alt, name="COP-DEM-ALT")

    logger.info("Scaling data")
    band_names = [b.upper() for b in percentiles.band.values]

    scales = np.ones(percentiles.band.values.size) * 1 / 10000
    scales_exceptions = {"L2A-OBS-NB": 1, "COP-DEM-ALT": 1}
    for k, v in scales_exceptions.items():
        if k in band_names:
            scales[band_names.index(k)] = v

    nodata_value = -32768
    nodata_mask = percentiles.isnull()

    percentiles.data = percentiles.data / np.broadcast_to(
        np.expand_dims(scales, axis=(0, 2, 3)), percentiles.data.shape
    )
    percentiles.data = np.round(percentiles.data)
    percentiles = percentiles.clip(-32767, 32767)  # clip to int16
    percentiles.data = percentiles.data.astype(np.int16)
    percentiles = percentiles.where(~nodata_mask, nodata_value)

    logger.info(f"Saving features {out_fn}")

    save_geotiff(
        percentiles.data[0],
        bounds=bounds,
        epsg=epsg,
        bands_names=band_names,
        filename=out_fn,
        scales=np.array(scales),
    )


def process_block_lsf_annual_v100(
    s2_coll,
    tile,
    block_id,
    bounds=None,
    epsg=None,
    year=2020,
    loi_version="v100",
    lsf_annual_version="v100",
    lsf_volume="products/",
    annual_periods=24,
    loi_weights_params=None,
    interpolation_params=None,
    chunks=(-1, -1, 128, 128),
    rio_gdal_options=RIO_GDAL_OPTIONS,
    compositing_max_workers=10,
    loi_loader_max_workers=10,
    loi_volume="/vsis3/vito-lcfm/products/",
    upload=True,
    bucket="vito-lcfm",
    cache_path=".",
    delete_after_upload=True,
):
    from loguru import logger  # noqa
    from satio_pc.extension import SatioTimeSeries  # noqa
    from satio.grid import get_blocks_gdf

    loi_coll = Loi60Collection(
        version=loi_version, products_base_path=loi_volume
    )
    lsf_annual_coll = LsfAnnualCollection(
        version=lsf_annual_version, products_base_path=lsf_volume
    )

    if (bounds is None) or (epsg is None):
        block = (
            get_blocks_gdf([tile], s2_coll.s2grid)
            .query(f"block_id == {block_id}")
            .iloc[0]
        )

        # vars setup
        bounds = block.bounds
        epsg = block.epsg

    bands_10m = ["B02", "B03", "B04", "B08"]
    bands_20m = ["B11", "B12"]

    bands_core = ["B02", "B03", "B04", "B08", "B11", "B12", "ndvi"]
    bands_extra = ["nbr", "evi", "ndmi", "ndwi"]

    features_core_band_name = "L2A-BANDS"
    features_extra_band_name = "L2A-INDICES"

    # collections
    lsf_block = lsf_annual_coll.block(tile, block_id, year)
    tile_coll = filter_satio_collection(s2_coll, year, tile, bounds, epsg)

    logger.info(
        f"tile: {tile}_{block_id:03d} - products: {tile_coll.df.shape[0]}"
    )

    loi_weights_params = loi_weights_params or get_loi_weights_params(
        drop_nodata_products=True,
        composite_delta=0.1,
        composite_snow_prob_weight=0.5,
        loader_max_workers=loi_loader_max_workers,
    )

    interpolation_params = interpolation_params or dict(
        valid_prob_range=0.15,
        time_weight_sigma=0.9,
        time_weight_alpha=0.999,
        time_min_weight=0.001,
    )

    lcp_annual = LoiAnnualCompositesProcessor(
        bounds=bounds,
        l2a_coll=tile_coll,
        loi_coll=loi_coll,
        year=year,
        periods_number=annual_periods,
        loi_weights_params=loi_weights_params,
        verbose=True,
        max_workers=compositing_max_workers,
        rio_gdal_options=rio_gdal_options,
    )

    logger.info("Computing LOI-60 weights")
    _ = lcp_annual.weights  # pre-compute weights

    logger.info("Computing composites")
    task_cache_path = Path(cache_path) / f"tmp_lsf_v100_{tile}_{block_id:03d}"
    task_cache_path.mkdir(exist_ok=True, parents=True, mode=0o777)
    composites = xr.concat(
        [
            band_composite(
                lcp_annual,
                band,
                resolution=10,
                interpolate=True,
                interpolation_params=interpolation_params,
                chunks=chunks,
                cache_path=task_cache_path,
            )
            for band in bands_10m
        ]
        + [
            band_composite(
                lcp_annual,
                band,
                resolution=20,
                interpolate=True,
                interpolation_params=interpolation_params,
                chunks=chunks,
                cache_path=task_cache_path,
            )
            for band in bands_20m
        ],
        dim="band",
    )

    lcp_annual.timer.log()

    composites = composites.chunk(chunks)
    indices = composites.satio.indices(["ndvi"] + bands_extra)
    composites = xr.concat([composites, indices], dim="band")

    percentiles = (
        composites.sel(band=bands_core)
        .chunk(chunks)
        .satio.percentile(name_prefix="L2A")
    )
    percentiles_extra = (
        composites.sel(band=bands_extra)
        .chunk(chunks)
        .satio.percentile(name_prefix="L2A")
    )

    task_cache_path.mkdir(exist_ok=True, parents=True)

    out_fn = lsf_block.path(features_core_band_name)
    tmp_fn = task_cache_path / out_fn.name
    save_features_tif(
        percentiles,
        tmp_fn,
        tile,
        block_id,
        bounds,
        epsg,
        lcp_annual,
        add_quality_score=True,
        add_dem=False,
        add_obs=True,
    )

    if upload:
        s3 = get_bucket_client(bucket=bucket)
        s3.upload(tmp_fn, str(out_fn))
        if delete_after_upload:
            tmp_fn.unlink()

    out_fn = lsf_block.path(features_extra_band_name)
    tmp_fn = task_cache_path / out_fn.name
    save_features_tif(
        percentiles_extra,
        tmp_fn,
        tile,
        block_id,
        bounds,
        epsg,
        lcp_annual,
        add_quality_score=False,
        add_dem=False,
        add_obs=False,
    )
    if upload:
        s3.upload(tmp_fn, str(out_fn))
        if delete_after_upload:
            tmp_fn.unlink()

    # if upload and delete_after_upload:
    #     import shutil

    #     # delete all cache files
    #     shutil.rmtree(task_cache_path)


# if __name__ == "__main__":
#     from loguru import logger

#     aws_env = "/data/users/Private/dzanaga/configs/aws.env"
#     load_dotenv(aws_env)
#     load_dotenv("/home/ubuntu/aws.env")

#     parser = argparse_parser()
#     parser.add_argument("config_uri", type=str, help="Configuration URI")
#     args = parser.parse_args()

#     config = load_config(args.config_uri)

#     app_name = config["app_name"]
#     lsf_annual_version = config["lsf_annual_version"]
#     annual_periods = config["annual_periods"]
#     chunks = config["chunks"]
#     s2_db_uri = config["s2_db_uri"]
#     blocks_grid_uri = config["blocks_grid_uri"]
#     loi_version = config["loi_version"]
#     lsf_volume = config["lsf_volume"]
#     year = config["year"]
#     overwrite = config["overwrite"]
#     satio_max_workers = config["satio_max_workers"]
#     compositing_max_workers = config["compositing_max_workers"]
#     loi_loader_max_workers = config["loi_loader_max_workers"]
#     rio_gdal_options = config["rio_gdal_options"]
#     num_slices_ratio = config["num_slices_ratio"]
#     local = config["local"]
#     local_threads = config.get("local_threads", 1)
#     blocks_number = config.get("blocks_number")

#     sc = get_spark_context(local, threads=2)

#     logger.info(f"Loading blocks grid from: {blocks_grid_uri}")
#     blocks = get_blocks(blocks_grid_uri, s2_db_uri)

#     if blocks_number is not None:
#         logger.info(f"Sampling {blocks_number} blocks")
#         blocks = blocks.sample(n=blocks_number, random_state=42)
#     else:
#         logger.info("Shuffling blocks")
#         blocks = blocks.sample(frac=1, random_state=42)

#     elogs = Elogs(app_id=app_name, overwrite_table=overwrite)

#     @elogs
#     def process(block):
#         import socket

#         from loguru import logger  # noqa
#         from satio_pc.extension import SatioTimeSeries  # noqa

#         logger.info(f"Executor running on: {socket.gethostname()}")

#         logger.info(f"Loading satio collection from {s2_db_uri}")
#         s2_coll = get_satio_collection(
#             s2_db_uri=s2_db_uri,
#             tile=block.tile,
#             progressbar=False,
#             max_workers=satio_max_workers,
#         )

#         return process_block(
#             block,
#             loi_version=loi_version,
#             lsf_annual_version=lsf_annual_version,
#             lsf_volume=lsf_volume,
#             s2_coll=s2_coll,
#             annual_periods=annual_periods,
#             chunks=chunks,
#             rio_gdal_options=rio_gdal_options,
#             compositing_max_workers=compositing_max_workers,
#             loi_loader_max_workers=loi_loader_max_workers,
#         )

#     logger.info(f"Blocks: {blocks.shape[0]}")

#     tasks = [
#         ElogsTask(f"{block.tile}_{block.block_id:03d}_{year}", block)
#         for block in blocks.itertuples()
#     ]

#     with elogs.start(tasks) as filtered_tasks:
#         if local:
#             # selected_tasks = ["38KPA_006_2020", "14QND_019_2020"]
#             # selected_tasks = ["14QND_019_2020"]
#             # selected_tasks = ["33XXG_085_2020"]  # slow on cluster - took 11 minutes locally
#             # selected_tasks = ["42WWE_066_2020"]
#             # selected_tasks = ["04WFS_078_2020"]
#             # selected_tasks = ["01GEL_008_2020"]
#             # selected_tasks = ["13SBD_102_2020"]
#             # filtered_tasks = [
#             #     e for e in filtered_tasks if e.task_id in selected_tasks
#             # ]
#             logger.info(f"Tasks: {len(filtered_tasks)}/{len(tasks)}")
#             # logger.info("Running first one - testing mode.")
#             # filtered_tasks = filtered_tasks[:1]

#         try:
#             if len(filtered_tasks) > 10_000:
#                 num_slices = int(len(filtered_tasks) * num_slices_ratio)
#                 num_slices = max(1, num_slices)
#             else:
#                 num_slices = len(filtered_tasks)

#             logger.info(f"Number of slices: {num_slices}")
#             sc.parallelize(filtered_tasks, num_slices).foreach(process)
#         except Exception as e:
#             logger.error(e)
#             raise e
#         finally:
#             sc.stop()

#     logger.success("Done")
