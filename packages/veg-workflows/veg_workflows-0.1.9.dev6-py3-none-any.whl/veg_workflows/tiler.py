import atexit
import os
import shutil
import subprocess
import sys
from pathlib import Path

import geopandas as gpd
import rasterio
from loguru import logger
from shapely.geometry import Polygon
from veg_workflows.paths.grids import BLOCKS_GRID_PATH, LCFM_10PERCENT_BLOCKS_FGB

from satio.utils import random_string
from satio.utils.buildvrt import build_vrt_files


def warp_geom(geom, src_epsg, dst_epsg):
    import pyproj
    from shapely.ops import transform

    if src_epsg == dst_epsg:
        return geom

    project = pyproj.Transformer.from_proj(
        pyproj.Proj(init=f"epsg:{src_epsg}"),  # source coordinate system
        pyproj.Proj(init=f"epsg:{dst_epsg}"),
    )  # destination coordinate system

    out_geom = transform(project.transform, geom)  # apply projection
    return out_geom


def gdal_warp(
    src_fnames,
    dst_fname,
    bounds,
    width=12000,
    height=12000,
    dst_epsg=4326,
    center_long=0,
    gdal_cachemax=2000,
    resampling="near",
):
    import os
    import sys

    py = sys.executable.split("/")[-1]
    bin = sys.executable.replace(py, "gdalwarp")

    proj_data = Path(bin).parent.parent / "share/proj"
    if isinstance(src_fnames, str):
        src_fnames = [src_fnames]

    str_bounds = " ".join(list(map(str, bounds)))

    fns = " ".join(list(map(str, src_fnames)))
    cmd = (
        f"{bin} "
        f"-t_srs EPSG:{dst_epsg} "
        f"-of vrt -multi "
        f"-r {resampling} "
        f"--config CENTER_LONG {center_long} "
        f"--config GDAL_CACHEMAX {gdal_cachemax} "
        f"-te {str_bounds} "
        f"-ts {width} {height} "
        f"{fns} "
        f"{dst_fname}"
    )

    logger.debug(cmd)

    if "PROJ_DATA" not in os.environ.keys():
        env = dict(**os.environ, PROJ_DATA=proj_data)
    else:
        env = None

    p = subprocess.run(cmd.split(), env=env)
    if p.returncode != 0:
        raise IOError("GDAL warping failed")


class ConversionFailed(Exception): ...


def gdal_translate_cog(
    fn,
    out_fn,
    bounds,
    scale,
    offset,
    nodata,
    gdal_cachemax=2000,
    resampling="NEAR",
    overview_resampling="NEAR",
):
    import sys

    py = sys.executable.split("/")[-1]
    bin = sys.executable.replace(py, "gdal_translate")
    proj_data = Path(bin).parent.parent / "share/proj"

    os.environ["GDAL_CACHEMAX"] = f"{gdal_cachemax}"
    b = bounds
    bounds_str = " ".join(map(str, [b[0], b[3], b[2], b[1]]))

    scale_str = f"-a_scale {1 / scale}" if scale is not None else ""
    offset_str = f"-a_offset -{offset}" if offset is not None else ""
    nodata_str = f"-a_nodata {nodata}" if nodata is not None else ""

    cmd = (
        f"{bin} "
        "-of COG "
        "-co COMPRESS=DEFLATE "
        "-co PREDICTOR=2 "
        "-co BLOCKSIZE=1024 "
        f"-co RESAMPLING={resampling} "
        f"-co OVERVIEW_RESAMPLING={overview_resampling} "
        "-co OVERVIEWS=IGNORE_EXISTING "
        "-co BIGTIFF=YES "
        f"{scale_str} "
        f"{offset_str} "
        f"{nodata_str} "
        f"-projwin {bounds_str} "
        f"{fn} {out_fn}"
    )
    logger.debug(cmd)

    if "PROJ_DATA" not in os.environ.keys():
        env = dict(**os.environ, PROJ_DATA=proj_data)
    else:
        env = None
    p = subprocess.run(cmd.split(), env=env, capture_output=True)
    if p.stdout:
        logger.info(p.stdout.decode())

    if p.stderr:
        logger.error(p.stderr.decode())

    if p.returncode:
        raise ConversionFailed(p.stderr.decode())


def gdalbuildvrt(
    vrt_fn,
    paths,
    srcband=None,
    overwrite=True,
    src_nodata=None,
    print_cmd=False,
):
    vrt_fn = Path(vrt_fn)

    py = sys.executable.split("/")[-1]
    bin_pth = sys.executable.replace(py, "gdalbuildvrt")

    if vrt_fn.exists():
        if overwrite:
            vrt_fn.unlink()
        else:
            raise FileExistsError(f"{vrt_fn} exists and overwrite is False")

    vrt_fn.parent.mkdir(exist_ok=True, parents=True, mode=0o775)

    vrt_str = ""
    for f in paths:
        vrt_str += f" {f}"

    cmnd = f"{bin_pth} {vrt_fn} {vrt_str}"

    if srcband is not None:
        if isinstance(srcband, int):
            srcband = [srcband]

        for b in srcband:
            cmnd += f" -b {b}"

    if src_nodata is not None:
        cmnd += f" -srcnodata {src_nodata} -vrtnodata {src_nodata}"

    if print_cmd:
        logger.info(cmnd)
    process_output = subprocess.run(cmnd.split(), capture_output=True)
    if process_output.stdout:
        logger.info(process_output.stdout.decode())

    if process_output.stderr:
        logger.error(process_output.stderr.decode())

    if process_output.returncode:
        raise ConversionFailed(process_output.stderr.decode())


def _cleanup(path):
    if Path(path).is_file():
        os.remove(path)
    else:
        shutil.rmtree(path)


class NoDatasetsError(Exception): ...


class BaseBlocksTiler:
    def __init__(
        self,
        bounds,
        epsg,
        blocks_grid_path=None,
        tmp_folder=None,
        src_nodata=None,
    ) -> None:
        self._blocks_grid_path = blocks_grid_path or BLOCKS_GRID_PATH

        geom = Polygon.from_bounds(*bounds)
        self.geom_latlon = warp_geom(geom, epsg, 4326)

        if tmp_folder is None:
            tmp_folder = Path(".") / f".veg_blocks_tiler_{random_string(8)}"

        tmp_folder.mkdir(exist_ok=True, parents=True)
        atexit.register(_cleanup, tmp_folder)

        self._tmp_folder = tmp_folder

        self.bounds = bounds
        self.epsg = epsg
        self._blocks = None

    @property
    def blocks(self):
        if self._blocks is None:
            blocks_gdf = gpd.read_file(self._blocks_grid_path, mask=self.geom_latlon)

            blocks_gdf["bounds"] = blocks_gdf["bounds"].apply(eval)

            if blocks_gdf.shape[0] == 0:
                raise NoDatasetsError("No blocks for requested geometry")

            self._blocks = blocks_gdf
        return self._blocks

    def export(
        self,
        filename,
        scale,
        offset,
        nodata,
        get_blocks_filenames,
        width=12000,
        height=12000,
        metadata=None,
        bands_tags=None,
        bands_names=None,
        center_long=0,
        resampling="NEAR",
        overview_resampling="NEAR",
        srcband=None,
        src_nodata=None,
    ):
        tmp_folder = self._tmp_folder

        blocks_gdf = self.blocks

        def wrapped_get_blocks_filenames(row):
            path = Path(get_blocks_filenames(row))
            if path.exists():
                return path
            else:
                return None

        blocks_gdf["tmp_path"] = blocks_gdf.apply(wrapped_get_blocks_filenames, axis=1)
        blocks_gdf = blocks_gdf[~blocks_gdf.tmp_path.isna()]
        if blocks_gdf.shape[0] == 0:
            raise NoDatasetsError

        epsgs = blocks_gdf.epsg.unique()

        bounds = self.bounds
        vrt_fns = []

        for epsg in epsgs:
            paths = blocks_gdf[blocks_gdf.epsg == epsg].tmp_path.values

            if paths.size == 0:
                continue

            tmp_vrt_fn = tmp_folder / f"epsg_vrts/{epsg}.vrt"

            gdalbuildvrt(
                tmp_vrt_fn,
                paths,
                srcband,
                overwrite=True,
                src_nodata=src_nodata,
            )

            tmp_vrt_fn_latlon = tmp_folder / f"epsg_vrts/{epsg}_latlon.vrt"
            tmp_vrt_fn_latlon.parent.mkdir(exist_ok=True, parents=True)
            if tmp_vrt_fn_latlon.is_file():
                tmp_vrt_fn_latlon.unlink()

            gdal_warp(
                [tmp_vrt_fn],
                tmp_vrt_fn_latlon,
                bounds,
                width=width,
                height=height,
                dst_epsg=self.epsg,
                center_long=center_long,
                resampling=resampling,
            )

            vrt_fns.append(tmp_vrt_fn_latlon)

        if len(vrt_fns) > 1:
            final_vrt_fn = tmp_folder / f"{epsg}_merged.vrt"
            build_vrt_files(final_vrt_fn, vrt_fns)
        elif len(vrt_fns) == 0:
            raise NoDatasetsError
        else:
            final_vrt_fn = vrt_fns[0]

        if metadata:
            with rasterio.open(final_vrt_fn, "r+") as dst:
                dst.update_tags(**metadata)

        if bands_tags:
            with rasterio.open(final_vrt_fn, "r+") as dst:
                for i, bt in enumerate(bands_tags):
                    dst.update_tags(i + 1, **bt)

        if bands_names:
            with rasterio.open(final_vrt_fn, "r+") as dst:
                for i, b in enumerate(bands_names):
                    dst.set_band_description(i + 1, b)

        gdal_translate_cog(
            final_vrt_fn,
            filename,
            bounds,
            scale,
            offset,
            nodata,
            resampling=resampling,
            overview_resampling=overview_resampling,
        )

        return filename


class Lcfm10PercentTiler(BaseBlocksTiler):
    def __init__(self, bounds, epsg, tmp_folder=None) -> None:
        super().__init__(bounds, epsg, LCFM_10PERCENT_BLOCKS_FGB, tmp_folder)
