import time
import warnings
from dataclasses import dataclass
from functools import wraps
from math import ceil, floor
from random import shuffle
from typing import List

import numpy as np
import pandas as pd
import rasterio
import xarray as xr
from loguru import logger
from satio.collections import L2ACollection
from satio.geoloader import ParallelLoader
from satio.utils import TaskTimer
from satio_pc import parallelize
from scipy.interpolate import griddata
from scipy.ndimage import binary_dilation, gaussian_filter
from skimage.transform import rescale
from tqdm.auto import tqdm

from veg_workflows.constants import BANDS_L2A_RESOLUTION
from veg_workflows.io import (
    coords_from_bounds,
    shape_from_bounds,
)
from veg_workflows.products import Loi10Collection

RIO_GDAL_OPTIONS = {
    "AWS_REGION": "eu-central-1",
    "AWS_REQUEST_PAYER": "requester",
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "GDAL_HTTP_MAX_RETRY": 3,
    "GDAL_HTTP_RETRY_DELAY": 1,
    "GDAL_HTTP_TCP_KEEPALIVE": "YES",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".jp2,.tif",
    "CPL_VSIL_CURL_CHUNK_SIZE": 2_097_152,
    "CPL_VSIL_CURL_CACHE_SIZE": 100_000_000,
    "CPL_VSIL_CURL_CACHE": "YES",
    "CPL_VSIL_CURL_USE_HEAD": "YES",
    "CPL_TIMESTAMP": "YES",
    "CPL_DEBUG": "ON",
    "CPL_CURL_VERBOSE": "YES",
    "CPL_LOG_ERRORS": "ON",
}


def to_dataarray(
    arr,
    bounds,
    time_values=None,
    band_values=None,
):
    has_band_dim = arr.ndim == 4
    if not has_band_dim:
        arr = np.expand_dims(arr, axis=1)

    ntime, nband, ny, nx = arr.shape

    if band_values is None:
        band_values = [f"band_{i}" for i in range(nband)]
    if time_values is None:
        time_values = [f"time_{i}" for i in range(ntime)]

    xmin_60m, ymin_60m, xmax_60m, ymax_60m = bounds
    resolution = (xmax_60m - xmin_60m) / nx
    half_pixel = resolution / 2

    arr = xr.DataArray(
        arr,
        dims=["time", "band", "y", "x"],
        coords={
            "time": time_values,
            "band": band_values,
            "y": np.linspace(
                ymax_60m - half_pixel,
                ymin_60m + half_pixel,
                ny,
            ),
            "x": np.linspace(
                xmin_60m + half_pixel,
                xmax_60m - half_pixel,
                nx,
            ),
        },
    )

    if not has_band_dim:
        arr = arr.isel(band=0)  # remove dummy band dim
    return arr


def cut_to_bounds(arr, bounds):
    xmin, ymin, xmax, ymax = bounds
    return arr.sel(y=slice(ymax, ymin), x=slice(xmin, xmax))


def get_compatible_bounds(bounds, resolution):
    new_bounds = []
    for i, b in enumerate(bounds):
        if b % resolution == 0:
            nb = b
        else:
            if i in [0, 1]:
                nb = floor(b / resolution) * resolution  # round down
            else:
                nb = ceil(b / resolution) * resolution  # round up
        new_bounds.append(nb)
    return new_bounds


def cubify(func):
    """
    Decorator to apply a function slice-wise if the input array has more
    than 2 dimensions.
    Assumes the first argument is the array.
    """

    @wraps(func)
    def wrapper(arr, *args, **kwargs):
        if arr.ndim > 2:
            new_arr = [
                func(arr[i], *args, **kwargs) for i in range(arr.shape[0])
            ]
            return np.array(new_arr)
        return func(arr, *args, **kwargs)

    return wrapper


@cubify
def nan_gaussian_filter(arr, sigma=1, radius=12):
    """
    Apply a gaussian filter to an array with nans

    Uses 2 arrays to correct for nans in the input array
    https://stackoverflow.com/questions/18697532/gaussian-filtering-a-image-with-nan-in-python
    """
    nans_mask = np.isnan(arr)

    arr = arr.copy()
    arr[nans_mask] = 0
    arr = gaussian_filter(arr, sigma=sigma, radius=radius)

    arr2 = np.ones_like(arr)
    arr2[nans_mask] = 0
    eps = 1e-6
    arr2 = gaussian_filter(arr2, sigma=sigma, radius=radius) + eps

    arr = arr / arr2
    arr[nans_mask] = np.nan
    return arr


@cubify
def nan_interpolate(image):
    """Simple nans interpolation"""
    mask_nan = np.isnan(image)
    if mask_nan.all():
        # logger.debug("All values are NaN, skipping interpolation...")
        return image
    coords = np.array(np.nonzero(~mask_nan)).T
    values = image[~mask_nan]
    grid = np.array(np.nonzero(mask_nan)).T
    image_filled = image.copy()
    image_filled[mask_nan] = griddata(coords, values, grid, method="nearest")
    return image_filled


def rolling_fill(darr, max_iter=30):
    """Inpaint AgERA5 data by rolling the original data."""
    if max_iter == 0:
        return darr
    else:
        max_iter -= 1
    # arr of shape (bands, rows, cols)
    mask = np.isnan(darr)

    if ~np.any(mask):
        return darr

    roll_params = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    shuffle(roll_params)

    for roll_param in roll_params:
        rolled = np.roll(darr, roll_param, axis=(1, 2))
        darr[mask] = rolled[mask]

    # print(max_iter, mask.sum(), np.isnan(darr).sum())

    return rolling_fill(darr, max_iter=max_iter)


@cubify
def fast_nan_interpolate(image):
    """Fast NaN interpolation only near valid pixels"""
    mask_nan = np.isnan(image)
    if mask_nan.all():
        return image

    # Step 1: Create a mask of valid pixels
    mask_valid = ~mask_nan

    # Step 2: Dilate valid mask by 3 pixels
    struct = np.ones((7, 7))  # 3-pixel radius in a 2D square
    mask_dilated = binary_dilation(mask_valid, structure=struct)

    # Step 3: Identify NaN pixels within the dilated region
    mask_target = mask_nan & mask_dilated
    if not mask_target.any():
        return image  # No NaNs near valid pixels, nothing to interpolate

    # Step 4: Get interpolation points
    coords_valid = np.array(np.nonzero(mask_valid)).T
    values_valid = image[mask_valid]
    coords_target = np.array(np.nonzero(mask_target)).T

    # Step 5: Interpolate only near valid pixels
    image_filled = image.copy()
    image_filled[mask_target] = griddata(
        coords_valid, values_valid, coords_target, method="nearest"
    )

    return image_filled


def expand_nans(image, n=1):
    """Expands NaN regions by 1 pixel in all directions,
    modifying image in-place."""
    mask_nan = np.isnan(image)  # Find NaN locations
    struct = np.ones(
        (n * 2 + 1, n * 2 + 1)
    )  # 3x3 structure to expand by 1 pixel
    expanded_mask = binary_dilation(
        mask_nan, structure=struct
    )  # Expand NaN mask

    image[expanded_mask] = np.nan  # Apply expanded NaNs
    return image  # (Optional, since it's modified in-place)


@cubify
def nan_rescale(arr, scale=6, order=1, **kwargs):
    nan_mask = np.isnan(arr)
    has_nans = np.any(nan_mask)

    if has_nans:
        # arr = fast_nan_interpolate(arr)
        # # skipping due to artefacts at orbit borders, expanding them instead
        # to avoid artefacts
        arr = expand_nans(arr, n=2)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)

        arr_new = rescale(
            arr,
            scale=scale,
            order=order,
            preserve_range=True,
            **kwargs,
        ).astype(np.float32)

        # if has_nans:
        #     nan_mask = rescale(
        #         nan_mask,
        #         scale=scale,
        #         order=0,
        #         preserve_range=True,
        #     )

        #     arr_new[nan_mask] = np.nan

    return arr_new


@cubify
def smooth_nan_rescale(
    arr,
    src_resolution=10,
    dst_resolution=60,
    order=1,
    sigma=2,
    radius=9,
    anti_aliasing=False,
):
    scale = src_resolution / dst_resolution

    if scale == 1:
        return arr

    elif scale < 1:
        return nan_rescale(
            arr,
            scale=scale,
            order=order,
            anti_aliasing=anti_aliasing,
        )
    else:
        arr = nan_rescale(
            arr, scale=scale, order=order, anti_aliasing=anti_aliasing
        )
        if sigma > 0:
            arr = nan_gaussian_filter(arr, sigma=sigma, radius=radius)

    return arr


def gaussian_weight(x: float, x0: float, delta: float) -> float:
    """
    Computes the weight of a sample using a Gaussian function.

    Parameters:
        x (float): The input probability (0 to 1).
        x0 (float): The position of the highest weight (1).
        delta (float): The value where the weight approaches
                       0 at 3σ (x0 + delta).

    Returns:
        float: The computed weight.
    """
    # if delta <= 0:
    #     raise ValueError("Delta must be positive.")

    sigma = delta / 3  # Ensuring 3σ covers the delta range
    return np.exp(-((x - x0) ** 2) / (2 * sigma**2))


def get_weights(loi_probs, delta=0.1, snow_prob_weight=0.5, labels=None):
    lab = labels or LoiLabels()

    valid_prob = (
        loi_probs[:, lab.surface, ...]
        + snow_prob_weight * loi_probs[:, lab.snow, ...]
    )

    # ignore runtime warning all nans slice
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        max_valid_prob = np.nanmax(valid_prob, axis=0)

    # the range of positive weights is
    # [max_valid_prob - delta * max_valid_prob, max_valid_prob]
    # such that the range is progressively smaller for lower max_valid_prob
    weights = gaussian_weight(
        valid_prob, max_valid_prob, delta * max_valid_prob
    )
    return weights, max_valid_prob


LOI_NATIVE_RESOLUTION = 60


@dataclass
class LoiLabels:
    surface: int = 0
    clouds: int = 1
    shadows: int = 2
    snow: int = 3
    unknown: int = 254
    nodata: int = 255

    def names(self):
        return [field.name for field in self.__dataclass_fields__.values()]


@dataclass
class LoiCogSettings:
    nodata: int = 255
    scale: float = 1 / 250
    resolution: int = 60


@dataclass
class LoaderParams:
    max_retries: int = 3
    max_workers: int = 10
    retry_sleep: float = 0.1


@dataclass
class RescaleParams:
    order: int = 1
    sigma: int = 2
    radius: int = 9


@dataclass
class LoiMaskParams:
    surface: float = 0.5
    clouds: float = 0.5
    shadows: float = 0.5
    snow: float = 0.5
    dark_surface: float = 0.65
    bright_surface: float = 0.65


@dataclass
class LoiACLParams:
    min_valid_obs: int = 5
    valid_snow_freq_th: float = 0.96
    max_invalid_freq_th: float = 0.96
    min_invalid_shadow_freq_th: float = 0.1


@dataclass
class LoiCCLParams:
    min_valid_obs: int = 1


@dataclass
class LoiCompositeParams:
    delta: float = 0.1
    snow_prob_weight: float = 0.5


class LoiMaskProcessor:
    def __init__(
        self,
        mask_params: LoiMaskParams = None,
        labels: LoiLabels = None,
    ):
        self.labels = labels or LoiLabels()
        self.mask_params = mask_params or LoiMaskParams()

    def get_observation_mask(self, prob):
        """prob is a single timestamp, band, y, x array"""
        lab = self.labels
        th = self.mask_params

        # init to invalid
        mask = (
            np.ones(prob[0].shape, dtype=np.uint8) * lab.unknown  # 254
        )

        #
        mask[np.isnan(prob[0])] = lab.nodata  # 255

        # surface
        surface_mask = prob[lab.surface] > th.surface  # surface_prob > 0.5

        # surface_prob + surface_shadow > 0.65
        # and surface_prob > surface_shadow
        surface_mask = surface_mask | (
            ((prob[lab.surface] + prob[lab.shadows]) > th.dark_surface)
            & (prob[lab.surface] > prob[lab.shadows])
        )

        # surface_prob + surface_snow > 0.65 and surface_prob > surface_snow
        surface_mask = surface_mask | (
            ((prob[lab.surface] + prob[lab.snow]) > th.bright_surface)
            & (prob[lab.surface] > prob[lab.snow])
        )

        # surface
        mask[surface_mask] = lab.surface

        # snow
        mask[(prob[lab.snow] > th.snow)] = lab.snow

        # shadow
        mask[(prob[lab.shadows] > th.shadows)] = lab.shadows

        # clouds
        mask[(prob[lab.shadows] > th.clouds)] = lab.clouds

        return mask

    def get_mask(self, loi_probs):
        n_obs, n_bands, ny, nx = loi_probs.shape
        mask = np.zeros((n_obs, ny, nx), dtype=np.uint8)
        for i in tqdm(range(n_obs)):
            mask[i] = self.get_observation_mask(loi_probs[i])
        return mask


class LoiObs:
    def __init__(self, loi_mask, labels: LoiLabels = None):
        self.labels = labels or LoiLabels()
        self.mask = loi_mask

    @property
    def total(self):
        return (self.mask != self.labels.nodata).sum(axis=0)

    @property
    def surface(self):
        return (self.mask == self.labels.surface).sum(axis=0)

    @property
    def clouds(self):
        return (self.mask == self.labels.clouds).sum(axis=0)

    @property
    def shadows(self):
        return (self.mask == self.labels.shadows).sum(axis=0)

    @property
    def snow(self):
        return (self.mask == self.labels.snow).sum(axis=0)

    @property
    def valid(self):
        return self.surface + self.snow

    @property
    def surface_freq(self):
        return self.surface / self.total

    @property
    def shadow_freq(self):
        return self.shadows / self.total

    @property
    def snow_freq(self):
        return self.snow / self.total

    @property
    def cloud_freq(self):
        return self.cloud / self.total

    @property
    def valid_freq(self):
        return self.valid / self.total

    @property
    def valid_surface_freq(self):
        return self.surface / self.valid

    @property
    def valid_snow_freq(self):
        return self.snow / self.valid


class LoiLoader:
    def __init__(
        self,
        loi_coll: Loi10Collection,
        max_retries: int = 3,
        max_workers: int = 10,
        retry_sleep: float = 0.1,
        nodata: int = 255,
        scale: float = 1 / 250,
        resolution: int = 60,
        progressbar: bool = False,
        rio_gdal_options: dict = None,
    ):
        self.loi_coll = loi_coll
        self._max_retries = max_retries
        self._max_workers = max_workers
        self._retry_sleep = retry_sleep
        self._loi_native_resolution = resolution
        self._nodata_value = nodata
        self._scale_value = scale
        self._progressbar = progressbar
        self._rio_gdal_options = rio_gdal_options or RIO_GDAL_OPTIONS

    def _load_loi_product_probs(
        self,
        s2_product_id,
        bounds=None,
    ):
        loi_prod = self.loi_coll.tile_utm(s2_product_id=s2_product_id)
        fn = loi_prod.path("PROBS")

        with rasterio.Env(**self._rio_gdal_options):
            with rasterio.open(fn) as src:
                bounds = bounds or src.bounds
                window = src.window(*bounds)
                arr = src.read(
                    window=window,
                    boundless=True,
                    fill_value=self._nodata_value,
                )

        arr = arr.astype(np.float32)
        arr[arr == self._nodata_value,] = np.nan
        arr = arr * self._scale_value  # scale to 0-1

        return arr

    def load_loi_product_probs(
        self,
        s2_product_id,
        bounds=None,
        attempt=0,
    ):
        attempt += 1
        try:
            return self._load_loi_product_probs(
                s2_product_id,
                bounds,
            )
        except Exception as e:
            if attempt <= self._max_retries:
                logger.debug(
                    f"Error loading {s2_product_id}, "
                    f"attempt {attempt}/{self._max_retries}"
                )
                if self._retry_sleep:
                    time.sleep(self._retry_sleep)
                return self.load_loi_product_probs(
                    s2_product_id,
                    bounds=bounds,
                    attempt=attempt,
                )
            else:
                raise ValueError(f"Error:**{s2_product_id}**: {e}")

    def __call__(self, s2_product_ids, bounds):
        bounds_60m = get_compatible_bounds(
            bounds, self._loi_native_resolution
        )  # loi bounds at 60m

        if np.any(np.array(bounds) != np.array(bounds_60m)):
            raise ValueError(
                f"Provided bounds {bounds} are not compatible with "
                f"LOI native resolution {self._loi_native_resolution}. "
                f"Suggested bounds: {bounds_60m}"
            )

        if self._max_workers > 1:
            loi_probs = parallelize(
                lambda prod: self.load_loi_product_probs(
                    prod, bounds=bounds_60m
                ),
                s2_product_ids,
                max_workers=self._max_workers,
                progressbar=self._progressbar,
            )
        else:
            loi_probs = [
                self.load_loi_product_probs(prod, bounds=bounds_60m)
                for prod in s2_product_ids
            ]
        return np.array(loi_probs)


class LoiWeightsProcessor:
    def __init__(
        self,
        loi_coll: Loi10Collection,
        bounds: list,
        s2_products_ids: list,
        drop_nodata_products: bool = True,
        cog: LoiCogSettings = LoiCogSettings(
            nodata=255, scale=1 / 250, resolution=60
        ),
        labels: LoiLabels = LoiLabels(
            surface=0, clouds=1, shadows=2, snow=3, unknown=254, nodata=255
        ),
        mask_params: LoiMaskParams = LoiMaskParams(
            surface=0.5,
            clouds=0.5,
            shadows=0.5,
            snow=0.5,
            dark_surface=0.65,
            bright_surface=0.55,
        ),
        composite_params: LoiCompositeParams = LoiCompositeParams(
            delta=0.1, snow_prob_weight=0.5
        ),
        ccl_params: LoiCCLParams = LoiCCLParams(min_valid_obs=1),
        rescale_params: RescaleParams = RescaleParams(
            order=1, sigma=2, radius=9
        ),
        loader_params: LoaderParams = LoaderParams(
            max_retries=3, max_workers=10, retry_sleep=0.1
        ),
        rio_gdal_options: dict = None,
        progressbar: bool = False,
    ):
        self.loi_coll = loi_coll
        self.cog = cog
        self.labels = labels
        self.mask_params = mask_params
        self.composite_params = composite_params
        self.ccl_params = ccl_params
        self.rescale_params = rescale_params
        self.loader_params = loader_params

        self.load = LoiLoader(
            loi_coll=self.loi_coll,
            progressbar=False,
            rio_gdal_options=rio_gdal_options,
            **self.cog.__dict__,
            **self.loader_params.__dict__,
        )

        self._drop_nodata_products = drop_nodata_products

        self.bounds = bounds
        self.bounds_native = get_compatible_bounds(bounds, cog.resolution)

        self.resolution = 10
        self.products_ids = s2_products_ids

        self._probs = None
        self._probs_native = None

        self._masks = None
        self._ccl = None

        self._weights = None
        self._weights20 = None
        self._weights60 = None

        self._labels_names = [
            n for n in self.labels.names() if n not in ["nodata", "unknown"]
        ]
        self._max_valid_prob = None
        self._max_valid_prob20 = None
        self._max_valid_prob60 = None

        self._progress = progressbar

    @property
    def probs(self):
        if self._probs is None:
            self._probs = smooth_nan_rescale(
                self.probs_native.data,
                src_resolution=self.cog.resolution,
                dst_resolution=self.resolution,
                **self.rescale_params.__dict__,
            )

            # normalize
            self._probs = self._probs / np.nansum(
                self._probs, axis=1, keepdims=True
            )

            # cut to target bounds
            self._probs = to_dataarray(
                self._probs,
                self.bounds_native,
                time_values=self.products_ids,
                band_values=self._labels_names,
            )

            self._probs = cut_to_bounds(self._probs, self.bounds)

        return self._probs

    @property
    def probs_native(self):
        if self._probs_native is None:
            self._probs_native = self.load(
                self.products_ids, self.bounds_native
            )

            if self._drop_nodata_products:
                valid_ids = ~np.all(
                    np.isnan(self._probs_native[:, 0, ...]), axis=(-2, -1)
                )

                if not np.any(valid_ids):
                    # logger.debug(
                    #     "All products are empty, returning single NaN array"
                    # )
                    valid_ids = [0]

                self._probs_native = self._probs_native[valid_ids]
                self.products_ids = self.products_ids[valid_ids]

            # cut to target bounds
            self._probs_native = to_dataarray(
                self._probs_native,
                self.bounds_native,
                time_values=self.products_ids,
                band_values=self._labels_names,
            )

        return self._probs_native

    @property
    def masks(self):
        if self._masks is None:
            self._masks = LoiMaskProcessor(
                mask_params=self.mask_params, labels=self.labels
            ).get_mask(self.probs.data)
            self._masks = to_dataarray(
                self._masks,
                self.bounds,
                time_values=self.products_ids,
                band_values=["loi_mask"],
            )
        return self._masks

    @property
    def weights(self):
        if self._weights is None:
            self._weights, self._max_valid_prob = get_weights(
                self.probs,
                delta=self.composite_params.delta,
                snow_prob_weight=self.composite_params.snow_prob_weight,
                labels=self.labels,
            )

            self._weights = to_dataarray(
                self._weights,
                self.bounds,
                time_values=self.products_ids,
                band_values=["weight"],
            )

            self._max_valid_probs = np.expand_dims(self._max_valid_prob, 0)
            self._max_valid_prob = xr.DataArray(
                self._max_valid_prob,
                dims=["y", "x"],
                coords={
                    "y": self.probs.y.values,
                    "x": self.probs.x.values,
                },
            )

        return self._weights

    @property
    def weights20(self):
        if self._weights20 is None:
            self._weights20 = self.rescale(
                self._weights.data, src_resolution=10, dst_resolution=20
            )

            self._weights20 = to_dataarray(
                self._weights20,
                self.bounds,
                time_values=self.products_ids,
                band_values=["weight"],
            )

            self._max_valid_prob20 = self.rescale(
                self._max_valid_prob.data, src_resolution=10, dst_resolution=20
            )
            self._max_valid_prob20 = xr.DataArray(
                self._max_valid_prob20,
                dims=["y", "x"],
                coords={
                    "y": self._weights20.y.values,
                    "x": self._weights20.x.values,
                },
            )

        return self._weights20

    @property
    def weights60(self):
        if self._weights60 is None:
            self._weights60, self._max_valid_prob60 = get_weights(
                self.probs_native.data,
                delta=self.composite_params.delta,
                snow_prob_weight=self.composite_params.snow_prob_weight,
                labels=self.labels,
            )
            self._weights60 = to_dataarray(
                self._weights60,
                self.bounds_native,
                time_values=self.products_ids,
                band_values=["weight"],
            )

            self._max_valid_prob60 = xr.DataArray(
                self._max_valid_prob60,
                dims=["y", "x"],
                coords={
                    "y": self.probs_native.y.values,
                    "x": self.probs_native.x.values,
                },
            )

        return self._weights60

    @property
    def max_valid_prob(self):
        if self._max_valid_prob is None:
            _ = (
                self.weights
            )  # compute weights which also computes max_valid_prob
        return self._max_valid_prob

    @property
    def max_valid_prob20(self):
        if self._max_valid_prob20 is None:
            _ = (
                self.weights20
            )  # compute weights which also computes max_valid_prob
        return self._max_valid_prob20

    @property
    def max_valid_prob60(self):
        if self._max_valid_prob60 is None:
            _ = self.weights60
        return self._max_valid_prob60

    @property
    def ccl(self):
        if self._ccl is None:
            self._ccl = self._get_ccl_mask(
                self.masks, self.labels, self.ccl_params
            )
        return self._ccl

    @property
    def acl(self):
        if self._acl is None:
            self._acl = self._get_acl_mask(
                self.masks, self.labels, self.acl_params
            )
        return self._acl

    def rescale(self, data, src_resolution, dst_resolution):
        return smooth_nan_rescale(
            data,
            src_resolution=src_resolution,
            dst_resolution=dst_resolution,
            **self.rescale_params.__dict__,
        )

    @staticmethod
    def _get_ccl_mask(loi_masks, labels: LoiLabels, ccl_params: LoiCCLParams):
        """From a timeseries of Loi masks, compute the Composite Classification
        Layer (CCL) mask. Which determines the LOI class of each pixel based on
        the most frequent class in the timeseries.
        """
        obs = LoiObs(loi_masks, labels=labels)
        lab = labels or LoiLabels()
        ccl_params = ccl_params or LoiCCLParams()

        # init mask with unknown
        mask = np.ones(obs.valid.shape, dtype=np.uint8) * lab.unknown

        # surface
        surface_mask = (obs.surface >= ccl_params.min_valid_obs) & (
            obs.surface >= obs.snow
        )
        mask[surface_mask] = lab.surface

        # snow
        snow_mask = (obs.snow >= ccl_params.min_valid_obs) & (
            obs.snow > obs.surface
        )
        mask[snow_mask] = lab.snow

        # nodata
        mask[obs.total == 0] = lab.nodata

        # shadows
        shadow_mask = (obs.shadows == obs.total) & (obs.total > 0)
        mask[shadow_mask] = lab.shadows

        # clouds
        cloud_mask = (obs.clouds == obs.total) & (obs.total > 0)
        mask[cloud_mask] = lab.clouds

        # thre remainings are mixed pixels, we keep them as unknown
        return mask

    @staticmethod
    def _get_acl_mask(loi_masks, labels: LoiLabels, acl_params: LoiACLParams):
        obs = LoiObs(loi_masks, labels=labels)
        valid_obs = obs.valid
        shadow_freq = obs.shadow_freq
        snow_valid_freq = obs.valid_snow_freq

        min_valid_obs = acl_params.min_valid_obs
        min_invalid_shadow_freq_th = acl_params.min_invalid_shadow_freq_th

        acl_mask = np.ones(valid_obs.shape, dtype=np.uint8) * labels.unknown

        # if valid_obs < min_valid_obs: don't mask, compute comp/percentiles directly and register as nodata mask
        # this case is either fully clouded or a bright feature that is always flagged as clouds, in both case we just take all data
        # acl_mask[valid_obs < min_valid_obs] = self.labels.unknown  # don't mask anything

        # if there are no valid obs above min, and in the invalid there is an exceptionally high shadow freq, we keep shadows and mask out clouds
        acl_mask[
            (valid_obs < min_valid_obs)
            & (shadow_freq > min_invalid_shadow_freq_th)
        ] = labels.shadows  # do not mask shadows, mask only clouds

        # if we have only snow observations above min valid surface obs, we keep snow in the percentiles, as it's permanent snow
        acl_mask[
            (valid_obs >= min_valid_obs)
            & (snow_valid_freq >= acl_params.valid_snow_freq_th)
        ] = labels.snow  # mask clouds and shadows

        # if we have a min number of surface obs we use those for the percentiles
        acl_mask[
            (valid_obs >= min_valid_obs)
            & (snow_valid_freq < acl_params.valid_snow_freq_th)
        ] = labels.surface  # mask clouds, shadows and snow -> surface only

        return acl_mask

    def get_annual_valid_mask(self):
        # valid_mask: mask with t, y, x shape. each pixel is a combination
        # of the surface, shadow, snow, clouds mask based on its acl label
        mask = self.masks

        valid_mask = np.zeros(mask.shape, dtype=np.uint8) > 0
        labels = self.labels
        acl = np.broadcast_to(np.expand_dims(self.acl, 0), mask.shape)

        # acl = surface -> keep only surface pixels
        pixels_group = acl == labels.surface
        valid_mask[pixels_group] = (mask == labels.surface)[pixels_group]

        # acl = snow -> keep only snow pixels
        pixels_group = acl == labels.snow
        valid_mask[pixels_group] = (mask == labels.snow)[pixels_group]

        # acl = shadow -> keep shadow and surface pixels
        pixels_group = acl == labels.shadows
        valid_mask[pixels_group] = (
            (mask == labels.shadows) | (mask == labels.surface)
        )[pixels_group]

        # acl = clouds or unknown -> keep all pixels except nodata ones
        # no mask applied: all non-nodata pixels are valid for this group. They will be treated as nodata but we keep information
        # on this last one, we could actually keep only the best observation (highest surface prob) and mask the rest - does it make sense to compute percentiles of clouds? maybe yes, we still have info
        pixels_group = (acl == labels.clouds) | (acl == labels.unknown)
        valid_mask[pixels_group] = (mask != labels.nodata)[pixels_group]

        # check that all nodata pixels are False
        assert not np.any(valid_mask[mask == labels.nodata])

        return valid_mask

    def composite(self, darr, weights=None):
        # data is a t, y, x array
        # weights is a t, y, x array
        resolution = darr.x.values[1] - darr.x.values[0]

        if weights is None:
            if resolution == 10:
                weights = self.weights
            elif resolution == 20:
                weights = self.weights20
            elif resolution == 60:
                weights = self.weights60

        if "band" in darr.dims:
            weights = weights.expand_dims("band", axis=1)

        data_composite = np.nansum(
            darr * weights.data, axis=0, keepdims=True
        ) / np.nansum(weights.data, axis=0, keepdims=True)

        central_time = darr.time.values[len(darr.time) // 2]
        data_composite = xr.DataArray(
            data_composite,
            dims=["time", "band", "y", "x"],
            coords={
                "time": [central_time],
                "band": darr.band.values,
                "y": darr.y.values,
                "x": darr.x.values,
            },
        )
        return data_composite


@dataclass
class Period:
    start_date: str
    end_date: str
    idx: int


@dataclass
class CompositesInterpolationParams:
    valid_prob_range: float = 0.2
    time_weight_sigma: float = 1.15
    time_weight_alpha: float = 0.999
    time_min_weight: float = 0.001
    min_valid_weight: float = 0.01


@dataclass
class LoiWeightsParams:
    drop_nodata_products: bool = (True,)
    cog: LoiCogSettings = (
        LoiCogSettings(nodata=255, scale=1 / 250, resolution=60),
    )
    labels: LoiLabels = (
        LoiLabels(
            surface=0, clouds=1, shadows=2, snow=3, unknown=254, nodata=255
        ),
    )
    mask_params: LoiMaskParams = (
        LoiMaskParams(
            surface=0.5,
            clouds=0.5,
            shadows=0.5,
            snow=0.5,
            dark_surface=0.65,
            bright_surface=0.55,
        ),
    )
    composite_params: LoiCompositeParams = (
        LoiCompositeParams(delta=0.1, snow_prob_weight=0.5),
    )
    ccl_params: LoiCCLParams = (LoiCCLParams(min_valid_obs=1),)
    rescale_params: RescaleParams = (
        RescaleParams(order=1, sigma=2, radius=9),
    )
    loader_params: LoaderParams = LoaderParams(
        max_retries=3, max_workers=10, retry_sleep=0.1
    )


def get_loi_weights_params(
    drop_nodata_products: bool = True,
    cog_nodata: int = 255,
    cog_scale: float = 1 / 250,
    cog_resolution: int = 60,
    labels_surface: int = 0,
    labels_clouds: int = 1,
    labels_shadows: int = 2,
    labels_snow: int = 3,
    labels_unknown: int = 254,
    labels_nodata: int = 255,
    mask_surface: float = 0.5,
    mask_clouds: float = 0.5,
    mask_shadows: float = 0.5,
    mask_snow: float = 0.5,
    mask_dark_surface: float = 0.65,
    mask_bright_surface: float = 0.55,
    composite_delta: float = 0.1,
    composite_snow_prob_weight: float = 0.5,
    ccl_min_valid_obs: int = 1,
    rescale_order: int = 1,
    rescale_sigma: int = 2,
    rescale_radius: int = 9,
    loader_max_retries: int = 3,
    loader_max_workers: int = 10,
    loader_retry_sleep: float = 0.1,
):
    return LoiWeightsParams(
        drop_nodata_products=drop_nodata_products,
        cog=LoiCogSettings(
            nodata=cog_nodata,
            scale=cog_scale,
            resolution=cog_resolution,
        ),
        labels=LoiLabels(
            surface=labels_surface,
            clouds=labels_clouds,
            shadows=labels_shadows,
            snow=labels_snow,
            unknown=labels_unknown,
            nodata=labels_nodata,
        ),
        mask_params=LoiMaskParams(
            surface=mask_surface,
            clouds=mask_clouds,
            shadows=mask_shadows,
            snow=mask_snow,
            dark_surface=mask_dark_surface,
            bright_surface=mask_bright_surface,
        ),
        composite_params=LoiCompositeParams(
            delta=composite_delta,
            snow_prob_weight=composite_snow_prob_weight,
        ),
        ccl_params=LoiCCLParams(min_valid_obs=ccl_min_valid_obs),
        rescale_params=RescaleParams(
            order=rescale_order,
            sigma=rescale_sigma,
            radius=rescale_radius,
        ),
        loader_params=LoaderParams(
            max_retries=loader_max_retries,
            max_workers=loader_max_workers,
            retry_sleep=loader_retry_sleep,
        ),
    )


class TaskTimerThreads(TaskTimer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._counter = 0

    def start(self):
        self._counter += 1
        super().start()

    def stop(self):
        self._counter -= 1
        if self._counter <= 0:
            self._counter = 0
            super().stop()


@dataclass
class LoiCompositingTimer:
    loading: TaskTimerThreads = TaskTimerThreads("Loading")
    compositing: TaskTimerThreads = TaskTimerThreads("Loading/Compositing")
    interpolation: TaskTimerThreads = TaskTimerThreads("Interpolation")
    weights: TaskTimerThreads = TaskTimerThreads("LOI-60 Weights")

    def log(self):
        self.weights.log()
        self.compositing.log()
        self.interpolation.log()


def timeit(timer_attr):
    """Decorator that retrieves a timer from self and starts/stops it."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            timer = getattr(self.timer, timer_attr)
            timer.start()
            result = func(self, *args, **kwargs)
            timer.stop()
            return result

        return wrapper

    return decorator


class LoiBaseCompositesProcessor:
    """
    This class computes weighted composites based on per-period weights
    and interpolates missing observations.
    """

    def __init__(
        self,
        periods: List[Period],
        bounds: List[int],
        l2a_coll: L2ACollection,
        loi_coll: Loi10Collection,
        min_valid_weight: float = 0.01,
        max_workers: int = 10,
        loi_weights_params: LoiWeightsParams = LoiWeightsParams(),
        verbose: bool = False,
        progressbar: bool = True,
        rio_gdal_options: dict = RIO_GDAL_OPTIONS,
    ):
        self.periods = periods
        self.bounds = bounds

        self._l2a_coll = l2a_coll.filter_bounds(bounds, l2a_coll.epsg)
        if self._l2a_coll._loader is None:
            self._l2a_coll._loader = ParallelLoader(max_workers=max_workers)
        self._loi_coll = loi_coll

        self._min_valid_weight = min_valid_weight
        self._max_workers = max_workers

        self._valid_score_weights = None  # Stored weights for later use

        self._weights_list = None
        self._max_valid_probs: dict = None
        self._loi_weights_params = loi_weights_params

        self.timer = LoiCompositingTimer()
        self._verbose = verbose

        self._valid_score_weights = {}
        self._progressbar = progressbar
        self._rio_gdal_options = rio_gdal_options

    def _get_single_period_weights(self, period):
        start_date, end_date = period.start_date, period.end_date
        period_coll = self._l2a_coll.filter_dates(start_date, end_date)

        if len(period_coll.df) == 0:
            logger.warning(f"No products for period {start_date} - {end_date}")
            return {}, {}

        s2_product_ids = period_coll.df.product_id.values
        loi = LoiWeightsProcessor(
            self._loi_coll,
            self.bounds,
            s2_product_ids,
            progressbar=False,
            rio_gdal_options=self._rio_gdal_options,
            **self._loi_weights_params.__dict__,
        )

        weights = {}
        max_valid_prob = {}

        weights[10] = loi.weights
        weights[20] = loi.weights20
        weights[60] = loi.weights60

        max_valid_prob[10] = loi.max_valid_prob
        max_valid_prob[20] = loi.max_valid_prob20
        max_valid_prob[60] = loi.max_valid_prob60

        return weights, max_valid_prob

    def _get_single_period_probs(self, period):
        start_date, end_date = period.start_date, period.end_date
        period_coll = self._l2a_coll.filter_dates(start_date, end_date)

        if len(period_coll.df) == 0:
            logger.warning(f"No products for period {start_date} - {end_date}")
            return None

        s2_product_ids = period_coll.df.product_id.values
        loi = LoiWeightsProcessor(
            self._loi_coll,
            self.bounds,
            s2_product_ids,
            progressbar=False,
            rio_gdal_options=self._rio_gdal_options,
            **self._loi_weights_params.__dict__,
        )

        return loi.probs

    @timeit("weights")
    def _get_periods_weights(self, periods):
        weights_validprobs_list = parallelize(
            self._get_single_period_weights,
            periods,
            max_workers=self._max_workers,
            progressbar=self._progressbar,
        )
        # weights_validprobs_list = [
        #     self._get_single_period_weights(p) for p in periods
        # ]
        weights_list, validprobs_list = zip(*weights_validprobs_list)
        return weights_list, validprobs_list

    def _get_periods_probs(self, periods):
        probs_list = parallelize(
            self._get_single_period_probs,
            periods,
            max_workers=self._max_workers,
            progressbar=False,
        )
        return probs_list

    @property
    def weights_list(self):
        if self._weights_list is None:
            self._weights_list, validprobs_list = self._get_periods_weights(
                self.periods
            )
            self._max_valid_probs = {
                r: self._validprobs_list_to_darr(validprobs_list, r)
                for r in [10, 20, 60]
            }
        return self._weights_list

    @property
    def max_valid_probs(self):
        if self._max_valid_probs is None:
            _ = (
                self.weights_list
            )  # compute weights which also computes max_valid_prob
        return self._max_valid_probs

    def weights_period(self, period: Period, resolution: int):
        return self.weights_list[period.idx].get(resolution)

    def get_weights_darr(self, resolution: int = 10):
        wl_res = [w.get(resolution) for w in self.weights_list]
        weights = xr.concat([w for w in wl_res if w is not None], dim="time")

        periods_idx = []
        for i, wl in enumerate(wl_res):
            if wl is None:
                continue
            for _ in range(len(wl.time)):
                periods_idx.append(i)

        weights = weights.assign_coords(periods_idx=("time", periods_idx))
        return weights

    @property
    def weights(self):
        return self.get_weights_darr(10)

    @property
    def probs(self):
        periods_idx = []
        probs_list = self._get_periods_probs(self.periods)
        for i, probs in enumerate(probs_list):
            if probs is None:
                continue
            for _ in range(len(probs.time)):
                periods_idx.append(i)

        probs = xr.concat([p for p in probs_list if p is not None], dim="time")
        probs = probs.assign_coords(periods_idx=("time", periods_idx))

        return probs

    def get_quality_score(self, resolution):
        max_valid_probs_mean = self.max_valid_probs[10].mean(axis=0)
        max_valid_probs_max = self.max_valid_probs[10].max(axis=0)

        quality_score = xr.concat(
            [max_valid_probs_mean, max_valid_probs_max], dim="band"
        )
        y, x = coords_from_bounds(self.bounds, resolution)
        quality_score["y"] = y
        quality_score["x"] = x
        quality_score["band"] = ["quality_score_mean", "quality_score_max"]
        return quality_score

    def _validprobs_list_to_darr(self, validprobs_list, resolution):
        mvp = [validprobs_list[p.idx].get(resolution) for p in self.periods]
        dates = [p.start_date for p in self.periods]
        valid_dates = [d for d, m in zip(dates, mvp) if m is not None]
        mvp = xr.concat([m for m in mvp if m is not None], dim="time")
        mvp["time"] = valid_dates
        mvp = mvp.reindex(time=dates)  # add missing periods as nans
        return mvp

    def _nan_composite(self, period, bands, resolution):
        shape = shape_from_bounds(self.bounds, resolution)
        y, x = coords_from_bounds(self.bounds, resolution)
        nan_composite = xr.DataArray(
            np.full((1, len(bands), *shape), np.nan),
            dims=["time", "band", "y", "x"],
            coords={
                "time": [period.start_date],
                "band": bands,
                "y": y,
                "x": x,
            },
        )
        return nan_composite

    def _discard_low_weights(self, weights, min_valid_weight):
        if weights is None:
            return None
        weights = weights.where(weights >= min_valid_weight, np.nan)

        if weights.isnull().all():
            return None

        # discard timestamps where weights are all 0s or below min threshold
        weights = weights.dropna(dim="time", how="all")
        weights = weights.fillna(0)
        return weights

    def _compute_composite(self, darr, weights, start_date):
        # data is a t, y, x array
        # weights is a t, y, x array

        if "band" in darr.dims:
            weights = weights.expand_dims("band", axis=1)

        weights = np.broadcast_to(weights.data, darr.shape)
        weights = darr.copy(data=weights)

        data_composite = np.nansum(
            darr * weights.data, axis=0, keepdims=True
        ) / np.nansum(
            weights.where(~darr.isnull(), np.nan), axis=0, keepdims=True
        )

        data_composite = xr.DataArray(
            data_composite,
            dims=["time", "band", "y", "x"],
            coords={
                "time": [start_date],
                "band": darr.band.values,
                "y": darr.y.values,
                "x": darr.x.values,
            },
        )
        return data_composite

    def period_composite(
        self,
        period: Period,
        bands: List[str],
        resolution: int = 10,
        force_compatible_bounds: bool = True,
    ):
        start_date, end_date = period.start_date, period.end_date
        weights = self.weights_period(period, resolution)

        # weights = self._discard_low_weights(weights, self._min_valid_weight)

        if weights is None:
            # logger.debug(
            #     f"No weights for period {start_date} - {end_date}, filling with NaNs"
            # )
            return self._nan_composite(period, bands, resolution)

        s2_product_ids = weights.time.values
        period_coll = self._l2a_coll._clone()
        period_coll.df = period_coll.df[
            period_coll.df.product_id.isin(s2_product_ids)
        ]

        if len(period_coll.df) == 0:
            self.warning(f"No products for period {start_date} - {end_date}")
            return self._nan_composite(period, bands, resolution)

        darr = self.load_bands(
            period_coll,
            bands,
            resolution,
            force_compatible_bounds=force_compatible_bounds,
        )
        return self._compute_composite(darr, weights, period.start_date)

    def load_period_bands(
        self,
        period: Period,
        bands: List[str],
        resolution: int = 10,
        force_compatible_bounds: bool = True,
    ):
        start_date, end_date = period.start_date, period.end_date
        coll = self._l2a_coll.filter_dates(start_date, end_date)
        darr = self.load_bands(
            coll,
            bands,
            resolution,
            force_compatible_bounds=force_compatible_bounds,
        )
        return darr

    @timeit("compositing")
    def composites(
        self,
        bands: List[str],
        resolution: int = 10,
        force_compatible_bounds: bool = True,
        randomize_periods: bool = True,
    ):
        bands_str = ",".join(bands)

        if self._weights_list is None:
            # compute weights first or it gets parallelized multiple times
            self.log("Computing LOI weights")
            _ = self.weights_list

        timer = TaskTimer(f"Compositing {bands_str}")
        timer.start()

        if randomize_periods:
            # randomize periods to avoid overloading disk loading from
            # different workers on same files, not needed with network fs (s3)
            periods = self.periods.copy()
            shuffle(periods)
        else:
            periods = self.periods

        composites = parallelize(
            lambda period: self.period_composite(
                period,
                bands,
                resolution,
                force_compatible_bounds=force_compatible_bounds,
            ),
            periods,
            max_workers=self._max_workers,
            progressbar=self._progressbar,
        )

        if randomize_periods:
            # sort back to correct order
            composites = sorted(composites, key=lambda x: x.time.values[0])

        composites = xr.concat(composites, dim="time")
        timer.stop()
        self.log(f"Composite/Loading {bands_str}: {timer.total:.2f} minutes")

        return composites

    def compute_valid_score_weights(
        self,
        resolution,
        valid_prob_range: float = 0.15,
    ):
        max_valid_probs = self.max_valid_probs[resolution]
        overall_max_valid_prob = np.nanmax(
            max_valid_probs, axis=0, keepdims=True
        )

        overall_max_valid_prob = np.broadcast_to(
            overall_max_valid_prob, max_valid_probs.shape
        )
        # time weight is a gaussian with same shape as composite
        # self.log("Interpolation - valid score weights")
        valid_score_weights = gaussian_weight(
            max_valid_probs, overall_max_valid_prob, valid_prob_range
        )
        valid_score_weights = valid_score_weights.fillna(0)
        return valid_score_weights

    @timeit("interpolation")
    def interpolate(
        self,
        composites: xr.DataArray,
        valid_score_weights: xr.DataArray = None,
        valid_prob_range: float = 0.15,
        time_weight_sigma: float = 1.15,
        time_weight_alpha: float = 0.999,
        time_min_weight: float = 0.001,
    ):
        bands_str = ",".join(composites.band.values)
        timer = TaskTimer(f"Interpolating {bands_str}")
        timer.start()

        # self.log(f"Interpolating {bands_str}")
        resolution = composites[0].x.values[1] - composites[0].x.values[0]

        if valid_score_weights is None:
            valid_score_weights = self.compute_valid_score_weights(
                resolution, valid_prob_range=valid_prob_range
            )

        composites = composites.fillna(0)

        composites_interp = composites.copy()

        x = np.arange(composites.time.size)

        for i in tqdm(range(composites_interp.time.size)):
            x0 = i
            time_weights = (
                time_weight_alpha
                * gaussian_weight(x, x0, 3 * time_weight_sigma)
                + time_min_weight
            )
            time_weights = np.expand_dims(time_weights, axis=(1, 2))

            comp_weights = time_weights * valid_score_weights
            comp_weights = comp_weights / comp_weights.sum(axis=0)

            # TODO: check if this is needed
            # comp_weights[comp_weights < self._interp_params.min_valid_weight] = 0
            # comp_weights = comp_weights / comp_weights.sum(axis=0)

            comp_weights = comp_weights.expand_dims("band", axis=1)
            comp_weights = np.broadcast_to(comp_weights, composites.shape)

            comp = (composites * comp_weights).sum(axis=0, keepdims=True)

            composites_interp.data[i] = comp.data

        timer.stop()
        self.log(f"Interpolation {bands_str}: {timer.total:.2f} minutes")
        return composites_interp

    def log(self, msg):
        if self._verbose:
            logger.info(msg)

    def warning(self, msg):
        if self._verbose:
            logger.warning(msg)

    @staticmethod
    def load_band(
        coll: L2ACollection,
        band,
        resolution,
        resample_order=1,
        resample_sigma=2,
        force_compatible_bounds=True,
    ):
        if band == "SCL":
            band_resolution = 20
        else:
            band_resolution = BANDS_L2A_RESOLUTION[band]
        target_bounds = coll.bounds
        bounds_compatible = get_compatible_bounds(coll.bounds, resolution)
        incompatible_bounds = any(
            [bc != b for bc, b in zip(bounds_compatible, coll.bounds)]
        )
        if incompatible_bounds:
            if force_compatible_bounds:
                logger.warning(
                    f"Given bounds: {coll.bounds} are not compatible "
                    f"with resolution {resolution}. "
                    f"Forcing compatible bounds: {bounds_compatible}"
                )
                coll = coll.filter_bounds(bounds_compatible, coll.epsg)
            else:
                raise ValueError(
                    f"Given bounds: {coll.bounds} are not compatible "
                    f"with resolution {resolution}. "
                    "Set force_compatible_bounds=True to force "
                    "compatible bounds."
                )

        data = coll.load(
            bands=[band], resolution=band_resolution, resample=False
        )
        darr = data[band]
        darr = darr.expand_dims(band=[band]).rename({"timestamp": "time"})
        darr = darr.transpose("time", "band", "y", "x")
        darr = darr.astype("float32")

        # PB-dependent offset
        baseline_mask = (
            coll.df["baseline"]
            .str.extract("N(\d{4})")
            .astype(int)
            .to_numpy()
            .squeeze()
            >= 400
        )

        offset = xr.DataArray(
            (baseline_mask * 1000).astype(np.float32),
            dims=["time"],
            coords={"time": darr.time},
        )

        darr = darr.astype(np.float32)
        darr -= offset

        # TODO: add nodata mask from SCL // enabling lines below will use -1000 as nodata. not fully correct since PB4
        # nodata_mask = np.expand_dims(-offset, axis=(1, 2, 3))
        # nodata_mask = np.broadcast_to(nodata_mask, darr.shape)

        # darr = darr.where(darr != nodata_mask, np.nan)
        darr = darr / 10000
        y, x = coords_from_bounds(coll.bounds, band_resolution)
        darr = darr.assign_coords({"y": y, "x": x})

        if band_resolution != resolution:
            scale = resolution / band_resolution
            sigma = (
                0 if scale < 2 else resample_sigma
            )  # smooth only for upsampling from 60m
            darr_resampled = smooth_nan_rescale(
                darr.data,
                src_resolution=band_resolution,
                dst_resolution=resolution,
                order=resample_order,
                sigma=sigma,
            )

            y, x = coords_from_bounds(coll.bounds, resolution)
            darr_resampled = xr.DataArray(
                darr_resampled,
                dims=["time", "band", "y", "x"],
                coords={
                    "time": darr.time,
                    "band": darr.band,
                    "y": y,
                    "x": x,
                },
            )
            if incompatible_bounds:
                logger.info(
                    f"Cutting resampled data to target bounds at {resolution}m"
                )
                darr_resampled = cut_to_bounds(
                    darr_resampled,
                    target_bounds,
                )

            darr = darr_resampled

        return darr

    @timeit("loading")
    def load_bands(
        self,
        coll: L2ACollection,
        bands: List[str],
        resolution,
        resample_order=1,
        resample_sigma=2,
        force_compatible_bounds=True,
    ):
        darrs = [
            LoiBaseCompositesProcessor.load_band(
                coll,
                band,
                resolution,
                resample_order=resample_order,
                resample_sigma=resample_sigma,
                force_compatible_bounds=force_compatible_bounds,
            )
            for band in bands
        ]
        return xr.concat(darrs, dim="band")


class LoiAnnualCompositesProcessor(LoiBaseCompositesProcessor):
    """
    This class computes weighted composites based on per-period weights
    and interpolates missing observations.
    """

    def __init__(
        self,
        bounds: List[int],
        l2a_coll: L2ACollection,
        loi_coll: Loi10Collection,
        year: int,
        periods_number: int = 36,
        max_workers: int = 10,
        min_valid_weight: float = 0.01,
        loi_weights_params: LoiWeightsParams = LoiWeightsParams(),
        verbose: bool = False,
        rio_gdal_options: dict = RIO_GDAL_OPTIONS,
    ):
        periods = self._get_annual_periods(year, periods_number=periods_number)

        super().__init__(
            periods,
            bounds,
            l2a_coll,
            loi_coll,
            max_workers=max_workers,
            min_valid_weight=min_valid_weight,
            loi_weights_params=loi_weights_params,
            verbose=verbose,
            rio_gdal_options=rio_gdal_options,
        )

    @staticmethod
    def _get_annual_periods(year, periods_number=36):
        """
        Returns the list of periods for the given year.
        """
        start_date, end_date = f"{year}-01-01", f"{year + 1}-01-01"
        dekads = pd.date_range(
            start_date, end_date, periods=periods_number + 1
        )
        periods = [
            Period(dekads[i], dekads[i + 1], i) for i in range(dekads.size - 1)
        ]
        return periods

    def interpolate_composites(
        self,
        composites: xr.DataArray,
        valid_prob_range: float = 0.15,
        time_weight_sigma: float = 1.15,
        time_weight_alpha: float = 0.999,
        time_min_weight: float = 0.001,
    ):
        return super().interpolate_composites(
            composites,
            valid_prob_range=valid_prob_range,
            time_weight_sigma=time_weight_sigma,
            time_weight_alpha=time_weight_alpha,
            time_min_weight=time_min_weight,
        )


class LoiMonthlyCompositesProcessor(LoiBaseCompositesProcessor):
    """
    This class computes weighted composites based on per-period weights
    and interpolates missing observations.
    """

    def __init__(
        self,
        bounds: List[int],
        l2a_coll: L2ACollection,
        loi_coll: Loi10Collection,
        year: int,
        months: List[int] = range(1, 13),
        max_workers: int = 10,
        min_valid_weight: float = 0.01,
        loi_weights_params: LoiWeightsParams = LoiWeightsParams(),
        verbose: bool = False,
        rio_gdal_options: dict = RIO_GDAL_OPTIONS,
    ):
        periods = self._get_monthly_periods(months, year)

        super().__init__(
            periods,
            bounds,
            l2a_coll,
            loi_coll,
            max_workers=max_workers,
            min_valid_weight=min_valid_weight,
            loi_weights_params=loi_weights_params,
            verbose=verbose,
            rio_gdal_options=rio_gdal_options,
        )

    @staticmethod
    def _get_month_period_dates(month, year):
        """
        Returns the list of periods for the given year.
        """
        start_date = pd.Timestamp(f"{year}-{month:02d}-01")
        end_date = start_date + pd.DateOffset(months=1)

        return start_date, end_date

    def _get_monthly_periods(self, months: List[int], year: int):
        """
        Returns the list of periods for the given year.
        """
        periods = []
        for month in months:
            start_date, end_date = self._get_month_period_dates(month, year)
            periods.append(Period(start_date, end_date, month - 1))
        return periods

    def interpolate_composites(
        self,
        composites: xr.DataArray,
        valid_prob_range: float = 0.15,
        time_weight_sigma: float = 0.5,
        time_weight_alpha: float = 0.999,
        time_min_weight: float = 0.001,
    ):
        return super().interpolate_composites(
            composites,
            valid_prob_range=valid_prob_range,
            time_weight_sigma=time_weight_sigma,
            time_weight_alpha=time_weight_alpha,
            time_min_weight=time_min_weight,
        )
