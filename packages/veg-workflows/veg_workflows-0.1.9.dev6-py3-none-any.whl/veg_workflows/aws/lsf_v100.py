from typing import Dict, List

import satio
from elogs.elogs import ElogsBlocks, ElogsTask
from loguru import logger
from satio.collections import L2ACollection
from satio.geoloader import ParallelLoader

from veg_workflows.aws import SafePool
from veg_workflows.errors import NoAcquisitionsError
from veg_workflows.features import process_block_lsf_annual_v100


class LsfConfigV100:
    config_fields = (
        "app_id",
        "lsf_annual_version",
        "tiles",
        "blocks_number",
        "s2_db_uri",
        "blocks_grid_uri",
        "annual_periods",
        "chunks",
        "loi_version",
        "lsf_volume",
        "l2a_path",
        "year",
        "satio_max_workers",
        "satio_random_loading",
        "compositing_max_workers",
        "loi_loader_max_workers",
        "blocks_workers",
        "loi_volume",
        "rio_gdal_options",
        "skip_done",
        "skip_errors",
        "output_bucket",
        "overwrite_elogs_table",
    )

    def __init__(self, config: Dict, validate: bool = True):
        if validate:
            self.validate_config(config)

        for k in self.config_fields:
            setattr(self, k, config[k])

    def validate_config(self, config: Dict):
        for config_key in config.keys():
            if config_key not in self.config_fields:
                logger.warning(f"Unknown field: {config_key} in config")

        for required_key in self.config_fields:
            if required_key not in config:
                raise ValueError(
                    f"Missing required field: {required_key} in config"
                )

    def __getitem__(self, key):
        if key not in self.config_fields:
            raise KeyError(f"Unknown field: {key} in config")
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key not in self.config_fields:
            raise KeyError(f"Unknown field: {key} in config")
        setattr(self, key, value)

    def __repr__(self):
        return f"LsfConfig({self.app_id})"

    def __str__(self):
        return f"LsfConfig({self.app_id})"

    def to_dict(self):
        return {k: getattr(self, k) for k in self.config_fields}

    def to_json(self, fname=None, indent=2):
        import json

        if fname is None:
            fname = f"{self.app_id}.json"

        with open(fname, "w") as f:
            json.dump(self.to_dict(), f, indent=indent)

        return fname

    @classmethod
    def from_uri(cls, uri: str):
        from veg_workflows.aws import load_config

        config = load_config(uri)
        return cls(config)

    def to_uri(self, uri: str):
        import os

        from veg_workflows.aws import upload_config

        fname = self.to_json()
        upload_config(fname, uri)
        os.remove(fname)

    @property
    def blocks(self):
        from veg_workflows.aws import get_blocks

        blocks = get_blocks(self.blocks_grid_uri, self.s2_db_uri)
        blocks_number = self.blocks_number
        tiles = self.tiles

        if tiles is not None:
            blocks = blocks[blocks.tile.isin(tiles)]

        if isinstance(blocks_number, int):
            if blocks_number > 0:
                return blocks.sample(n=blocks_number, random_state=42)
            elif blocks_number == 0:
                return blocks
            else:
                raise ValueError(
                    "blocks_number must be a positive integer "
                    "or zero (all blocks) or a list of block ids"
                )
        elif isinstance(blocks_number, list):
            blocks = blocks[blocks.tile_block_id.isin(blocks_number)]
            if len(blocks) == 0:
                raise ValueError("No blocks found for the specified block ids")
            return blocks
        else:
            raise ValueError(
                "blocks_number must be a positive integer "
                "or zero (all blocks) or a list of block ids"
            )

    @property
    def tasks_tiles(self):
        from elogs.elogs import ElogsTask

        blocks = self.blocks
        tiles = blocks.tile.unique()
        tasks = [
            ElogsTask(
                tile,
                tile=tile,
                block_ids=sorted(
                    blocks.query(f"tile == '{tile}'").block_id.values.tolist()
                ),
            )
            for tile in tiles
        ]
        return tasks

    @property
    def tasks_blocks(self):
        from elogs.elogs import ElogsTask

        blocks = self.blocks
        tasks = [
            ElogsTask(
                tile_block_id,
                tile_block_id,
            )
            for tile_block_id in blocks.tile_block_id.values
        ]
        return tasks


class LsfAnnualTileProcessor:
    def __init__(
        self,
        lsf_config: LsfConfigV100,
        debug_mode: bool = False,
    ) -> None:
        self.app_id = lsf_config.app_id
        self.debug_mode = debug_mode

        self.config = lsf_config

        table_name = f"{self.app_id}_blocks"
        self.elogs_blocks = ElogsBlocks(
            table_name,
            skip_done=lsf_config.skip_done,
            skip_errors=lsf_config.skip_errors,
            overwrite_table=False,  #
            custom_entry_builder=None,
            force_process_termination=True,
            register_signal_handlers=False,
        )
        self.s2grid = satio.layers.load("s2grid")
        self.l2a_collection = self.get_satio_collection(
            lsf_config.l2a_path,
            s2grid=self.s2grid,
            loader_threads=lsf_config.satio_max_workers,
            random_loading=lsf_config.satio_random_loading,
            rio_gdal_options=lsf_config.rio_gdal_options,
        )

    @staticmethod
    def get_satio_collection(
        l2a_path,
        s2grid=None,
        loader_threads=1,
        random_loading=True,
        rio_gdal_options=None,
    ):
        l2a_collection = L2ACollection.from_path(l2a_path, s2grid=s2grid)
        l2a_collection._loader = ParallelLoader(
            max_workers=loader_threads,
            random_order=random_loading,
            rio_gdal_options=rio_gdal_options,
        )
        return l2a_collection

    def _process_block(self, tile_block_id):
        from satio.grid import get_blocks_gdf

        tile, block_id = tile_block_id.split("_")
        block_id = int(block_id)

        block = (
            get_blocks_gdf([tile], self.s2grid)
            .query(f"block_id == {block_id}")
            .iloc[0]
        )

        # vars setup
        bounds = block.bounds
        epsg = block.epsg

        if self.debug_mode:
            from satio.grid import buffer_bounds

            logger.debug("DEBUG MODE: Processing block with reduced bounds")
            bounds = buffer_bounds(bounds, int((640 - 10240) / 2))

        config = self.config

        return process_block_lsf_annual_v100(
            self.l2a_collection,
            tile,
            block_id,
            bounds=bounds,
            epsg=epsg,
            year=config.year,
            loi_version="v100",
            lsf_annual_version=config.lsf_annual_version,
            lsf_volume=config.lsf_volume,
            annual_periods=config.annual_periods,
            loi_weights_params=None,
            interpolation_params=None,
            chunks=config.chunks,
            rio_gdal_options=config.rio_gdal_options,
            compositing_max_workers=config.compositing_max_workers,
            loi_loader_max_workers=config.loi_loader_max_workers,
            loi_volume=config.loi_volume,
            upload=True,
            bucket=config.output_bucket,
            cache_path=".",
            delete_after_upload=True,
        )

    def process_block(self, tile_block_id):
        @self.elogs_blocks
        def process_func(tile_block_id):
            try:
                return self._process_block(tile_block_id)
            except NoAcquisitionsError as e:
                logger.error(e)

        task = ElogsTask(tile_block_id, tile_block_id)
        process_func(task)

    def process_tile(
        self, tile: str, blocks_ids: List = None, workers: int = 1
    ):
        if blocks_ids is None:
            blocks_ids = list(range(121))

        tile_block_ids = [f"{tile}_{block_id:03d}" for block_id in blocks_ids]

        logger.info("Starting blocks processing...")

        if workers < 1:
            logger.info(
                f"Processing {len(tile_block_ids)} blocks "
                "sequentially in main thread"
            )
            for b in tile_block_ids:
                self.process_block(b)

        elif workers >= 1:
            logger.info(
                f"Processing {len(tile_block_ids)} blocks "
                f"with {workers} parallel processes"
            )

            pool = SafePool(workers=workers, update_interval=10)
            pool.map(self.process_block, tile_block_ids)
