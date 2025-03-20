# module-qc-tools history

---

All notable changes to module-qc-tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

**_Changed:_**

**_Added:_**

**_Fixed:_**

## [2.4.0](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.4.0) - 2025-03-11 ## {: #mqt-v2.4.0 }

**_Changed:_**

- reduce number of steps in VCAL calibration (!215)
- increase voltage compliance during SLDO scan (!219)
- improve compatibility of mqt with Felix (!186)

**_Added:_**

- add BOM information to output of SLDO, LP and ADC calibration (!220)
- add ability to enable/disable LPM on targeted TX channels (!207)
- add data merging substest to data transmission test (!218)
- add Iref trim information to output of the AR test (!221)
- add protection when ramping HV down (!211)
- CLI to retrieve input current based on chip version (!210)

**_Fixed:_**

- fix write register issue when running with separate vmux (!208)
- fixed number of points in SLDO (!213)

## [2.3.0](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.3.0) - 2024-07-12 ## {: #mqt-v2.3.0 }

**_Changed:_**

**_Added:_**

**_Fixed:_**

## [2.2.8](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.2.8) - 2024-12-17 ## {: #mqt-v2.2.8 }

**_Changed:_**

**_Added:_**

**_Fixed:_**

## [2.2.7](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.2.7) - 2024-10-03 ## {: #mqt-v2.2.7 }

**_Changed:_**

**_Added:_**

**_Fixed:_**

## [2.2.6](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.2.6) - 2024-07-12 ## {: #mqt-v2.2.6 }

**_Changed:_**

- logging now uses `rich` and the formatting is a little different, and should
  be improved once `module-qc-data-tools` is updated (!166)
- refactored all measurements to be more pythonic and getting ready for v3
  (!153, !165, !173, !174)

**_Added:_**

- allow non-zero ADC ground counts (!152)
- `use_calib_adc` is added to all measurements (!156, !157)
- retry configure and read/write registers when communication is lost with
  module (!139)
- `LONG-TERM-STABILITY-DCS` measurement (!175, !176, !177, !178)

**_Fixed:_**

- hard-coded chip type (!105)
- emulator handles disabled chips (!162)
- `pandas` is removed, speeding up this package (!168)
- `hardware_control_base` is refactored to speed up emulator (!169)
- `pkg_resources` is deprecated (!172)

## [2.2.5](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.2.5) - 2024-07-12 ## {: #mqt-v2.2.5 }

Note: this version is skipped due to a packaging issue.

## [2.2.4](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools/-/tags/v2.2.4) - 2024-04-30 ## {: #mqt-v2.2.4 }

First release for this documentation. (!171)

**_Changed:_**

- lower max current for L1 quads (!147)
- improved error handling when measurement uploads to localDB fails (!144)

**_Added:_**

- spec number argument to LP mode switch (!143)

**_Fixed:_**

- support for disabled chips (!145)
- data transmission test ensures correct power supply settings for
  voltage/current (!148)
- `switchLPM` works for more than 1 spec card (!149)
- clear registers when eyeDiagram is launched with the reconfiguration option
  (!150)
- values for emulator are integers (!151)
