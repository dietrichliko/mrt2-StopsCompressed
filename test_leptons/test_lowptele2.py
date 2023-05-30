#!/usr/bin/env python

import pathlib
import logging

import ROOT
from tools import leptons

PATH = pathlib.Path(
    "/scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL16APVv9_nano_v10/Met/WJetsToLNu_HT400to600/WJetsToLNu_HT400to600_0.root"
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%y%m%d - %H:%M:%S",
)

log = logging.getLogger(__package__)


def main():
    # ROOT.EnableImplicitMT()
    leptons.init()
    ROOT.gROOT.ProcessLine('#include "leptons_print.hxx"')

    chain = ROOT.TChain("Events")
    chain.Add(str(PATH))
    # for file in PATH.iterdir():
    #     chain.Add(str(file))

    is_mc = True

    df = ROOT.RDataFrame(chain)
    df = df.Range(0, 10000)

    if is_mc:
        elec_attrs = leptons.ELEC_ATTRS + leptons.MC_ATTRS
        lowpt_elec_attrs = leptons.LOWPT_ELEC_ATTRS + leptons.MC_ATTRS
        comb_elec_attrs = leptons.COMB_ELEC_ATTRS + leptons.MC_ATTRS
    else:
        elec_attrs = leptons.ELEC_ATTRS
        lowpt_elec_attrs = leptons.LOWPT_ELEC_ATTRS
        comb_elec_attrs = leptons.COMB_ELEC_ATTRS

    df = leptons.def_vector_obj(
        df, "GoodElectron", leptons.ELEC_SELECT_HYBRID_ISO, "Electron", elec_attrs
    )
    df = leptons.def_vector_obj(
        df,
        "GoodLowPtElectron",
        leptons.LOWPT_ELEC_SELECT_HYBRID_ISO,
        "LowPtElectron",
        lowpt_elec_attrs,
    )

    df = leptons.define_combined_electrons(
        df, "CombElectron", "GoodElectron", "GoodLowPtElectron", comb_elec_attrs
    )

    df = df.Filter("nGoodElectron > 0 || nGoodLowPtElectron > 0")

    print_elec = ROOT.PrintAsCsv()
    print_elec.open("electron2.csv")
    print_lowpt_elec = ROOT.PrintAsCsv()
    print_lowpt_elec.open("lowpt_electron2.csv")
    print_comb_elec = ROOT.PrintAsCsv1()
    print_comb_elec.open("comb_electron2.csv")

    df.Foreach(
        print_elec, ["event", "GoodElectron_pt", "GoodElectron_eta", "GoodElectron_phi"]
    )
    df.Foreach(
        print_lowpt_elec,
        [
            "event",
            "GoodLowPtElectron_pt",
            "GoodLowPtElectron_eta",
            "GoodLowPtElectron_phi",
        ],
    )
    df.Foreach(
        print_comb_elec,
        [
            "event",
            "CombElectron_pt",
            "CombElectron_eta",
            "CombElectron_phi",
            "CombElectron_idx",
        ],
    )
    print_elec.close()
    print_lowpt_elec.close()
    events = df.Count()
    print(f"Events {events.GetValue()}")


if __name__ == "__main__":
    main()
