import numpy as np
from collections import namedtuple

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


def read_nnw_config(
    f_nnw=r"L:\TEMP\Erwin\Terrascope\biopars\SENTINEL2-R8-LAI_withSNAP.NNW",
):
    with open(f_nnw) as f:
        d_nnw = f.readlines()
        return parse_nnw_config(d_nnw)


def parse_nnw_config(nnw_config):
    norm = np.array([])

    bias = np.array([])
    weights = np.array([])

    def getValuesFromLine(line, delimiter):
        line = line.rstrip("\n").rstrip("\r")
        begin_pos = line.find(delimiter)
        temp = list(map(float, line[begin_pos + 1 :].split(",")))

        return temp

    # read lines 32 - 37 for the biases and weights
    # normalization in line 25 - 26, denormalization in line 28 - 29
    d_norm = nnw_config[24:26]
    d_denorm = nnw_config[27:29]
    d_bias_weights = nnw_config[31:37]

    for wline in d_bias_weights:
        lst_el = getValuesFromLine(wline, ":")
        flt_lst_el = lst_el
        bias = np.append(bias, flt_lst_el[0])
        weights = np.append(weights, flt_lst_el[1 : np.size(flt_lst_el)])

    for line in d_norm:
        temp = getValuesFromLine(line, ":")
        norm = np.append(norm, temp)

    denormalization = np.asarray(
        [getValuesFromLine(d_denorm[0], ":"), getValuesFromLine(d_denorm[1], ":")]
    ).flatten()

    mindomain = getValuesFromLine(nnw_config[39], ":")
    maxdomain = getValuesFromLine(nnw_config[40], ":")

    number_of_layer1_weights = len(weights) - 5
    parsed_config = NeuralNetworkConfig(
        normalization=norm.reshape((2, -1)).T,
        denormalization=denormalization,
        layer1_weights=weights[0:number_of_layer1_weights].reshape((5, -1)),
        layer1_bias=bias[0:5],
        layer2_weights=weights[number_of_layer1_weights : np.size(weights)],
        layer2_bias=bias[5:6],
        input_minmax=np.asarray([mindomain, maxdomain]),
        output_minmax=np.insert(denormalization, 0, np.nan),
    )
    return parsed_config
