import json
import logging
import shutil
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

import numpy as np
import typer

from module_qc_tools import data
from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_tools.utils.misc import get_yarr_logging_timestamp

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

rng = np.random.default_rng(42)
logger = logging.getLogger("emulator")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


class PSAction(str, Enum):
    on = "on"
    off = "off"
    getV = "getV"
    getI = "getI"
    measV = "measV"
    measI = "measI"


_MODULE_STATE_FILE = data / "emulator" / "module_state.json"

_DEFAULT_SPEC_INIT = [
    "[  info  ][  ScanHelper   ]: Loading controller ...",
    "[  info  ][  ScanHelper   ]: Found controller of type: spec",
    "[  info  ][    SpecCom    ]: Opening SPEC with id #0",
    "[  info  ][    SpecCom    ]: Mapping BARs ...",
    "[  info  ][    SpecCom    ]: ... Mapped BAR0 at 0x7fd97e24a000 with size 1048576",
    "[warning ][    SpecCom    ]: ... BAR4 not mapped (Mmap failed)",
    "[  info  ][    SpecCom    ]: ~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "[  info  ][    SpecCom    ]: Firmware Hash: 0xe7985d6",
    "[  info  ][    SpecCom    ]: Firmware Version: v1.4.0",
    "[  info  ][    SpecCom    ]: Firmware Identifier: 0x1030242",
    "[  info  ][    SpecCom    ]: FPGA card: Trenz TEF1001_R1",
    "[  info  ][    SpecCom    ]: FE Chip Type: RD53A/B/C",
    "[  info  ][    SpecCom    ]: FMC Card Type: Ohio Card (Display Port)",
    "[  info  ][    SpecCom    ]: RX Speed: 1280Mbps",
    "[  info  ][    SpecCom    ]: Channel Configuration: 16x1",
    "[  info  ][    SpecCom    ]: LPM Status: 0",
    "[  info  ][    SpecCom    ]: ~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "[  info  ][    SpecCom    ]: Flushing buffers ...",
    "[  info  ][    SpecCom    ]: Init success!",
]

_DEFAULT_SPEC_DELAY = [
    "[  info  ][    SpecRx     ]: Delay lane 0 fixed to 3",
    "[  info  ][    SpecRx     ]: Delay lane 1 fixed to 10",
    "[  info  ][    SpecRx     ]: Delay lane 2 fixed to 9",
    "[  info  ][    SpecRx     ]: Delay lane 3 fixed to 7",
    "[  info  ][    SpecRx     ]: Delay lane 4 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 5 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 6 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 7 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 8 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 9 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 10 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 11 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 12 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 13 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 14 fixed to 0",
    "[  info  ][    SpecRx     ]: Delay lane 15 fixed to 0",
    "[  info  ][  ScanHelper   ]: Loaded controller config:",
    "[  info  ][  ScanHelper   ]: ~~~ {",
    '[  info  ][  ScanHelper   ]: ~~~     "cmdPeriod": 6.25e-09,',
    '[  info  ][  ScanHelper   ]: ~~~     "delay": [3, 10, 9, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],',
    '[  info  ][  ScanHelper   ]: ~~~     "idle": {',
    '[  info  ][  ScanHelper   ]: ~~~         "word": 2863311530',
    "[  info  ][  ScanHelper   ]: ~~~     },",
    '[  info  ][  ScanHelper   ]: ~~~     "pulse": {',
    '[  info  ][  ScanHelper   ]: ~~~         "interval": 500,',
    '[  info  ][  ScanHelper   ]: ~~~         "word": 0',
    "[  info  ][  ScanHelper   ]: ~~~     },",
    '[  info  ][  ScanHelper   ]: ~~~     "rxActiveLanes": 1,',
    '[  info  ][  ScanHelper   ]: ~~~     "rxPolarity": 65535,',
    '[  info  ][  ScanHelper   ]: ~~~     "specNum": 0,',
    '[  info  ][  ScanHelper   ]: ~~~     "spiConfig": 541200,',
    '[  info  ][  ScanHelper   ]: ~~~     "sync": {',
    '[  info  ][  ScanHelper   ]: ~~~         "interval": 16,',
    '[  info  ][  ScanHelper   ]: ~~~         "word": 2172551550',
    "[  info  ][  ScanHelper   ]: ~~~     },",
    '[  info  ][  ScanHelper   ]: ~~~     "txPolarity": 0',
    "[  info  ][  ScanHelper   ]: ~~~ }",
]

_LOAD_CHIP_CONFIG = [
    "[  info  ][  ScanHelper   ]: Chip count 4",
    "[  info  ][  ScanHelper   ]: Loading chip #0",
    "[  info  ][  ScanHelper   ]: Loading config file: /path/to/chip1_config.json",
    "[  info  ][  ScanHelper   ]: Loading chip #1",
    "[  info  ][  ScanHelper   ]: Loading config file: /path/to/chip2_config.json",
    "[  info  ][  ScanHelper   ]: Loading chip #2",
    "[  info  ][  ScanHelper   ]: Loading config file: /path/to/chip3_config.json",
    "[  info  ][  ScanHelper   ]: Loading chip #3",
    "[  info  ][  ScanHelper   ]: Loading config file: /path/to/chip4_config.json",
]


def initialize_module_state():
    with resources.as_file(data / "emulator/module_state_template.json") as path:
        shutil.copyfile(path, _MODULE_STATE_FILE)


def get_module_state():
    # Copy module state from template if not existing
    if not _MODULE_STATE_FILE.is_file():
        initialize_module_state()

    with _MODULE_STATE_FILE.open(encoding="utf-8") as serialized:
        return json.load(serialized)


def update_module_state(state):
    with _MODULE_STATE_FILE.open("w", encoding="utf-8") as serialized:
        json.dump(state, serialized, indent=4)


def update_Vmux(chip_state):
    """
    This function updates the Vmux voltage values to the corresponding channel.
    Currently emulates MonitorV = 1, 30, 33, 37, 34, 38, 36, 32, and
    MonitorI = 0, 28, 29, 30, 31, 63.
    For other MonitorV and MonitorI channels, return a random number between 0 and 2.
    One needs to write a new if statement for a new MonitorV or MonitorI.
    Note that all grounds are assumed to be perfect (0V). R_Imux is assumed to be 10kohm.
    Also updates the internal ADC based on MonitorV/I setting
    """
    if chip_state["MonitorV"] == 0:
        chip_state["Vmux"] = 0.0
    elif chip_state["MonitorV"] == 1:
        if chip_state["MonitorI"] == 0:
            chip_state["Vmux"] = chip_state["Iref"] * 10000.0
        elif chip_state["MonitorI"] == 28:
            chip_state["Vmux"] = chip_state["IinA"] * 10000.0 / 21000.0
        elif chip_state["MonitorI"] == 29:
            chip_state["Vmux"] = chip_state["IshuntA"] * 10000.0 / 26000.0
        elif chip_state["MonitorI"] == 30:
            chip_state["Vmux"] = chip_state["IinD"] * 10000.0 / 21000.0
        elif chip_state["MonitorI"] == 31:
            chip_state["Vmux"] = chip_state["IshuntD"] * 10000.0 / 26000.0
        elif chip_state["MonitorI"] == 9:
            # Typical Imux9 value for NTC pad current.
            chip_state["Vmux"] = 0.054
        elif (
            (chip_state["MonitorI"] <= 63 and chip_state["MonitorI"] >= 32)
            or (chip_state["MonitorI"] == 26)
            or (chip_state["MonitorI"] == 27)
        ):
            chip_state["Vmux"] = 0.0
        else:
            # If non of the above MonitorI settings are satisfied, return a random number between 0 and 2.
            chip_state["Vmux"] = 2 * rng.random()
    elif chip_state["MonitorV"] == 30:
        chip_state["Vmux"] = 0
    elif chip_state["MonitorV"] == 33:
        chip_state["Vmux"] = chip_state["VinA"] / 4.0
    elif chip_state["MonitorV"] == 37:
        chip_state["Vmux"] = chip_state["VinD"] / 4.0
    elif chip_state["MonitorV"] == 34:
        chip_state["Vmux"] = chip_state["VDDA"] / 2.0
    elif chip_state["MonitorV"] == 38:
        chip_state["Vmux"] = chip_state["VDDD"] / 2.0
    elif chip_state["MonitorV"] == 36:
        chip_state["Vmux"] = chip_state["Vofs"] / 4.0
    elif chip_state["MonitorV"] == 32:
        chip_state["Vmux"] = chip_state["VrefOVP"] / 3.33
    elif chip_state["MonitorV"] == 8:
        # When measuring voltage for VcalMed or VCalHigh, it's essentially computing a liner equation plus/minus
        # a random number. The random number is generated within (-0.005, 0.005). The seed is set global so it's
        # deterministic and reproducible.
        if chip_state["InjVcalRange"] == 1:
            chip_state["Vmux"] = chip_state["InjVcalMed"] / 4096 * 0.8 + 0.005 * (
                2 * rng.random() - 1
            )
        elif chip_state["InjVcalRange"] == 0:
            chip_state["Vmux"] = chip_state["InjVcalMed"] / 4096 * 0.4 + 0.005 * (
                2 * rng.random() - 1
            )
    elif chip_state["MonitorV"] == 7:
        if chip_state["InjVcalRange"] == 1:
            chip_state["Vmux"] = chip_state["InjVcalHigh"] / 4096 * 0.8 + 0.005 * (
                2 * rng.random() - 1
            )
        elif chip_state["InjVcalRange"] == 0:
            chip_state["Vmux"] = chip_state["InjVcalHigh"] / 4096 * 0.4 + 0.005 * (
                2 * rng.random() - 1
            )
    elif chip_state["MonitorV"] == 2:
        # Typical Vmux value for NTC pad voltage.
        chip_state["Vmux"] = 0.084
    elif chip_state["MonitorV"] == 63:
        chip_state["Vmux"] = 0.0
    else:
        # If non of the above MonitorV settings are satisfied, return a random number between 0 and 2.
        chip_state["Vmux"] = 2 * rng.random()

    if chip_state["MonitorV"] == 30 or (
        chip_state["MonitorV"] == 1 and chip_state["MonitorI"] == 63
    ):
        chip_state["MonitoringDataAdc"] = 0
    else:
        if chip_state.get("ADCcalOffset") and chip_state.get("ADCcalSlope"):
            chip_state["MonitoringDataAdc"] = round(
                (chip_state["Vmux"] - chip_state["ADCcalOffset"])
                / chip_state["ADCcalSlope"]
            )
        else:
            chip_state["MonitoringDataAdc"] = 0

    return chip_state


@app.command()
def scanConsole(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    scan: Optional[Path] = typer.Option(
        None,
        "-s",
        "--scan",
        help="Scan config",
        # exists=True,  # NB: enable when fixed for emulator (does not check for valid paths)
        file_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
    ),
    _num_threads: int = typer.Option(
        1,
        "-n",
        "--nThreads",
        help="Number of threads",
    ),
    _output_dir: Path = typer.Option(
        "./",
        "-o",
        "--output-dir",
        help="output directory",
        exists=False,
        writable=True,
    ),
    _skip_reset: bool = typer.Option(
        False,
        "--skip-reset",
        help="skip reset",
    ),
    _verbosity: LogLevel = OPTIONS["verbosity"],
):
    """
    This function emulates the effect of running YARR scanConsole to configure chips
    """

    module_state = get_module_state()

    with connectivity.open(encoding="utf-8") as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    disabled_chip_positions = []
    for chip in range(nChips):
        if not spec_connectivity["chips"][chip]["enable"]:
            disabled_chip_positions += [chip]
    module_state["disabled_chip_positions"] = disabled_chip_positions

    for chip in range(nChips):
        config_path = spec_connectivity["chips"][chip]["config"]
        with connectivity.parent.joinpath(config_path).open(encoding="utf-8") as path:
            spec = json.load(path)
        chipname = ""
        try:
            chipname = next(iter(spec))
        except Exception:
            logger.error("Empty chip config")

        GlobalConfig = spec[chipname]["GlobalConfig"]
        Parameter = spec[chipname]["Parameter"]
        # VDDA/D should be trimmed to 1.2 after chip configuring
        module_state[f"Chip{chip+1}"]["VDDA"] = min(1.2, module_state["Vin"])
        module_state[f"Chip{chip+1}"]["VDDD"] = min(1.2, module_state["Vin"])
        # MonitorI and V set according to chip configs
        module_state[f"Chip{chip+1}"]["MonitorI"] = GlobalConfig.get("MonitorI", 0)
        module_state[f"Chip{chip+1}"]["MonitorV"] = GlobalConfig.get("MonitorV", 0)
        # set InjVcalMed, InjVcalHigh and InjVcalRange based on the chip configs
        module_state[f"Chip{chip+1}"]["InjVcalMed"] = GlobalConfig.get("InjVcalMed", 0)
        module_state[f"Chip{chip+1}"]["InjVcalHigh"] = GlobalConfig.get(
            "InjVcalHigh", 0
        )
        module_state[f"Chip{chip+1}"]["InjVcalRange"] = GlobalConfig.get(
            "InjVcalRange", 0
        )
        module_state[f"Chip{chip+1}"]["MonitoringDataAdc"] = GlobalConfig.get(
            "MonitoringDataAdc", 0
        )
        ADCcalPar = Parameter.get("ADCcalPar", [0, 0, 0])
        module_state[f"Chip{chip+1}"]["ADCcalOffset"] = ADCcalPar[0] * 0.001
        module_state[f"Chip{chip+1}"]["ADCcalSlope"] = ADCcalPar[1] * 0.001

        # Update Vmux
        module_state[f"Chip{chip+1}"] = update_Vmux(module_state[f"Chip{chip+1}"])

    update_module_state(module_state)

    # YARR returns 0 when scan is run
    if scan is not None:
        raise typer.Exit(0)
    raise typer.Exit(1)


@app.command()
def write_register(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
    name: str = typer.Argument(),
    value: int = typer.Argument(),
):
    """
    This function emulates the effect of running YARR write-register
    Currently only emulates register MonitorI, MonitorV. One needs to add a new if statement for a new register name.
    """
    module_state = get_module_state()

    with connectivity.open(encoding="utf-8") as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    logger.info("%s, %s", name, value)

    for chip in range(nChips):
        if chip_position != -1 and chip is not chip_position:
            continue
        if name == "MonitorI":
            module_state[f"Chip{chip+1}"]["MonitorI"] = value
        elif name == "MonitorV":
            module_state[f"Chip{chip+1}"]["MonitorV"] = value
        elif name == "InjVcalMed":
            module_state[f"Chip{chip+1}"]["InjVcalMed"] = value
        elif name == "InjVcalHigh":
            module_state[f"Chip{chip+1}"]["InjVcalHigh"] = value
        elif name == "InjVcalRange":
            module_state[f"Chip{chip+1}"]["InjVcalRange"] = value
        module_state[f"Chip{chip+1}"] = update_Vmux(module_state[f"Chip{chip+1}"])

    update_module_state(module_state)


@app.command()
def read_register(
    name: str,
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
):
    """
    This function emulates the effect of running YARR read-register
    Currently only emulates register SldoTrimA and SldoTrimD. One needs to add a new if statement for a new register name.
    """

    with connectivity.open(encoding="utf-8") as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    module_state = get_module_state()
    disabled_chip_positions = module_state["disabled_chip_positions"]

    for chip in range(nChips):
        if chip_position != -1 and chip is not chip_position:
            continue
        if chip in disabled_chip_positions:
            continue
        if name in ["SldoTrimA", "SldoTrimD"]:
            sys.stdout.write("8 ")
        else:
            sys.stdout.write("0 ")
    raise typer.Exit(0)


@app.command()
def control_PS(
    action: PSAction = typer.Option(
        ...,
        "-a",
        "--action",
        help="Action to PS",
    ),
    voltage: float = typer.Option(
        None,
        "-v",
        "--voltage",
        help="Set voltage",
    ),
    current: float = typer.Option(
        None,
        "-i",
        "--current",
        help="Set current",
    ),
):
    """
    This function emulates the effect of powering the module
    """
    if action == "off":
        # Turning off the power simply means module states go back to initial states. Thus copy the initial states from the template
        initialize_module_state()
        raise typer.Exit(0)

    module_state = get_module_state()

    if action in ["getV", "measV"]:
        # measure Vin
        v = module_state["Vin"]
        sys.stdout.write(f"{v}")
        raise typer.Exit(0)

    if action in ["getI", "measI"]:
        # measure Iin
        i = module_state["Iin"]
        sys.stdout.write(f"{i}")
        raise typer.Exit(0)

    if action == "on":
        if current is None or voltage is None:
            typer.echo(
                f"Must set LV voltage and current. (voltage: {voltage}, current: {current}"
            )
            raise typer.Exit(2)

        nChips = module_state["nChips"]

        # check if the module has already been powered on
        already_power = module_state["Vin"] > 0

        #### TODO: LV is off for for IV_MEASURE, do this??
        # if not already_power:
        # module_state["Vin"] = 0
        # module_state["Iin"] = 0

        # Calculate Vin based on the prediction (slope and offset), as well as the voltage and the current set to the power supply
        module_state["Vin"] = min(0.348293 / nChips * current + 1, voltage, 2.0)
        # Calculate Iin from the calculated Vin
        module_state["Iin"] = (module_state["Vin"] - 1) * nChips / 0.348293
        # Assume temperature increases linearly with Iin
        module_state["temperature"] = 25.0 + module_state["Iin"] * 2.0
        for chip in range(nChips):  # loop over all the chips
            # VinA = VinD = Vin
            module_state[f"Chip{chip+1}"]["VinA"] = module_state["Vin"]
            module_state[f"Chip{chip+1}"]["VinD"] = module_state["Vin"]
            # Fun assumption: VDDA/D = 1.1 before configuring; otherwise stay the same values
            module_state[f"Chip{chip+1}"]["VDDA"] = min(
                1.1 if not already_power else module_state[f"Chip{chip+1}"]["VDDA"],
                module_state["Vin"],
            )
            module_state[f"Chip{chip+1}"]["VDDD"] = min(
                1.1 if not already_power else module_state[f"Chip{chip+1}"]["VDDD"],
                module_state["Vin"],
            )
            module_state[f"Chip{chip+1}"]["Vofs"] = min(
                1.0, module_state["Vin"]
            )  # VOFS = 1V
            module_state[f"Chip{chip+1}"]["VrefOVP"] = 2.0  # VrefOVP = 2V
            module_state[f"Chip{chip+1}"]["IinA"] = (
                module_state["Iin"] / nChips / 2
            )  # IinA = Iin/nChips/2
            module_state[f"Chip{chip+1}"]["IinD"] = (
                module_state["Iin"] / nChips / 2
            )  # IinD = Iin/nChips/2
            module_state[f"Chip{chip+1}"]["IcoreA"] = min(
                0.2, module_state["Iin"] / nChips / 2
            )  # ICoreA assumed to be 0.2A
            module_state[f"Chip{chip+1}"]["IcoreD"] = min(
                0.2, module_state["Iin"] / nChips / 2
            )  # ICoreD assumed to be 0.2A
            module_state[f"Chip{chip+1}"]["IshuntA"] = (
                module_state[f"Chip{chip+1}"]["IinA"]
                - module_state[f"Chip{chip+1}"]["IcoreA"]
            )  # IShunt = Iin - Icore
            module_state[f"Chip{chip+1}"]["IshuntD"] = (
                module_state[f"Chip{chip+1}"]["IinD"]
                - module_state[f"Chip{chip+1}"]["IcoreD"]
            )
            module_state[f"Chip{chip+1}"]["Iref"] = 4e-6  # Iref = 4 uA
            if not already_power:
                module_state[f"Chip{chip+1}"]["MonitorI"] = 0  # default minitorI = 0
            if not already_power:
                module_state[f"Chip{chip+1}"]["MonitorV"] = 0  # default minitorV = 0
            module_state[f"Chip{chip+1}"] = update_Vmux(
                module_state[f"Chip{chip+1}"]
            )  # update Vmux voltage

        update_module_state(module_state)


@app.command()
def control_HV(
    action: PSAction = typer.Option(
        ...,
        "-a",
        "--action",
        help="Action to HV PS",
    ),
    voltage: float = typer.Option(
        0.0,
        "-v",
        "--voltage",
        help="Set voltage",
    ),
    current: float = typer.Option(
        0.0,
        "-i",
        "--current",
        help="Set current",
    ),
):
    """
    This function emulates the effect of powering the module
    """
    if action == "off":
        # Turning off the power simply means module states go back to initial states. Thus copy the initial states from the template
        initialize_module_state()
        raise typer.Exit(0)

    module_state = get_module_state()

    if action == "getV":
        # measure the bias voltage
        v = module_state["Vbias"]
        sys.stdout.write(f"{v}")
        raise typer.Exit(0)

    if action == "getI":
        # measure the leakage current
        i = module_state["Ileak"]
        sys.stdout.write(f"{i}")
        raise typer.Exit(0)

    if action == "on":
        if current is None or voltage is None:
            typer.echo("HV: Must set voltage and current.")
            raise typer.Exit(2)

        module_state["time"] += 2
        module_state["Vbias"] = voltage

        # Calculate Ileak from the Vbias (fit from 20UPIS25300160)
        # Don't use theoretical calc because basically constant
        a = -9.04601528e-14
        b = 9.99999999e-01
        module_state["Ileak"] = a * (np.exp(b * voltage) - 1)

        # Assume temperature increases linearly with Iin
        module_state["temperature"] = round(np.random.uniform(22.0, 24.0), 3)

        update_module_state(module_state)


@app.command()
def measureV():
    """
    This function emulates the effect of multimeter (measuring the Vmux)
    """
    module_state = get_module_state()

    nChips = module_state["nChips"]
    disabled_chip_positions = module_state["disabled_chip_positions"]

    v = 0
    for chip in range(nChips):
        if chip in disabled_chip_positions:
            continue
        v += module_state[f"Chip{chip+1}"]["Vmux"]
    sys.stdout.write(f"{v}")
    raise typer.Exit(0)


@app.command()
def read_adc(
    vmux: int,
    _controller: Path = OPTIONS["emulator_controller"],
    _connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
    read_current: bool = typer.Option(
        False,
        "-I",
        "--readCurrent",
        help="Read current instead of voltage",
    ),
    read_raw: bool = typer.Option(
        False,
        "-R",
        "--rawCounts",
        help="Read raw ADC counts",
    ),
    _shared_vmux: int = typer.Option(
        -1,
        "-s",
        help="Assume FE's have shared vmux, and set MonitorV register to this value (high-Z) on all FE's when not reading",
    ),
):
    """
    This function emulates the effect of ADC reading
    R_Imux is assumed to be 10kohm.
    """
    module_state = get_module_state()

    nChips = module_state["nChips"]
    disabled_chip_positions = module_state["disabled_chip_positions"]

    # Update Vmux settings first
    for chip in range(nChips):
        if chip_position != -1 and chip is not chip_position:
            continue
        if chip in disabled_chip_positions:
            continue
        if read_current:
            module_state[f"Chip{chip+1}"]["MonitorV"] = 1
            module_state[f"Chip{chip+1}"]["MonitorI"] = vmux
        else:
            module_state[f"Chip{chip+1}"]["MonitorV"] = vmux
        module_state[f"Chip{chip+1}"] = update_Vmux(module_state[f"Chip{chip+1}"])

    # Then read ADC
    for chip in range(nChips):
        if chip_position != -1 and chip is not chip_position:
            continue
        if chip in disabled_chip_positions:
            continue
        if read_raw:
            v = module_state[f"Chip{chip+1}"]["MonitoringDataAdc"]
            u = ""
        elif read_current:
            v = (module_state[f"Chip{chip+1}"]["Vmux"] / 10000.0) / 1e-6
            u = "uA"
        else:
            v = module_state[f"Chip{chip+1}"]["Vmux"]
            u = "V"
        sys.stdout.write(f"{v} {u}\n")
    raise typer.Exit(0)


@app.command()
def read_ringosc(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
):
    """
    This function emulates the effect of ROSC reading
    """

    with connectivity.open(encoding="utf-8") as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    module_state = get_module_state()
    disabled_chip_positions = module_state["disabled_chip_positions"]

    for chip in range(nChips):
        if chip_position != -1 and chip is not chip_position:
            continue
        if chip in disabled_chip_positions:
            continue

        rosc_freq = "500 " * 42
        sys.stdout.write(rosc_freq + "\n")
    raise typer.Exit(0)


@app.command()
def data_merging_check(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    _testsize: int = OPTIONS["test_size"],
    _mode: str = OPTIONS["mode"],
    _quiet: str = OPTIONS["quiet"],
):
    """
    This function emulates the effect of DATA MERGING CHECK
    """

    logger.debug(f"Printing emulator connectivity path pass pipeline {connectivity}")

    yarr_output_header = ["[  info  ][dataMergingCheck]: Init spec"]
    yarr_output_header += _DEFAULT_SPEC_INIT
    yarr_output_header += _DEFAULT_SPEC_DELAY
    yarr_output_header += _DEFAULT_SPEC_INIT
    yarr_output_header += [
        "[  info  ][dataMergingCheck]: Doing data merging test on Spec Card 0"
    ]
    yarr_output_header += ["[  info  ][  ScanHelper   ]: Chip type: ITKPIXV2"]
    yarr_output_header += _LOAD_CHIP_CONFIG

    results = {
        "4-to-1": [
            "[  info  ][dataMergingCheck]: Setting up configuration for all chips...",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21394 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21394 as secondary for 4-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21395 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21395 as secondary for 4-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21396 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21396 as secondary for 4-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21397 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21397 as primary for 4-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuration done.",
            "[  info  ][dataMergingCheck]: Soft resets all chips to synch gearboxes.",
            "[  info  ][   Itkpixv2    ]: Performing soft reset ...",
            "[  info  ][dataMergingCheck]: Loop over primaries:",
            "[  info  ][dataMergingCheck]: Testing lane #3",
            "[  info  ][dataMergingCheck]: [3] Error Count: 266515 (expected [81682,81685])",
            "[  info  ][dataMergingCheck]: [3] Link quality: -0.06281526394266856",
            "[warning ][dataMergingCheck]: Lane 3 failed data merging test",
            "Failed",
        ],
        "2-to-1": [
            "[  info  ][dataMergingCheck]: Setting up configuration for all chips...",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21394 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21394 as secondary for 2-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21395 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21395 as primary for 2-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21396 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21396 as secondary for 2-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuring chip 0x21397 ...",
            "[  info  ][dataMergingCheck]: Setting up 0x21397 as primary for 2-to-1 merging",
            "[  info  ][dataMergingCheck]: Configuration done.",
            "[  info  ][dataMergingCheck]: Soft resets all chips to synch gearboxes.",
            "[  info  ][   Itkpixv2    ]: Performing soft reset ...",
            "[  info  ][dataMergingCheck]: Loop over primaries:",
            "[  info  ][dataMergingCheck]: Testing lane #1",
            "[  info  ][dataMergingCheck]: [1] Error Count: 61263 (expected [61261,61264])",
            "[  info  ][dataMergingCheck]: [1] Link quality: 1",
            "[  info  ][dataMergingCheck]: Testing lane #3",
            "[  info  ][dataMergingCheck]: [3] Error Count: 61261 (expected [61261,61264])",
            "[  info  ][dataMergingCheck]: [3] Link quality: 1",
            "Passed",
        ],
    }

    string = ""
    if not _quiet:
        for log_item in yarr_output_header:
            string += f"[{get_yarr_logging_timestamp()}]{log_item}\n"

        for log_item in results[_mode][:-1]:
            string += f"[{get_yarr_logging_timestamp()}]{log_item}\n"
    for log_item in results[_mode][-1:]:
        string += f"{log_item}\n"

    sys.stdout.write(string)

    raise typer.Exit(0)


@app.command()
def eye_diagram(
    _controller: Path = OPTIONS["emulator_controller"],
    connectivity: Path = OPTIONS["emulator_connectivity"],
    chip_position: int = OPTIONS["emulator_chip_position"],
    dryrun: bool = OPTIONS["dry_run"],
    _skipconfig: bool = OPTIONS["skip_config"],
    _testsize: int = OPTIONS["test_size"],
):
    """
    This function emulates the effect of EYE DIAGRAM
    """

    with connectivity.open(encoding="utf-8") as path:
        spec_connectivity = json.load(path)

    nChips = len(spec_connectivity["chips"])

    testdata = {}
    testdata["Delay"] = []
    for d in range(32):
        testdata["Delay"] += [d]

    for lane in range(16):
        testdata[f"lane{lane}"] = 32 * [0.0]

    for chip in range(nChips):
        if chip_position != -1 and chip is not chip_position:
            continue

        testdata[f"lane{chip}"] = rng.random(32)

    yarr_output_header = ["[  info  ][  eyeDiagram   ]: Init spec"]
    yarr_output_header += _DEFAULT_SPEC_INIT
    yarr_output_header += [
        "[  info  ][  eyeDiagram   ]: Scanning link quality against delay on Spec Card 0",
    ]
    yarr_output_header += _DEFAULT_SPEC_INIT
    yarr_output_header += _DEFAULT_SPEC_DELAY
    yarr_output_header += ["[  info  ][  ScanHelper   ]: Chip type: RD53B"]
    yarr_output_header += _LOAD_CHIP_CONFIG
    yarr_output_header += [
        "[ error  ][ Rd53bPixelCfg ]: Could not find pixel registers, using default!",
        '[  info  ][  eyeDiagram   ]: Read "CdrClkSel" 0 and "ServiceBlockPeriod" 50 from virtual register read',
        "[ error  ][ Rd53bPixelCfg ]: Could not find pixel registers, using default!",
        '[  info  ][  eyeDiagram   ]: Read "CdrClkSel" 0 and "ServiceBlockPeriod" 50 from virtual register read',
        "[ error  ][ Rd53bPixelCfg ]: Could not find pixel registers, using default!",
        '[  info  ][  eyeDiagram   ]: Read "CdrClkSel" 0 and "ServiceBlockPeriod" 50 from virtual register read',
        "[ error  ][ Rd53bPixelCfg ]: Could not find pixel registers, using default!",
        '[  info  ][  eyeDiagram   ]: Read "CdrClkSel" 0 and "ServiceBlockPeriod" 50 from virtual register read',
    ]

    string = ""
    for log_item in yarr_output_header:
        string += f"[{get_yarr_logging_timestamp()}]{log_item}\n"

    for i in testdata["Delay"]:
        for _key, value in testdata.items():
            prefix = ""
            suffix = ""
            if rng.random() > 0.5 and value[i] > 0.0:
                prefix = "\033[32m"
                suffix = "\033[0m"
            string += f"{prefix}{round(value[i], 2)}{suffix} | "
        string += "\n"

    string += f"[{get_yarr_logging_timestamp()}][  info  ][  eyeDiagram   ]: Done scanning!\n\n"
    string += f"[{get_yarr_logging_timestamp()}][  info  ][  eyeDiagram   ]: Determining delay settings:\n"

    for lane in range(len(testdata) - 1):
        if chip_position != -1 and lane is not chip_position:
            string += f"[{get_yarr_logging_timestamp()}][  info  ][  eyeDiagram   ]: No good delay setting for lane {lane}"
        else:
            eyewidth = round(31 * rng.random(), 0)
            delay = round(31 * rng.random(), 0)
            string += f"[{get_yarr_logging_timestamp()}][  info  ][  eyeDiagram   ]: Delay setting for lane {lane} with eye width {eyewidth}: {delay}"
        string += "\n"

    if dryrun:
        string += "All done, without updating the emulator controller config!"
    else:
        string += f"Writing to emulator controller config {_controller}"

    sys.stdout.write(string)

    raise typer.Exit(0)


@app.command()
def measureT():
    """
    This function emulates the effect of NTC (measure module temperature)
    """
    module_state = get_module_state()

    T = module_state["temperature"]
    sys.stdout.write(f"{T}")
    raise typer.Exit(0)


@app.command()
def switchLPM(
    _specNum: int = typer.Option(
        0,
        "-s",
        help="Spec card number",
    ),
    _enableTx: int = typer.Option(
        0,
        "-e",
        help="TX channels to modify (decimal number from binary pattern starting from TX 0 as the least significant bit, for example 13 to modify 1101, i.e. all TX channels apart from TX 1)",
    ),
    _mask: bool = typer.Option(
        False,
        "--m",
        "-m",
        help="Modify the TX channels specified with -e without overwriting the others",
    ),
    _action: str = typer.Argument(
        help="Action (on/off)",
    ),
):
    raise typer.Exit(0)


def run_scanConsole():
    typer.run(scanConsole)


def run_write_register():
    typer.run(write_register)


def run_read_register():
    typer.run(read_register)


def run_read_adc():
    typer.run(read_adc)


def run_read_ringosc():
    typer.run(read_ringosc)


def run_switchLPM():
    typer.run(switchLPM)


def run_control_PS():
    typer.run(control_PS)


def run_control_HV():
    typer.run(control_HV)


def run_measureV():
    typer.run(measureV)


def run_measureT():
    typer.run(measureT)


def run_dataMergingCheck():
    typer.run(data_merging_check)


def run_eyeDiagram():
    typer.run(eye_diagram)


if __name__ == "__main__":
    app()
