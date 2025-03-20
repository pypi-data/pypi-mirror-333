import logging

import numpy as np
from module_qc_data_tools import (
    qcDataFrame,
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


TEST_TYPE = "ADC_CALIBRATION"


@inject_metadata(test_type=TEST_TYPE)
def run(config, ps, yr, layer, bom, debug_gnd):
    """The function which does the ADC calibration.

    Args:
        config (dict): Full config dictionary
        ps (Class power_supply): An instance of Class power_supply for power on and power off.
        yr (Class yarr): An instance of Class yarr for chip conifugration and change register.
        layer (str): Layer information for the module
        debug_gnd (bool): Debug GND measurement: measure GND before each Vmux measurement

    Returns:
        data (list): data[chip_id][vmux/imux_type].
    """

    meter = multimeter(config["multimeter"])

    data = [
        qcDataFrame(
            columns=["DACs_input"]
            + [
                f"Vmux{v_mux}"
                for v_mux in config["MonitorV"] + [config["MonitorV_GND"]]
            ]
            + [
                f"ADC_Vmux{v_mux}"
                for v_mux in config["MonitorV"] + [config["MonitorV_GND"]]
            ],
            units=["Count"]
            + ["V" for v_mux in config["MonitorV"] + [config["MonitorV_GND"]]]
            + ["Count" for v_mux in config["MonitorV"] + [config["MonitorV_GND"]]],
        )
        for _ in range(yr._number_of_chips)
    ]

    initialize_chip_metadata(yr, data)
    for chip in yr._enabled_chip_positions:
        chiptype = get_chip_type(data[chip]._meta_data["ChipConfigs"])
        data[chip]._meta_data["ChipConfigs"][chiptype]["GlobalConfig"][
            "InjVcalRange"
        ] = config["InjVcalRange"]
        data[chip].set_x("DACs_input", True)

    if yr.running_emulator():
        ps.on(
            config["v_max"], config["i_config"][layer]
        )  # Only for emulator do the emulation of power on/off
        # For real measurements avoid turn on/off the chip by commands. Just leave the chip running.

    status = yr.configure()
    assert status >= 0

    MonitorV = config["MonitorV"]
    yr.write_register("InjVcalRange", config["InjVcalRange"])

    Range = [
        config["Range"]["start"],
        config["Range"]["stop"],
        config["Range"]["step"],
    ]
    DACs = np.arange(start=Range[0], stop=Range[1], step=Range[2])

    # Check ADC ground
    vmux_adc_gnd, imux_adc_gnd = check_adc_ground(yr, config)
    for i, chip in enumerate(yr._enabled_chip_positions):
        data[chip].add_meta_data("VMUX30_ADC", vmux_adc_gnd[i])
        data[chip].add_meta_data("IMUX63_ADC", imux_adc_gnd[i])
        data[chip].add_meta_data("BOMCode", bom)

    # Measure ground (just once at the beginning if the GND debug mode is disabled)
    vmux_value_GNDA = config["MonitorV_GND"]
    gnd_vmux = -999.0
    gnd_adc = -999.0
    if not debug_gnd:
        gnd_vmux = read_vmux(meter, yr, config, v_mux=vmux_value_GNDA, use_adc=False)
        gnd_adc = read_vmux(
            meter,
            yr,
            config,
            v_mux=vmux_value_GNDA,
            use_adc=True,
            raw_adc_counts=True,
        )

    for DAC in DACs:
        yr.write_register("InjVcalMed", DAC)  # write DAC values
        v_mea = [{} for _ in range(yr._number_of_chips)]

        for _i, vmux_value in enumerate(MonitorV):
            # measure GND before each VMUX measurement if dbgGND enabled
            if debug_gnd:
                gnd_vmux = read_vmux(
                    meter, yr, config, v_mux=vmux_value_GNDA, use_adc=False
                )
                gnd_adc = read_vmux(
                    meter,
                    yr,
                    config,
                    v_mux=vmux_value_GNDA,
                    use_adc=True,
                    raw_adc_counts=True,
                )
            mea_chips_vmux = read_vmux(
                meter, yr, config, v_mux=vmux_value, use_adc=False
            )
            mea_chips_adc = read_vmux(
                meter,
                yr,
                config,
                v_mux=vmux_value,
                use_adc=True,
                raw_adc_counts=True,
            )

            for i, chip in enumerate(yr._enabled_chip_positions):
                v_mea[chip][f"Vmux{vmux_value}"] = [mea_chips_vmux[i]]
                v_mea[chip][f"ADC_Vmux{vmux_value}"] = [mea_chips_adc[i]]
                v_mea[chip][f"Vmux{vmux_value_GNDA}"] = [gnd_vmux[i]]
                v_mea[chip][f"ADC_Vmux{vmux_value_GNDA}"] = [gnd_adc[i]]

        # Add data to frame
        for chip in yr._enabled_chip_positions:
            v_mea[chip]["DACs_input"] = [float(DAC)]
            data[chip].add_data(v_mea[chip])

    if yr.running_emulator():
        ps.off()

    return data
