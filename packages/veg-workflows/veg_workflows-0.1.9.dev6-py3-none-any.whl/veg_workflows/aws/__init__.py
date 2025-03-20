import multiprocessing as mp
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import boto3
import botocore
import pandas as pd
import rasterio
from elogs.s3 import S3BucketReader
from satio.collections import L2ACollection
from satio.geoloader import (
    BACKOFF,
    DELAY,
    RETRIES,
    ParallelLoader,
    get_jp2_filenames,
    get_l2a_aws_filenames,
    retry,
)
from satio_pc import parallelize
from satio_pc.extension import SatioTimeSeries  # noqa

from veg_workflows.errors import MaxDiskUsageError

RIO_GDAL_OPTIONS = {
    "AWS_REGION": "eu-central-1",
    "AWS_REQUEST_PAYER": "requester",
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "GDAL_HTTP_MAX_RETRY": 3,
    "GDAL_HTTP_RETRY_DELAY": 1,
    "GDAL_HTTP_TCP_KEEPALIVE": "YES",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".jp2,.tif",
    "CPL_VSIL_CURL_CHUNK_SIZE": 100_000,
    "CPL_VSIL_CURL_CACHE_SIZE": 1_000_000,
    "CPL_VSIL_CURL_CACHE": "YES",
    "CPL_VSIL_CURL_USE_HEAD": "YES",
}


def parse_s3_uri(s3_uri):
    """Parse an S3 URI and return the bucket and key."""
    if not s3_uri.startswith("s3://"):
        raise ValueError("Invalid S3 URI")
    parts = s3_uri[5:].split(
        "/", 1
    )  # Remove "s3://" and split into bucket and key
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    return bucket, key


def get_blocks(blocks_grid_uri, s2_db_uri, tiles=None):
    blocks = pd.read_parquet(blocks_grid_uri)
    s2_db = pd.read_parquet(s2_db_uri)
    if tiles is not None:
        blocks = blocks[blocks.tile.isin(tiles)]
    blocks = blocks[blocks.tile.isin(s2_db.tile.unique())]
    return blocks


def get_aws_s2_df(s2_db_uri):
    s2_db = pd.read_parquet(s2_db_uri)
    s2_db = s2_db[s2_db.sensing_time.dt.year == 2020]
    # s2_db = s2_db[s2_db.sensing_time.dt.month == 6]  # to debug faster
    s2_db["level"] = "L2A"
    s2_db = s2_db.rename(columns={"sensing_time": "date", "s3_uri": "path"})
    s2_db["baseline"] = s2_db.product_id.apply(lambda x: x.split("_")[3])
    s2_db["orbit"] = s2_db.product_id.apply(lambda x: x.split("_")[4])
    s2_db["path"] = s2_db.s3_uri.apply(lambda x: x.replace("s3://", "/vsis3/"))

    cols = ["level", "product_id", "date", "baseline", "orbit", "tile", "path"]

    return s2_db[cols]


def get_aws_satio_collection(
    s2_db_uri, s2grid=None, tile=None, progressbar=False, max_workers=20
):
    s2_df = get_aws_s2_df(s2_db_uri)
    s2_collection = L2AAWSJP2Collection(s2_df, s2grid=s2grid)
    if tile is not None:
        s2_collection = s2_collection.filter_tiles(tile)

    _ = s2_collection.loader
    s2_collection._loader._progressbar = progressbar
    s2_collection._loader._max_workers = max_workers

    return s2_collection


class AWSL2AParallelLoader(ParallelLoader):
    def __init__(
        self,
        rio_gdal_options=None,
        max_workers=20,
        fill_value=0,
        progressbar=False,
    ):
        if rio_gdal_options is None:
            rio_gdal_options = RIO_GDAL_OPTIONS

        super().__init__(
            rio_gdal_options=rio_gdal_options,
            max_workers=max_workers,
            fill_value=fill_value,
            progressbar=progressbar,
        )

    @retry(
        exceptions=Exception,
        tries=RETRIES,
        delay=DELAY,
        backoff=BACKOFF,
        logger=None,
    )
    def _load_array_bounds(self, fname, bounds):
        with rasterio.Env(**self._rio_gdal_options):
            with rasterio.open(fname) as src:
                window = src.window(*bounds)
                arr = src.read(
                    1,
                    window=window,
                    boundless=True,
                    fill_value=self._fill_value,
                )

        return arr


class L2AAWSJP2Collection(L2ACollection):
    @property
    def loader(self):
        if self._loader is None:
            self._loader = AWSL2AParallelLoader()
        return self._loader

    def get_band_filenames(self, band, resolution):
        if self._filenames is None:
            self._filenames = self.df["path"].apply(
                lambda x: get_l2a_aws_filenames(x)
            )

        jp2_filenames = self._filenames.apply(
            lambda x: get_jp2_filenames(x, band, resolution)
        )

        return jp2_filenames.values.tolist()


def disk_usage(path=None, max_disk_usage=None, verbose=False):
    if path is None:
        path = os.environ.get("LCFM_MAX_DISK_USAGE_MOUNT", "/")

    total, used, free = shutil.disk_usage(path)
    s = 2**30
    total /= s
    used /= s
    free /= s

    if max_disk_usage is None:
        max_disk_usage = int(os.environ.get("LCFM_MAX_DISK_USAGE", 0))

    if (max_disk_usage > 0) and (used > max_disk_usage):
        raise MaxDiskUsageError(
            f"Disk usage: {used} GB, exceeded"
            f" threshold: {max_disk_usage} GB"
        )

    if verbose:
        from loguru import logger

        logger.info(
            f"Disk usage - used: {used // (2**30)}/{total // (2**30)} GiB"
        )

    return total, used, free


def get_bucket_client(bucket="vito-lcfm") -> S3BucketReader:
    from elogs.s3 import S3BucketReader

    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    s3 = S3BucketReader.from_credentials(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        bucket=bucket,
    )
    return s3


def load_config(config_uri):
    bucket, key = parse_s3_uri(config_uri)
    s3 = get_bucket_client(bucket)
    config = s3.read_json(key)
    return config


def upload_config(config_json, config_uri):
    bucket, key = parse_s3_uri(config_uri)
    s3 = get_bucket_client(bucket)
    s3.upload(config_json, key)


def get_spark_context(local, threads=1):
    import sys
    from datetime import datetime

    from pyspark import SparkConf, SparkContext

    conf = SparkConf().setAppName(
        f"lcf_sparkapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    # conf.set(
    #     "spark.serializer",
    #     "org.apache.spark.serializer.KryoSerializer",
    # )
    # conf.set(
    #     "spark.kryo.registrationRequired", "false"
    # )  # (Set to true and register classes for even more efficiency)

    if local:
        from loguru import logger

        logger.info(f"Setting env var: PYSPARK_PYTHON={sys.executable}")
        os.environ["PYSPARK_PYTHON"] = sys.executable

        conf.setMaster(f"local[{threads}]")
        conf.set("spark.driver.bindAddress", "127.0.0.1")

    sc = SparkContext(conf=conf)

    return sc


def spark_foreach(spark_context, func, iterable, num_slices=None):
    if (num_slices is None) or (num_slices < 1):
        num_slices = len(iterable)
        num_slices = max(1, num_slices)

    try:
        rdd = spark_context.parallelize(iterable, num_slices)
        rdd.foreach(func)
    except Exception as e:
        from loguru import logger

        logger.error(f"Error in spark_foreach: {e}")
        raise e
    finally:
        spark_context.stop()


@dataclass
class L2AProductKeyFname:
    key: str
    fname: str


class AWSL2ABucket(S3BucketReader):
    def __init__(self, client, bucket="sentinel-s2-l2a"):
        super().__init__(client, bucket, requester_pays=True)

    @classmethod
    def from_credentials(
        cls, aws_access_key_id, aws_secret_access_key, max_pool_connections=100
    ):
        client_config = botocore.config.Config(
            max_pool_connections=max_pool_connections,
        )

        AWS_REGION = "eu-central-1"  # L2A bucket location
        client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=AWS_REGION,
            config=client_config,
        )
        return cls(client)

    def _get_product_keys_fnames(
        self,
        product_id,
        product_key,
        download_folder,
        bands_10m=["B02", "B03", "B04", "B08"],
        bands_20m=["B11", "B12"],
        bands_60m=[],
    ):
        r10_files = [f"R10m/{b}.jp2" for b in bands_10m]
        r20_files = [f"R20m/{b}.jp2" for b in bands_20m]
        r60_files = [f"R60m/{b}.jp2" for b in bands_60m]

        basenames = r10_files + r20_files + r60_files

        separator = "" if product_key.endswith("/") else "/"
        keys = [f"{product_key}{separator}{f}" for f in basenames]

        download_folder = Path(download_folder)
        product_folder = download_folder / product_key
        # product_folder.mkdir(parents=True, exist_ok=True, mode=0o775)

        # for f in ["R10m", "R20m", "R60m"]:
        #     sub_folder = product_folder / f
        #     sub_folder.mkdir(parents=True, exist_ok=True)

        dst_filenames = [product_folder / product_id / b for b in basenames]
        for dst_fname in dst_filenames:
            dst_fname.parent.mkdir(parents=True, exist_ok=True, mode=0o775)

        keys_fnames = [
            L2AProductKeyFname(k, d) for k, d in zip(keys, dst_filenames)
        ]
        return keys_fnames

    def get_products_keys_fnames(
        self,
        products_ids,
        products_keys,
        download_folder,
        bands_10m=["B02", "B03", "B04", "B08"],
        bands_20m=["B11", "B12"],
        bands_60m=[],
    ):
        keys_fnames = []
        for product_id, product_key in zip(products_ids, products_keys):
            keys_fnames += self._get_product_keys_fnames(
                product_id,
                product_key,
                download_folder,
                bands_10m=bands_10m,
                bands_20m=bands_20m,
                bands_60m=bands_60m,
            )
        return keys_fnames

    def download_products(
        self,
        products_ids,
        products_keys,
        download_folder,
        bands_10m=["B02", "B03", "B04", "B08"],
        bands_20m=["B11", "B12"],
        bands_60m=[],
        max_workers=20,
        verbose=False,
        overwrite=False,
        progressbar=True,
        max_disk_usage=0,
    ):
        products_keys_fnames = self.get_products_keys_fnames(
            products_ids, products_keys, download_folder
        )

        def _download(product: L2AProductKeyFname):
            if max_disk_usage > 0:
                # raises if disk usage exceeds max_disk_usage
                _ = disk_usage(max_disk_usage=max_disk_usage)

            self.download(
                product.key,
                product.fname,
                verbose=verbose,
                overwrite=overwrite,
            )

        _ = parallelize(
            _download,
            products_keys_fnames,
            max_workers=max_workers,
            progressbar=progressbar,
        )


class AWSL2ADownloader:
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        debug_mode=False,
        max_pool_connections=50,
    ) -> None:
        self.aws_access_key_id = aws_access_key_id or os.getenv(
            "AWS_ACCESS_KEY_ID"
        )
        self.aws_secret_access_key = aws_secret_access_key or os.getenv(
            "AWS_SECRET_ACCESS_KEY"
        )
        self.debug_mode = debug_mode  # only download 3 l2a products if True
        self._max_pool_connections = max_pool_connections

    @property
    def s3_l2a(self):
        # AWS S3 L2A bucket client
        from veg_workflows.aws import AWSL2ABucket

        s3_l2a = AWSL2ABucket.from_credentials(
            self.aws_access_key_id,
            self.aws_secret_access_key,
            max_pool_connections=self._max_pool_connections,
        )
        return s3_l2a

    def download_l2a(
        self,
        s2_db: pd.DataFrame,
        tile: str = None,
        download_folder: str = "./l2a_products",
        bands_10m=["B02", "B03", "B04", "B08"],
        bands_20m=["B11", "B12"],
        bands_60m=[],
        max_workers=10,
        verbose=False,
        overwrite=False,
        progressbar=True,
        max_disk_usage=0,
    ):
        if tile is not None:
            s2_db = s2_db[s2_db.tile == tile]
            if len(s2_db) == 0:
                raise ValueError(f"No products found for tile {tile}")

        if self.debug_mode:
            # only download 3 products when testing
            s2_db = s2_db.iloc[:3]

        products_keys = s2_db.s3_uri.apply(
            lambda x: x.replace("s3://sentinel-s2-l2a/", "")
        )
        products_ids = s2_db.product_id.values

        self.s3_l2a.download_products(
            products_ids,
            products_keys,
            download_folder,
            bands_10m=bands_10m,
            bands_20m=bands_20m,
            bands_60m=bands_60m,
            max_workers=max_workers,
            verbose=verbose,
            overwrite=overwrite,
            progressbar=progressbar,
            max_disk_usage=max_disk_usage,
        )


class SafePool:
    def __init__(self, workers, update_interval=1, daemon_pool=True):
        self.workers = workers
        mp.set_start_method("spawn", force=True)

        self.pool = []
        self.active_workers = 0
        self._update_interval = update_interval
        self.daemon = daemon_pool

    def map(self, func, iter):
        import time

        self._scheduled = [
            mp.Process(target=func, args=(i,), daemon=self.daemon)
            for i in iter
        ]
        self._scheduled.reverse()

        while True:
            if self.active_workers < self.workers:
                self.start_next()

            self.update_pool()

            if (len(self._scheduled) == 0) and self.active_workers == 0:
                break

            time.sleep(self._update_interval)

    def start_next(self):
        from loguru import logger  # noqa

        if len(self._scheduled):
            p = self._scheduled.pop()
            p.start()
            self.active_workers += 1
            self.pool.append(p)
            logger.debug(
                f"Starting process {p.pid}."
                f" Current active workers: {self.active_workers}"
            )

    def update_pool(self):
        from loguru import logger  # noqa

        old_pool_size = len(self.pool)
        new_pool = []

        for p in self.pool:
            if p.is_alive():
                new_pool.append(p)
            else:
                logger.debug(f"Process {p.pid} terminated.")

        terminated = old_pool_size - len(new_pool)
        self.active_workers -= terminated
        self.pool = new_pool
