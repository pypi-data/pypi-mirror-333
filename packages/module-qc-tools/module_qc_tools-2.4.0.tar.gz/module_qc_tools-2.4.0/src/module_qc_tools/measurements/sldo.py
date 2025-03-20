import logging

import numpy as np
import typer
from module_qc_data_tools import (
    qcDataFrame,
)

from module_qc_tools.cli.globals import (
    CONTEXT_SETTINGS,
)
from module_qc_tools.utils.misc import (
    check_adc_ground,
    initialize_chip_metadata,
    inject_metadata,
    read_vmux,
)
from module_qc_tools.utils.multimeter import multimeter
from module_qc_tools.utils.ntc import ntc

logger = logging.getLogger("measurement")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)

TEST_TYPE = "SLDO"


@inject_metadata(test_type=TEST_TYPE)
def run(config, ps, yr, layer, bomcode, use_calib_adc):
    """
    VI scans for SLDO.

    Args:
        config (dict): Full config dictionary
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        layer (str): Layer information for the module
        use_calib_adc (bool): use calibrated ADC instead of multimeter

    Returns:
        data (list): data[chip_id][vmux/imux_type].
    """
    meter = multimeter(config["multimeter"])
    nt = ntc(config["ntc"])

    data = [
        qcDataFrame(
            columns=["Temperature", "SetCurrent", "Current"]
            + [f"Vmux{v_mux}" for v_mux in config["v_mux"]]
            + [f"Imux{i_mux}" for i_mux in config["i_mux"]],
            units=["C", "A", "A"]
            + ["V" for v_mux in config["v_mux"]]
            + ["V" for i_mux in config["i_mux"]],
        )
        for _ in range(yr._number_of_chips)
    ]
    initialize_chip_metadata(yr, data)

    for chip in yr._enabled_chip_positions:
        data[chip].set_x("Current", True)

    # turn on power supply and configure all chips
    ps.set(v=config["v_max"], i=config["i_config"][layer])
    _status = yr.configure()

    # Check ADC ground
    if use_calib_adc:
        vmux_adc_gnd, imux_adc_gnd = check_adc_ground(yr, config)
        for i, chip in enumerate(yr._enabled_chip_positions):
            data[chip].add_meta_data("VMUX30_ADC", vmux_adc_gnd[i])
            data[chip].add_meta_data("IMUX63_ADC", imux_adc_gnd[i])

    currents = sorted(
        np.concatenate(
            [
                np.linspace(
                    config["i_min"][layer],
                    config["i_max"][layer],
                    config["n_points"][layer],
                ),
                np.array(config["extra_i"]),
            ]
        ),
        reverse=True,
    )
    for i in currents:
        # set and measure current for power supply
        ps.set(v=config["v_max"], i=i)
        current, _status = ps.measI()
        i_mea = [{} for _ in range(yr._number_of_chips)]
        yr.eyeDiagram()

        try:
            # measure v_mux
            for v_mux in config["v_mux"]:
                mea_chips = read_vmux(
                    meter,
                    yr,
                    config,
                    v_mux=v_mux,
                    use_adc=use_calib_adc,
                )
                for j, chip in enumerate(yr._enabled_chip_positions):
                    i_mea[chip][f"Vmux{v_mux}"] = [mea_chips[j]]

            # measure i_mux
            for i_mux in config["i_mux"]:
                mea_chips = read_vmux(
                    meter,
                    yr,
                    config,
                    i_mux=i_mux,
                    use_adc=use_calib_adc,
                )
                for j, chip in enumerate(yr._enabled_chip_positions):
                    i_mea[chip][f"Imux{i_mux}"] = [mea_chips[j]]

        except Exception as e:
            logger.error(e)
            logger.error(
                f"Problem running SLDO at Iin = {i}, continuing to next current point"
            )
            for chip in yr._enabled_chip_positions:
                for v_mux in config["v_mux"]:
                    i_mea[chip][f"Vmux{v_mux}"] = [0]
                for i_mux in config["i_mux"]:
                    i_mea[chip][f"Imux{i_mux}"] = [0]

        # measure temperature from NTC
        temp, _status = nt.read()

        for chip in yr._enabled_chip_positions:
            i_mea[chip]["SetCurrent"] = [i]
            i_mea[chip]["Current"] = [current]
            i_mea[chip]["Temperature"] = [temp]
            data[chip].add_data(i_mea[chip])

    # Return to initial state
    ps.set(v=config["v_max"], i=config["i_config"][layer])

    for chip in yr._enabled_chip_positions:
        data[chip].add_meta_data(
            "AverageTemperature", np.average(data[chip]["Temperature"])
        )
        data[chip].add_meta_data("BOMCode", bomcode)

    return data
