import logging
from typing import Any
from typing import Callable

import click

from mrtools import datasets
from tools import leptons

log = logging.getLogger("mrtools.user")

DATASETS_DEF = "datasets/Met_NanoNtuple_v10_scratch.yaml"
HISTOS_DEF = "analysis02.yaml"

RDataFrame = Any
CallableDefineDF = Callable[
    [RDataFrame, str, datasets.DatasetType, str], dict[str, RDataFrame]
]


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
    loose: bool

    def __init__(self, loose: bool) -> None:
        self.loose = loose
        leptons.init()

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

        if self.loose:
            muon_select = leptons.MUON_SELECT_LOOSE_HYBRID_ISO
            elec_select = leptons.ELEC_SELECT_LOOSE_HYBRID_ISO
        else:
            muon_select = leptons.MUON_SELECT_HYBRID_ISO
            elec_select = leptons.ELEC_SELECT_HYBRID_ISO

        muon_attrs = leptons.MUON_ATTRS
        elec_attrs = leptons.ELEC_ATTRS
        lept_attrs = leptons.LEPT_ATTRS
        if dataset_type != datasets.DatasetType.DATA:
            muon_attrs += leptons.MC_ATTRS
            elec_attrs += leptons.MC_ATTRS
            lept_attrs += leptons.MC_ATTRS

        df = leptons.def_vector_obj(df, "GoodMuon", muon_select, "Muon", muon_attrs)
        df = leptons.def_vector_obj(df, "GoodElec", elec_select, "Electron", elec_attrs)

        df = leptons.def_combined_leptons(
            df, "GoodLept", "GoodMuon", "GoodElec", lept_attrs
        )

        return {"main": df}


@click.command
@click.option("--loose/--no-loose", help="Loose HybridIso lepton selection")
def get_analysis(loose: bool):
    return Analysis(loose)
