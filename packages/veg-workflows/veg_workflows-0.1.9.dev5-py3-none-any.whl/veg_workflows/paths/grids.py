from pathlib import Path

WORLDCOVER_EXTENT = [-180, -60, 180, 82.75]

LCFM_SHAPEFILES_PATH = Path("/vitodata/vegteam_vol2/data/lcfm/shapefiles")

# 1% (0.5%) tiles
LCFM_1PERCENT_TILES_FGB = LCFM_SHAPEFILES_PATH / "LCFM-1_S2_tiles.fgb"

# 10% AOI
LCFM_10PERCENT = LCFM_SHAPEFILES_PATH / "LCFM_10percent_v5-1.fgb"
LCFM_10PERCENT_BUFFERED004 = (
    LCFM_SHAPEFILES_PATH / "LCFM_10percent_v5-1_buffered004.fgb"
)

# 10% tiles. V2 is the one with less tiles but inconsistent with the
# global blocks grid. V1 is the one with more tiles but consistent with the
# global blocks grid.
LCFM_10PERCENT_TILES_V1_FGB = (
    LCFM_SHAPEFILES_PATH / "LCFM-10_S2_tiles_v1.fgb"
)  # file not found
LCFM_10PERCENT_TILES_V2_FGB = LCFM_SHAPEFILES_PATH / "LCFM-10_S2_tiles_v2.fgb"
LCFM_10PERCENT_TILES_V3_FGB = LCFM_SHAPEFILES_PATH / "LCFM-10_S2_tiles_v3.fgb"
LCFM_10PERCENT_TILES_FGB = LCFM_10PERCENT_TILES_V3_FGB

# 10% blocks. V1 is consistent with the global blocks grid.
LCFM_10PERCENT_BLOCKS_V1_FGB = LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_v1.fgb"
LCFM_10PERCENT_BLOCKS_MISSING_V1_FGB = (
    LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_missing_v1.fgb"
)
LCFM_10PERCENT_BLOCKS_V2_FGB = (
    LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_v2.fgb"
)  # integrated missing blocks
LCFM_10PERCENT_BLOCKS_V3_FGB = LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_v3.fgb"
LCFM_10PERCENT_BLOCKS_FGB = LCFM_10PERCENT_BLOCKS_V3_FGB

# 10% blocks TCD.
LCFM_10PERCENT_BLOCKS_TCD_V1_FGB = LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_tcd_v1.fgb"
LCFM_10PERCENT_BLOCKS_MISSING_V1_TCD_FGB = (
    LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_missing_v1_tcd.fgb"
)
LCFM_10PERCENT_BLOCKS_TCD_V2_FGB = LCFM_SHAPEFILES_PATH / "LCFM-10_S2_blocks_tcd_v2.fgb"
LCFM_10PERCENT_BLOCKS_TCD_V4_FGB = (
    LCFM_SHAPEFILES_PATH / "LCFM_blocks_10percent_TCD_v4.fgb"
)
LCFM_10PERCENT_BLOCKS_TCD_FGB = LCFM_10PERCENT_BLOCKS_TCD_V4_FGB

# Tropical AOI
LCFM_TROPICAL_AOI_V1_FGB = LCFM_SHAPEFILES_PATH / "LCFM_tropical_AOI_v1.fgb"


SEN4LDN_SHAPEFILES_PATH = Path("/vitodata/vegteam/projects/sen4ldn/shapefiles")
SEN4LDN_TILES_FGB = SEN4LDN_SHAPEFILES_PATH / "sen4ldn_countries_tiles.fgb"
SEN4LDN_COUNTRIES_FGB = SEN4LDN_SHAPEFILES_PATH / "sen4ldn_countries.fgb"
SEN4LDN_COUNTRIES_BUF01_FGB = SEN4LDN_SHAPEFILES_PATH / "sen4ldn_countries_buf01.fgb"
SEN4LDN_BLOCKS_ALL_FGB = (
    SEN4LDN_SHAPEFILES_PATH / "sen4ldn_countries_blocks_no_overlap.fgb"
)
SEN4LDN_BLOCKS_FGB = (
    SEN4LDN_SHAPEFILES_PATH / "sen4ldn_countries_blocks_no_overlap_reduced_buf01.fgb"
)

# grids
VEG_GRIDS_PATH = Path("/vitodata/vegteam/auxdata/grid")

WORLDCOVER_3DEG = VEG_GRIDS_PATH / "esa_worldcover_2020_3deg.fgb"
WORLDCOVER_3DEG_SQUARES = VEG_GRIDS_PATH / "esa_worldcover_2020_3deg_squares_v2.fgb"
LCFM_10PERCENT_3DEG_SQUARES = (
    VEG_GRIDS_PATH / "esa_worldcover_2020_3deg_squares_v2_lcfm_10percent.fgb"
)

# grid for LCM100 30deg
LCFM_LCM100_30DEG = LCFM_SHAPEFILES_PATH / "LCFM_LCM100_30deg.fgb"

LATLON_10DEG = VEG_GRIDS_PATH / "latlon_grid_10deg.geojson"
LATLON_5DEG = VEG_GRIDS_PATH / "latlon_grid_5deg.geojson"
LATLON_1DEG_LANDMASS = VEG_GRIDS_PATH / "latlon_grid_1deg_landmass.geojson"

VEG_GRIDS_H3_PATH = VEG_GRIDS_PATH / "h3"
H3_GRID_RES2 = VEG_GRIDS_H3_PATH / "h3_grid_res2.fgb"
H3_GRID_RES2_LAND = VEG_GRIDS_H3_PATH / "h3_grid_res2_land.fgb"
H3_GRID_RES3 = VEG_GRIDS_H3_PATH / "h3_grid_res3.fgb"
H3_GRID_RES4 = VEG_GRIDS_H3_PATH / "h3_grid_res4.fgb"

# Blocks
BLOCKS_GRID_PATH = VEG_GRIDS_PATH / "blocks_global" / "blocks_global_v9_all.fgb"
BLOCKS_GRID_TCD_PATH = (
    VEG_GRIDS_PATH / "blocks_global" / "tropical_blocks_global_v10.fgb"
)
# S2 Grid
S2_GRID_PATH = VEG_GRIDS_PATH / "s2_grid_kml/s2grid_kml_latlon_land_v1_bounds.gpkg"

# Shapefile of the world with borders
WORLD_BORDERS = Path("/vitodata/vegteam/auxdata/eo_layers/world_countries_border.fgb")
