"""Lepton selection for StopsCompressed.

Implementation for RDataFrame.

ElectronID from https://github.com/1LStopBudapest/Helper/blob/master/ANEle.py

Example:
    from tools import leptons

    if is_mc:
        elec_attrs = leptons.ELEC_ATTRS + leptons.MC_ATTRS
        lowpt_elec_attrs = leptons.LOWPT_ELEC_ATTRS + leptons.MC_ATTRS
        comb_elec_attrs = leptons.COMB_ELEC_ATTRS + leptons.MC_ATTRS
    else:
        elec_attrs = leptons.ELEC_ATTRS
        lowpt_elec_attrs = leptons.LOWPT_ELEC_ATTRS
        comb_elec_attrs = leptons.COMB_ELEC_ATTRS
   
    df = leptons.define_vector_object(
        df, "GoodElectron", leptons.ELEC_SELECT_HYBRID_ISO, "Electron", elec_attrs
    )
    df = leptons.define_vector_object(
        df,
        "GoodLowPtElectron",
        leptons.LOWPT_ELEC_SELECT_HYBRID_ISO,
        "LowPtElectron",
        lowpt_elec_attrs,
    )

    df = leptons.define_combined_electrons(
        df, "CombElectron", "GoodElectron", "GoodLowPtElectron", comb_elec_attrs
    )

"""

import pathlib
from typing import Any
import logging

import ROOT

log = logging.getLogger("mrtools.user")

RDataFrame = Any

MUON_ATTRS = ["pt", "eta", "phi", "dxy", "dz", "charge"]

ELEC_ATTRS = ["pt", "eta", "deltaEtaSC", "phi", "dxy", "dz", "charge"]

LEPT_ATTRS = ["pt", "eta", "phi", "dxy", "dz", "charge"]

LOWPT_ELEC_ATTRS = ["pt", "eta", "deltaEtaSC", "phi", "dxy", "dz", "charge"]

MC_ATTRS = ["genPartIdx", "genPartFlav"]

COMB_ELEC_ATTRS = ["pt", "eta", "deltaEtaSC", "phi", "dxy", "dz", "charge"]

MUON_SELECT = ["Muon_pt > 3.5", "abs(Muon_eta) < 2.4", "Muon_looseID"]

MUON_SELECT_HYBRID_ISO = [
    "Muon_pt > 3.5",
    "abs(Muon_eta) < 2.4",
    "Muon_looseId",
    "HybridIso(Muon_pt,Muon_pfRelIso03_all,5.,0.2)",
    "abs(Muon_dxy) < 0.02",
    "abs(Muon_dz) < 0.1",
]

MUON_SELECT_LOOSE_HYBRID_ISO = [
    "Muon_pt > 3.5",
    "abs(Muon_eta) < 2.4",
    "Muon_looseID",
    "HybridIso(Muon_pt,Muon_pfRelIso03_all,20.,0.8)",
    "abs(Muon_dxy) < 0.1",
    "abs(Muon_dz) < 0.5",
]

ELEC_SELECT = [
    "Electron_pt > 5.",
    "abs(Electron_eta) < 2.5",
    "ECalGap(Electron_eta, Electron_deltaEtaSC)",
    "ElectronVid(Electron_vidNestedWPBitmap,1)",
]

ELEC_SELECT_HYBRID_ISO = [
    "Electron_pt > 5.",
    "abs(Electron_eta) < 2.5",
    "ECalGap(Electron_eta, Electron_deltaEtaSC)",
    "HybridIso(Electron_pt,Electron_pfRelIso03_all,5.0,0.2)",
    "abs(Electron_dxy) < 0.02",
    "abs(Electron_dz) < 0.1",
    "ElectronVid::Eval(Electron_vidNestedWPBitmap,1,ElectronVid::GsfEleRelPFIsoScaledCut)",
]

ELEC_SELECT_LOOSE_HYBRID_ISO = [
    "Electron_pt > 5.",
    "abs(Electron_eta) < 2.5",
    "ECalGap(Electron_eta, Electron_deltaEtaSC)",
    "HybridIso(Electron_pt,Electron_pfRelIso03_all,20.0,0.8)",
    "abs(Electron_dxy) < 0.1",
    "abs(Electron_dz) < 0.5",
    "ElectronVid::Eval(Electron_vidNestedWPBitmap,1,ElectronVid::GsfEleRelPFIsoScaledCut)",
]

LOWPT_ELEC_SELECT = [
    "LowPtElectron_pt > 3.",
    "abs(LowPtElectron_eta) < 2.5",
    "EcalGap(LowPtElectron_eta, LowPtElectron_deltaEtaSC)",
    "LowPtElectron_ID > 0",
]

LOWPT_ELEC_SELECT_HYBRID_ISO = [
    "LowPtElectron_pt > 3.",
    "abs(LowPtElectron_eta) < 2.5",
    "ECalGap(LowPtElectron_eta, LowPtElectron_deltaEtaSC)",
    "HybridIso(LowPtElectron_pt,LowPtElectron_miniPFRelIso_all,5.0,0.2,true)",
    "abs(LowPtElectron_dxy) < 0.02",
    "abs(LowPtElectron_dz) < 0.1",
    "LowPtElectron_ID > 0",
]

LOWPT_ELEC_SELECT_LOOSE_HYBRID_ISO = [
    "LowPtElectron_pt > 3.",
    "abs(LowPtElectron_eta) < 2.5",
    "ECalGap(LowPtElectron_eta, LowPtElectron_deltaEtaSC)",
    "HybridIso(LowPtElectron_pt,LowPtElectron_miniPFRelIso_all,20.0,0.8,true)",
    "abs(LowPtElectron_dxy) < 0.1",
    "abs(LowPtElectron_dz) < 0.5",
    "LowPtElectron_ID > 0",
]


def init():
    log.debug("Load leptons C++ routines.")
    ROOT.gInterpreter.AddIncludePath(str(pathlib.Path(__file__).parent))
    ROOT.gROOT.ProcessLine('#include "leptons_inc.hxx"')


def def_vector_obj(
    df: RDataFrame, name: str, select: list[str], old: str, attrs: list[str]
) -> Any:
    filter = " && ".join(select)
    log.debug('Define("%s_mask", "%s")', name, filter)
    df = df.Define(f"{name}_mask", filter)

    log.debug('Define("n%s", "Sum(%s_mask)")', name, name)
    df = df.Define(f"n{name}", f"Sum({name}_mask)")

    for attr in attrs:
        log.debug('Define("%s_%s","%s_%s[%s_mask]")', name, attr, old, attr, name)
        df = df.Define(f"{name}_{attr}", f"{old}_{attr}[{name}_mask]")

    return df


def define_combined_electrons(
    df: RDataFrame, name: str, one: str, two: str, attrs: list[str]
) -> RDataFrame:
    log.debug(
        'Define("%s_idx","ElectronMerge(%s_eta,%s_phi,%s_eta,%s_phi)")',
        name,
        one,
        one,
        two,
        two,
    )
    df = df.Define(
        f"{name}_idx", f"ElectronMerge({one}_eta,{one}_phi,{two}_eta,{two}_phi)"
    )
    for attr in attrs:
        log.debug(
            'Define("%s_%s","MergeCopy(%s_idx,%s_%s,%s_%s)")',
            name,
            attr,
            name,
            one,
            attr,
            two,
            attr,
        )
        df = df.Define(
            f"{name}_{attr}", f"MergeCopy({name}_idx,{one}_{attr},{two}_{attr})"
        )
    return df


def def_combined_leptons(
    df: RDataFrame, name: str, one: str, two: str, attrs: list[str]
):
    log.debug('Define("%s","LeptonMerge(%s_pt, %s_pt)")', name, one, two)
    df = df.Define(f"{name}_idx", f"LeptonMerge({one}_pt,{two}_pt)")

    for attr in attrs:
        log.debug(
            'Define("%s_%s","MergeCopy(%s_idx, %s_%s, %s_%s))',
            name,
            attr,
            name,
            one,
            attr,
            two,
            attr,
        )
        df = df.Define(
            f"{name}_{attr}", f"MergeCopy({name}_idx,{one}_{attr},{two}_{attr})"
        )

    return df
