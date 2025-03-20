"""SQLite dbs to quickly query s2 grid tiles bounds and blocks

DBs

- s2tiles.db: Contains the bounds of each s2 grid tile
    Columns: tile, epsg, xmin, ymin, xmax, ymax

- s2blocks.db: Contains the bounds of each s2 grid block
    Columns: tile_block_id, tile, block_id, landtype, antimeridian, xmin, ymin, xmax, ymax
    where cid = f"{tile}_{block_id}"

"""

import sqlite3
from importlib.resources import as_file, files
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from satio_pc.grid import get_blocks_gdf

S2TILES_DB = files("veg_workflows.db").joinpath("s2tiles.db")
# S2BLOCKS_DB = files("veg_workflows.db").joinpath('s2blocks.db')  # too big
S2BLOCKS_DB = Path("/vitodata/vegteam/auxdata/grid/sqlite_dbs/s2blocks.db")
LATLON_3DEG_DB = files("veg_workflows.db").joinpath("latlon_3deg_grid.db")

S2TILES_COLUMNS = ["tile", "epsg", "xmin", "ymin", "xmax", "ymax"]
S2BLOCKS_COLUMNS = [
    "tile_block_id",
    "tile",
    "block_id",
    "epsg",
    "ice",
    "xmin",
    "ymin",
    "xmax",
    "ymax",
]
LATLON_GRID_COLUMNS = ["tile", "xmin", "ymin", "xmax", "ymax"]

# Function to query the database by tile


def build_latlon_3deg_db():
    import geopandas as gpd
    from sqlalchemy import create_engine

    from veg_workflows.paths.grids import WORLDCOVER_3DEG_SQUARES

    grid = gpd.read_file(WORLDCOVER_3DEG_SQUARES)
    bounds = grid.bounds
    grid["xmin"] = bounds.minx
    grid["ymin"] = bounds.miny
    grid["xmax"] = bounds.maxx
    grid["ymax"] = bounds.maxy
    grid = grid.rename(columns={"ll_tile": "tile"})

    grid = grid[LATLON_GRID_COLUMNS]

    grid.set_index("tile", inplace=True)

    db_fn = "latlon_3deg_grid.db"

    engine = create_engine(f"sqlite:///{db_fn}")
    grid.to_sql("latlon_3deg_grid", con=engine, if_exists="replace")


def build_s2tiles_db():
    """Builds the s2tiles database"""
    import geopandas as gpd
    from sqlalchemy import create_engine

    from veg_workflows.paths.grids import S2_GRID_PATH

    s2grid = gpd.read_file(S2_GRID_PATH)

    s2grid["bounds"] = s2grid["bounds"].apply(eval)
    s2grid["xmin"] = s2grid["bounds"].apply(lambda x: int(x[0]))
    s2grid["ymin"] = s2grid["bounds"].apply(lambda x: int(x[1]))
    s2grid["xmax"] = s2grid["bounds"].apply(lambda x: int(x[2]))
    s2grid["ymax"] = s2grid["bounds"].apply(lambda x: int(x[3]))
    s2grid = s2grid[S2TILES_COLUMNS]
    s2grid.set_index("tile", inplace=True)

    db_fn = "s2tiles.db"

    engine = create_engine(f"sqlite:///{db_fn}")
    s2grid.to_sql("s2tiles", con=engine, if_exists="replace")


def build_s2blocks_db():
    import geopandas as gpd
    import numpy as np
    from sqlalchemy import create_engine

    from veg_workflows.paths.grids import BLOCKS_GRID_PATH

    blocks = gpd.read_file(BLOCKS_GRID_PATH)
    blocks["bounds"] = blocks["bounds"].apply(eval)
    blocks = blocks.drop(columns=["geometry"])
    blocks["xmin"] = blocks["bounds"].apply(lambda x: int(x[0]))
    blocks["ymin"] = blocks["bounds"].apply(lambda x: int(x[1]))
    blocks["xmax"] = blocks["bounds"].apply(lambda x: int(x[2]))
    blocks["ymax"] = blocks["bounds"].apply(lambda x: int(x[3]))

    blocks["tile_block_id"] = blocks.apply(
        lambda x: f"{x['tile']}_{x['block_id']:03d}", axis=1
    )
    blocks["ice"] = (
        blocks["landtype"].apply(lambda x: True if x == "ice" else False).astype(bool)
    )
    blocks = blocks[S2BLOCKS_COLUMNS]
    blocks.set_index("tile_block_id", inplace=True)

    db_fn = "s2blocks.db"
    engine = create_engine(f"sqlite:///{db_fn}")
    blocks.to_sql("s2blocks", con=engine, if_exists="replace")

    for c in blocks.columns:
        if blocks[c].dtype == "object":
            blocks[c] = blocks[c].astype(str)
        elif blocks[c].dtype == np.int64:
            blocks[c] = blocks[c].astype(np.int32)

    # create additional index for the tiles
    conn = sqlite3.connect(db_fn)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX idx_tile ON s2blocks (tile)")
    conn.commit()


def query_tile(tile: str) -> Tuple:
    # Connect to the SQLite database on disk

    with as_file(S2TILES_DB) as db:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query the database using the tile as the index
        cursor.execute("SELECT * FROM s2tiles WHERE tile=?", (tile,))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

    return result


def query_tiles(tiles: List) -> List:
    with as_file(S2TILES_DB) as db:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query the database using the tile as the index
        tiles_str = ",".join(["?"] * len(tiles))
        cursor.execute(f"SELECT * FROM s2tiles WHERE tile IN ({tiles_str})", tiles)
        result = cursor.fetchall()

        # Close the connection
        conn.close()

    return result


def query_latlon_tile(tile: str) -> Tuple:
    with as_file(LATLON_3DEG_DB) as db:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query the database using the tile as the index
        cursor.execute("SELECT * FROM latlon_3deg_grid WHERE tile=?", (tile,))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

    return result


def query_latlon_tiles(tiles: List) -> List:
    with as_file(LATLON_3DEG_DB) as db:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query the database using the tile as the index
        tiles_str = ",".join(["?"] * len(tiles))
        cursor.execute(
            f"SELECT * FROM latlon_3deg_grid WHERE tile IN ({tiles_str})", tiles
        )
        result = cursor.fetchall()

        # Close the connection
        conn.close()

    return result


def query_block(tile, block_id):
    with as_file(S2BLOCKS_DB) as db:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query the database using the tile and block_id as the index
        cursor.execute(
            "SELECT * FROM s2blocks WHERE tile_block_id=?", (f"{tile}_{block_id:03d}",)
        )
        result = cursor.fetchone()

        # Close the connection
        conn.close()

    return result


def query_blocks(tiles: List):
    with as_file(S2BLOCKS_DB) as db:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Query the database using LIKE and the tile_prefix
        # Query the database using the tile as the index
        tiles_str = ",".join(["?"] * len(tiles))
        cursor.execute(f"SELECT * FROM s2blocks WHERE tile IN ({tiles_str})", tiles)
        result = cursor.fetchall()

        # Close the connection
        conn.close()

    return result


def get_blocks_df(tiles):
    blocks = get_blocks_gdf(tiles)

    blocks["tile_block_id"] = blocks.apply(
        lambda x: f"{x['tile']}_{x['block_id']:03d}", axis=1
    )
    blocks["ice"] = False
    bounds = blocks["bounds"].values
    (blocks["xmin"], blocks["ymin"], blocks["xmax"], blocks["ymax"]) = zip(*bounds)
    df = blocks[S2BLOCKS_COLUMNS]
    return df


def get_blocks(tiles: List[str]) -> List:
    blocks = query_blocks(tiles)
    if blocks is None:
        blocks = get_blocks_df(tiles)
    else:
        df = pd.DataFrame(blocks, columns=S2BLOCKS_COLUMNS)

    return df


def get_utm_tile_bounds(tile: str) -> Tuple:
    tile_attrs = query_tile(tile)
    tile_attrs = dict(zip(S2TILES_COLUMNS, tile_attrs))
    bounds = (
        tile_attrs["xmin"],
        tile_attrs["ymin"],
        tile_attrs["xmax"],
        tile_attrs["ymax"],
    )
    return bounds


def get_block_bounds(tile, block_id):
    block_attrs = query_block(tile, block_id)
    if block_attrs is None:
        block_attrs = get_blocks_df([tile])
        block_attrs = block_attrs[block_attrs.block_id == block_id].iloc[0]
        bounds = (
            block_attrs.xmin,
            block_attrs.ymin,
            block_attrs.xmax,
            block_attrs.ymax,
        )
    else:
        block_attrs = dict(zip(S2BLOCKS_COLUMNS, block_attrs))
        bounds = (
            block_attrs["xmin"],
            block_attrs["ymin"],
            block_attrs["xmax"],
            block_attrs["ymax"],
        )
    return bounds


def get_latlon_tile_bounds(tile: str) -> Tuple:
    tile_attrs = query_latlon_tile(tile)
    tile_attrs = dict(zip(LATLON_GRID_COLUMNS, tile_attrs))
    bounds = (
        tile_attrs["xmin"],
        tile_attrs["ymin"],
        tile_attrs["xmax"],
        tile_attrs["ymax"],
    )
    return bounds
