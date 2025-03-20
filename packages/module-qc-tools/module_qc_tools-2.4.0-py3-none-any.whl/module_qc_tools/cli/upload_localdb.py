#!/usr/bin/env python3
from __future__ import annotations

import warnings
from pathlib import Path

import typer

from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    _measurement_path: Path = OPTIONS["measurement_path"],
    _host: str = OPTIONS["host"],
    _port: int = OPTIONS["port"],
    _dry_run: bool = OPTIONS["dry_run"],
    _output_path: Path = OPTIONS["output_path"],
    _verbosity: LogLevel = OPTIONS["verbosity"],
):
    """
    !!! warning "Deprecated"

        Please use module-qc-database-tools instead:

        ```bash
        mqdbt upload-measurement ...
        ```

    Walk through the specified directory (recursively) and attempt to submit all json files to LocalDB as the QC measurement

    Given a path to a directory with the output files, the script will recursively
    search the directory and upload all files with the `.json` extension. Supply the
    option `--dry-run` to see which files the script finds without uploading to
    localDB.

    Args:
        path (str or pathlib.Path): root directory to walk through
        host (str): localDB server host
        port (int): localDB server port
        out  (str): analysis output result json file path to save in the local host

    Returns:
        None: The files are uploaded to localDB.
    """

    warnings.warn("deprecated", DeprecationWarning, stacklevel=1)
    raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(main)
