import numpy as np
from collections import namedtuple
from veg_workflows.biopar.biopar_config_reader import read_nnw_config, parse_nnw_config

import pkgutil

NeuralNetworkConfig = namedtuple(
    "NeuralNetworkConfig",
    [
        "normalization",
        "denormalization",
        "layer1_bias",
        "layer1_weights",
        "layer2_bias",
        "layer2_weights",
        "input_minmax",
        "output_minmax",
    ],
)


class BioParNNW:
    def __init__(self, version="3band", parameter="FAPAR", singleConfig=True):
        band_indices_array = [0, 1, 2]
        self.band_indices = np.ix_(band_indices_array)
        self.config = {}
        if singleConfig:
            from io import StringIO

            #             from biopar.nnw_config_reader import parse_nnw_config
            prefix = "SENTINEL2-R8"
            if "3band" == version:
                prefix = "SENTINEL2-R3"
            config = StringIO(
                pkgutil.get_data(
                    "evoland_lsc", f"resources/{prefix}-{parameter}.NNW"
                ).decode("utf-8")
            ).readlines()

            self.config["nnw"] = parse_nnw_config(config)

        config = self.config["nnw"]
        normalization = config.normalization
        xMin = normalization.transpose()[0]
        xMax = normalization.transpose()[1]
        self.normalization_offset = -2.0 * xMin / (xMax - xMin) - 1
        self.normalization_scale = 2.0 / (xMax - xMin)

        yMin = config.denormalization[0]
        yMax = config.denormalization[1]
        self.denormalization_scale = 0.5 * (yMax - yMin)
        self.denormalization_offset = 0.5 * (yMax - yMin) + yMin

        self.l1_weights = config.layer1_weights.transpose()
        self.l1_bias = config.layer1_bias
        self.l2_weights = config.layer2_weights.reshape((5, 1))
        self.l2_bias = config.layer2_bias

    # inputs shape: r,c,b
    def _compute_biopar(self, inputs, output_scale):
        config = self.config["nnw"]
        x_normalised = (inputs * self.normalization_scale) + self.normalization_offset

        layer_1 = np.tanh(np.matmul(x_normalised, self.l1_weights) + self.l1_bias)
        layer_2 = np.matmul(layer_1, self.l2_weights) + self.l2_bias

        result_float = np.float32(output_scale) * np.clip(
            (layer_2 * self.denormalization_scale) + self.denormalization_offset,
            config.output_minmax[1],
            config.output_minmax[2],
        )

        return result_float

    def run(
        self,
        input_bands,
        output_scale=200.0,
        nodata_val=255,
        output_dtype=np.uint8,
        minmax_flagging=False,
        scaled_max=None,
        offset=0.0,
    ):
        """
        :param input_bands: reflectance bands, floats in range [0.0,1.0]
        :param output_scale: scaling factor to apply to output
        :param output_dtype: expected datatype of the output
        :param minmax_flagging: check if the input and output values lie within the valid range specified by INRA. This is not enabled in Terrascope products.
        :param offset: offset to apply before scaling

        :return:
        """

        config = self.config["nnw"]
        normalization = config.normalization

        if input_bands.shape[0] != normalization.shape[0]:
            raise ValueError(
                "Expected number of input bands: "
                + str(normalization.shape[0])
                + " but received: "
                + str(input_bands.shape[1])
            )

        nb_reflectance = input_bands.shape[0] - 3
        # check 1: is input within min max (INRA)
        if minmax_flagging:
            invalid_inputs = np.any(
                input_bands[0:nb_reflectance, :] < config.input_minmax[0][:, None],
                axis=0,
            )
            invalid_inputs = invalid_inputs | np.any(
                input_bands[0:nb_reflectance, :] > config.input_minmax[1][:, None],
                axis=0,
            )
        # check 2: 'definition domain' not implemented because disabled in Sentinel-2

        invalid_bands = np.any(
            (input_bands[0:nb_reflectance, :] < 0)
            | (input_bands[0:nb_reflectance, :] > 1),
            axis=0,
        )
        # invalid_sza = np.rad2deg(np.arccos(input_bands[4])) > 70.

        image_tensor = self._compute_biopar(
            input_bands.transpose().astype(np.float32), np.float32(output_scale)
        )
        image_tensor = np.squeeze(image_tensor.transpose())

        if scaled_max is not None:
            # push output out_of_range to noData
            invalid_outputs = (
                image_tensor[:, 0] > scaled_max
            )  ## Config file for LAI is set to 14.xxx to avoid tensorflow to clip
            image_tensor = np.clip(image_tensor, 0.0, scaled_max)
        if np.issubdtype(output_dtype, np.floating):
            image = image_tensor.astype(output_dtype)
        else:
            image = np.round(image_tensor).astype(output_dtype)

        if np.issubdtype(output_dtype, np.floating):
            nodata_val = np.nan

        # HRVPP
        if (scaled_max is not None) and (not (output_dtype == np.uint8)):
            try:
                image[invalid_outputs] = nodata_val
                # image[invalid_sza] = nodata_val
            except:
                print("ERROR handling biopar nnet_out_of_range")

        image[invalid_bands] = nodata_val
        if minmax_flagging:
            image[image == output_scale * config.output_minmax[2]] = nodata_val
            image[invalid_inputs] = nodata_val

        return image
