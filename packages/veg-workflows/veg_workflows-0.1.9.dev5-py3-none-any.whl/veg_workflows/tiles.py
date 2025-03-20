from pathlib import Path

import geopandas as gpd
from satio.grid import get_blocks_gdf

from veg_workflows.paths.grids import (
    BLOCKS_GRID_PATH,
    LCFM_1PERCENT_TILES_FGB,
    LCFM_10PERCENT_BLOCKS_FGB,
    LCFM_10PERCENT_BLOCKS_TCD_FGB,
    LCFM_10PERCENT_TILES_FGB,
    SEN4LDN_BLOCKS_FGB,
    SEN4LDN_TILES_FGB,
    WORLDCOVER_3DEG_SQUARES,
)


def load_missing_v1_blocks():
    from veg_workflows.paths.grids import LCFM_10PERCENT_BLOCKS_MISSING_V1_FGB

    blocks = gpd.read_file(LCFM_10PERCENT_BLOCKS_MISSING_V1_FGB)
    blocks["bounds"] = blocks["bounds"].apply(eval)

    bounds = blocks["bounds"].values
    (blocks["xmin"], blocks["ymin"], blocks["xmax"], blocks["ymax"]) = zip(*bounds)

    blocks["tile_block_id"] = blocks.apply(
        lambda x: f"{x.tile}_{x.block_id:03d}", axis=1
    )

    return blocks


class _TilesBase:
    _path = None

    def __init__(self) -> None:
        self._tiles_gdf = None
        self._blocks = None

    @property
    def tiles_gdf(self):
        if self._tiles_gdf is None:
            self._tiles_gdf = gpd.read_file(self._path)
        return self._tiles_gdf

    @property
    def tiles(self):
        return self.tiles_gdf.tile.values

    def get_blocks(self, remove_overlapping_blocks=True):
        if remove_overlapping_blocks:
            blocks = gpd.read_file(BLOCKS_GRID_PATH, mask=self.tiles_gdf.unary_union)
            blocks["bounds"] = blocks["bounds"].apply(eval)
        else:
            blocks = get_blocks_gdf(self.tiles)

        bounds = blocks["bounds"].values
        (blocks["xmin"], blocks["ymin"], blocks["xmax"], blocks["ymax"]) = zip(*bounds)

        if "cid" not in blocks.columns:
            blocks["cid"] = blocks["tile"] + "_" + blocks["block_id"].astype(str)

        return blocks

    @property
    def blocks(self):
        if self._blocks is None:
            self._blocks = self.get_blocks()
        return self._blocks


class _LcfmTiles10Percent(_TilesBase):
    _path = LCFM_10PERCENT_TILES_FGB
    _remove_overlapping_blocks = True

    def get_blocks(self):
        return get_lcfm_10percent_blocks()

    @property
    def blocks_tcd(self):
        if not hasattr(self, "_blocks_tcd"):
            self._blocks_tcd = get_lcfm_10percent_tcd_blocks()
        return self._blocks_tcd


class _LcfmTiles1Percent(_TilesBase):
    _path = LCFM_1PERCENT_TILES_FGB
    _remove_overlapping_blocks = False


class _Sen4LdnTiles(_TilesBase):
    _path = SEN4LDN_TILES_FGB
    _remove_overlapping_blocks = True

    def get_blocks(self):
        blocks = gpd.read_file(SEN4LDN_BLOCKS_FGB)
        return blocks

    @property
    def tiles_cdr(self):
        tiles = [
            "36NTF",
            "36NUF",
            "36MTE",
            "36MUE",
            "36NXF",
            "36NVF",
            "36NWF",
            "36NXG",
            "36NXH",
            "36NWH",
            "36NVH",
            "36NWG",
            "36NVG",
            "36NUG",
            "36NUH",
            "36NWK",
            "36NVJ",
            "36NWJ",
            "36NXJ",
            "36NXK",
            "29TQG",
            "29TPG",
            "29TQF",
            "29TPF",
            "29TPE",
            "29SPD",
            "29SPC",
            "29SPB",
            "29SNB",
            "29SMD",
            "29SMC",
            "29SNC",
            "29SND",
            "29TNE",
            "29TME",
            "29TNF",
            "29TNG",
            "18NYL",
            "18NXL",
            "18NVL",
            "18NWL",
            "18NWM",
            "18NVM",
            "18NUM",
            "18NUL",
            "18NTJ",
            "18NUJ",
            "18NTK",
            "18NUK",
            "18NVK",
            "18NWK",
            "18NXK",
            "18NWJ",
            "18NVJ",
            "18NYH",
        ]
        return tiles


def _load_blocks_gdf(path):
    blocks = gpd.read_file(path)
    blocks["bounds"] = blocks["bounds"].apply(eval)
    bounds = blocks["bounds"].values
    (blocks["xmin"], blocks["ymin"], blocks["xmax"], blocks["ymax"]) = zip(*bounds)
    return blocks


def get_lcfm_10percent_blocks():
    return _load_blocks_gdf(LCFM_10PERCENT_BLOCKS_FGB)


def get_lcfm_10percent_tcd_blocks():
    return _load_blocks_gdf(LCFM_10PERCENT_BLOCKS_TCD_FGB)


def get_sen4ldn_ppr_blocks():
    return _load_blocks_gdf(SEN4LDN_BLOCKS_FGB)


def get_latlon_3deg_grid():
    grid = gpd.read_file(WORLDCOVER_3DEG_SQUARES)
    return grid


lcfm_tiles_10percent = _LcfmTiles10Percent()
lcfm_tiles_1percent = _LcfmTiles1Percent()
sen4ldn_tiles = _Sen4LdnTiles()
