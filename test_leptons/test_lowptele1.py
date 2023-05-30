#!/usr/bin/env python

import pathlib
import itertools

import ROOT

from Helper.ANEle import ANEle

dataset = "WJetsToLNu_HT400to600"
PATH = pathlib.Path(
    f"/scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples/compstops_UL16APVv9_nano_v10/Met/{dataset}/{dataset}_0.root"
)


def main():
    # ROOT.EnableImplicitMT()
    chain = ROOT.TChain("Events")
    # for file in PATH.iterdir():
    #     chain.Add(str(file))
    chain.Add(str(PATH))
    nr_events = chain.GetEntries()
    with (
        open("electron1.csv", "w") as out_elec,
        open("lowpt_electron1.csv", "w") as out_lowpt_elec,
        open("comb_electron1.csv", "w") as out_comb_elec,
    ):
        print("event, index, pt, eta, phi", file=out_elec)
        print("event, index, pt, eta, phi", file=out_lowpt_elec)
        print("event, index, pt, eta, phi, type", file=out_comb_elec)
        for i, evt in itertools.islice(enumerate(chain), 0, 10000):
            if evt.nElectron == 0 and evt.nLowPtElectron == 0:
                continue
            print(f"Event {i}/{nr_events}")
            print(
                f"Nr Electron: {evt.nElectron} Nr LowPt Electron: {evt.nLowPtElectron}"
            )
            anele = ANEle(evt, "comb", "Std")
            good_elec = anele.getStdEleVar(anele.StdselectEleIdx())
            good_lowpt_elec = anele.getLowPtEleVar(anele.LowselectEleIdx())
            comb_elec = anele.getCombEleVar(anele.CombEleIdx())
            for j, ge in enumerate(good_elec):
                print(
                    f"{evt.event}, {j}, {ge['pt']:7.3f}, {ge['eta']:7.3f}, {ge['phi']:7.3f}",
                    file=out_elec,
                )
            for j, gle in enumerate(good_lowpt_elec):
                print(
                    f"{evt.event}, {j}, {gle['pt']:7.3f}, {gle['eta']:7.3f}, {gle['phi']:7.3f}",
                    file=out_lowpt_elec,
                )
            for j, ce in enumerate(comb_elec):
                print(
                    f"{evt.event}, {j}, {ce['pt']:7.3f}, {ce['eta']:7.3f}, {ce['phi']:7.3f}, {0 if ce['type'] == 'Electron' else 1}",
                    file=out_comb_elec,
                )


if __name__ == "__main__":
    main()
