"""
# 3 types of products

# 1. Annual products: date_id is year
# 2. Sub-annual (Quarterly, Monthly, Dekad) products: date_id is startdate_enddate
# 3. Single observation products: date_id is observation date

# we then have blocks, tiles_utm, tiles_latlon_3deg

# the tiling determines the path and name as well

# naming for blocks. since for blocks we have multiple bands in a single file, and multiple blocks per tile. for each tile we also separate on the layer
# <BASE_PATH>/<PROJECT_NAME>/<PRODUCT_NAME>/<VERSION>/<tile_separator>/<DATE_SEPARATOR>/<LAYER>/<BASENAME>
annual product:
    /vitodata/vegteam_vol2/data/lcfm/prototypes/  LCFM/ LCM-10/  v001/  blocks/31/U/FS/  2020/  MAP/ LCFM_LCM-10_2020_31UFS_000_V001_MAP.tif
monthly product:
    /vitodata/vegteam_vol2/data/lcfm/prototypes/  LCFM/ LSF-MONTHLY/  v001/  blocks/31/U/FS/  2020/05/ MAP/ LCFM_LSF-MONTHLY_20200501_20200531_31UFS_000_V001_MAP.tif
single observation product: # S2A_MSIL2A_20200102T102421_N0500_R065_T31PBK_20230425T023320
    /vitodata/vegteam_vol2/data/lcfm/prototypes/  LCFM/ LOI-10/  v001/  blocks/31/U/FS/  S2_PRODUCT_ID/ MAP/ LCFM_LOI-10_20200501THHMMSS_20230425T023320_31UFS_000_V001_MAP.tif

for single obs date_id is observationdate_processingdate
date_separator is s2_product_id

# naming for tiles s2grid. since for tiles we have a single band/layer per file. we do not separate on the layer.
# /vitodata/vegteam_vol2/data/lcfm/prototypes/LCM-10/v001/utm_tiles/31/2020/MAP/LCFM_LCM-10_2020_31UFS_V001_MAP.tif

# <BASE_PATH>/<PROJECT_NAME>/<PRODUCT_NAME>/<VERSION>/<tile_separator>/<DATE_SEPARATOR>/<BASENAME>
new: /vitodata/vegteam_vol2/data/lcfm/prototypes/  LCFM/ LCM-10/  v001/  tiles_utm/31/U/FS/ 2020/ LCFM_LCM-10_2020_31UFS_V001_MAP.tif

# naming for tiles latlon_3deg. these tiles represents global products. All tiles are in the same folder, and we separate on the layer
# /vitodata/vegteam_vol2/data/lcfm/prototypes/LCM-10/v001/latlon_3deg_tiles/2020/MAP/LCFM_LCM-10_2020_N00E000_V001_MAP.tif
new: /vitodata/vegteam_vol2/data/lcfm/prototypes/  LCFM/ LCM-10/  v001/  tiles_latlon_3deg/N00E000/ 2020/ LCFM_LCM-10_2020_N00E000_V001_MAP.tif



"""

import calendar
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
from rasterio.enums import Resampling
from satio_pc.geotiff import get_rasterio_profile_shape, write_geotiff_tags
from satio_pc.grid import tile_to_epsg

from veg_workflows.db import (
    get_block_bounds,
    get_latlon_tile_bounds,
    get_utm_tile_bounds,
)
from veg_workflows.io import load_array_bounds, load_cloudsen_mask
from veg_workflows.paths import slash_tile

LCFM_BASE_PATH = Path("/vitodata/vegteam_vol2/data/lcfm/prototypes")

L2A_BANDS_RESOLUTIONS = {
    "B01": 60,
    "B02": 10,
    "B03": 10,
    "B04": 10,
    "B05": 20,
    "B06": 20,
    "B07": 20,
    "B08": 10,
    "B8A": 20,
    "B09": 60,
    "B11": 20,
    "B12": 20,
    "NDVI": 10,
}


def last_day_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return last_day


def start_end_dates(year, month):
    start_date = f"{year}{month:02d}01"
    end_date = f"{year}{month:02d}{last_day_of_month(year, month)}"
    return start_date, end_date


def s2_product_id_to_date(s2_product_id):
    # S2A_MSIL2A_20200102T102421_N0500_R065_T31PBK_20230425T023320
    split = s2_product_id.split("_")
    obs_date = split[2]
    proc_date = split[-1]
    return obs_date, proc_date


def s2_product_relative_orbit(s2_product_id):
    # S2A_MSIL2A_20200102T102421_N0500_R065_T31PBK_20230425T023320
    split = s2_product_id.split("_")
    return split[4]


def s2_product_tile(s2_product_id):
    # S2A_MSIL2A_20200102T102421_N0500_R065_T31PBK_20230425T023320
    split = s2_product_id.split("_")
    return split[5][1:]


def s2_product_day_orbit(s2_product_id):
    # S2A_MSIL2A_20200102T102421_N0500_R065_T31PBK_20230425T023320
    obs_date, _ = s2_product_id_to_date(s2_product_id)
    obs_day = obs_date[:8]
    orbit = s2_product_relative_orbit(s2_product_id)
    return f"{obs_day}_{orbit}"


class BaseProduct(ABC):
    def __init__(
        self,
        *,
        project_name: str,
        product_name: str,
        version: str,
        products_base_path,
    ) -> None:
        self.project_name = project_name
        self.product_name = product_name
        self.version = version
        self.products_base_path = Path(products_base_path)

        required_attrs = [
            "date_id",
            "tile_id",
            "date_separator",
            "tile_separator",
        ]

        # disabling as this raises if super is called before setting the attributes
        # for attr in required_attrs:
        #     if not hasattr(self, attr):
        #         raise AttributeError(f"{self.__class__} must define {attr}")

    @property
    @abstractmethod
    def bounds(self): ...

    @abstractmethod
    def layer_separator(self, layer): ...

    @abstractmethod
    def path(self, layer=None): ...

    def basename(self, layer, suffix=".tif"):
        name = (
            f"{self.project_name}_{self.product_name}_{self.version}_"
            f"{self.date_id}_{self.tile_id}_{layer}"
        ).upper()
        return f"{name}{suffix}"

    def read(self, layer, bounds=None, fill_value=np.nan):
        arr = load_array_bounds(self.path(layer), bounds, fill_value=fill_value)
        return arr

    def write(
        self,
        data,
        layer,
        nodata=None,
        bands_names=None,
        colormap=None,
        tags=None,
        bands_tags=None,
        scales=None,
        offsets=None,
        overwrite=False,
        create_folder_structure=True,
    ):
        profile = get_rasterio_profile_shape(
            data.shape, bounds=self.bounds, epsg=self.epsg, dtype=data.dtype
        )

        if create_folder_structure:
            self.path(layer).parent.mkdir(parents=True, exist_ok=True, mode=0o775)

        if self.path(layer).exists() and not overwrite:
            raise FileExistsError(f"{self.path(layer)} already exists")

        write_geotiff_tags(
            data,
            profile=profile,
            filename=self.path(layer),
            nodata=nodata,
            bands_names=bands_names,
            colormap=colormap,
            tags=tags,
            bands_tags=bands_tags,
            scales=scales,
            offsets=offsets,
        )

    def write_cog(self):
        raise NotImplementedError("https://cogeotiff.github.io/rio-cogeo/API/")


# Mixins


class PathMixin:
    def path(self, layer=None, suffix=".tif"):
        return (
            self.products_base_path
            / self.project_name
            / self.product_name
            / self.version
            / self.tile_separator
            / self.date_separator
            / self.layer_separator(layer)
            / self.basename(layer, suffix=suffix)
        )


class SingleObsUtmDateMixin:
    @property
    def date_id(self):
        return f"{self.observation_date}_{self.processing_date}"

    @property
    def date_separator(self):
        year = self.observation_date[:4]
        return f"{year}/{self.s2_product_id}/"


class SingleObsLatLonDateMixin:
    @property
    def date_id(self):
        return self.s2_day_orbit

    @property
    def date_separator(self):
        obs, _ = self.s2_day_orbit.split("_")
        year = obs[:4]
        month = obs[4:6]
        return f"{year}/{month}/{self.s2_day_orbit}/"


class UtmTileProductMixin:
    @property
    def epsg(self):
        return tile_to_epsg(self.tile)

    @staticmethod
    def _get_tile_bounds(tile):
        return get_utm_tile_bounds(tile)

    def layer_separator(self, layer):
        """For UTM tiles we do not separate on the layer"""
        return ""

    @property
    def tile_separator(self):
        return f"tiles_utm/{slash_tile(self.tile)}/"

    def read_block(self, layer, block_id, fill_value=np.nan):
        bounds = get_block_bounds(self.tile, block_id)
        return self.read(layer, bounds=bounds, fill_value=fill_value)


class LatLonTileProductMixin:
    @staticmethod
    def _get_tile_bounds(tile):
        return get_latlon_tile_bounds(tile)

    def layer_separator(self, layer):
        """For tiles we do not separate on the layer"""
        return ""

    @property
    def tile_separator(self):
        tile = self.tile
        northing = tile[:3]
        easting = tile[3:]
        return f"tiles_latlon/{self.resolution}deg/{northing}/{easting}/"


####### S2 Block products ########
class BaseS2BlockProduct(PathMixin, BaseProduct):
    def __init__(
        self,
        tile,
        block_id,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.tile = tile
        self.block_id = block_id
        self.tile_block_id = f"{self.tile}_{self.block_id:03d}"
        self._bounds = None
        self.epsg = tile_to_epsg(tile)

        self.tile_id = f"{self.tile}_{self.block_id:03d}"
        self.tile_separator = f"blocks/{slash_tile(self.tile)}/"

        super().__init__(
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )

    @property
    def bounds(self):
        if self._bounds is None:
            self._bounds = get_block_bounds(self.tile, self.block_id)
        return self._bounds

    def layer_separator(self, layer):
        return layer

    def __str__(self) -> str:
        return (
            f"<{self.project_name}_{self.product_name}_"
            f"{self.tile_block_id}_{self.date_id}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class AnnualS2BlockProduct(BaseS2BlockProduct):
    def __init__(
        self,
        tile,
        block_id,
        year,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.year = year

        self.date_id = f"{year}"
        self.date_separator = f"{year}/"

        super().__init__(
            tile,
            block_id,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class MonthlyS2BlockProduct(BaseS2BlockProduct):
    def __init__(
        self,
        tile,
        block_id,
        year,
        month,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.year = year
        self.month = month

        self.start_date, self.end_date = start_end_dates(year, month)

        self.date_id = f"{self.start_date}_{self.end_date}"
        self.date_separator = f"{year}/{month:02d}"

        super().__init__(
            tile,
            block_id,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class SingleObsS2BlockProduct(SingleObsUtmDateMixin, BaseS2BlockProduct):
    def __init__(
        self,
        s2_product_id,
        block_id,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.s2_product_id = s2_product_id

        self.observation_date, self.processing_date = s2_product_id_to_date(
            s2_product_id
        )

        super().__init__(
            s2_product_tile(s2_product_id),
            block_id,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


####### Tile products ########
class BaseTileProduct(PathMixin, BaseProduct):
    def __init__(
        self, tile, *, project_name, product_name, version, products_base_path
    ) -> None:
        self.tile = tile
        self._bounds = None

        self.tile_id = f"{self.tile}"

        super().__init__(
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )

    @property
    def bounds(self):
        if self._bounds is None:
            self._bounds = self._get_tile_bounds(self.tile)
        return self._bounds

    @staticmethod
    def _get_tile_bounds(tile):
        raise NotImplementedError("Implement in subclass")

    def __str__(self) -> str:
        return (
            f"<{self.project_name}_{self.product_name}_"
            f"{self.version}_{self.tile}_{self.date_id}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class BaseAnnualTileProduct(BaseTileProduct):
    def __init__(
        self,
        tile,
        year,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.year = year

        self.date_id = f"{year}"
        self.date_separator = f"{year}/"

        super().__init__(
            tile,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class AnnualUtmTileProduct(UtmTileProductMixin, BaseAnnualTileProduct): ...


class AnnualLatLonTileProduct(LatLonTileProductMixin, BaseAnnualTileProduct):
    def __init__(
        self,
        tile,
        year,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
        resolution=3,
    ) -> None:
        self.resolution = resolution

        super().__init__(
            tile,
            year,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class BaseMonthlyTileProduct(BaseTileProduct):
    def __init__(
        self,
        tile,
        year,
        month,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.year = year
        self.month = month

        self.start_date, self.end_date = start_end_dates(year, month)

        self.date_id = f"{self.start_date}_{self.end_date}"
        self.date_separator = f"{year}/{month:02d}/"

        super().__init__(
            tile,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class MonthlyUtmTileProduct(UtmTileProductMixin, BaseMonthlyTileProduct): ...


class MonthlyLatLonTileProduct(LatLonTileProductMixin, BaseMonthlyTileProduct):
    def __init__(
        self,
        tile,
        year,
        month,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
        resolution=3,
    ) -> None:
        self.resolution = resolution

        super().__init__(
            tile,
            year,
            month,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class SingleObsUtmTileProduct(
    UtmTileProductMixin, SingleObsUtmDateMixin, BaseTileProduct
):
    def __init__(
        self,
        s2_product_id,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
    ) -> None:
        self.s2_product_id = s2_product_id
        self.s2_day_orbit = s2_product_day_orbit(s2_product_id)
        self.observation_date, self.processing_date = s2_product_id_to_date(
            s2_product_id
        )

        super().__init__(
            s2_product_tile(s2_product_id),
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class SingleObsLatLonTileProduct(
    LatLonTileProductMixin, SingleObsLatLonDateMixin, BaseTileProduct
):
    def __init__(
        self,
        tile,
        s2_day_orbit,
        *,
        project_name,
        product_name,
        version,
        products_base_path,
        resolution=3,
    ) -> None:
        self.s2_day_orbit = s2_day_orbit
        self.resolution = resolution

        super().__init__(
            tile,
            project_name=project_name,
            product_name=product_name,
            version=version,
            products_base_path=products_base_path,
        )


class Loi10Product(SingleObsUtmTileProduct):
    def read(
        self,
        layer,
        bounds=None,
        fill_value=np.nan,
        blur_sigma=None,
        mask_threshold=None,
        resampling_method=Resampling.bilinear,
        resolution=10,
    ):
        arr = load_cloudsen_mask(
            self.path(layer),
            bounds,
            fill_value=fill_value,
            blur_sigma=blur_sigma,
            mask_threshold=mask_threshold,
            resampling_method=resampling_method,
            resolution=resolution,
        )
        return arr

    def read_block(
        self,
        layer,
        block_id,
        fill_value=np.nan,
        blur_sigma=None,
        mask_threshold=None,
        resampling_method=Resampling.bilinear,
        resolution=10,
    ):
        bounds = get_block_bounds(self.tile, block_id)
        return self.read(
            layer,
            bounds=bounds,
            fill_value=fill_value,
            blur_sigma=blur_sigma,
            mask_threshold=mask_threshold,
            resampling_method=resampling_method,
            resolution=resolution,
        )


####### Products Collections ########


class BaseProductsCollection:
    def __init__(
        self, *, project_name, product_name, version, products_base_path
    ) -> None:
        self.project_name = project_name
        self.product_name = product_name
        self.version = version
        self.products_base_path = products_base_path

    def __str__(self):
        return f"{self.project_name}_{self.product_name}_{self.version} Collection"

    def __repr__(self):
        return self.__str__()


class BaseMonthlyCollection(BaseProductsCollection):
    def block(self, tile: str, block_id: int, year: int, month: int):
        return MonthlyS2BlockProduct(
            tile=tile,
            block_id=block_id,
            year=year,
            month=month,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )

    def tile_utm(self, tile: str, year: int, month: int):
        return MonthlyUtmTileProduct(
            tile=tile,
            year=year,
            month=month,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )

    def tile_latlong(self, tile: str, year: int, month: int, resolution: int = 3):
        return MonthlyLatLonTileProduct(
            tile=tile,
            year=year,
            month=month,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
            resolution=resolution,
        )


class BaseAnnualCollection(BaseProductsCollection):
    def block(self, tile: str, block_id: int, year: int):
        return AnnualS2BlockProduct(
            tile=tile,
            block_id=block_id,
            year=year,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )

    def tile_utm(self, tile: str, year: int):
        return AnnualUtmTileProduct(
            tile=tile,
            year=year,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )

    def tile_latlon(self, tile: str, year: int, resolution: int = 3):
        return AnnualLatLonTileProduct(
            tile=tile,
            year=year,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
            resolution=resolution,
        )


class BaseSingleObsCollection(BaseProductsCollection):
    def block(
        self,
        s2_product_id: str,
        block_id: int,
    ):
        return SingleObsS2BlockProduct(
            s2_product_id=s2_product_id,
            block_id=block_id,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )

    def tile_utm(self, s2_product_id: str):
        return SingleObsUtmTileProduct(
            s2_product_id=s2_product_id,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )

    def tile_latlon(self, tile: str, s2_day_orbit: str, resolution: int = 3):
        return SingleObsLatLonTileProduct(
            tile=tile,
            s2_day_orbit=s2_day_orbit,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
            resolution=resolution,
        )


class LsfAnnualCollection(BaseAnnualCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LSF-ANNUAL",
            version=version,
            products_base_path=products_base_path,
        )


class LsfMonthlyCollection(BaseMonthlyCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LSF-MONTHLY",
            version=version,
            products_base_path=products_base_path,
        )


class Lcm10Collection(BaseAnnualCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LCM-10",
            version=version,
            products_base_path=products_base_path,
        )


class LsfMonthlyCollection(BaseMonthlyCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LSF-MONTHLY",
            version=version,
            products_base_path=products_base_path,
        )


class Lsc10MonthlyCollection(BaseMonthlyCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LSC-10-MONTHLY",
            version=version,
            products_base_path=products_base_path,
        )


class Lsc120MonthlyCollection(BaseMonthlyCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LSC-120-MONTHLY",
            version=version,
            products_base_path=products_base_path,
        )


class Loi10Collection(BaseSingleObsCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LOI-10",
            version=version,
            products_base_path=products_base_path,
        )

    def tile_utm(self, s2_product_id: str):
        return Loi10Product(
            s2_product_id=s2_product_id,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )


class Loi60Collection(BaseSingleObsCollection):
    def __init__(self, version, products_base_path) -> None:
        super().__init__(
            project_name="LCFM",
            product_name="LOI-60",
            version=version,
            products_base_path=products_base_path,
        )

    def tile_utm(self, s2_product_id: str):
        return Loi10Product(
            s2_product_id=s2_product_id,
            project_name=self.project_name,
            product_name=self.product_name,
            version=self.version,
            products_base_path=self.products_base_path,
        )
