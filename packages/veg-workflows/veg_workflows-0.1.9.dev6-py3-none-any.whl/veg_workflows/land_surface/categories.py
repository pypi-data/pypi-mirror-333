from veg_workflows.paths import models as veg_model_paths
import numpy as np
import catboost as cb
import geopandas as gpd
from veg_workflows.land_surface.categories_stats import (
    generate_frac,
    generate_fracnosnow,
    generate_nunique,
    generate_probmean,
    generate_probmeannosnow,
    generate_probstd,
    generate_probstdnosnow,
)
from veg_workflows.land_surface import (
    ProcessBlock,
    last_day_of_month,
    _process,
    _post_process,
)
from loguru import logger
from tqdm import tqdm

if __name__ == "__main__":
    from evotrain.v2ts import EvoTrainV2TSDataset
    from evotrain.v2 import EvoTrainV2Dataset
    from veg_workflows.paths.datasets import EVOTRAIN
    from veg_workflows.land_surface.composites import (
        LandSurfaceFeatures,
        compositing_settings,
    )

    evo_dataset = EvoTrainV2Dataset()
    evots_dataset = EvoTrainV2TSDataset()

    locs = gpd.read_file(EVOTRAIN)

    evo_dataset._locs = evots_dataset._locs = locs

    # locs = locs[locs["tile"] == "04VEP"]
    loc = locs.sample(1).iloc[0]
    loc_id = loc.location_id

    ts = evots_dataset.read(
        loc_id,
        year=2020,
        bands=[
            "B02",
            "B03",
            "B04",
            "B08",
            "B05",
            "B06",
            "B07",
            "B8A",
            "B11",
            "B12",
            "B01",
            "B09",
            "SCL",
        ],
    )

    lsf = LandSurfaceFeatures(compositing_settings)
    ts_composites = lsf.process_timeseries(ts)

    LSF_VERSION = "v007"

    nrt_model_version = "v4_1_f"  #'v4_1_f' 'v4_1_h'
    hist_model_version = "v4_1_h"  #'v4_1_f' 'v4_1_h'
    LSC_BASE_VERSION = "v003"

    nrt_cb_model_path = veg_model_paths.LSC_CB_MODEL[
        LSC_BASE_VERSION + nrt_model_version[-1]
    ]
    hist_cb_model_path = veg_model_paths.LSC_CB_MODEL[
        LSC_BASE_VERSION + hist_model_version[-1]
    ]

    years = [2020]
    months = list(np.arange(1, 13))  # [1,2,3,4,5,6,7,8,9,10,11,12
    resolution = 10  # 10 or 120 # resolution of the predictions in meters

    # load the model and predict the LSC
    nrt_model = cb.CatBoostRegressor()
    nrt_model.load_model(nrt_cb_model_path)

    hist_model = cb.CatBoostRegressor()
    hist_model.load_model(hist_cb_model_path)

    year = 2020
    bands_lsf_annual = [
        "s2-ndvi-p10",
        "s2-ndvi-p25",
        "s2-ndvi-p50",
        "s2-ndvi-p75",
        "s2-ndvi-p90",
    ]

    ALL_FEAT_NAMES = hist_model.feature_names_ + nrt_model.feature_names_

    if len([f for f in ALL_FEAT_NAMES if f.startswith("hist")]) > 0:
        lsf_annual_year = year - 1
    else:
        lsf_annual_year = year

    darr_lsf_annual = evo_dataset.read(
        loc_id,
        year=lsf_annual_year,
        bands=bands_lsf_annual,
    )  # these are the  yearly features (can also pass a bands arg to the read method to make reading faster)
    # feats.band.values.tolist()

    nrt_pred_list = []
    nrt_prob_list = []

    hist_pred_list = []
    hist_prob_list = []

    year = 2020
    for month in tqdm(months, desc="Predicting LSC"):
        darr_lsf_monthly = ts_composites.sel(time=month - 1).copy()
        darr_lsf_monthly = darr_lsf_monthly.astype(np.float32)
        darr_lsf_monthly = darr_lsf_monthly.where(darr_lsf_monthly != 32767, np.nan)

        lsc_block = ProcessBlock(
            tile=loc.tile,
            block_id=loc.block_id,
            bounds=[loc.xmin, loc.ymin, loc.xmax, loc.ymax],
            epsg=loc.epsg,
            resolution=10,
            startdate=dict({"year": year, "month": month, "day": 1}),
            enddate=dict(
                {
                    "year": year,
                    "month": month,
                    "day": last_day_of_month(year, month).day,
                }
            ),
        )

        # get the nrt lsc prediction and probability
        pred, prob = _process(lsc_block, nrt_model, darr_lsf_monthly, darr_lsf_annual)
        nrt_pred_list.append(pred)
        nrt_prob_list.append(prob)

        # get the hist lsc prediction and probability
        pred, prob = _process(lsc_block, hist_model, darr_lsf_monthly, darr_lsf_annual)
        hist_pred_list.append(pred)
        hist_prob_list.append(prob)

    nrt_pred = np.stack(nrt_pred_list)
    nrt_prob = np.stack(nrt_prob_list)
    hist_pred = np.stack(hist_pred_list)
    hist_prob = np.stack(hist_prob_list)

    epsg = lsc_block.epsg
    bounds = lsc_block.bounds
    nrt_prob = nrt_prob.astype(np.float32)
    hist_prob = hist_prob.astype(np.float32)
    nrt_prob[nrt_prob == 255] = np.nan
    hist_prob[hist_prob == 255] = np.nan
    merged_map, merged_prob = _post_process(
        hist_pred, hist_prob, nrt_pred, nrt_prob, bounds, epsg
    )

    frac = generate_frac(merged_map, nodata_value=255)
    fracnosnow = generate_fracnosnow(merged_map, nodata_value=255)
    nunique = generate_nunique(merged_map, nodata_value=255)
    probmean = generate_probmean(merged_prob, merged_map, nodata_value=255)
    probmeannosnow = generate_probmeannosnow(merged_prob, merged_map, nodata_value=255)
    probstd = generate_probstd(merged_prob, merged_map, nodata_value=255)
    probstdnosnow = generate_probstdnosnow(merged_prob, merged_map, nodata_value=255)
