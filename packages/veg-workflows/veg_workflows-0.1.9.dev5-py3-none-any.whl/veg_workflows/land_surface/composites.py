import numpy as np
import xarray as xr
from loguru import logger
import geopandas as gpd
from skimage.morphology import binary_dilation, binary_erosion, footprints
from tqdm import tqdm
from scipy.ndimage import gaussian_filter

compositing_settings = {
    "max_cloud_cover": 90,
    "composite": {"freq": 40, "window": 40, "mode": "median"},
    "mask": {
        "erode_r": 3,  # 3, #NOTE
        "dilate_r": 7,  # 13, #NOTE
        "snow_dilate_r": 3,
        "max_invalid_ratio": 1,
        "max_invalid_snow_cover": 0.9,
    },
    "scl_valid_th": 0.1,
    "s2bands": [
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B8A",
        "B09",
        "B11",
        "B12",
    ],
    "indices": ["ndvi"],
    "percentiles": [10, 25, 50, 75, 90],
    "loi_blur_sigma": 8,
    "snow_invalid_blur_sigma": 8,
    "max_products": 150,
    "nodata_value": 32767,
}


class LandSurfaceFeatures:
    def __init__(self, settings):
        self.settings = settings
        assert "s2bands" in settings, "s2bands must be defined in settings"
        self.s2bands = settings["s2bands"]
        self.SCL_ORIGINAL_CATEGORIES = {
            "no_data": 0,
            "saturated_defective": 1,
            "dark_area_pixels": 2,
            "cloud_shadows": 3,
            "vegetation": 4,
            "bare_soils": 5,
            "water": 6,
            "clouds_low_probability": 7,
            "clouds_medium_probability": 8,
            "clouds_high_probability": 9,
            "cirrus": 10,
            "snow": 11,
        }
        self.CCL_CATEGORIES = {
            "surface": 0,
            "snow": 1,
            "invalid": 2,
            "nodata": 3,
        }
        self.SCL_CATEGORIES = {
            "surface": 0,
            "snow": 1,
            "invalid": 2,
            "nodata": 3,
        }

    def prep_band_single_observation(self, darr, band, scl, ccl, nodata_value):
        darr_band = darr.sel(band=band).squeeze("time")
        assert darr_band.ndim == 2, (
            f"Expected 2 dimensions (y, x), but got {darr_band.ndim} dimensions"
        )
        scl = scl.squeeze("time")
        assert scl.ndim == 2, (
            f"Expected 2 dimensions (y, x), but got {scl.ndim} dimensions"
        )

        darr_band = darr_band.where(scl.data != 0, 0)
        darr_band = darr_band.astype("float32")
        darr_band = darr_band.where(darr_band != 0, np.nan).data.squeeze()

        darr_band[ccl.squeeze() > 1] = nodata_value
        darr_band[np.isnan(darr_band)] = nodata_value
        darr_band = darr_band.astype(np.uint16)

        # put the composite array in
        darr_band = xr.DataArray(darr_band, dims=["y", "x"]).expand_dims(
            dim="band", axis=0
        )

        return darr_band

    def generate_band_composite(
        self, darr, band, scl_raw, ccl, group_masks, nodata_value
    ):
        """
        Generate a composite image for the specified band using the given parameters.
        """
        darr_band = darr.sel(band=band)
        darr_band = darr_band.squeeze().where(scl_raw.data != 0, 0)
        darr_band = darr_band.astype("float32")
        darr_band = darr_band.where(darr_band != 0, np.nan)
        arr_ccl = np.squeeze(ccl.data)

        composite_surface = self.group_median(darr_band, group_masks["surface"])
        composite_surface[arr_ccl != 0] = np.nan

        composite_snow = self.group_median(darr_band, group_masks["snow"])
        composite_snow[arr_ccl != 1] = np.nan

        composite = np.nansum([composite_surface, composite_snow], axis=0)
        composite[arr_ccl > 1] = nodata_value
        composite[np.isnan(composite)] = nodata_value
        composite = composite.astype(np.uint16)

        # put the composite array into the darr
        composite = xr.DataArray(composite, dims=["y", "x"]).expand_dims(
            dim="band", axis=0
        )

        return composite

    def generate_empty_composite(self, darr_month):
        """
        Generate an empty composite for the given DataArray.
        """
        darr_composite = xr.concat(
            [
                xr.DataArray(
                    np.ones((1, darr_month.y.size, darr_month.x.size))
                    * compositing_settings["nodata_value"],
                    dims=["band", "y", "x"],
                )
                for band in self.s2bands
            ],
            dim="band",
        )
        darr_composite = darr_composite.assign_coords(band=self.s2bands)
        ccl = xr.DataArray(
            np.ones((darr_month.y.size, darr_month.x.size))
            * self.CCL_CATEGORIES["nodata"],
            dims=["y", "x"],
        )
        ccl = ccl.expand_dims(band=["CCL"])
        ccl = ccl.assign_coords(band=["CCL"])
        ccl = ccl.astype(np.uint16)

        darr_composite = xr.concat([darr_composite, ccl], dim="band")
        darr_composite = darr_composite.assign_coords(band=self.s2bands + ["CCL"])
        darr_composite.data = darr_composite.data.astype(np.uint16)
        return darr_composite

    def group_median(self, darr_band, group_mask):
        """
        Compute the median of the data array band within the specified group mask.
        """
        arr_band = np.squeeze(darr_band.data.copy())
        arr_band[~group_mask.data] = np.nan
        # Let's filter out warnings for nanmedian
        from warnings import simplefilter

        simplefilter(action="ignore", category=RuntimeWarning)
        return np.nanmedian(arr_band, axis=0)

    def filter_valid_times(self, darr, month, verbose=False):
        """
        Filter out times with no valid SCL data.
        """
        assert "SCL" in darr.band.values, "SCL band not found in darr_month"
        scl = darr.sel(band="SCL")
        nodata_mask = scl == 0
        valid_times = ~np.all(nodata_mask, axis=(1, 2))
        valid_inds = np.where(valid_times)[0]
        if verbose:
            logger.info(f"Found {len(valid_inds)} valid times for month {month}")

        darr = darr.isel(time=valid_inds)
        scl = scl.isel(time=valid_inds)

        return darr, scl

    def generate_masks_for_scl(self, scl, categories):
        """
        Generate masks for surface, snow, and invalid categories based on the original SCL categories.
        """
        surface_mask = np.isin(
            scl,
            [
                categories["vegetation"],
                categories["bare_soils"],
                categories["water"],
            ],
        )
        snow_mask = scl == categories["snow"]
        invalid_mask = np.isin(
            scl,
            [
                categories["saturated_defective"],
                categories["dark_area_pixels"],
                categories["cloud_shadows"],
                categories["clouds_low_probability"],
                categories["clouds_medium_probability"],
                categories["clouds_high_probability"],
                categories["cirrus"],
            ],
        )

        return surface_mask, snow_mask, invalid_mask

    def process_scl_layer(self, scl):
        """
        Process the SCL layer to group categories into surface, snow, and invalid.
        """
        # Initialize an array with three layers (channels)
        # to store masks for surface, snow, and invalid categories
        scl_grouped = np.zeros([3] + list(scl.shape))

        surface_mask, snow_mask, invalid_mask = self.generate_masks_for_scl(
            scl, self.SCL_ORIGINAL_CATEGORIES
        )

        scl_grouped[0, surface_mask] = 1
        scl_grouped[1, snow_mask] = 1
        scl_grouped[2, invalid_mask] = 1

        d = footprints.disk(compositing_settings["mask"]["snow_dilate_r"])
        scl_grouped[1, ...] = np.stack([binary_dilation(m, d) for m in snow_mask])

        scl_cloud_mask = np.isin(
            scl,
            [
                self.SCL_ORIGINAL_CATEGORIES["cloud_shadows"],
                self.SCL_ORIGINAL_CATEGORIES["clouds_medium_probability"],
                self.SCL_ORIGINAL_CATEGORIES["clouds_high_probability"],
                self.SCL_ORIGINAL_CATEGORIES["cirrus"],
            ],
        )
        erode_r = compositing_settings["mask"]["erode_r"]
        dilate_r = compositing_settings["mask"]["dilate_r"]

        if erode_r is not None and erode_r > 0:
            e = footprints.disk(erode_r)
            scl_cloud_mask = np.stack([binary_erosion(m, e) for m in scl_cloud_mask])

        if dilate_r is not None and dilate_r > 0:
            d = footprints.disk(dilate_r)
            scl_cloud_mask = np.stack([binary_dilation(m, d) for m in scl_cloud_mask])

        scl_grouped[1, snow_mask] = 1
        scl_grouped[2, scl_cloud_mask] = 1

        blurred_scl = np.array(
            [
                [
                    (
                        gaussian_filter(
                            scl_grouped[i, j, ...].astype(np.float32),
                            sigma=compositing_settings["snow_invalid_blur_sigma"],
                        )
                        > 0.5
                    )
                    for j in range(scl_grouped.shape[1])
                ]
                for i in range(scl_grouped.shape[0])
            ]
        )

        blurred_scl10 = np.argmax(blurred_scl, axis=0)
        blurred_scl10[scl == 0] = 3
        blurred_scl10 = np.expand_dims(blurred_scl10, axis=1)
        blurred_scl10 = xr.DataArray(blurred_scl10, dims=["time", "band", "y", "x"])
        blurred_scl10 = blurred_scl10.isel(band=0)

        return blurred_scl10

    def build_classification_groups(self, blurred_scl):
        """
        Create classification groups based on the blurred SCL layer.
        """
        # Calculate total valid times and snow times
        total_valid_times = (blurred_scl < self.SCL_CATEGORIES["invalid"]).sum(
            dim="time"
        )
        total_snow_times = (blurred_scl == self.SCL_CATEGORIES["snow"]).sum(dim="time")
        # Calculate snow frequency and create snow mask
        snow_freq = total_snow_times / total_valid_times.where(total_valid_times > 0)
        snow_mask = snow_freq > 0.5
        snow_mask = snow_mask.expand_dims(time=blurred_scl.time.size).transpose(
            "time", "y", "x"
        )

        # Initialize group masks
        group_snow = snow_mask.copy()
        processed_pixels = group_snow.any(dim="time")

        group_masks = {
            "snow": (blurred_scl == 1) & group_snow,
            "surface": (blurred_scl == self.SCL_CATEGORIES["surface"])
            & ~processed_pixels,
            "invalid": (blurred_scl == self.SCL_CATEGORIES["invalid"])
            & ~processed_pixels,
        }

        # Update processed pixels for each group
        for group_name in ["surface", "invalid"]:
            processed_pixels |= group_masks[group_name].any(dim="time")

        # Create the rest group
        group_rest = ~processed_pixels
        group_rest = group_rest.expand_dims(time=blurred_scl.time.size).transpose(
            "time", "y", "x"
        )
        group_masks["rest"] = group_rest

        # Check for presence of snow, invalid, and surface in any time step
        has_snow = group_masks["snow"].any(dim="time").data
        has_invalid = group_masks["invalid"].any(dim="time").data
        has_surface = group_masks["surface"].any(dim="time").data

        # Initialize CCL with no data value
        ccl = (
            group_masks["rest"].any(dim="time").data.copy()
            * self.CCL_CATEGORIES["nodata"]
        )

        # Assign values to CCL based on masks
        ccl[has_invalid] = self.CCL_CATEGORIES["invalid"]
        ccl[has_surface] = self.CCL_CATEGORIES["surface"]
        ccl[has_snow] = self.CCL_CATEGORIES["snow"]

        # Convert CCL to DataArray
        ccl = xr.DataArray(ccl.squeeze(), dims=["y", "x"])
        ccl = ccl.expand_dims(band=["CCL"])
        ccl = ccl.assign_coords(band=["CCL"])
        ccl = ccl.astype(np.uint16)

        # Ensure all CCL values are within the expected range
        assert np.all(np.isin(ccl, list(self.CCL_CATEGORIES.values()))), (
            "CCL values are not in range [0, 1, 2] or nodata_value"
        )

        return group_masks, ccl

    def _prepare_single_product(self, darr, band, scl, ccl, compositing_settings):
        """
        Prepare the composite for a single product.
        """
        logger.info("Single product found, preparing bands directly")
        darr = darr.sel(band=self.s2bands)
        # For each of the bands, let's apply the prep_band function
        darr_composite = xr.concat(
            [
                self.prep_band_single_observation(
                    darr,
                    band,
                    scl,
                    ccl,
                    compositing_settings["nodata_value"],
                )
                for band in self.s2bands
            ],
            dim="band",
        )
        darr_composite = self._finalize_composite(darr_composite, ccl)

        return darr_composite

    def _prepare_multi_product(
        self, darr, band, scl, ccl, group_masks, compositing_settings
    ):
        """
        Prepare the composite for multiple products.
        """
        darr_composite = xr.concat(
            [
                self.generate_band_composite(
                    darr,
                    band,
                    scl,
                    ccl,
                    group_masks,
                    compositing_settings["nodata_value"],
                )
                for band in self.s2bands
            ],
            dim="band",
        )
        darr_composite = self._finalize_composite(darr_composite, ccl)

        return darr_composite

    def _finalize_composite(self, darr_composite, ccl):
        """
        Finalize the composite by adding the CCL band and setting the data type.
        """
        darr_composite = darr_composite.assign_coords(band=self.s2bands)
        darr_composite = xr.concat([darr_composite, ccl], dim="band")
        darr_composite = darr_composite.assign_coords(band=self.s2bands + ["CCL"])
        darr_composite.data = darr_composite.data.astype(np.uint16)
        return darr_composite

    def get_composite(self, ts, month):
        """
        Get the composite for the specified month.
        """
        darr_month = ts.sel(
            time=(ts.time.dt.month == month) & (ts.time.dt.year == 2020)
        ).copy()

        # First check if the DataArray is empty
        if darr_month.time.size == 0:
            return self.generate_empty_composite(darr_month)

        # Filter out times with no valid SCL data
        darr_month, scl10_raw = self.filter_valid_times(darr_month, month)

        # Check if the DataArray is empty after filtering
        if darr_month.time.size == 0:
            return self.generate_empty_composite(darr_month)

        # Process the SCL layer
        blurred_scl10 = self.process_scl_layer(scl10_raw)

        # Create classification groups
        group_masks, ccl = self.build_classification_groups(blurred_scl10)

        # The below 2 lines of code are not needed because
        # this is planetary computer data
        # (older i.e. don't require offset correction)
        ## from satio_pc.extension import SatioTimeSeries
        ## darr_month.satio.harmonize()

        if darr_month.time.size == 1:
            darr_composite = self._prepare_single_product(
                darr_month, self.s2bands, scl10_raw, ccl, compositing_settings
            )
        else:
            darr_composite = self._prepare_multi_product(
                darr_month,
                self.s2bands,
                scl10_raw,
                ccl,
                group_masks,
                compositing_settings,
            )
        return darr_composite

    def process_timeseries(self, ts):
        """
        Process the timeseries to generate composites. The timeseries should have the following dimensions:
        (time: N, band: 13, y: 128, x: 128) where N is the number of observations in a year.
        """
        list_composites = []
        for month in tqdm(range(1, 13), desc="Generating monthly composites"):
            list_composites.append(self.get_composite(ts, month))

        ts_composites = xr.concat(list_composites, dim="time")

        return ts_composites


if __name__ == "__main__":
    from evotrain.v2ts import EvoTrainV2TSDataset
    from evotrain.v2 import EvoTrainV2Dataset
    from veg_workflows.paths.datasets import EVOTRAIN

    evo_dataset = EvoTrainV2Dataset()
    evots_dataset = EvoTrainV2TSDataset()

    locs = gpd.read_file(EVOTRAIN)

    evo_dataset._locs = evots_dataset._locs = locs

    loc = locs.sample(1).iloc[0]
    loc_id = loc.location_id

    # loc = locs.iloc[608]
    # loc_id = "56HKH_072_16" # gave error on build_classification_groups; fixed

    print(f"Processing location: {loc_id}")

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
    print(ts_composites.shape)
