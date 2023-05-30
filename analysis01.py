import logging
from typing import Any
from typing import Callable

import click

from mrtools import datasets

log = logging.getLogger("mrtools.user")

RDataFrame = Any
CallableDefineDF = Callable[
    [RDataFrame, str, datasets.DatasetType, str], dict[str, RDataFrame]
]

DATASETS_DEF = "datasets/Met_NanoNtuple_v10_scratch.yaml"

HISTOS_DEF = "analysis01.yaml"

# Event Selection

SELECTION = [
    "nISRJets>=1",
    "nGoodTaus==0",
    "Sum(lep_pt>20)<=1",
    "l1_pt>0",
    "dphij0j1<2.5",
    "nJetGood<=2",
    "met_pt>=200",
    "HT>=300",
]

WEIGHTS = [
    "reweightPU",
    "reweightBTag_SF",
    "reweightL1Prefire",
    "reweightwPt",
    "reweightLeptonSF",
]


def def_event_selection(df: RDataFrame, selection: list[str]) -> RDataFrame:
    log.debug('Filter("%s")', " && ".join(selection))
    return df.Filter(" && ".join(selection))


def def_weight(
    df: RDataFrame, name: str, dataset_type: datasets.DatasetType
) -> RDataFrame:
    if dataset_type == datasets.DatasetType.DATA:
        w = "1"
    else:
        w = "*".join(WEIGHTS)
    log.debug('Define("%s","%s")', name, w)
    df = df.Define(name, w)

    return df


class Analysis:
    def __init__(self) -> None:
        pass

    def __call__(
        self,
        df: RDataFrame,
        dataset_name: str,
        dataset_type: datasets.DatasetType,
        period: str,
    ) -> dict[str, RDataFrame]:
        log.debug("Dataset %s", dataset_name)
        df = def_event_selection(df, SELECTION)
        df = def_weight(df, "the_weight", dataset_type)

        return {"main": df}


@click.command
def get_analysis(**kwargs: dict[str, Any]) -> CallableDefineDF:
    return Analysis()
