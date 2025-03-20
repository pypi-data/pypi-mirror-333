from pathlib import Path

import pandas as pd
import satio
from satio.collections import L2ACollection

from veg_workflows.paths.collections import (
    LCFM_1PERCENT_SATIO,
    LCFM_10PERCENT_SATIO,
    SEN4LDN_SATIO,
)


def extend_path_terrascope(path):
    path = Path(path)
    path = path / f"{path.name}.SAFE"
    return str(path)


def get_terrascope_l2a_satio_collection(collection_path, s2grid=None):
    if s2grid is None:
        s2grid = satio.layers.load("s2grid")

    coll = L2ACollection.from_path(collection_path, s2grid=s2grid)
    coll.df["path"] = coll.df.path.apply(extend_path_terrascope)
    coll.df.date = pd.to_datetime(
        coll.df["product_id"].str.split("_").str[2], format="%Y%m%dT%H%M%S"
    )

    return coll


def get_lcfm_10percent_satio_collection(s2grid=None):
    return get_terrascope_l2a_satio_collection(LCFM_10PERCENT_SATIO, s2grid=s2grid)


def get_lcfm_1percent_satio_collection(s2grid=None):
    return get_terrascope_l2a_satio_collection(LCFM_1PERCENT_SATIO, s2grid=s2grid)


def get_sen4ldn_satio_collection(s2grid=None):
    return get_terrascope_l2a_satio_collection(SEN4LDN_SATIO, s2grid=s2grid)


class VegSatioCollections:
    def __init__(self, s2grid=None) -> None:
        self._lcfm_10percent = None
        self._lcfm_1percent = None
        self._sen4ldn = None
        self.s2grid = s2grid or satio.layers.load("s2grid")

    @property
    def lcfm_10percent(self):
        if self._lcfm_10percent is None:
            self._lcfm_10percent = get_lcfm_10percent_satio_collection(self.s2grid)
        return self._lcfm_10percent

    @property
    def lcfm_1percent(self):
        if self._lcfm_1percent is None:
            self._lcfm_1percent = get_lcfm_1percent_satio_collection(self.s2grid)
        return self._lcfm_1percent

    @property
    def sen4ldn(self):
        if self._sen4ldn is None:
            self._sen4ldn = get_sen4ldn_satio_collection(self.s2grid)
        return self._sen4ldn


veg_collections = VegSatioCollections()
