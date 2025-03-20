import subprocess
from pathlib import Path
from typing import Dict, List

import numpy as np
import rasterio
import xarray as xr
from loguru import logger
from rasterio.enums import Resampling
from satio_pc.geotiff import get_rasterio_profile_shape, write_geotiff_tags
from scipy.ndimage import gaussian_filter


def load_array_bounds(
    fname,
    bounds=None,
    fill_value=0,
    unscale=False,
    out_shape=None,
    resampling=Resampling.bilinear,
):
    with rasterio.open(fname) as src:
        if bounds is not None:
            window = rasterio.windows.from_bounds(*bounds, src.transform)
        else:
            window = None

        arr = src.read(
            window=window,
            boundless=True,
            fill_value=fill_value,
            out_shape=out_shape,
            resampling=resampling,
        )

        if unscale:
            raise NotImplementedError("Unscaling not implemented")

            # nodata = src.nodata
            # scales = src.scales
            # offsets = src.offsets

            # nodata_mask = arr == nodata
            # arr = arr * scales + offsets

    return arr


def to_dataarray(arr, bounds=None, epsg=None, bands=None, attrs=None):
    if bounds is None:
        bounds = [0, 0, 1, 1]
    if bands is None and arr.ndim == 3:
        bands = [str(i) for i in range(arr.shape[0])]

    xmin, ymin, xmax, ymax = bounds
    resolution_x = (xmax - xmin) / arr.shape[-1]
    resolution_y = (ymax - ymin) / arr.shape[-2]
    y = np.linspace(ymax - resolution_y / 2, ymin + resolution_y / 2, arr.shape[-2])
    x = np.linspace(xmin + resolution_x / 2, xmax - resolution_x / 2, arr.shape[-1])

    if arr.ndim == 3:
        darr = xr.DataArray(
            arr,
            dims=["band", "y", "x"],
            coords={"y": y, "x": x, "band": bands},
        )
    elif arr.ndim == 2:
        darr = xr.DataArray(arr, dims=["y", "x"], coords={"y": y, "x": x})
    else:
        raise ValueError("Array must be 2D or 3D")
    new_attrs = dict(bounds=bounds, epsg=epsg)
    if attrs is None:
        attrs = new_attrs
    else:
        attrs.update(new_attrs)

    darr.attrs = attrs

    return darr


def gdal_warp(src_fn, dst_fn, resampling_method="NEAR"):
    import sys

    if Path(dst_fn).is_file():
        Path(dst_fn).unlink()

    py = sys.executable.split("/")[-1]
    bin = sys.executable.replace(py, "gdalwarp")

    resampling = resampling_method
    gdal_cachemax = 2000

    cmd = (
        f"{bin} "
        f"-of vrt "
        f"-r {resampling} -ts 10980 10980 "
        f"--config GDAL_CACHEMAX {gdal_cachemax} "
        f"{src_fn} "
        f"{dst_fn}"
    )
    logger.debug(cmd)
    p = subprocess.run(cmd.split())
    if p.returncode != 0:
        raise IOError("GDAL warping failed")


def shape_from_bounds(bounds, resolution=10):
    """Calculate shape from bounds and resolution
    Args:
        bounds (Tuple): (xmin, ymin, xmax, ymax)
        resolution (int, optional): Defaults to 10.

    Returns:
        Tuple(Int, Int): height, width
    """
    xmin, ymin, xmax, ymax = bounds
    xres, yres = resolution, resolution
    height = int((ymax - ymin) / yres)  # rows
    width = int((xmax - xmin) / xres)  # cols

    return height, width


def coords_from_bounds(bounds, resolution=10):
    height, width = shape_from_bounds(bounds, resolution=resolution)

    center_shift = resolution / 2
    xmin, xmax = (bounds[0] + center_shift), (bounds[2] - center_shift)
    ymin, ymax = (bounds[1] + center_shift), (bounds[3] - center_shift)

    x = np.linspace(xmin, xmax, width)

    y = np.linspace(ymax, ymin, height)

    return y, x


def load_cloudsen_mask(
    mask_path,
    bounds=None,
    fill_value=None,
    blur_sigma=None,
    mask_threshold=None,
    resampling_method=Resampling.bilinear,
    resolution=10,
):
    arr = load_array_bounds(
        mask_path,
        bounds,
        fill_value=fill_value,
        resampling=resampling_method,
        out_shape=shape_from_bounds(bounds, resolution=resolution),
    )

    if blur_sigma:
        arr = arr.astype(np.float32)
        arr[arr == fill_value] = 0  # nodata is set to 0 (valid) otherwise
        # it will be blurred and cause no data inside the image when there
        # is an orbit border. this might cause under detection on the border

        arr = gaussian_filter(arr, sigma=blur_sigma)

        if mask_threshold:  # apply threshold only when blurring
            arr = arr >= mask_threshold

    return arr


def save_geotiff(
    data,
    bounds: List = [0, 1, 0, 1],
    epsg: int = 4326,
    bands_names: List = None,
    filename: str = None,
    nodata_value: int = None,
    tags: Dict = None,
    bands_tags: List[Dict] = None,
    colormap: str = None,
    scales: np.ndarray = None,
    offsets: np.ndarray = None,
    **profile_kwargs,
):
    """Save geotiff of 3d features array. Sets the band names (first dimension)
    as bands description.

    Args:
        data (np.ndarray): numpy array with dims (band, y, x)
        bounds (List, optional): _description_. Defaults to [0, 1, 0, 1].
        epsg (int, optional): _description_. Defaults to 4326.
        filename (str, optional): _description_. Defaults to None.
        tags (Dict, optional): _description_. Defaults to None.
        compress_tag (str, optional): _description_. Defaults to
        'deflate-uint16'.

    """

    profile = get_rasterio_profile_shape(data.shape, bounds, epsg, data.dtype)

    if nodata_value is not None:
        profile.update(nodata=nodata_value)

    profile.update(**profile_kwargs)

    if scales is not None:
        scales = np.array(scales)
        if scales.ndim > 1:
            scales = np.squeeze(scales).tolist()
    if offsets is not None:
        offsets = np.array(offsets)
        if offsets.ndim > 1:
            offsets = np.squeeze(offsets).tolist()

    default_tags = {
        "bands": bands_names,
    }

    tags = tags or {}
    tags = {**default_tags, **tags}

    if filename is not None:
        write_geotiff_tags(
            data,
            profile,
            filename,
            bands_names=bands_names,
            colormap=colormap,
            nodata=nodata_value,
            tags=tags,
            bands_tags=bands_tags,
            scales=scales,
            offsets=offsets,
        )


class GdalBandScaler:
    def __init__(
        self,
        unscaled_range,
        scaled_range,
        scaled_nodata=None,
        scaled_dtype=None,
        clip_outside_unscaled_range=False,
    ):
        """
        Computes scale and offset for scaling data between unscaled_range and scaled_range using the gdal formula:
        unscaled_value = scaled_value * scale + offset
        and the inverse:
        scaled_value = (unscaled_value - offset) / scale

        Args:
            unscaled_range (Tuple): (min, max) of the unscaled data
            scaled_range (Tuple): (min, max) of the scaled data
            scaled_nodata (int, optional): nodata value for the scaled data. Defaults to None.
            scaled_dtype (np.dtype, optional): dtype for the scaled data. Defaults to None.
            clip_outside_unscaled_range (bool, optional): clip values outside the unscaled range. Defaults to False.
        """
        # formula: true_value = tif_value * scale + offset
        # inverse formula: tif_value = (true_value - offset) / scale
        self._unscaled_min, self._unscaled_max = unscaled_range
        self._scaled_min, self._scaled_max = scaled_range

        self._uscaled_extent = self._unscaled_max - self._unscaled_min
        self._scaled_extent = self._scaled_max - self._scaled_min

        self._scaled_nodata = scaled_nodata
        self._scaled_dtype = scaled_dtype
        self._clip_outside_unscaled_range = clip_outside_unscaled_range

    def scale_data(self, unscaled_data):
        nodata_mask = np.isnan(unscaled_data)
        if self._clip_outside_unscaled_range:
            unscaled_data = np.clip(
                unscaled_data, self._unscaled_min, self._unscaled_max
            )

        scaled_data = unscaled_data * self.scale + self.offset
        if self._scaled_nodata is not None:
            scaled_data[nodata_mask] = self._scaled_nodata

        if self._scaled_dtype is not None:
            scaled_data = scaled_data.astype(self._scaled_dtype)

        return scaled_data

    def unscale_data(self, scaled_data):
        uscaled_data = (scaled_data.astype(np.float32) - self.offset) / self.scale

        if self._scaled_nodata is not None:
            nodata_mask = scaled_data == self._scaled_nodata
            uscaled_data[nodata_mask] = np.nan
        return uscaled_data

    @property
    def scale(self):
        return self._uscaled_extent / self._scaled_extent

    @property
    def offset(self):
        return self._unscaled_min - self._scaled_min * self.scale


class GdalScaler:
    def __init__(
        self,
        unscaled_ranges,
        scaled_ranges,
        scaled_nodata=None,
        scaled_dtype=None,
        clip_outside_unscaled_range=False,
    ):
        """
        Computes scales and offsets for scaling data between unscaled_range and scaled_range using the gdal formula:
        unscaled_value = scaled_value * scale + offset
        and the inverse:
        scaled_value = (unscaled_value - offset) / scale

        Args:
            unscaled_range (Tuple): (min, max) of the unscaled data
            scaled_range (Tuple): (min, max) of the scaled data
            scaled_nodata (int, optional): nodata value for the scaled data. Defaults to None.
            scaled_dtype (np.dtype, optional): dtype for the scaled data. Defaults to None.
            clip_outside_unscaled_range (bool, optional): clip values outside the unscaled range. Defaults to False.
        """

        self._band_scalers = [
            GdalBandScaler(
                unscaled_range,
                scaled_range,
                scaled_nodata,
                scaled_dtype,
                clip_outside_unscaled_range,
            )
            for unscaled_range, scaled_range in zip(unscaled_ranges, scaled_ranges)
        ]

    def scale_data(self, unscaled_data):
        if unscaled_data.ndim == 2:
            return self._band_scalers[0].scale_data(unscaled_data)
        elif unscaled_data.ndim == 3:
            # band is on axis 0
            return np.stack(
                [
                    scaler.scale_data(unscaled_data[i])
                    for i, scaler in enumerate(self._band_scalers)
                ]
            )
        else:
            raise ValueError("Data must be 2D or 3D")

    def unscale_data(self, scaled_data):
        if scaled_data.ndim == 2:
            return self._band_scalers[0].unscale_data(scaled_data)
        elif scaled_data.ndim == 3:
            # band is on axis 0
            return np.stack(
                [
                    scaler.unscale_data(scaled_data[i])
                    for i, scaler in enumerate(self._band_scalers)
                ]
            )
        else:
            raise ValueError("Data must be 2D or 3D")

    @property
    def scales(self):
        return [scaler.scale for scaler in self._band_scalers]

    @property
    def offsets(self):
        return [scaler.offset for scaler in self._band_scalers]
