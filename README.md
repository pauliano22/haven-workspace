# haven_workspace

Working root for **Project Haven** — a wearable hearing-protection device
(nRF52 + ADAU1860 DSP) with a companion mobile app. Haven's hardware and
firmware are built on top of **OpenEarable**, an open-source ear-worn sensing
platform; this workspace keeps Haven's own custom work alongside the
OpenEarable reference material it's derived from, so the two are always easy
to diff against.

Assembled 2026-08-06 from four sources: OpenEarable hardware exports out of
Downloads, three cloned OpenEarable reference repos, and Haven's own local
repos (moved here with git history intact).

## Layout

```
haven_workspace/
├── hardware/
│   ├── openearable_base_pcb/     OpenEarable's official PCB exports (schematic/layout
│   │                             PDFs, BOM, .epro Altium 365 release packages) — main
│   │                             2.0, flex 2.0, and a debugging breakout 1.0. No raw
│   │                             .PcbDoc/.SchDoc source, only the packaged exports as
│   │                             downloaded from Altium 365.
│   ├── mechanical_cad/            OpenEarable enclosure 2.0.1: .step + .stl for the
│   │                             front/back shells, speaker mount, battery mount.
│   └── haven_dev_board/
│       └── component_libraries/  Ultra Librarian Altium parts for chips on Haven's
│                                 OWN stripped-down dev board: ADAU1860 (DSP) and
│                                 SPH0645LM4H-B (MEMS mic). Haven's custom board
│                                 Altium source files go directly in haven_dev_board/
│                                 once they exist — currently only the component
│                                 libraries are present.
├── firmware/
│   ├── open-earable-2/            Cloned upstream OpenEarable Zephyr firmware (nRF
│   │                             Connect SDK — see its README for the VS Code +
│   │                             J-Link + nRF-Util toolchain setup). Reference only;
│   │                             don't commit changes here.
│   └── haven_zephyr_app/          Haven's own Zephyr application: NUS BLE peripheral
│                                 advertising as "Haven", the JSON control protocol
│                                 parser, and the ADAU1860 driver (I2C/SPI
│                                 transactions currently stubbed pending PCB
│                                 bring-up). See its README.md and docs/.
├── mobile_app/
│   ├── haven_custom_app/          Haven's own Expo/React Native app — the real
│   │                             product. Full docs in haven_custom_app/docs/
│   │                             (architecture, BLE protocol, design system,
│   │                             safety invariants, roadmap). Start there.
│   ├── open_earable_flutter/     Cloned OpenEarable reference Flutter app.
│   └── open_earable_app/         Cloned OpenEarable reference native app
│                                 (includes an "open_wearable" package).
│                                 Reference only.
├── dsp_tuning/                    SigmaStudio / ADAU1860 filter + limiter configs.
│                                 Currently empty — see dsp_tuning/README.md.
└── legacy_prototypes/
    ├── teensy_hearing_shield/    Validated Teensy 4.1 + SGTL5000 prototype — the
    │                             multi-band notch filter design haven_zephyr_app's
    │                             DSP math is ported from. Superseded, not extended.
    └── tinnitus_dsp/              Desktop C++ DSP sandbox (RtAudio real-time notch,
                                  offline test runners, numpy-verified filter math).
                                  Contains its own nested git repo at rtaudio/ (a
                                  third-party dependency clone) — left as-is.
```

## How the pieces connect

**Haven is a fork-in-spirit of OpenEarable**, not a from-scratch design: the
hardware (`hardware/`) and firmware toolchain (`firmware/open-earable-2/`)
both target the nRF Connect SDK / Nordic ecosystem, and Haven's custom
firmware (`firmware/haven_zephyr_app/`) follows the same platform so
OpenEarable's board files, enclosure CAD, and firmware patterns stay directly
comparable/reusable as Haven's own dev board (`hardware/haven_dev_board/`)
and app diverge from the reference.

The signal path, end to end:

```
haven_custom_app (mobile_app/)
    │  Nordic UART Service, newline-terminated JSON, MTU 247
    ▼
haven_zephyr_app (firmware/)  ──I2C/SPI control──▶  ADAU1860 DSP
    │                                                (tuned via dsp_tuning/,
    │                                                 once that exists)
    ▼
runs on hardware assembled from openearable_base_pcb/ + haven_dev_board/,
housed in mechanical_cad/ enclosure
```

The `open_earable_flutter/` and `open_earable_app/` clones are **not**
part of Haven's product — they're reference material for seeing how
OpenEarable's own app talks to OpenEarable's own firmware, useful when
Haven's BLE protocol or sensor handling needs a working example to compare
against. `legacy_prototypes/` is where the DSP approach was first proven out
on a Teensy before the nRF52/ADAU1860 hardware existed; it's kept for
reference, not built on top of.

## Where to start

- Building/running the app: `mobile_app/haven_custom_app/docs/README.md`.
- Understanding the wire protocol between app and firmware:
  `mobile_app/haven_custom_app/docs/ble-protocol.md`.
- Firmware status and TODOs: `firmware/haven_zephyr_app/README.md`.
- Output-safety invariants (read before touching any tone/level code):
  `mobile_app/haven_custom_app/docs/safety.md`.
