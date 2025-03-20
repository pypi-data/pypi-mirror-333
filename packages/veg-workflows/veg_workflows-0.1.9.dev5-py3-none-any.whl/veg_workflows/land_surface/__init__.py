from dataclasses import dataclass
import pathlib
import geopandas as gpd
import satio
import pandas as pd
import numpy as np
from pathlib import Path
import os
import xml.etree.ElementTree as ET
import rasterio
from rasterio.enums import Resampling
import datetime
import shapely
import xarray as xr
from scipy.stats import norm
from scipy.integrate import quad
import catboost as cb
import enum
from ast import literal_eval

from satio.geoloader import load_reproject4

# from rio_tiler.reader import point as rio_tiler_point
# from daz.agera5 import Agera5Dataset
import datetime

from veg_workflows.paths import grids as veg_grid_paths
from veg_workflows.tiles import lcfm_tiles_10percent
from veg_workflows.tiles import lcfm_tiles_1percent
from veg_workflows.paths import models as veg_model_paths
from veg_workflows.features import get_latlon
from veg_workflows import products as lcfm_products

from veg_workflows.products import (
    Lsc10MonthlyCollection,
    Lsc120MonthlyCollection,
)
from veg_workflows.products import LsfMonthlyCollection
from veg_workflows.products import LsfAnnualCollection

from loguru import logger

import atexit
from tqdm import tqdm
from shapely.geometry import Polygon


##############################################
# Constants
##############################################
# paths to files
DEM_PATH = pathlib.Path("/vitodata/vegteam/auxdata/dem/COP-DEM_GLO-30-DTED/dem.vrt")

LSC_LABELS = [1, 2, 3, 4, 5]

PROB_BAND_NAMES = [
    "woody_vegetation",
    "herbaceous_vegetation",
    "not_vegetated_land",
    "snow_ice",
    "water",
    "clouds_shadow",
]

S2_BANDS = [
    "SCL",
    "B02",
    "B03",
    "B04",
    "B05",
    "B06",
    "B07",
    "B08",
    "B8A",
    "B11",
    "B12",
]

percentiles = ["p10", "p25", "p50", "p75", "p90"]
annual_bands = ["ndvi", "B02", "B03", "B04", "B08", "B11", "B12"]
LSF_ANNUAL_BANDS_SAME = [f"s2-{b}-{p}" for b in annual_bands for p in percentiles]
LSF_ANNUAL_BANDS_HIST = [f"hist-s2-{b}-{p}" for b in annual_bands for p in percentiles]
LSF_ANNUAL_BANDS = LSF_ANNUAL_BANDS_SAME + LSF_ANNUAL_BANDS_HIST

BLOCKS_FN = veg_grid_paths.BLOCKS_GRID_PATH

LSF_BANDS_10M = ["B02", "B03", "B04", "B08", "CCL"]
LSF_BANDS_20M = ["B05", "B06", "B07", "B8A", "B11", "B12"]
LSF_MONTHLY_BANDS = LSF_BANDS_10M + LSF_BANDS_20M
LSF_RESOLUTION = {
    "B02": "10M",
    "B03": "10M",
    "B04": "10M",
    "B08": "10M",
    "CCL": "10M",
    "B05": "20M",
    "B06": "20M",
    "B07": "20M",
    "B8A": "20M",
    "B11": "20M",
    "B12": "20M",
}

DEM_PATH = pathlib.Path("/vitodata/vegteam/auxdata/dem/COP-DEM_GLO-30-DTED/dem.vrt")

LSC_LABELS = [1, 2, 3, 4, 5]

PROB_BAND_NAMES = [
    "woody_vegetation",
    "herbaceous_vegetation",
    "not_vegetated_land",
    "snow_ice",
    "water",
    "clouds_shadow",
]


##############################################
# Seasonality score
##############################################


class NoDatasetsError(Exception): ...


# Functions to get the seasonality score
def compute_sigma(days):
    return days / 3


def day_of_year(day, month, year=2020):
    date = datetime.datetime(year, month, day)
    start_of_year = datetime.datetime(year, 1, 1)
    return (date - start_of_year).days + 1


def get_season_borders(year):
    seasons = {
        "fall_before": (
            day_of_year(21, 9, year - 1),
            day_of_year(20, 12, year - 1),
        ),
        "winter": (day_of_year(21, 12, year - 1), day_of_year(20, 3, year)),
        "spring": (day_of_year(21, 3, year), day_of_year(20, 6, year)),
        "summer": (day_of_year(21, 6, year), day_of_year(20, 9, year)),
        "fall": (day_of_year(21, 9, year), day_of_year(20, 12, year)),
        "winter_after": (
            day_of_year(21, 12, year),
            day_of_year(20, 3, year + 1),
        ),
    }
    return seasons


def seasonality_score(day, month, year, smoothing_days):
    day_of_year_val = day_of_year(day, month, year)
    sigma = compute_sigma(smoothing_days)

    seasons = get_season_borders(year)

    # Gaussian distribution centered on the day_of_year value
    x = np.arange(-730, 731)  # Span over two years for buffer zones
    gaussian = norm.pdf(x, loc=day_of_year_val, scale=sigma)
    gaussian /= gaussian.sum()  # Normalize the area to 1

    season_scores = []
    for season, (start, end) in seasons.items():
        if start < end:
            season_area, _ = quad(norm.pdf, start, end, args=(day_of_year_val, sigma))
        else:  # Crossing the year boundary, handle integration in two parts
            part1, _ = quad(norm.pdf, start, 730, args=(day_of_year_val, sigma))
            part2, _ = quad(norm.pdf, -730, end, args=(day_of_year_val, sigma))
            season_area = part1 + part2
        season_scores.append(season_area)

    # Return the scores for the 4 main seasons, excluding the buffer seasons
    scores = season_scores[1:-1]
    scores = list(map(lambda x: round(x, 4), scores))
    return scores


##############################################
# Scaling functions
##############################################


# Functions to apply jitter and logistic scaling to the dataset
def logistic(x, L=1, k=3.60, x0=0, y0=-0.5, s=2):
    return (L / (1 + np.exp(-k * (x - x0))) + y0) * s


def random_jitter(n):
    import random

    return random.uniform(-n, n)


def apply_cb_scaling(
    darr,
    apply_jitter,
    s2_bands,
    dem_band,
    history_bands,
    meteo_vars=None,
    k_factor=5,
    k_factor_jitter=2,
    lat_lon_jitter=1,
    dem_scaling=4000,
    lat_scaling=90,
    lon_scaling=180,
    meteo_scaling_dict=None,
    meteo_jitter_relative=0.1,
):
    darr = darr.astype(np.float32)

    def _random_jitter(x, apply_jitter=apply_jitter):
        return random_jitter(x) if apply_jitter else 0

    k_noised_signal = k_factor + _random_jitter(k_factor_jitter)
    k_noised_dem = k_factor + _random_jitter(k_factor_jitter)
    lat_jitter = _random_jitter(lat_lon_jitter)
    lon_jitter = _random_jitter(lat_lon_jitter)

    # we rescale the dem band by 4000 as upper limit for high altitudes
    # we then apply the logistic scaling to it as well
    dem_band = [dem_band] if dem_band in darr.band.values else None
    lat_band = ["lat"] if "lat" in darr.band.values else None
    lon_band = ["lon"] if "lon" in darr.band.values else None
    history_bands = (
        history_bands if set(history_bands).issubset(darr.band.values) else None
    )
    seas_bands = (
        ["seas_1", "seas_2", "seas_3", "seas_4"]
        if set(["seas_1", "seas_2", "seas_3", "seas_4"]).issubset(darr.band.values)
        else None
    )

    # we rescale lat lon bands between their ranges, no logistic scaling
    darr_s2 = darr.sel(band=s2_bands)
    # darr_s2 = darr_s2 / s2_scaling
    if k_factor > 0:
        darr_s2 = logistic(darr_s2, k=k_noised_signal)

    darr_history = None
    if history_bands is not None:
        darr_history = darr.sel(band=history_bands)
        if k_factor > 0:
            darr_history = logistic(darr_history, k=k_noised_signal)

    darr_dem = None
    if dem_band is not None:
        darr_dem = darr.sel(band=dem_band)
        darr_dem = darr_dem / dem_scaling

    if (k_factor > 0) and (dem_band is not None):
        darr_dem = logistic(darr_dem, k=k_noised_dem)

    darr_lat = (
        (darr.sel(band=["lat"]) + lat_jitter) / lat_scaling
        if lat_band is not None
        else None
    )
    darr_lon = (
        (darr.sel(band=["lon"]) + lon_jitter) / lon_scaling
        if lon_band is not None
        else None
    )

    darr_seas = darr.sel(band=seas_bands) if seas_bands is not None else None

    darr_meteo = None
    if meteo_vars is not None:
        meteo_bands = meteo_vars
        darr_meteo = darr.sel(band=meteo_bands)
        meteo_scaling_vals = np.array(
            [meteo_scaling_dict[v.split("-")[0]] for v in meteo_bands]
        )
        darr_meteo = darr_meteo / np.expand_dims(meteo_scaling_vals, (1, 2))
        if meteo_jitter_relative > 0:
            # adding relative noise to meteo
            meteo_jitter_vars = np.array(
                [random_jitter(meteo_jitter_relative) for _ in range(len(meteo_vars))]
            )
            darr_meteo = darr_meteo + darr_meteo * np.expand_dims(
                meteo_jitter_vars, (1, 2)
            )

    darrs = [
        d
        for d in (
            darr_s2,
            darr_dem,
            darr_lat,
            darr_lon,
            darr_meteo,
            darr_history,
            darr_seas,
        )
        if d is not None
    ]

    if len(darrs) > 1:
        darr = xr.concat(darrs, dim="band")
    else:
        darr = darrs[0]

    return darr


##############################################
# Loading functions
##############################################


# load the features for a given area
def load_features(block, bands, darr_lsf_monthly, darr_lsf_annual):
    (_, bounds, epsg, resolution) = (
        block.tile,
        block.bounds,
        block.epsg,
        block.resolution,
    )
    (xmin, ymin, xmax, ymax) = bounds
    nrows = int((ymax - ymin) / resolution)
    ncols = int((xmax - xmin) / resolution)

    list_arr = []
    list_bands = []
    for band in bands:
        if band in list(darr_lsf_monthly.band.values):  # monthly features
            if band in S2_BANDS:
                scale = 10000
            else:
                scale = 1
            # load Sentinel data
            b = darr_lsf_monthly.sel(band=band).data.astype(np.float32) / scale
            list_arr.append(b)
            list_bands.append(band)

        elif band in LSF_ANNUAL_BANDS_SAME:
            # load the LSF annual of the same year
            list_arr.append(darr_lsf_annual.sel(band=band).data.astype(np.float32))
            list_bands.append(band)

        elif band in LSF_ANNUAL_BANDS_HIST:
            # load the LSF annual of the past year
            list_arr.append(
                darr_lsf_annual.sel(band=band.split("hist_")[-1]).data.astype(
                    np.float32
                )
            )
            list_bands.append(band)

        elif band == "DEM":
            # load DEM
            arr_dem = np.squeeze(
                load_reproject4(DEM_PATH, bounds, epsg, resolution=resolution)
            )
            list_arr.append(arr_dem)
            list_bands.append(band)

        elif band in ["seas_1", "seas_2", "seas_3", "seas_4"]:
            # load time
            (year, month, day) = block.get_mid_date()
            smoothing_days = 60
            scores = seasonality_score(day, month, year, smoothing_days)
            index = ["seas_1", "seas_2", "seas_3", "seas_4"].index(band)
            seas_score = np.ones((nrows, ncols)) * scores[index]
            list_arr.append(seas_score)
            list_bands.append(band)

        elif band in ["lat", "lon"]:
            # load lat & lon
            lat, lon = get_latlon(
                block.bounds, block.epsg, resolution=resolution, steps=5
            )
            if band == "lon":
                list_arr.append(lon)
                list_bands.append(band)
            else:
                list_arr.append(lat)
                list_bands.append(band)

        elif band in ["ndvi", "ndsi", "ndwi", "nbr"]:
            continue
        else:
            raise ValueError(
                f"Error with band: {band}.\nFailed to extract band: {band}"
            )
    # for tst in list_arr:
    # print(tst.shape)
    arr = np.stack(list_arr)

    attrs = {"epsg": epsg, "bounds": bounds}

    new_y, new_x = compute_pixel_coordinates(bounds, arr.shape[-2:])

    darr = xr.DataArray(
        arr,
        dims=["band", "y", "x"],
        coords={"band": list_bands, "y": new_y, "x": new_x},
        attrs=attrs,
    )
    return darr.astype(np.float32)


def compute_pixel_coordinates(bounds, shape):
    """
    Compute the y and x coordinates for every pixel in an image.

    Args:
    bounds (tuple): A tuple containing (xmin, ymin, xmax, ymax).
    shape (tuple): A tuple containing the image shape (rows, columns).

    Returns:
    tuple: Two arrays containing y and x coordinates for every pixel.
    """
    xmin, ymin, xmax, ymax = bounds
    rows, cols = shape

    x_res = (xmax - xmin) / cols
    y_res = (ymax - ymin) / rows

    if x_res != y_res:
        raise ValueError(
            "Different resolution for y and x axis are not "
            "supported. Bounds and shape are not consistent "
            "with the same resolution on both axis."
        )

    res_half = x_res / 2

    xx = np.linspace(xmin + res_half, xmax - res_half, cols)

    yy = np.linspace(ymax - res_half, ymin + res_half, rows)

    return yy, xx


def compute_vi(arr, b1, b2):
    return (arr.sel(band=b1) - arr.sel(band=b2)) / (arr.sel(band=b1) + arr.sel(band=b2))


def last_day_of_month(year, month):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = datetime.date(year, month, 28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)


##############################################
# Label colors
##############################################


class LabelsColorsLsc(enum.Enum):
    NO_DATA = (255, "nodata", "Not sure", "No Data", np.array([0, 0, 0]))
    WOODY = (
        1,
        "woody",
        "woody",
        "Woody vegetation",
        np.array([128, 144, 17]) / 255,
    )
    HERBACEOUS = (
        2,
        "herb_act",
        "herb_act",
        "Photosynthetically active herbaceous vegetation",
        np.array([255, 255, 76]) / 255,
    )
    NOT_VEGETATED = (
        3,
        "bare",
        "bare",
        "Bare areas",
        np.array([180, 180, 180]) / 255,
    )
    SNOW_AND_ICE = (
        4,
        "snow",
        "snow and ice",
        "Snow and/or ice cover",
        np.array([240, 240, 240]) / 255,
    )
    WATER = (
        5,
        "water",
        "water",
        "Permanent water",
        np.array([0, 100, 200]) / 255,
    )
    OCCLUDED = (
        0,
        "cloud",
        "cloud",
        "cloud",
        np.array([184, 2, 129]) / 255,
    )  # 80, 80, 80

    def __init__(self, val1, val2, val3, val4, val5):
        self.id = val1
        self.class_name = val2
        self.iiasa_name = val3
        self.esa_class_name = val4
        self.color = val5


lsc_colormap = {
    0: (184, 2, 129, 255),
    1: (128, 144, 17, 255),
    2: (255, 255, 76, 255),
    3: (180, 180, 180, 255),
    4: (240, 240, 240, 255),
    5: (0, 100, 200, 255),
    255: (0, 0, 0, 255),
}

##############################################
# Process block
##############################################


@dataclass
class ProcessBlock:
    """LSC process unit information"""

    tile: str
    block_id: int
    bounds: list
    epsg: int
    resolution: int
    startdate: dict  # year, month, day
    enddate: dict  # year, month, day

    def get_mid_date(self):
        a = datetime.datetime(
            self.startdate["year"],
            self.startdate["month"],
            self.startdate["day"],
        )
        b = datetime.datetime(
            self.enddate["year"], self.enddate["month"], self.enddate["day"]
        )
        mid = a + (b - a) / 2
        return (mid.year, mid.month, mid.day)


##############################################
# Process function
##############################################


def _process(lsc_block, model, darr_lsf_monthly, darr_lsf_annual, verbose=False):
    if verbose:
        pass
        # logger.info(
        #     f'processing {lsc_block.tile} {lsc_block.block_id} year {lsc_block.startdate["year"]} month {lsc_block.startdate["month"]}'
        # )

    CB_FEAT_NAMES = model.feature_names_

    # load the features for a given area
    feats_arr = load_features(
        lsc_block, CB_FEAT_NAMES, darr_lsf_monthly, darr_lsf_annual
    )
    nrows = feats_arr.shape[-2]
    ncols = feats_arr.shape[-1]

    # get clouds, cloud_probs, and nodata
    clouds_arr = darr_lsf_monthly.sel(band="CCL").data
    clouds = np.squeeze(clouds_arr == 2) * 1
    cloud_probs = clouds * 100

    nodata = (np.isnan(feats_arr.sel(band=["B02", "B08"]).data) * 1).sum(axis=0)
    nodata = (nodata > 0) * 1
    nodata[np.squeeze(clouds_arr.data == 3)] = 1
    cloud_probs[(cloud_probs < 100) & (nodata == 1)] = 255

    # apply logistic scaling to the data
    cb_s2_feat_names = [
        feat_name for feat_name in CB_FEAT_NAMES if feat_name in S2_BANDS
    ]
    cb_lsf_annual_feat_names = [
        feat_name for feat_name in CB_FEAT_NAMES if feat_name in LSF_ANNUAL_BANDS
    ]
    if len(cb_lsf_annual_feat_names) == 0:
        cb_lsf_annual_feat_names = [""]

    darr_scaled = apply_cb_scaling(
        feats_arr,
        apply_jitter=False,
        s2_bands=cb_s2_feat_names,
        dem_band="DEM",
        history_bands=cb_lsf_annual_feat_names,
        k_factor=5,
        k_factor_jitter=0,
        lat_lon_jitter=0,
    )

    # compute the NDVI, NDSI, NBR, NDWI from the scaled data and add the VI to the feature array
    ndvi = compute_vi(darr_scaled, "B08", "B04")
    ndsi = compute_vi(darr_scaled, "B03", "B11")
    nbr = compute_vi(darr_scaled, "B08", "B12")
    ndwi = compute_vi(darr_scaled, "B03", "B08")

    arr = np.vstack(
        (
            nbr.data[np.newaxis, ...],
            ndvi.data[np.newaxis, ...],
            ndwi.data[np.newaxis, ...],
            ndsi.data[np.newaxis, ...],
        )
    )

    attrs = {"epsg": lsc_block.epsg, "bounds": lsc_block.bounds}

    new_y, new_x = compute_pixel_coordinates(lsc_block.bounds, nbr.shape[-2:])

    darr = xr.DataArray(
        arr,
        dims=["band", "y", "x"],
        coords={
            "band": ["nbr", "ndvi", "ndwi", "ndsi"],
            "y": new_y,
            "x": new_x,
        },
        attrs=attrs,
    )

    darr = darr.astype(np.float32)
    feats_cb = xr.concat([darr_scaled, darr], dim="band")

    # convert the features to a dataframe
    feat_shape = feats_cb.values.shape
    feat_names = list(feats_cb.band.values)
    df = pd.DataFrame(
        np.reshape(feats_cb.values, (len(feat_names), -1)).transpose(),
        columns=feat_names,
    )

    # probabilities
    prob_cb = np.squeeze(
        np.reshape(
            model.predict(df[CB_FEAT_NAMES]),
            (feat_shape[1], feat_shape[2], len(LSC_LABELS)),
        )
    )

    # predictions
    pred_cb_ind = np.argmax(prob_cb, axis=2)
    pred_cb = np.zeros((nrows, ncols))

    for ind, lab in enumerate(LSC_LABELS):
        pred_cb[pred_cb_ind == ind] = lab

    # clip the probabilities to 0-100 range
    prob_cb = np.moveaxis(prob_cb, [0, 1, 2], [1, 2, 0])
    prob_cb[prob_cb < 0] = 0
    prob_cb[prob_cb > 100] = 100

    # set the nodata pixels to 255
    prob_cb[:, nodata == 1] = 255
    pred_cb[nodata == 1] = 255

    # set the cloud class in the predictions
    pred_cb[np.squeeze(clouds) == 1] = 0
    # prob_cb[clouds == 1,:] = 0

    # add clouds probs
    prob_cb = np.vstack(
        [prob_cb, cloud_probs[np.newaxis, ...]]
    )  # add probability for clouds class

    # adjust datatype
    prob_cb = prob_cb.astype(np.uint8)  # store as uint8 - values between 0 and 255
    pred_cb = pred_cb.astype(np.uint8)

    return pred_cb, prob_cb


# climate
def agera_var_path(var_name, date_id="20200101", agera_path=Path("/data/MTDA/AgERA5")):
    agera_sub_path = agera_path / date_id[:4] / date_id
    return agera_sub_path / f"AgERA5_{var_name}_{date_id}.tif"


# def agera_var_point(
#     var_name,
#     date_id="20200101",
#     lon=0,
#     lat=0,
#     agera_path=Path("/data/MTDA/AgERA5"),
# ):
#     agera_path = agera_var_path(var_name, date_id, agera_path)
#     with rasterio.open(str(agera_path)) as src:
#         scale = src.scales[0]
#         return rio_tiler_point(src, coordinates=(lon, lat)).data[0] * scale


def _post_process(
    map_hist,
    prob_hist,
    map_nrt,
    prob_nrt,
    bounds,
    epsg,
    year=2020,
    verbose=False,
):
    # load the climate time series
    if verbose:
        logger.info("loading climate data")
    [xmin, ymin, xmax, ymax] = bounds
    lat_point_list = [ymin, ymax, ymax, ymin, ymin]
    lon_point_list = [xmin, xmin, xmax, xmax, xmin]

    polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
    polygon = gpd.GeoDataFrame(index=[0], crs=f"epsg:{epsg}", geometry=[polygon_geom])
    geom_centroid = polygon.centroid.to_crs("epsg:4326").geometry
    [lon_centroid, lat_centroid] = [geom_centroid.x[0], geom_centroid.y[0]]

    agera_dataset = Agera5Dataset()
    t_min = []
    for month in range(1, 13):
        last_day = last_day_of_month(year, month).day
        t_min.append(
            agera_dataset.var_point(
                "temperature-min",
                f"{year}{month:02d}{last_day:02d}",
                lon_centroid,
                lat_centroid,
                30,
            )
            - 273.15
        )

    # change detection
    if verbose:
        logger.info("Starting change detection")
    woody_mask = ((map_nrt == 1).sum(axis=0) > 0) * 1
    list_change_prob = []
    list_frac_pre = []
    list_frac_post = []
    if verbose:
        logger.info(prob_nrt.shape)
    for t in np.arange(1, 12):
        # disturbance magnitude
        t_pre_start = max(0, t - 3)
        t_pre_end = max(0, t)
        t_post_start = min(t, 12)
        t_post_end = min(t + 3, 12)

        p_pre = np.nanmean(prob_nrt[t_pre_start:t_pre_end, 0, ...], axis=0)
        # logger.info(t)
        # logger.info(f'{t_pre_start, t_pre_end, t_post_start, t_post_end}')
        # logger.info(prob_nrt[t_pre_start:t_pre_end,0,...].shape)
        # logger.info(prob_nrt[t_post_start:t_post_end,0,...].shape)
        p_post = np.nanmean(prob_nrt[t_post_start:t_post_end, 0, ...], axis=0)
        p_pre[p_pre == 0] = 1

        delta_p = (p_pre - p_post) / p_pre
        list_change_prob.append(delta_p)

        # pre-disturbance state
        t_pre_start = max(0, t - 12)
        t_pre_end = max(0, t)

        is_woody = (map_nrt[t_pre_start:t_pre_end, ...] == 1).sum(axis=0)
        is_valid = (
            (map_nrt[t_pre_start:t_pre_end, ...] > 0)
            & (map_nrt[t_pre_start:t_pre_end, ...] < 255)
            & (map_nrt[t_pre_start:t_pre_end, ...] != 4)
        ).sum(axis=0)
        is_valid[is_valid == 0] = 1
        list_frac_pre.append(is_woody / is_valid)

        # post-disturbance state
        t_post_start = min(t, 12)
        t_post_end = min(t + 6, 12)

        is_not_woody = (
            (map_nrt[t_post_start:t_post_end, ...] > 1)
            & (map_nrt[t_post_start:t_post_end, ...] < 5)
        ).sum(axis=0)
        is_valid = (
            (map_nrt[t_post_start:t_post_end, ...] > 0)
            & (map_nrt[t_post_start:t_post_end, ...] < 255)
            & (map_nrt[t_post_start:t_post_end, ...] != 4)
        ).sum(axis=0)
        is_valid[is_valid == 0] = 1
        list_frac_post.append(is_not_woody / is_valid)

    delta_p = np.stack(list_change_prob)
    frac_woody_pre = np.stack(list_frac_pre)
    frac_nonwoody_post = np.stack(list_frac_post)
    has_change = np.nanmax(
        (delta_p > 0.5) & (frac_woody_pre > 0.6) & (frac_nonwoody_post == 1),
        axis=0,
    )

    mask = ~has_change.squeeze() & woody_mask.squeeze()
    merged_prob = prob_nrt.copy()
    merged_prob[:, :2, mask == 1] = prob_hist[:, :2, mask == 1]

    merged_map = merged_prob.argmax(axis=1) + 1
    merged_map[map_nrt == 255] = 255
    merged_map[map_nrt == 0] = 0

    # correct snow over clouds
    if verbose:
        logger.info("Starting snow correction")
    is_snow = np.nansum(merged_map == 4, axis=0)
    is_valid = np.nansum((merged_map > 0) & (merged_map < 255), axis=0)
    frac_snow = is_snow / is_valid
    for ind, p in enumerate(merged_prob):
        if t_min[ind] > 5:
            to_clouds = (frac_snow[1] < 0.5) & (merged_map[ind, ...] == 4)
            merged_prob[ind, 5, to_clouds] = p[3, to_clouds]  # clouds get the snow prob
            merged_prob[ind, 3, to_clouds] = 0  # set probability snow to zero
    merged_map = merged_prob.argmax(axis=1) + 1
    merged_map[merged_map == 6] = 0
    merged_map[map_nrt == 255] = 255
    merged_map[map_nrt == 0] = 0

    assert np.all(np.isin(merged_map, [0, 1, 2, 3, 4, 5, 255])), (
        "LSC values are not in range [0, 5] or nodata_value"
    )

    # write to file
    # adjust datatype
    merged_prob[np.isnan(merged_prob)] = 255

    merged_prob = merged_prob.astype(
        np.uint8
    )  # store as uint8 - values between 0 and 255
    merged_map = merged_map.astype(np.uint8)

    return merged_map, merged_prob
