from __future__ import annotations

from types import SimpleNamespace

import module_qc_tools as mqt
import pytest
from module_qc_database_tools.utils import default_BOMCode_from_layer
from module_qc_tools.measurements.adc_calibration import run
from module_qc_tools.utils.misc import (
    load_hw_config,
    load_meas_config,
)
from module_qc_tools.utils.power_supply import power_supply
from module_qc_tools.utils.yarr import yarr


@pytest.fixture()
def config_emulator():
    config_hw = load_hw_config(
        mqt.data / "configs" / "hw_config_emulator_merged_vmux.json"
    )
    config = load_meas_config(
        mqt.data / "configs" / "meas_config.json",
        test_type="ADC_CALIBRATION",
        chip_type="RD53B",
    )
    config.update(config_hw)
    return config


@pytest.fixture()
def hardware(config_emulator):
    return SimpleNamespace(
        ps=power_supply(config_emulator["power_supply"]),
        yr=yarr(config_emulator["yarr"]),
    )


def test_issue114(config_emulator, hardware):
    layer = "L1"
    BOM = default_BOMCode_from_layer(layer)

    hardware.ps.set(
        v=config_emulator["v_max"],
        i=config_emulator["i_config"][layer],
    )

    data = run(config_emulator, hardware.ps, hardware.yr, layer, BOM, False)
    metadata = data[0].get_meta_data()

    assert "ChipConfigs" in metadata
    assert "RD53B" in metadata["ChipConfigs"]
    assert "GlobalConfig" in metadata["ChipConfigs"]["RD53B"]
    assert "InjVcalRange" in metadata["ChipConfigs"]["RD53B"]["GlobalConfig"]
