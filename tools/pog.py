"""Auxiliary scripts for jsonpog-integration."""

from typing import Any
import logging

import ROOT

log = logging.getLogger("mrtools.tools")

RDataFrame = Any

ROOT."""
std::unique_ptr<Correction::Cset> PileupCorrection;
"""

def def_pileup_weight(df: RDataFrame, name: str, period: str) -> RDataFrame:
    
    """
    PileupCorrection = new Correction::CSet()
    """
    log.debug('Define(%s, PileupCorrection->evaluate(BlaBla,"nominal"))', name)
    return df.Define(
        name, 
        f'PileupCorrection->evaluate(,"nominal")'
    )