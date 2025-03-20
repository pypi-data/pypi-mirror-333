"""
Cloud mask inference pipeline for LOI-60 products.
Contact: YK
"""

# import getpass
from pathlib import Path
import numpy as np

# import torch
from loguru import logger
from typing import Tuple, Dict, Any, Optional

from evotrain.models.loi.infer import get_feats_head, load_model_files
from evotrain.models.loi.data.bands import build_bands_data_array, get_filenames_dict
from evotrain.models.loi.data.preprocessing import scale_s2_l2a_bands
from evotrain.models.loi.io import save_geotiff
from veg_workflows.paths.models import CLOUDSEN_MODELS_60M
from veg_workflows.products import Loi10Product
from veg_workflows.collections import veg_collections


class CloudInferencePipeline:
    def __init__(
        self,
        model_name: str,
        model_idx: int = -1,
        version: str = "v999",
        export_products: bool = False,
    ):
        """Initialize the cloud inference model.

        Args:
            model_name: Name of the model to use
            model_idx: Model index to use
            version: Version string
            export_products: Whether to export GeoTIFF products
        """
        if not model_name:
            raise ValueError("model_name cannot be empty")
        if model_idx < -1:
            raise ValueError("model_idx must be >= -1")

        self.model_name = model_name
        self.model_idx = model_idx
        self.version = version
        # Note that this is like a "global" settings for the pipeline
        # but it can be overridden in the run_inference method if needed
        self.export_products = export_products

        # # Set torch hub directory
        # username = getpass.getuser()
        # torch.hub.set_dir(f"/data/users/Public/{username}/share/.torchhub_cache")

        # Load model
        self.model_path = f"{CLOUDSEN_MODELS_60M}/{model_name}/version_0/"
        self.model, self.class_mapping, self.model_config = load_model_files(
            self.model_path, idx=model_idx, load_last=False
        )
        logger.info("Model initialized successfully")

    def get_input(
        self, product_id: str, collection_name: str
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Get and prepare input data from a product ID.

        Args:
            product_id: Sentinel-2 product ID
            collection_name: Name of the collection

        Returns:
            Tuple containing the input array and metadata
        """
        logger.info(f"Processing product: {product_id}")

        # Prepare product
        loi10prod, product_collection, epsg, bounds, date = (
            prepare_loi_product_for_inference(product_id, collection_name, self.version)
        )

        # Get bands data
        bands_list = self.model_config["bands_config"]["s2_bands"]
        bands_list = [
            band[4:] if band.startswith("l2a-") else band for band in bands_list
        ]
        filenames_dict = get_filenames_dict(product_collection, bands_list)
        darr_og = build_bands_data_array(
            filenames_dict,
            bands_list,
            source_resolution=60,
            target_resolution=60,
        )

        # Get SCL band
        filenames_dict = get_filenames_dict(
            product_collection, ["SCL"], source_resolution=60
        )
        scl_array = (
            build_bands_data_array(
                filenames_dict,
                bands_list=["SCL"],
                source_resolution=60,
                target_resolution=60,
            )
            .sel(band="SCL")
            .values
        )

        metadata = {
            "loi10prod": loi10prod,
            "epsg": epsg,
            "bounds": bounds,
            "date": date,
            "bands": bands_list,
            "scl_array": scl_array,
        }

        self.current_metadata = metadata

        return darr_og, metadata

    def preprocess(self, input_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess the input data.

        Args:
            input_array: Raw input array
        Returns:
            Tuple of preprocessed data and features
        """
        if not hasattr(self, "current_metadata"):
            raise RuntimeError("get_input must be called before preprocess")

        # Apply SCL mask
        scl_array = self.current_metadata["scl_array"]
        input_array = input_array.where(scl_array != 0, np.nan)
        if np.isnan(input_array).any(axis=0).data.any():
            logger.debug("Block has NaNs")
            input_array = input_array.fillna(0)

        # Scale data
        scaled_data = scale_s2_l2a_bands(
            input_array.data,
            scaling_factor=10_000,
            apply_logistic=True,
            k_factor=self.model_config["scaling_config"]["k_factor"],
            apply_jitter=False,
            k_factor_jitter=0,
        )

        # Generate additional features
        feats_head = get_feats_head(
            scaled_data.shape,
            self.current_metadata["epsg"],
            self.current_metadata["bounds"],
            self.current_metadata["date"],
            self.model_config,
        )

        return scaled_data, feats_head

    def run_inference(
        self,
        preprocessed_data: np.ndarray,
        feats_head: np.ndarray,
        export: bool = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Run model inference on preprocessed data.

        Args:
            preprocessed_data: Preprocessed input data
            feats_head: Additional features
            export: Whether to export the results

        Returns:
            Tuple of probability outputs and class outputs (argmax)
        """
        should_export = export if export is not None else self.export_products

        logger.info("Starting model inference")
        model_output = self.model.predict(preprocessed_data, feats_head)
        out = model_output.squeeze()

        # Get argmax output
        out_argmax = np.argmax(out.copy(), axis=0).astype(np.float32)

        # Apply masks
        scl_array = self.current_metadata["scl_array"]
        mask_scl_invalid = np.where(scl_array == 0)
        out[:, mask_scl_invalid[0], mask_scl_invalid[1]] = np.nan

        # Process outputs
        mask_out_invalid = np.isnan(out)
        nodata_value = 255
        out = np.round(out * 250).astype(np.uint8)
        out[mask_out_invalid] = nodata_value
        out_argmax[mask_scl_invalid] = nodata_value

        if should_export:
            self.export_results(out, out_argmax, nodata_value)
            logger.success("Results exported successfully")

        logger.success("Model inference completed successfully")

        return out, out_argmax

    def export_results(
        self,
        prob_output: np.ndarray,
        class_output: np.ndarray,
        nodata_value: int,
        prob_path: Optional[Path] = None,
        mask_path: Optional[Path] = None,
    ):
        """Export results to GeoTIFF files.

        Args:
            prob_output: Probability outputs to save
            class_output: Class outputs to save
            nodata_value: Value to use for no data
            prob_path: Optional custom path for probability file
            mask_path: Optional custom path for mask file
        """
        if not self.model_config["data_config"]["classify_snow"]:
            raise NotImplementedError("Only snow classification is supported for now")

        bands_names = [
            f"PROB_{k}"
            for k in self.model_config["labels_config"][
                "cloudsen12_mergedclouds_extrasnow"
            ].keys()
        ]
        tags = {
            "bands_names": bands_names,
            "legend": "0 Surface \n 1 Clouds \n2 Shadows \n3 Snow \n255 No data",
        }

        # Use custom path if provided, otherwise use default from loi10prod
        save_path_probs = prob_path or self.current_metadata["loi10prod"].path("probs")
        save_path_mask = mask_path or self.current_metadata["loi10prod"].path("mask")

        # Save probability output
        save_geotiff(
            prob_output,
            self.current_metadata["bounds"],
            self.current_metadata["epsg"],
            save_path_probs,  # Use the chosen path
            scales=[1 / 250] * prob_output.shape[0],
            nodata_value=nodata_value,
            bands_names=bands_names,
            tags=tags,
        )

        # Save class output
        save_geotiff(
            class_output.astype(np.uint8),
            self.current_metadata["bounds"],
            self.current_metadata["epsg"],
            save_path_mask,  # Use the chosen path
            nodata_value=nodata_value,
            bands_names=["CLASS"],
            tags={"band_names": ["CLASS"], "legend": tags["legend"]},
        )

    def process(
        self, product_id: str, collection_name: str, export: bool = False
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Process a product end-to-end in one call."""
        input_array, _ = self.get_input(product_id, collection_name)
        preprocessed_data, feats_head = self.preprocess(input_array)
        return self.run_inference(preprocessed_data, feats_head, export)


def prepare_loi_product_for_inference(
    s2_product_id: str, collection_name: str, version: str
) -> Tuple[Loi10Product, object, int, tuple, str]:
    """
    Prepare LOI product by loading its information and creating necessary directories.

    Args:
        s2_product_id (str): Sentinel-2 product ID.
        collection_name (str): Name of the collection from veg_collections (e.g. "lcfm_1percent", "lcfm_10percent").
        version (str): Version of the product (e.g. "v999").

    Returns:
        Tuple[Loi10Product, object, int, tuple, str]: A tuple containing the LOI product, product collection, EPSG code, bounds, and date.
    """
    logger.success("Preparing LOI product")

    # Create the LOI-10 product
    loi10prod = create_loi10_product(
        s2_product_id,
        "LCFM",
        version,
        Path("/vitodata/vegteam_vol2/products/"),
        "LOI-10",
    )

    # Load the collection and s2grid
    veg_collection, s2grid = get_collection_and_s2grid(collection_name)

    # Filter the product collection
    product_collection = filter_product_collection(
        veg_collection, s2grid, s2_product_id
    )

    # Extract product information
    bounds, date, epsg, product_tile = extract_product_info(product_collection, s2grid)

    return loi10prod, product_collection, epsg, bounds, date


def create_loi10_product(
    s2_product_id: str,
    project_name: str,
    version: str,
    products_base_path: Path,
    product_name: str,
) -> Loi10Product:
    """
    Create a Loi10Product object and the necessary directories.

    Args:
        s2_product_id (str): Sentinel-2 product ID.
        project_name (str): Name of the project.
        version (str): Version of the product.
        products_base_path (Path): Base path for the products.
        product_name (str): Name of the product.

    Returns:
        Loi10Product: A Loi10Product object.
    """
    loi10prod = Loi10Product(
        s2_product_id=s2_product_id,
        project_name=project_name,
        version=version,
        products_base_path=str(products_base_path),
        product_name=product_name,
    )
    # Create the necessary directories (parent directory of the "probs" directory)
    layer = "probs"
    logger.info(f"Creating necessary directories for: {loi10prod.path(layer)}")
    loi10prod.path(layer).parent.mkdir(parents=True, exist_ok=True, mode=0o775)
    logger.info(f"LOI product created successfully. Path: {loi10prod.path(layer)}")
    return loi10prod


def extract_product_info(
    product_collection: object, s2grid: object
) -> Tuple[int, tuple, str]:
    """
    Extract the EPSG code, bounds, and date from the product collection.

    Args:
        product_collection (object): Product collection object from veg_collections.
        s2grid (object): S2Grid object from veg_collections.

    Returns:
        Tuple[int, tuple, str]: A tuple containing the EPSG code, bounds, and date.
    """
    product_tile = product_collection.df.tile.unique()[0]
    epsg = s2grid[s2grid.tile == product_tile].epsg.values[0]
    # Note: .bounds != ["bounds"]
    bounds = s2grid[s2grid.tile == product_tile]["bounds"].values[0]
    date = product_collection.df.date.values[0]
    logger.info(
        f"Product information extracted successfully: EPSG={epsg}, bounds={bounds}, date={date}, tile={product_tile}"
    )
    return bounds, date, epsg, product_tile


def filter_product_collection(
    veg_collection: object, s2grid: object, s2_product_id: str
) -> object:
    """
    Filter the product collection based on the Sentinel-2 product ID.

    Args:
        veg_collection (object): Collection object from veg_collections.
        s2grid (object): S2Grid object from veg_collections.
        s2_product_id (str): Sentinel-2 product ID.

    Returns:
        object: Filtered product collection object.
    """
    product_collection = veg_collection.__class__(
        veg_collection.df[veg_collection.df.product_id == s2_product_id],
        s2grid,
    )
    assert len(product_collection.df), f"No products found for {s2_product_id}"
    return product_collection


def get_collection_and_s2grid(collection_name: str) -> Tuple[object, object]:
    """
    Load the collection and s2grid from the veg_collections module.

    Args:
        collection_name (str): Name of the collection from veg_collections (e.g. "lcfm_1percent", "lcfm_10percent").

    Returns:
        Tuple[object, object]: A tuple containing the collection and s2grid objects.
    """
    collection = getattr(veg_collections, collection_name)
    s2grid = veg_collections.s2grid
    logger.info("Collection and S2 grid loaded successfully")
    return collection, s2grid


if __name__ == "__main__":
    # Initialize the pipeline
    cloud_inferencer = CloudInferencePipeline(
        model_name="2501241011_v8aa",
        model_idx=2,
        version="v999",
        export_products=False,  # Set to True if you want to save GeoTIFF outputs
    )

    # Get input data
    input_array, metadata = cloud_inferencer.get_input(
        product_id="S2A_MSIL2A_20200612T023601_N0500_R089_T50NKJ_20230327T190018",
        collection_name="lcfm_10percent",
    )
    # Preprocess input data
    prepared_input_array, feats_head = cloud_inferencer.preprocess(input_array)

    # Run inference
    prob_output, class_output = cloud_inferencer.run_inference(
        prepared_input_array, feats_head, export=True
    )
