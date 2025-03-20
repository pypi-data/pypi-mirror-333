import logging
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

import typer
from module_qc_data_tools import (
    get_layer_from_sn,
    get_sn_from_connectivity,
    outputDataFrame,
    save_dict_list,
)
from module_qc_database_tools.utils import (
    get_chip_type_from_serial_number,
)

from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_tools.console import console
from module_qc_tools.measurements.undershunt_protection import (
    run,
)
from module_qc_tools.utils.misc import (
    add_identifiers_metadata,
    copytree,
    load_hw_config,
    load_meas_config,
)
from module_qc_tools.utils.power_supply import power_supply
from module_qc_tools.utils.yarr import yarr

logger = logging.getLogger("measurement")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)

tests = ["nominal", "analog", "digital"]

# Taking the test-type from the script name which is the test-code in ProdDB.
TEST_TYPE = Path(__file__).stem


@app.command()
def main(
    hw_config_path: Path = OPTIONS["config_hw"],
    meas_config_path: Path = OPTIONS["config_meas"],
    base_output_dir: Path = OPTIONS["output_dir"],
    module_connectivity: Optional[Path] = OPTIONS["module_connectivity"],
    _verbosity: LogLevel = OPTIONS["verbosity"],
    perchip: bool = OPTIONS["perchip"],
    institution: str = OPTIONS["site"],
    use_pixel_config: bool = OPTIONS["use_pixel_config"],
    save_local: bool = OPTIONS["save_local"],
    use_calib_adc: bool = OPTIONS["use_calib_ADC"],
):
    timestart = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # if -o option used, overwrite the default output directory
    output_dir = module_connectivity.parent if module_connectivity else base_output_dir

    if base_output_dir != Path("outputs"):
        output_dir = base_output_dir

    output_dir = output_dir.joinpath("Measurements", TEST_TYPE, timestart)
    # Make output directory and start log file
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Start {TEST_TYPE.replace('_',' ')}!")
    logger.info(f"TimeStart: {timestart}")

    logger.addHandler(logging.FileHandler(output_dir.joinpath("output.log")))

    config_hw = load_hw_config(hw_config_path)

    if module_connectivity:
        config_hw["yarr"]["connectivity"] = module_connectivity

    # Taking the module SN from YARR path to config in the connectivity file.
    module_serial = get_sn_from_connectivity(config_hw["yarr"]["connectivity"])
    layer = get_layer_from_sn(module_serial)
    chip_type = get_chip_type_from_serial_number(module_serial)

    # Load the  measurement config and combine it with the hardware config
    config = load_meas_config(
        meas_config_path, test_type=TEST_TYPE, chip_type=chip_type
    )
    config.update(config_hw)

    # initialize hardware
    ps = power_supply(config["power_supply"])
    yr = yarr(config["yarr"])

    if not use_pixel_config:
        yr.omit_pixel_config()

    try:
        data = run(config, ps, yr, layer, use_calib_adc)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
        yr.switchLPM("off")
        yr.remove_tmp_connectivity()
    except Exception as err:
        logger.exception(err)
        yr.switchLPM("off")
        yr.remove_tmp_connectivity()
        raise typer.Exit(1) from err
    add_identifiers_metadata(data, module_serial, institution)

    alloutput = []
    chipnames = []

    for chip in yr._enabled_chip_positions:
        chip_name = data[chip]._meta_data["Name"]
        console.print(data[chip])
        outputDF = outputDataFrame()
        outputDF.set_test_type(TEST_TYPE)
        outputDF.set_results(data[chip])
        alloutput += [outputDF.to_dict()]
        chipnames += [chip_name]

    with TemporaryDirectory() as tmpdirname:
        if perchip:
            for outputDF, chip_name in zip(alloutput, chipnames):
                save_dict_list(
                    Path(tmpdirname).joinpath(f"{chip_name}.json"),
                    [outputDF],
                )
        else:
            save_dict_list(
                Path(tmpdirname).joinpath(f"{module_serial}.json"),
                alloutput,
            )

        # for now, set to false until localDB upload functionality implemented
        upload_failed = True
        upload_implemented = False

        if not save_local:
            # add in logic here to upload to localDB
            msg = "Not implemented yet"
            raise RuntimeError(msg)

        if upload_failed or save_local:
            copytree(tmpdirname, output_dir)
            if upload_failed and upload_implemented:
                logger.warning(
                    "The upload to localDB failed. Please fix and retry uploading the measurement output again."
                )

            logger.info(f"Writing output measurements in {output_dir}")

    logger.info("Done!")
    logger.info(f"TimeEnd: {datetime.now().strftime('%Y-%m-%d_%H%M%S')}")

    # Delete temporary files
    if not use_pixel_config:
        yr.remove_tmp_connectivity()


if __name__ == "__main__":
    typer.run(main)
