import logging
from datetime import datetime

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
    get_chip_type,
    initialize_chip_metadata,
    inject_metadata,
    read_vmux,
)
from module_qc_tools.utils.multimeter import multimeter

logger = logging.getLogger("measurement")

app = typer.Typer(context_settings=CONTEXT_SETTINGS)

TEST_TYPE = "VCAL_CALIBRATION"


@inject_metadata(test_type=TEST_TYPE)
def run(config, ps, yr, layer, debug_gnd, use_calib_adc):
    """
    The function which does the VCal calibration for VCal_Med and VCal_Hi in both large and small range.

    Args:
        config (dict): Full config dictionary
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        layer (str): Layer information for the module
        use_calib_adc (bool): use calibrated ADC instead of multimeter
        debug_gnd (bool): Debug GND measurement: measure GND before each Vmux measurement

    Returns:
        data (list): data[chip_id][vcal_type].
    """

    meter = multimeter(config["multimeter"])

    if yr.running_emulator():
        ps.on(
            config["v_max"], config["i_config"][layer]
        )  # Only for emulator do the emulation of power on/off
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    status = yr.configure()  # Should always be 0. Essentially it calls send_command() in the hardware_control_base where protection is added.
    assert status >= 0

    MonitorV = config["MonitorV"]
    InjVcalRange = config["InjVcalRange"]
    vmux_value_GNDA = config["MonitorV_GND"]

    data = [
        [
            qcDataFrame(
                columns=["DACs_input", f"Vmux{vmux_value}", f"Vmux{vmux_value_GNDA}"],
                units=["Count", "V", "V"],
                x=[True, False, False],
            )
            for vmux_value in MonitorV  # outer loop
            for vcalrange in InjVcalRange  # inner loop
        ]
        for _ in range(yr._number_of_chips)
    ]

    initialize_chip_metadata(yr, data)
    for chip in yr._enabled_chip_positions:
        for i, vmux_value in enumerate(MonitorV):
            for j, vcalrange in enumerate(InjVcalRange):
                chip_data = data[chip][i * len(InjVcalRange) + j]
                chiptype = get_chip_type(chip_data._meta_data["ChipConfigs"])
                chip_data._meta_data["ChipConfigs"][chiptype]["GlobalConfig"][
                    "MonitorEnable"
                ] = 1
                chip_data._meta_data["ChipConfigs"][chiptype]["GlobalConfig"][
                    "MonitorV"
                ] = vmux_value
                chip_data._meta_data["ChipConfigs"][chiptype]["GlobalConfig"][
                    "InjVcalRange"
                ] = vcalrange

    Large_Range = [
        config["Large_Range"]["start"],
        config["Large_Range"]["stop"],
        config["Large_Range"]["step"],
    ]
    Small_Range = [
        config["Small_Range"]["start"],
        config["Small_Range"]["stop"],
        config["Small_Range"]["step"],
    ]
    vmux_value_GNDA = config["MonitorV_GND"]
    Ranges = [Large_Range, Small_Range]

    Ranges_maps = {"1": "LargeRange", "0": "SmallRange"}
    RegisterNames_maps = {"8": "InjVcalMed", "7": "InjVcalHigh"}

    cal_count = 0
    for i, vmux_value in enumerate(MonitorV):
        for j, vcalrange in enumerate(InjVcalRange):
            logger.info(
                f"    Start {RegisterNames_maps[str(vmux_value)]}, {Ranges_maps[str(vcalrange)]} for all chips"
            )
            DACs = np.arange(start=Ranges[j][0], stop=Ranges[j][1], step=Ranges[j][2])
            meased_voltages = {}
            meased_voltages_gnd = {}
            for chip in yr._enabled_chip_positions:
                data[chip][cal_count].add_meta_data(
                    "TimeStart", round(datetime.timestamp(datetime.now()))
                )
                meased_voltages.update({chip: -9999.0 * np.ones(len(DACs))})
                meased_voltages_gnd.update({chip: -9999.0 * np.ones(len(DACs))})

            x_label = "DACs_input"
            y_label = "Vmux" + str(MonitorV[i])

            # Check ADC ground
            if use_calib_adc:
                vmux_adc_gnd, imux_adc_gnd = check_adc_ground(yr, config)
                for k, chip in enumerate(yr._enabled_chip_positions):
                    data[chip][cal_count].add_meta_data("VMUX30_ADC", vmux_adc_gnd[k])
                    data[chip][cal_count].add_meta_data("IMUX63_ADC", imux_adc_gnd[k])

            # Read ground (assume the same for all DACs) unless in the GND debug mode
            if not debug_gnd:
                mea_gnd_chips = read_vmux(
                    meter,
                    yr,
                    config,
                    v_mux=vmux_value_GNDA,
                    use_adc=use_calib_adc,
                )
                for k, chip in enumerate(yr._enabled_chip_positions):
                    meased_voltages_gnd[chip] = np.repeat(
                        mea_gnd_chips[k], repeats=len(DACs)
                    )
            yr.write_register("InjVcalRange", vcalrange)

            # Read voltages for all DACs
            for k, DAC in enumerate(DACs):
                yr.write_register(RegisterNames_maps[str(vmux_value)], DAC)

                if debug_gnd:
                    mea_gnd_chips = read_vmux(
                        meter,
                        yr,
                        config,
                        v_mux=vmux_value_GNDA,
                        use_adc=use_calib_adc,
                    )

                    for chip in yr._enabled_chip_positions:
                        meased_voltages_gnd[chip][k] = mea_gnd_chips[chip]

                mea_chips = read_vmux(
                    meter,
                    yr,
                    config,
                    v_mux=MonitorV[i],
                    use_adc=use_calib_adc,
                )
                for m, chip in enumerate(yr._enabled_chip_positions):
                    meased_voltages[chip][k] = mea_chips[m]

            for chip in yr._enabled_chip_positions:
                data[chip][cal_count].add_data(
                    {
                        x_label: DACs.tolist(),
                        y_label: (meased_voltages.get(chip)),
                        f"Vmux{vmux_value_GNDA}": (meased_voltages_gnd.get(chip)),
                    }
                )
                data[chip][cal_count].add_meta_data(
                    "TimeEnd", round(datetime.timestamp(datetime.now()))
                )
            cal_count += 1

    if yr.running_emulator():
        ps.off()

    return data
