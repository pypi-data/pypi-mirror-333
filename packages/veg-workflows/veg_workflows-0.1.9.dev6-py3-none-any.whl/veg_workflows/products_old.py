import calendar
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

import numpy as np
import rasterio
import xarray as xr
from dateutil.parser import parse
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


class BaseProduct(ABC):
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    @abstractmethod
    def bounds(self): ...

    @property
    @abstractmethod
    def path(self): ...

    def read(self, bounds=None, fill_value=np.nan):
        arr = load_array_bounds(self.path, bounds, fill_value=fill_value)
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
            raise FileExistsError(f"{self.path} already exists")

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


class BaseTileProduct(BaseProduct):
    def __init__(
        self,
        tile,
        project_id,
        project_product_id,
        version="v001",
        product_base_path=None,
    ) -> None:
        self.tile = tile
        self.project_id = project_id
        self.project_product_id = project_product_id
        self.version = version
        self.product_base_path = Path(product_base_path or LCFM_BASE_PATH)

    @property
    def bounds(self):
        if self._bounds is None:
            self._bounds = self._get_tile_bounds(self.tile)
        return self._bounds

    def _tile_split(self):
        """By default there is no split after product sub-type"""
        return ""


class BaseAnnualTileProduct(BaseTileProduct):
    def __init__(
        self,
        tile,
        year,
        *,
        project_id,
        project_product_id,
        version="v001",
        product_base_path=None,
    ) -> None:
        super().__init__(
            tile, project_id, project_product_id, version, product_base_path
        )
        self.year = year

    def path(self, layer):
        tif_name = (
            f"{self.project_id}_{self.project_product_id}_"
            f"{self.year}_{self.tile}_"
            f"{self.version.upper()}_{layer}.tif"
        )

        product_path = (
            self.product_base_path
            / self.project_product_id
            / self.version
            / self._product_subtype
            / self._tile_split()
            / str(self.year)
            / layer
            / tif_name
        )

        return product_path

    def __str__(self) -> str:
        return (
            f"<{self.project_id}_{self.project_product_id}_"
            f"{self.year}_{self.tile}_"
            f"{self.version.upper()}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class BaseMonthlyTileProduct(BaseTileProduct):
    def __init__(
        self,
        tile,
        year,
        month,
        *,
        project_id,
        project_product_id,
        version="v001",
        product_base_path=None,
    ) -> None:
        super().__init__(
            tile, project_id, project_product_id, version, product_base_path
        )
        self.year = year
        self.month = month

        self.start_date = f"{year}{month:02d}01"

        _, last_day = calendar.monthrange(year, month)
        self.end_date = f"{year}{month:02d}{last_day}"

    def path(self, layer):
        tif_name = (
            f"{self.project_id}_{self.project_product_id}_"
            f"{self.start_date}_{self.end_date}_{self.tile}_"
            f"{self.version.upper()}_{layer}.tif"
        )

        product_path = (
            self.product_base_path
            / self.project_product_id
            / self.version
            / self._product_subtype
            / self._tile_split()
            / str(self.year)
            / f"{self.month:02d}"
            / layer
            / tif_name
        )

        return product_path

    def __str__(self) -> str:
        return (
            f"<{self.project_id}_{self.project_product_id}_"
            f"{self.year}_{self.start_date}_{self.end_date}_{self.tile}_"
            f"{self.version.upper()}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class UtmTileProductMixin:
    _product_subtype = "utm_tiles"
    _get_bounds = get_utm_tile_bounds

    def _tile_split(self):
        return self.tile[:2]

    def read_block(
        self, block_id, fill_value=np.nan, bool_mask=True, blur=True, res_meth="NEAR"
    ):
        bounds = get_block_bounds(self.tile, block_id)
        return self.read(
            bounds=bounds,
            fill_value=fill_value,
            bool_mask=bool_mask,
            blur=blur,
            res_meth=res_meth,
        )


class LatLon3DegTileProductMixin:
    _product_subtype = "latlon_3deg_tiles"
    _get_bounds = get_latlon_tile_bounds


class MonthlyUtmTileProduct(UtmTileProductMixin, BaseMonthlyTileProduct): ...


class MonthlyLatLon3DegTileProduct(
    LatLon3DegTileProductMixin, BaseMonthlyTileProduct
): ...


class AnnualUtmTileProduct(UtmTileProductMixin, BaseAnnualTileProduct): ...


class AnnualLatLon3DegTileProduct(
    LatLon3DegTileProductMixin, BaseAnnualTileProduct
): ...


class BaseS2BlockProduct(BaseProduct):
    def __init__(
        self,
        tile,
        block_id,
        project_id,
        project_product_id,
        version="v001",
        product_base_path=None,
    ) -> None:
        self.project_id = project_id
        self.project_product_id = project_product_id

        self.tile = tile
        self.block_id = block_id

        self.version = version
        self.product_base_path = Path(product_base_path or LCFM_BASE_PATH)

        self._bounds = None
        self.epsg = tile_to_epsg(tile)
        self.tile_block_id = f"{self.tile}_{self.block_id:03d}"

        self._product_subtype = "blocks"

    @property
    def bounds(self):
        if self._bounds is None:
            self._bounds = get_block_bounds(self.tile, self.block_id)
        return self._bounds

    def __str__(self) -> str:
        return f"<{self.project_product_id} {self.tile_block_id} Block Product>"

    def __repr__(self) -> str:
        return self.__str__()


class MonthlyS2BlockProduct(BaseS2BlockProduct):
    def __init__(
        self,
        tile,
        block_id,
        year,
        month,
        project_id,
        project_product_id,
        version="v001",
        product_base_path=None,
    ) -> None:
        super().__init__(
            tile, block_id, project_id, project_product_id, version, product_base_path
        )

        self.year = year
        self.month = month

        self.start_date = f"{year}{month:02d}01"

        _, last_day = calendar.monthrange(year, month)
        self.end_date = f"{year}{month:02d}{last_day}"

    def path(self, layer):
        tif_name = (
            f"{self.project_id}_{self.project_product_id}_"
            f"{self.start_date}_{self.end_date}_{self.tile}_"
            f"{self.block_id:03d}_{self.version.upper()}_{layer}.tif"
        )

        product_path = (
            self.product_base_path
            / self.project_product_id
            / self.version
            / self._product_subtype
            / slash_tile(self.tile)
            / str(self.year)
            / f"{self.month:02d}"
            / layer
            / tif_name
        )

        return product_path

    def __str__(self) -> str:
        return (
            f"<{self.project_id}_{self.project_product_id}_"
            f"{self.year}_{self.start_date}_{self.end_date}_{self.tile}_"
            f"{self.block_id:03d}_{self.version.upper()}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class AnnualS2BlockProduct(BaseS2BlockProduct):
    def __init__(
        self,
        tile,
        block_id,
        year,
        project_id,
        project_product_id,
        version="v001",
        product_base_path=None,
    ) -> None:
        super().__init__(
            tile, block_id, project_id, project_product_id, version, product_base_path
        )

        self.year = year

    def path(self, layer):
        tif_name = (
            f"{self.project_id}_{self.project_product_id}_"
            f"{self.year}_{self.tile}_"
            f"{self.block_id:03d}_{self.version.upper()}_{layer}.tif"
        )

        product_path = (
            self.product_base_path
            / self.project_product_id
            / self.version
            / self._product_subtype
            / slash_tile(self.tile)
            / str(self.year)
            / layer
            / tif_name
        )

        return product_path

    def __str__(self) -> str:
        return (
            f"<{self.project_id}_{self.project_product_id}_"
            f"{self.year}_{self.tile}_"
            f"{self.block_id:03d}_{self.version.upper()}>"
        )

    def __repr__(self) -> str:
        return self.__str__()


class BaseProductsCollection:
    def __init__(
        self, *, project_id, project_product_id, version, product_base_path=None
    ) -> None:
        self.project_id = project_id
        self.project_product_id = project_product_id
        self.version = version
        self.product_base_path = Path(product_base_path or LCFM_BASE_PATH)

    def __str__(self):
        return f"{self.project_product_id}_{self.version} Collection"

    def __repr__(self):
        return self.__str__()


class BaseMonthlyCollection(BaseProductsCollection):
    def block(self, tile: str, block_id: int, year: int, month: int):
        return MonthlyS2BlockProduct(
            tile=tile,
            block_id=block_id,
            year=year,
            month=month,
            project_id=self.project_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )

    def utm_tile(self, tile: str, year: int, month: int):
        return MonthlyUtmTileProduct(
            tile=tile,
            year=year,
            month=month,
            project_id=self.project_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )

    def latlon_3deg_tile(self, tile: str, year: int, month: int):
        return MonthlyLatLon3DegTileProduct(
            tile=tile,
            year=year,
            month=month,
            project_id=self.project_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )


class BaseAnnualCollection(BaseProductsCollection):
    def block(self, tile: str, block_id: int, year: int):
        return AnnualS2BlockProduct(
            tile=tile,
            block_id=block_id,
            year=year,
            project_id=self.project_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )

    def utm_tile(self, tile: str, year: int):
        return AnnualUtmTileProduct(
            tile=tile,
            year=year,
            project_id=self.project_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )

    def latlon_3deg_tile(self, tile: str, year: int):
        return AnnualLatLon3DegTileProduct(
            tile=tile,
            year=year,
            project_id=self.project_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )


class LsfAnnualCollection(BaseAnnualCollection):
    def __init__(
        self,
        project_product_id="LSF-ANNUAL",
        version="v001-satio",
        product_base_path=None,
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )


class LsfMonthlyCollection(BaseMonthlyCollection):
    def __init__(
        self, project_product_id="LSF-MONTHLY", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )


class Lcm10Collection(BaseAnnualCollection):
    def __init__(
        self, project_product_id="LCM-10", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )


class LsfMonthlyCollection(BaseMonthlyCollection):
    def __init__(
        self, project_product_id="LSF-MONTHLY", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )


class Lsc10MonthlyCollection(BaseMonthlyCollection):
    def __init__(
        self,
        project_product_id="LSC-10-MONTHLY",
        version="v001",
        product_base_path=None,
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )


class Lsc120MonthlyCollection(BaseMonthlyCollection):
    def __init__(
        self,
        project_product_id="LSC-120-MONTHLY",
        version="v001",
        product_base_path=None,
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )


######################################################################
# Old things, to remove once old files are renamed to new standard - dev8
class LsfMonthlyBlockProduct(BaseS2BlockProduct):
    def __init__(
        self,
        tile: str,
        block_id: int,
        band: str,
        year: int,
        month: int,
        project_product_id: str = "LSF-10-MONTHLY",
        version: str = "v001-median",
        product_base_path: str = None,
    ) -> None:
        """__init__ Constructor

        Args:
            tile (str): S2 Tile
            block_id (int): S2 block id
            band (str): Band name
            year (int): Year
            month (int): Month
            project_product_id (str, optional): Defaults to 'LSF-10-MONTHLY'.
            version (str, optional): Defaults to 'v001-median'.
            product_base_path (str, optional): Default folder path.
                                               Defaults to LCFM_BASE_PATH.
        """
        super().__init__(tile, block_id)

        self.band = band
        self.year = year
        self.month = month

        self.project_product_id = project_product_id
        self.version = version
        self.product_base_path = product_base_path or LCFM_BASE_PATH

    @property
    def path(self) -> Path:
        # LSF-10-MONTHLY/v001-median/blocks/05/V/NH/2020/01/B02/LCFM_LSF-10-B02-MONTHLY_05VNH_000.tif
        # tif_name = (
        #     f"LCFM_LSF-10-{self.band}-MONTHLY_{self.tile}_{self.block_id:03d}.tif")
        resolution = L2A_BANDS_RESOLUTIONS.get(self.band, 10)
        tif_name = (
            f"LCFM_{self.project_product_id}_{self.year}_{self.month:02d}_"
            f"{self.tile}_{self.block_id:03d}_{self.band}_{resolution}M.tif"
        )

        version_path = self.product_base_path / self.project_product_id / self.version
        block_path = (
            version_path
            / "blocks"
            / slash_tile(self.tile)
            / str(self.year)
            / f"{self.month:02d}"
            / self.band
            / tif_name
        )

        return block_path


class LsfAnnualBlocksCollection(BaseProductsCollection):
    def __init__(
        self, project_product_id="LSF-ANNUAL", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )

    def product(
        self, tile: str, block_id: int, band: str = "ALLBANDS", year: int = 2020
    ):
        return LsfAnnualBlockProduct(
            tile,
            block_id,
            band,
            year,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )


class LsfAnnualBlockProduct(BaseS2BlockProduct):
    """Land Surface Features - Annual - 10m"""

    def __init__(
        self,
        tile: str,
        block_id: int,
        band: str = "ALLBANDS",
        year: int = 2020,
        project_product_id="LSF-ANNUAL",
        version="v001-satio",
        product_base_path=None,
    ) -> None:
        super().__init__(
            tile,
            block_id,
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )

        self.band = band
        self.year = year

    @property
    def path(self):
        resolution = L2A_BANDS_RESOLUTIONS.get(self.band, 10)

        tif_name = (
            f"LCFM_{self.project_product_id}_{self.year}_{self.tile}_"
            f"{self.block_id:03d}_{self.band}_{resolution}M.tif"
        )

        version_path = self.product_base_path / self.project_product_id / self.version
        block_path = (
            version_path / "blocks" / slash_tile(self.tile) / str(self.year) / tif_name
        )

        return block_path


class LcmBlocksCollection(BaseProductsCollection):
    def __init__(
        self, project_product_id="LCM-10", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )

    def product(self, tile: str, block_id: int, year: int):
        return LcmBlockProduct(
            tile,
            block_id,
            year,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )


class LcmProductsCollection(BaseProductsCollection):
    def __init__(
        self, project_product_id="LCM-10", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )

    def block(self, tile: str, block_id: int, year: int):
        return LcmBlockProduct(
            tile,
            block_id,
            year,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )

    def latlon_tile(self, tile: str):
        return LcmTileProduct(
            tile,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )


class LcmBlockProduct(BaseS2BlockProduct):
    """Land Surface Features - Annual - 10m"""

    def __init__(
        self,
        tile: str,
        block_id: int,
        year: int,
        project_product_id="LCM-10",
        version="v001-satio",
        product_base_path=None,
    ) -> None:
        super().__init__(
            tile,
            block_id,
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )

        self.year = year

    def path(self, layer="PROB"):
        if layer not in ["MAP", "PROB", "PRED"]:
            raise ValueError("layer must be 'PROB' or 'PRED'")

        resolution = 10

        tif_name = (
            f"LCFM_{self.project_product_id}_{self.year}_{self.tile}_"
            f"{self.block_id:03d}_{layer}_{resolution}M.tif"
        )

        version_path = self.product_base_path / self.project_product_id / self.version
        block_path = (
            version_path
            / "blocks"
            / layer.lower()
            / slash_tile(self.tile)
            / str(self.year)
            / tif_name
        )

        return block_path

    @property
    def prob_path(self):
        return self.path(layer="PROB")

    @property
    def pred_path(self):
        return self.path(layer="PRED")


class LoiTilesCollection(BaseProductsCollection):
    def __init__(
        self, project_product_id="LOI-10", version="v001", product_base_path=None
    ) -> None:
        super().__init__(
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )

    def product(self, s2_product_id: str):
        return LoiTileProduct(
            s2_product_id,
            project_product_id=self.project_product_id,
            version=self.version,
            product_base_path=self.product_base_path,
        )


class LoiTileProduct(UtmTileProductMixin, BaseTileProduct):
    """Land Occlusion Index - 80m masks"""

    def __init__(
        self,
        s2_product_id,
        project_product_id="LOI-10",
        version="v001",
        product_base_path=None,
    ) -> None:
        self.s2_product_id = s2_product_id
        split = self.s2_product_id.split("_")

        tile = split[-2][1:]

        super().__init__(
            tile,
            project_id="LCFM",
            project_product_id=project_product_id,
            version=version,
            product_base_path=product_base_path,
        )
        self.date_str = split[2]
        date = parse(self.date_str)
        self.year = date.year
        self.month = date.month
        self.day = date.day

    @property
    def path(self):
        """Obtain LOI-10 mask product path from a S2 product id"""
        if self.version == "v000-sen4ldn":
            root_path_clouds = Path(
                "/vitodata/vegteam_vol2/data/sen4ldn/yearly_features/cloud_masks/"
            )

            model_name = "v0_80m_nodem_nolatlon"
            model_version = "version_0"
            mask_base_path = (
                f"{model_name}/{model_version}/"
                f"{self.tile}/{self.year}/{self.month}/"
                f"{self.s2_product_id}.tif"
            )
            product_path = root_path_clouds / mask_base_path

        else:
            tif_name = (
                f"LCFM_{self.project_product_id}_{self.tile}_{self.date_str}_mask.tif"
            )

            product_path = (
                self.product_base_path
                / self.project_product_id
                / self.version
                / "tiles"
                / slash_tile(self.tile)
                / str(self.year)
                / f"{self.month:02d}"
                / f"{self.day:02d}"
                / self.s2_product_id
                / tif_name
            )

        return product_path

    def read(
        self, bounds=None, fill_value=np.nan, bool_mask=True, blur=True, res_meth="NEAR"
    ):
        arr = load_cloudsen_mask(
            self.path,
            bounds=bounds,
            fill_value=fill_value,
            blur=blur,
            bool_mask=bool_mask,
            resampling_method=res_meth,
        )
        return arr
