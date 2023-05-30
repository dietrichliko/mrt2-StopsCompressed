#!/usr/bin/env python

import pathlib
import logging
import concurrent.futures

import click
import ROOT

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def correct(
    input: pathlib.Path, output: pathlib.Path, tree: str, columns: dict[str, str]
) -> None:
    log.debug("Processing %s ....", input)
    df = ROOT.RDataFrame(tree, str(input))
    file_columns = set(df.GetColumnNames())
    for col_name, col_type in columns.items():
        if col_name not in file_columns:
            log.debug("Missing column %s.", col_name)
            if col_type != "Bool_t":
                log.error("Column %s is not boolean.", col_name)
            df = df.Define(str(col_name), "false")

    log.info("Creating %s ...", output)
    df.Snapshot(tree, str(output))


@click.command
@click.argument(
    "path",
    type=click.Path(
        dir_okay=True, file_okay=False, exists=True, path_type=pathlib.Path
    ),
)
@click.option("-t", "--tree", default="Events")
@click.option("--filter", default="MET_Run*")
@click.option("-w", "--workers", default=4)
@click.option("-d", "--debug", is_flag=True)
def main(path: pathlib.Path, tree: str, filter: str, workers: int, debug: bool) -> None:
    """Merge NanoAODs."""
    if debug:
        log.setLevel(logging.DEBUG)

    columns: dict[str, str] = {}
    for sample in pathlib.Path(path).iterdir():
        if not sample.match(filter):
            continue
        log.info("Getting columns for %s", sample)
        for file in sample.iterdir():
            df = ROOT.RDataFrame(tree, str(file))
            for col_name in df.GetColumnNames():
                col_type = df.GetColumnType(col_name)
                if col_name not in columns:
                    log.debug("New column %s", col_name)
                    columns[col_name] = col_type
                else:
                    if col_type != columns[col_name]:
                        log.error("Column type mismatch for %s", col_name)

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for sample in pathlib.Path(path).iterdir():
            if not sample.match(filter):
                continue
            output = path / f"{sample.name}_cor"
            output.mkdir(parents=True, exist_ok=True)
            for file in sample.iterdir():
                executor.submit(
                    correct, file, output / f"{file.stem}_cor.root", tree, columns
                )


if __name__ == "__main__":
    main()
