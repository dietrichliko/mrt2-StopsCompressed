#!/usr/bin/env python
"""create_yaml

Read data definition from CSV file and create sample definition in yaml.
"""
import csv
import logging
import os
import pathlib
from typing import Any
from typing import TextIO
from typing import Callable

import click
import ruamel.yaml

logging.basicConfig(
    format="%(asctime)s - %(levelname)s -  %(name)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
log = logging.getLogger()

SKIMS = ["Met", "MetLepEnergy", "DoubleLep"]
PERIODES = ["Run2016preVFP", "Run2016postVFP", "Run2017", "Run2018"]

EOSPATH = "/store/user/liko/StopsCompressed/nanoTuples"
EOSTAG = "samples_from_eos"

SCRATCHPATH = "/scratch-cbe/users/dietrich.liko/StopsCompressed/nanoTuples"
SCRATCHTAG = "samples_from_fs"


def get_attr(v: dict[str, Any], name: str, func: Callable = str.strip) -> dict[str, Any]:
    
    if name in v and v[name].strip():
        return {name.lower(): func(v[name])}
    else:
        return {}


def make_sample(v: dict[str, Any], **kwargs: Any) -> dict[str, Any]:

    sample: dict[str, Any] = {"name": v["Name"], "type": v["Type"], "attributes": {}}
    sample |= kwargs
    sample |= get_attr(v, "Title")
    sample["attributes"] |= get_attr(v, "Color")
    sample["attributes"] |= get_attr(v, "integrated_luminosity", float)
    sample["attributes"] |= get_attr(v, "trigger", str.split)
    return sample


@click.command
@click.argument("output", type=click.File(mode="w"))
@click.option(
    "--skim",
    default="Met",
    type=click.Choice(SKIMS),
    help="Generate sample definition for a specific skim",
)
@click.option("--eos/--no-eos", default=False)
def main(output: TextIO, skim: str, eos: bool) -> None:
    """Generate sample definition for a skim."""
    log.info("Writing %s", output.name)

    if eos:
        file_path = EOSPATH
        yaml_tag = EOSTAG
    else:
        file_path = SCRATCHPATH
        yaml_tag = SCRATCHTAG

    with ruamel.yaml.YAML(output=output) as yaml:
        yaml.explicit_start = True

        for p in PERIODES:

            samples: dict[pathlib.PurePath, Any] = { 
                pathlib.PurePath("") : {
                    "name": os.path.splitext(os.path.basename(output.name))[0],
                    "period": p,
                    "samples_groups": [],
                    yaml_tag: [],
                    "attributes": {},
                }
            }
            fname = f"{skim} - {p}.csv"
            log.info("Reading %s", fname)
            with open(fname, "r") as inp:
                reader = csv.DictReader(inp)

                for v in reader:
                    if v["Path"].startswith("#"):
                        continue
                    
                    path = pathlib.PurePath(v["Path"], v["Name"])
                    
                    cp = pathlib.PurePath("")
                    for name in path.parent.parts:
                        cp /= name
                        if cp not in samples:
                            samples[cp] = {
                                "name": name,
                                "type": samples[cp.parent]["type"],
                                "samples_groups": [],
                                yaml_tag: [],
                                "attributes": {},
                            }
                            samples[cp.parent]["samples_groups"].append(samples[cp])
                        
                    if not v["Tag"]:
                        samples[path] = make_sample(
                            v,
                            **{ 
                                "samples_groups": [],
                                yaml_tag: [],
                            }
                        )
                        samples[path.parent]['samples_groups'].append(samples[path])
                    else:
                        samples[path] = make_sample(
                            v,
                            directory=f'{file_path}/{v["Tag"]}/{skim}/{v["Name"]}',
                        )
                        samples[path.parent][yaml_tag].append(samples[path])                        

                for path, sample in samples.items():
                    for attr in ("attributes", "samples_groups", yaml_tag):
                        if attr in sample and not sample[attr]:
                            del sample[attr]

                yaml.dump(samples[pathlib.PurePath("")])


if __name__ == "__main__":
    main()
