import json
import logging
from pathlib import Path

import typer
from module_qc_data_tools import (
    get_layer_from_sn,
    get_nominal_current,
)
from module_qc_database_tools.utils import (
    get_chip_type_from_serial_number,  # TODO move to data tools?
)

from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)

logger = logging.getLogger("measurement")


@app.command()
def main(
    meas_config_path: Path = OPTIONS["config_meas"],
    serial_number: str = OPTIONS["serial_number"],
    n_chips_input: int = OPTIONS["nchips"],
):
    """Print the nominal current value required for the given module."""

    # Taking the module SN from YARR path to config in the connectivity file.
    layer = get_layer_from_sn(serial_number)
    chip_type = get_chip_type_from_serial_number(serial_number)

    # Load the  measurement config just to retrieve general info
    # could be improved, need to see the requirements
    meas_config = json.loads(meas_config_path.read_text())

    nom_current = get_nominal_current(meas_config, layer, chip_type, n_chips_input)

    typer.echo(f"{nom_current:.2f}")


if __name__ == "__main__":
    typer.run(main)
