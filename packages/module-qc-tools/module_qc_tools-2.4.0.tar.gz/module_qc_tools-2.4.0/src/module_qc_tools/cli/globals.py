import logging
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from click.exceptions import MissingParameter
from module_qc_data_tools import check_sn_format

from module_qc_tools import data
from module_qc_tools.utils.misc import get_institution

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class LogLevel(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


OPTIONS = {}

OPTIONS["config_meas"]: Optional[Path] = typer.Option(
    str(data / "configs/meas_config.json"),
    "-cm",
    "--config-meas",
    help="Measurement config file path",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["config_hw"]: Path = typer.Option(
    None,
    "-c",
    "--config",
    help="Hardware Config file path",
    exists=True,
    file_okay=True,
    readable=True,
    resolve_path=True,
    is_eager=True,  # must be eagerly evaluated first so we can check it in config_callback()
)
OPTIONS["output_dir"]: Path = typer.Option(
    "outputs",
    "-o",
    "--output-dir",
    help="output directory",
    exists=False,
    writable=True,
)


def module_connectivity_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: Path
):
    # connectivity for emulator is defined in config, not true when running on module (on purpose)
    # NB: even though config_path is 'Path' type, it is a string in the context until passed to an actual function/coerced
    if "emulator" not in ctx.params["hw_config_path"] and not value:
        msg = "must supply path to connectivity file [-m --module-connectivity]"
        raise MissingParameter(message=msg, ctx=ctx, param=param)
    return value


OPTIONS["module_connectivity"]: Optional[Path] = typer.Option(
    None,
    "-m",
    "--module-connectivity",
    help="path to the module connectivity. Used also to identify the module SN, and to set the default output directory",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
    callback=module_connectivity_callback,
)


def verbosity_callback(ctx: typer.Context, value: LogLevel):
    if ctx.resilient_parsing:
        return None

    logging.getLogger("measurement").setLevel(value.value)
    logging.getLogger("emulator").setLevel(value.value)
    logging.getLogger("upload").setLevel(value.value)
    return value


OPTIONS["verbosity"]: LogLevel = typer.Option(
    LogLevel.info,
    "-v",
    "--verbosity",
    help="Log level [options: DEBUG, INFO (default) WARNING, ERROR]",
    callback=verbosity_callback,
)
OPTIONS["perchip"]: bool = typer.Option(
    False, help="Store results in one file per chip (default: one file per module)"
)
OPTIONS["use_pixel_config"]: bool = typer.Option(
    False,
    help="Use original chip configs; do not create temporary chip configs excluding Pixel Config",
)
OPTIONS["measurement_path"]: Path = typer.Option(
    "Measurement/",
    "-p",
    "--path",
    help="Path to directory with output measurement files",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)


def site_callback(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return None

    institution = get_institution(value)
    if not institution:
        msg = 'No institution found. Please specify your testing site as an environmental variable "INSTITUTION" or specify with the --site option.'
        raise typer.BadParameter(msg)

    return institution


OPTIONS["site"]: str = typer.Option(
    "",
    "--site",
    help='Your testing site. Required when submitting results to the database. Please use institute codes defined on production DB, i.e. "LBNL_PIXEL_MODULES" for LBNL, "IRFU" for Paris-Saclay, ...',
    callback=site_callback,
)

OPTIONS["host"]: str = typer.Option("localhost", "--host", help="localDB server")
OPTIONS["port"]: int = typer.Option(
    5000,
    "--port",
    help="localDB port",
)
OPTIONS["dry_run"]: bool = typer.Option(
    False,
    "-n",
    "--dry-run",
    help="Dry-run, do not submit to localDB or update controller config.",
)
OPTIONS["output_path"]: Path = typer.Option(
    "tmp.json",
    "--out",
    "--output-path",
    help="Analysis output result json file path to save in the local host",
    exists=False,
    writable=True,
)
OPTIONS["use_calib_ADC"]: bool = typer.Option(
    False,
    help="Use calibrated ADC instead of multimeter to read IMUX/VMUX",
)
OPTIONS["emulator_controller"]: Path = typer.Option(
    data / "emulator" / "configs/controller/specCfg-rd53b-16x1.json",
    "-r",
    "--controller",
    help="Controller",
    # exists=True,  # NB: enable when fixed for emulator (does not check for valid paths)
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["emulator_connectivity"]: Path = typer.Option(
    data / "emulator" / "configs/connectivity/20UPGXM1234567_Lx_dummy.json",
    "-c",
    "--connectivity",
    help="Connectivity",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["emulator_chip_position"]: int = typer.Option(
    -1, "-i", "--chipPosition", help="chip position"
)
OPTIONS["depl_volt"]: float = typer.Option(
    None,
    "--vdepl",
    help="Depletion voltage from production database",
)
OPTIONS["skip_config"]: bool = typer.Option(
    False,
    "-s",
    "--skip-config",
    help="Skip configuring the chip when running eye diagram.",
)
OPTIONS["test_size"]: int = typer.Option(
    None,
    "-t",
    "--test-size",
    help="Test size for eye diagram or data merging check.",
)
OPTIONS["mode"]: str = typer.Option(
    "4-to-1",
    "-m",
    "--mode",
    help="Mode of data merging check: '4-to-1' or '2-to-1'",
)
OPTIONS["quiet"]: bool = typer.Option(
    False,
    "-q",
    "--quiet",
    help="Quiet mode, no logger in data merging check.",
)
OPTIONS["debug_gnd"]: bool = typer.Option(
    False,
    "--debug-gnd",
    help="Measure GND before each Vmux measurement as opposed to just at the beginning. Relevant for ADC Calibration, Analog Readback and Injection capacitance.",
)
OPTIONS["save_local"]: bool = typer.Option(
    True,
    help="If true, save measurement to local filesystem and do not upload to localDB. If false, upload to localDB and remove from local filesystem if upload succeeds.",
)
OPTIONS["poweroff"]: bool = typer.Option(
    False,
    help="Whether to turn off power supplies (low-voltage, high-voltage) after measurement is done",
)
OPTIONS["nchips"]: int = typer.Option(
    0,
    "-n",
    "--nChips",
    help="Number of chips powered in parallel (e.g. 4 for a quad module, 3 for a triplet, 1 for an SCC.) If no argument is provided, the number of chips is assumed from the layer.",
)


def sn_callback(value: str):
    try:
        check_sn_format(value)
    except SystemExit as e:
        msg = f"Invalid serial number format: {value}"
        raise typer.BadParameter(msg) from e
    return value


OPTIONS["serial_number"]: str = typer.Option(
    "",
    "-sn",
    "--serial-number",
    help="Module serial number",
    callback=sn_callback,
)
