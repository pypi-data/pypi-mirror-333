import numpy as np
import xarray as xr
from pathlib import Path
from loguru import logger
from satio_pc.geotiff import (
    get_rasterio_profile_shape,
    write_geotiff_tags,
)

lsc_prob_mappping = {
    0: "woody_vegetation",
    1: "herbaceous_vegetation",
    2: "not_vegetated_land",
    3: "snow_ice",
    4: "water",
    5: "clouds_shadow",
    255: "no_data",
}
lsc_prob_mappping_inv = {v: k for k, v in lsc_prob_mappping.items()}

lsc_map_mapping = {
    0: "clouds",
    1: "woody_vegetation",
    2: "herbaceous_vegetation",
    3: "bare_soil",
    4: "snow",
    5: "water",
    255: "no_data",
}
lsc_map_mapping_inv = {v: k for k, v in lsc_map_mapping.items()}


def slash_tile(tile: str):
    if len(tile) != 5:
        raise ValueError(f"tile should be a str of len 5, not {tile}")

    return f"{tile[:2]}/{tile[2]}/{tile[3:]}"


def preprocess_path(path):
    """
    Preprocess the given path to modify its structure.

    Parameters:
    path (Path): The original path.

    Returns:
    Path: The modified path.
    """
    path_str = str(path)
    parts = path_str.split("/")
    # Remove the month part (second last element)
    new_parts = parts[:-3] + parts[-2:]
    path = Path("/".join(new_parts))
    # Replace "/blocks/" with "/stats/" in the path string
    path_str = str(path).replace("/blocks/", "/stats/")
    return Path(path_str)


def write_lsc_stats_geotiff(
    data,
    path,
    bounds,
    epsg,
    nodata=255,
    bands_names=None,
    colormap=None,
    tags=None,
    bands_tags=None,
    scales=None,
    offsets=None,
    overwrite=True,
    create_folder_structure=True,
):
    """
    Write the given data to a GeoTIFF file with the specified parameters.
    """
    profile = get_rasterio_profile_shape(
        data.shape, bounds=bounds, epsg=epsg, dtype=data.dtype
    )

    if create_folder_structure:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o775)

    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists")

    write_geotiff_tags(
        data,
        profile=profile,
        filename=path,
        nodata=nodata,
        bands_names=bands_names,
        colormap=colormap,
        tags=tags,
        bands_tags=bands_tags,
        scales=scales,
        offsets=offsets,
    )


def add_class_mapping(data, mapping):
    """
    Add the class mapping as an attribute to the given xarray DataArray.
    """
    wanted_classes = [
        name for name in mapping.values() if name not in ["clouds", "no_data"]
    ]

    data.attrs["class_mapping"] = {
        k: v for k, v in mapping.items() if v in wanted_classes
    }

    return data


def rename_bands(da, prefix):
    name_map = {
        "woody_vegetation": f"{prefix}_WOODY",
        "herbaceous_vegetation": f"{prefix}_HERB",
        "bare_soil": f"{prefix}_SOIL",
        "snow": f"{prefix}_SNOW",
        "water": f"{prefix}_WATER",
    }
    da = da.assign_coords(
        stat=[name_map[v] for v in da.attrs["class_mapping"].values()]
    )
    return da


def rename_nunique(da):
    da = da.assign_coords(stat=["NUNIQUEPCT"])
    return da


def generate_frac(
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    Generate the fractional cover data and save it as a GeoTIFF file.

    Parameters:
    map_data (xarray.DataArray): The map data.
    """
    if verbose:
        logger.info("Calculating frac statistics")

    # Mask out cloud pixels
    if nodata_value is not None:
        map_data = np.where(
            map_data != lsc_map_mapping_inv["clouds"], map_data, nodata_value
        )
    else:
        map_data = np.where(map_data != lsc_map_mapping_inv["clouds"], map_data, np.nan)
        # And replace any nodata_value with np.nan
        map_data = np.where(map_data != nodata_value, map_data, np.nan)

    # Determine the number of classes excluding 'clouds' and 'no_data'
    n_classes = len(list(lsc_map_mapping.keys())[1:-1])

    # Create an array of class values to calculate fractional cover
    frac_values = np.arange(1, n_classes + 1)

    # Initialize an array to hold fractional cover data
    frac_data = np.zeros(
        (n_classes, map_data.shape[1], map_data.shape[2]), dtype=np.uint8
    )

    # Calculate fractional cover for each class
    for i in frac_values:
        frac_data[i - 1] = (map_data == i).sum(axis=0) / (
            (map_data > 0) & (map_data < 100)
        ).sum(axis=0)

    # Convert the fractional cover data to an xarray DataArray
    frac_data = xr.DataArray(frac_data, dims=("stat", "y", "x"))

    # Add class mapping as an attribute to the DataArray
    frac_data = add_class_mapping(frac_data, lsc_map_mapping)

    # Rename the bands to match the naming convention
    frac_data = rename_bands(frac_data, "FRAC")

    if verbose:
        logger.info(f"Finished calculating frac values, shape: {frac_data.shape}")

    return frac_data


def generate_fracnosnow(
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    For this statistic, we want to calculate the fractions of each class
    but we don't want to consider any observation that was 'snow' when calculating the denominator
    """
    if verbose:
        logger.info("Calculating fracnosnow statistics")

    # Mask out cloud pixels
    if nodata_value is not None:
        map_data = np.where(
            map_data != lsc_map_mapping_inv["clouds"], map_data, nodata_value
        )
    else:
        map_data = np.where(map_data != lsc_map_mapping_inv["clouds"], map_data, np.nan)
        # And replace any nodata_value with np.nan
        map_data = np.where(map_data != nodata_value, map_data, np.nan)

    frac_woody = (map_data == lsc_map_mapping_inv["woody_vegetation"]).sum(axis=0) / (
        (map_data > 0) & (map_data < 100) & (map_data != lsc_map_mapping_inv["snow"])
    ).sum(axis=0)

    frac_herbaceous = (map_data == lsc_map_mapping_inv["herbaceous_vegetation"]).sum(
        axis=0
    ) / (
        (map_data > 0) & (map_data < 100) & (map_data != lsc_map_mapping_inv["snow"])
    ).sum(axis=0)

    frac_bare_soil = (map_data == lsc_map_mapping_inv["bare_soil"]).sum(axis=0) / (
        (map_data > 0) & (map_data < 100) & (map_data != lsc_map_mapping_inv["snow"])
    ).sum(axis=0)

    frac_snow = (map_data == lsc_map_mapping_inv["snow"]).sum(axis=0) / (
        (map_data > 0) & (map_data < 100)
    ).sum(axis=0)

    frac_water = (map_data == lsc_map_mapping_inv["water"]).sum(axis=0) / (
        (map_data > 0) & (map_data < 100) & (map_data != lsc_map_mapping_inv["snow"])
    ).sum(axis=0)

    # Convert the fractional cover data to a single xarray DataArray
    frac_data = xr.DataArray(
        np.stack(
            [
                frac_woody,
                frac_herbaceous,
                frac_bare_soil,
                frac_snow,
                frac_water,
            ]
        ),
        dims=("stat", "y", "x"),
    )

    # Add class mapping as an attribute to the DataArray
    frac_data = add_class_mapping(frac_data, lsc_map_mapping)

    # Rename the bands to match the naming convention
    frac_data = rename_bands(frac_data, "FRACNOSNOW")

    if verbose:
        logger.info(f"Finished calculating fracnosnow values, shape: {frac_data.shape}")

    return frac_data


def generate_probmean(
    prob_data,
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    Generate the mean probability data and save it as a GeoTIFF file.

    Parameters:
    prob_data (xarray.DataArray): The probability data.
    """
    if verbose:
        logger.info("Calculating mean probability")

    assert prob_data.ndim > map_data.ndim, (
        f"prob_data.ndim: {prob_data.ndim}, map_data.ndim: {map_data.ndim}. Check the order of the input arguments."
    )

    from warnings import simplefilter

    # Ignore runtime warnings
    simplefilter("ignore", category=RuntimeWarning)

    # Mask out cloud shadow pixels in the prob data using the map_data (labels)
    mask = map_data != lsc_map_mapping_inv["clouds"]
    mask = np.expand_dims(mask, axis=1)
    prob_data = np.where(mask, prob_data, np.nan)

    # Replace any nodata_value with np.nan
    if nodata_value is not None:
        prob_data = np.where(prob_data != nodata_value, prob_data, np.nan)

    # Calculate the mean probability across all months, ignoring NaNs
    prob_mean = np.nanmean(prob_data, axis=0)

    # Convert the mean probability data to an xarray DataArray
    prob_mean = xr.DataArray(prob_mean, dims=("stat", "y", "x"))

    # Exclude the 'no_data' class from the probability classes
    num_probs = len(lsc_prob_mappping) - 1  # Exclude 'no_data' class

    # Select the relevant probability classes (excluding 'no_data' and 'clouds')
    prob_mean = prob_mean.sel(stat=slice(0, num_probs - 1))

    # Add class mapping as an attribute to the DataArray
    prob_mean = add_class_mapping(prob_mean, lsc_map_mapping)

    # Rename the bands to match the naming convention
    prob_mean = rename_bands(prob_mean, "PROBMEAN")

    if verbose:
        logger.info(f"Finished calculating mean probability, shape: {prob_mean.shape}")

    return prob_mean


def generate_probmeannosnow(
    prob_data,
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    Generate the mean probability data and save it as a GeoTIFF file.

    Parameters:
    prob_data (xarray.DataArray): The probability data.
    """
    if verbose:
        logger.info("Calculating mean probability")

    from warnings import simplefilter

    # Ignore runtime warnings
    simplefilter("ignore", category=RuntimeWarning)

    mask = map_data != lsc_map_mapping_inv["clouds"]
    mask = np.expand_dims(mask, axis=1)
    prob_data = np.where(mask, prob_data, np.nan)

    # NOTE that the mean probability for the snow class is calculated separately here
    # Let's first calculate the mean probabilities for each class excluding 'clouds'
    prob_mean = np.nanmean(prob_data, axis=0)
    # Select the snow class
    prob_mean_snow = prob_mean[lsc_prob_mappping_inv["snow"]]

    mask = map_data != lsc_map_mapping_inv["snow"]
    mask = np.expand_dims(mask, axis=1)
    prob_data = np.where(mask, prob_data, np.nan)

    # Replace any nodata_value with np.nan
    if nodata_value is not None:
        prob_data = np.where(prob_data != nodata_value, prob_data, np.nan)

    # Calculate the mean probability across all months, ignoring NaNs
    prob_mean = np.nanmean(prob_data, axis=0)

    # Replace the mean probability for the snow class with the one we calculated earlier
    prob_mean[lsc_prob_mappping_inv["snow"]] = prob_mean_snow

    # Convert the mean probability data to an xarray DataArray
    prob_mean = xr.DataArray(prob_mean, dims=("stat", "y", "x"))

    # Determine the number of probability classes excluding 'no_data'
    num_probs = len(lsc_prob_mappping) - 1

    # Select the relevant probability classes (removes last class 'clouds')
    prob_mean = prob_mean.sel(stat=slice(0, num_probs - 1))

    # Add class mapping as an attribute to the DataArray
    prob_mean = add_class_mapping(prob_mean, lsc_map_mapping)

    # Rename the bands to match the naming convention
    prob_mean = rename_bands(prob_mean, "PROBMEANNOSNOW")

    if verbose:
        logger.info(f"Finished calculating mean probability, shape: {prob_mean.shape}")

    return prob_mean


# Let's make a probstd and probstdnosnow function that calculates the standard deviation of the probabilities
def generate_probstd(
    prob_data,
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    Generate the standard deviation of the probability data and save it as a GeoTIFF file.

    Parameters:
    prob_data (xarray.DataArray): The probability data.
    """
    if verbose:
        logger.info("Calculating standard deviation of probability")

    from warnings import simplefilter

    # Ignore runtime warnings
    simplefilter("ignore", category=RuntimeWarning)

    # Mask out cloud shadow pixels in the prob data using the map_data (labels)
    mask = map_data != lsc_map_mapping_inv["clouds"]
    mask = np.expand_dims(mask, axis=1)
    prob_data = np.where(mask, prob_data, np.nan)

    # Replace any nodata_value with np.nan
    if nodata_value is not None:
        prob_data = np.where(prob_data != nodata_value, prob_data, np.nan)

    # Calculate the standard deviation of the probability across all months, ignoring NaNs
    prob_std = np.nanstd(prob_data, axis=0)

    # Convert the standard deviation of the probability data to an xarray DataArray
    prob_std = xr.DataArray(prob_std, dims=("stat", "y", "x"))

    # Exclude the 'no_data' class from the probability classes
    num_probs = len(lsc_prob_mappping) - 1  # Exclude 'no_data' class

    # Select the relevant probability classes (excluding 'no_data' and 'clouds')
    prob_std = prob_std.sel(stat=slice(0, num_probs - 1))

    # Add class mapping as an attribute to the DataArray
    prob_std = add_class_mapping(prob_std, lsc_map_mapping)

    # Rename the bands to match the naming convention
    prob_std = rename_bands(prob_std, "PROBSTD")

    if verbose:
        logger.info(
            f"Finished calculating standard deviation of probability, shape: {prob_std.shape}"
        )

    return prob_std


def generate_probstdnosnow(
    prob_data,
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    Generate the standard deviation of the probability data and save it as a GeoTIFF file.

    Parameters:
    prob_data (xarray.DataArray): The probability data.
    """
    if verbose:
        logger.info("Calculating standard deviation of probability")

    from warnings import simplefilter

    # Ignore runtime warnings
    simplefilter("ignore", category=RuntimeWarning)

    mask = map_data != lsc_map_mapping_inv["clouds"]
    mask = np.expand_dims(mask, axis=1)
    prob_data = np.where(mask, prob_data, np.nan)

    mask = map_data != lsc_map_mapping_inv["snow"]
    mask = np.expand_dims(mask, axis=1)
    prob_data = np.where(mask, prob_data, np.nan)

    # Replace any nodata_value with np.nan
    if nodata_value is not None:
        prob_data = np.where(prob_data != nodata_value, prob_data, np.nan)

    # Calculate the standard deviation of the probability across all months, ignoring NaNs
    prob_std = np.nanstd(prob_data, axis=0)

    # Convert the standard deviation of the probability data to an xarray DataArray
    prob_std = xr.DataArray(prob_std, dims=("stat", "y", "x"))

    # Determine the number of probability classes excluding 'no_data'
    num_probs = len(lsc_prob_mappping) - 1

    # Select the relevant probability classes (removes last class 'clouds')
    prob_std = prob_std.sel(stat=slice(0, num_probs - 1))

    # Add class mapping as an attribute to the DataArray
    prob_std = add_class_mapping(prob_std, lsc_map_mapping)

    # Rename the bands to match the naming convention
    prob_std = rename_bands(prob_std, "PROBSTDNOSNOW")

    if verbose:
        logger.info(
            f"Finished calculating standard deviation of probability, shape: {prob_std.shape}"
        )

    return prob_std


def generate_nunique(
    map_data,
    nodata_value=255,
    verbose=False,
):
    """
    Generate the number of unique classes data and save it as a GeoTIFF file.

    Parameters:
    map_data (xarray.DataArray): The map data.
    """
    if verbose:
        logger.info("Calculating nunique statistics")

    available_months = np.sum(np.any(map_data != 255, axis=(1, 2)))
    assert 1 <= available_months <= 12, (
        f"available_months in nunique statistic: {available_months}"
    )

    # Mask out cloud pixels
    if nodata_value is not None:
        map_data = np.where(
            map_data != lsc_map_mapping_inv["clouds"], map_data, nodata_value
        )
    else:
        map_data = np.where(map_data != lsc_map_mapping_inv["clouds"], map_data, np.nan)
        # And replace any nodata_value with np.nan
        map_data = np.where(map_data != nodata_value, map_data, np.nan)

    # Get the dimensions of the map data
    _, height, width = map_data.shape

    # Initialize an array to hold the count of unique classes for each pixel
    class_counts = np.zeros((height, width), dtype=int)

    # Iterate over each pixel to count unique classes
    for i in range(height):
        for j in range(width):
            # Get the classes for the current pixel across all months
            pixel_classes = map_data[:, i, j]
            # Find the unique classes
            unique_classes = np.unique(pixel_classes)
            # Count the number of unique classes
            class_count = len(unique_classes)
            # Store the count in the class_counts array
            class_counts[i, j] = class_count

    # Convert the class_counts array to an xarray DataArray
    nunique_data = xr.DataArray(class_counts, dims=("y", "x"))
    # Normalize the unique class count by the number of months and scale to 0-100
    nunique_data = nunique_data / available_months

    # Add class mapping as an attribute to the DataArray
    nunique_data = add_class_mapping(nunique_data, lsc_map_mapping)

    # Rename the bands to match the naming convention
    nunique_data = rename_nunique(nunique_data.expand_dims("stat"))

    if verbose:
        logger.info(f"Finished calculating nunique values, shape: {nunique_data.shape}")

    return nunique_data
