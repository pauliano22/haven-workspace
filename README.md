# haven_workspace

Working root for **Project Haven** — a wearable hearing-protection device
(nRF5340 + ADAU1860 DSP) with a companion mobile app. Haven's hardware and
firmware are built on top of **OpenEarable**, an open-source ear-worn sensing
platform; this workspace keeps Haven's own custom work alongside the
OpenEarable reference material it's derived from, so the two are always easy
to diff against.

Assembled 2026-08-06 from four sources: OpenEarable hardware exports out of
Downloads, three cloned OpenEarable reference repos, and Haven's own local
repos (moved here with git history intact). Same day: seven logo concepts
designed and reviewed, the app icon (Concept D) shipped, and the marketing
site (Concept G) built and pushed — see `website/README.md`. The site's
GitHub Pages deploy is currently blocked by a GitHub-wide Actions/Pages
outage, not anything in this repo; it'll go live on its own once GitHub
recovers.

## Getting the code

This repo is an **umbrella** — it's mostly git submodules pointing at Haven's
real repos, plus documentation tying them together. Clone with submodules in
one shot:

```sh
git clone --recurse-submodules https://github.com/pauliano22/haven-workspace.git
```

| Path | Repo | Visibility |
| --- | --- | --- |
| `mobile_app/haven_custom_app` | [haven-app](https://github.com/pauliano22/haven-app) | public |
| `firmware/haven_zephyr_app` | [haven-zephyr-app](https://github.com/pauliano22/haven-zephyr-app) | public |
| `hardware/` | [haven-hardware](https://github.com/pauliano22/haven-hardware) | public, **Git LFS** |
| `legacy_prototypes/teensy_hearing_shield` | [haven-legacy-teensy](https://github.com/pauliano22/haven-legacy-teensy) | public |
| `legacy_prototypes/tinnitus_dsp` | [haven-legacy-dsp-sandbox](https://github.com/pauliano22/haven-legacy-dsp-sandbox) | public |
| `website/` | [haven-website](https://github.com/pauliano22/haven-website) | public, GitHub Pages |

`hardware/` uses Git LFS — run `git lfs install` once per machine before
cloning, or `git lfs pull` afterward if you cloned before installing it.

The three OpenEarable reference repos are **not submoduled** — they're
someone else's project, not pinned dependencies of ours. But
`open-earable-2` is more than reference material: it contains a **working
ADAU1860 driver** for this exact codec on this exact board
(`src/drivers/ADAU1860.h` — the full register map; `ADAU1860.cpp` — the
bring-up sequence; `Lark-fdsp.c` — a FastDSP program with five biquad
slots and hardware safeload). Haven's own codec driver is a port of it —
see the ADAU1860 driver PR on `haven-zephyr-app`. Clone them yourself if
you need them:

```sh
git clone https://github.com/OpenEarable/open-earable-2.git firmware/open-earable-2
git clone https://github.com/OpenEarable/open_earable_flutter.git mobile_app/open_earable_flutter
git clone https://github.com/OpenEarable/app.git mobile_app/open_earable_app
```

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
│                                 SPH0645LM4H-B (MEMS mic). NOTE: the SPH0645 is an
│                                 I2S mic; the stock board's SPH0641LU4H-1 is PDM and
│                                 feeds the codec's DMIC pins directly — the custom
│                                 board wants a PDM part too. Haven's custom board
│                                 Altium source files go directly in haven_dev_board/
│                                 once they exist — currently only the component
│                                 libraries are present.
├── firmware/
│   ├── open-earable-2/            Cloned upstream OpenEarable Zephyr firmware (nRF
│   │                             Connect SDK — see its README for the VS Code +
│   │                             J-Link + nRF-Util toolchain setup). Don't commit
│   │                             changes here, but DO read src/drivers/ADAU1860.*
│   │                             and Lark-fdsp.c: that's the codec driver Haven's
│   │                             firmware is ported from.
│   └── haven_zephyr_app/          Haven's own Zephyr application: NUS BLE peripheral
│                                 advertising as "Haven", the JSON control protocol
│                                 parser, and the ADAU1860 driver (I2C control port,
│                                 32-bit register addresses, FastDSP safeload). See
│                                 its README.md and docs/.
├── mobile_app/
│   ├── haven_custom_app/          Haven's own Expo/React Native app — the real
│   │                             product. Full docs in haven_custom_app/docs/
│   │                             (architecture, BLE protocol, design system,
│   │                             safety invariants, roadmap). Start there.
│   ├── open_earable_flutter/     Cloned OpenEarable reference Flutter app.
│   └── open_earable_app/         Cloned OpenEarable reference native app
│                                 (includes an "open_wearable" package).
│                                 Reference only.
├── dsp_tuning/                    ADAU1860 FastDSP program variants (ADI Lark Studio
│                                 projects + the "Download to Target" uint32 memory
│                                 images — NOT SigmaStudio; see UG-2017). Currently
│                                 empty — the first program to land here is a
│                                 DMIC-input variant of upstream's Lark-fdsp.c; see
│                                 dsp_tuning/README.md.
├── legacy_prototypes/
│   ├── teensy_hearing_shield/    Validated Teensy 4.1 + SGTL5000 prototype — the
│   │                             multi-band notch filter design haven_zephyr_app's
│   │                             DSP math is ported from. Superseded, not extended.
│   └── tinnitus_dsp/              Desktop C++ DSP sandbox (RtAudio real-time notch,
│                                 offline test runners, numpy-verified filter math).
│                                 Vendors RtAudio — clone it yourself, see its README.
└── website/                       Marketing site (GitHub Pages). Single-file static
                                  HTML, same Sanctuary/Evergreen tokens as the app.
                                  Hero mark ships as Radiant Bloom; five other
                                  designed marks are swappable — see its README.
```

## How the pieces connect

**Haven is a fork-in-spirit of OpenEarable**, not a from-scratch design: the
hardware (`hardware/`) and firmware toolchain (`firmware/open-earable-2/`)
both target the nRF Connect SDK / Nordic ecosystem, and Haven's custom
firmware (`firmware/haven_zephyr_app/`) follows the same platform so
OpenEarable's board files, enclosure CAD, and firmware patterns stay directly
comparable/reusable as Haven's own dev board (`hardware/haven_dev_board/`)
and app diverge from the reference.

The signal path, end to end. The important shape: **the codec owns the
audio path**; the nRF5340 is a BLE remote control that writes filter
coefficients over I2C and is never in the mic→speaker loop (that's what
keeps hear-through latency sub-millisecond and the nRF asleep most of the
time).

```
haven_custom_app (mobile_app/)
    │  Nordic UART Service, newline-terminated JSON, MTU 247
    ▼
haven_zephyr_app (firmware/, nRF5340)
    │  I2C1 control port (SDA1/SCL1, addr 0x64, 32-bit register addresses):
    │  power-up sequence, FastDSP program load, biquad coefficient safeloads
    ▼
ADAU1860 codec/DSP
    PDM mic (SPH0641) ──DMIC──▶ FastDSP: ≤5 biquads → limiter → volume ──▶ DAC ──▶ speaker
                                (program image from dsp_tuning/, once that exists)
    ▲ I2S0 (nRF is bus master; codec's ASRCs absorb the clock domain) —
      used for the LDL calibration tone, not for the hear-through path

runs on hardware assembled from openearable_base_pcb/ + haven_dev_board/,
housed in mechanical_cad/ enclosure
```

### Paths to working hardware (none of them cheap)

Three options, in the order worth considering. Prices as of Sept 2026.

1. **Bench: nRF5340 DK + ADI EVAL-ADAU1860EBZ, ~$535** (DK ~$50; eval
   board ~$485 at Newark). The eval board exposes the codec's DMIC input on
   header P44 and serial port 0 (I2S) on header P2, so it wires to the DK
   with exactly the real board's topology — PDM mic into the codec, nRF as
   I2S master on the side, I2C control from the DK. It also carries the
   USB interface ADI's **Lark Studio** talks to, which is how the
   DMIC-input FastDSP program gets designed and verified before it's ever
   loaded from the nRF. This is the lower-cost way to get real audio out
   of the real codec.
2. **The product hardware: a stock OpenEarable 2.0.** The Developer
   Starter Bundle (OpenEarable 2.0.1) is **€2,348** at
   shop.openwearables.com. It *is* Haven's hardware — same nRF5340 module,
   ADAU1860, PDM mic, speaker, and enclosure (Haven's dev board is a KiCad
   port of the stock main PCB) — so `haven_zephyr_app` flashes onto it
   with a J-Link and OpenEarable's debug breakout, wired as shown in
   `firmware/open-earable-2/README.md`. Expensive, but it's the only
   option that yields an in-ear device to actually test with.
3. **Fabricate the rescaled bench board in `haven-dev-board-kicad`** —
   the design has moved on since this list was first written: it is now a
   5× rescaled bench board (73×161 mm) that is routing-complete except two
   cosmetic same-net BGA pairs, DRC-checked, with the antenna keepout
   implemented and a `FABRICATION_GUIDE.md` for turnkey PCBA (JLCPCB /
   PCBWay; 0.35 mm BGA needs assembly, not hand soldering). **Read
   `HAVEN_HARDWARE_REVIEW.md` §0.7 before ordering**: the rescale left the
   32.768 kHz crystal 30 mm from the nRF module and the 24.576 MHz codec
   crystal 14 mm from the ADAU1860, with every decoupling cap 8–50 mm from
   its chip — a placement-only fix that is cheap now and impossible after
   assembly. Order 3–5 boards, not one.

Status of the hear-through path: the nRF side (BLE, protocol, safety
watchdogs, persistence) runs on the nRF5340 DK; the codec driver is being
ported from upstream (see the ADAU1860 driver PR on `haven-zephyr-app`);
the remaining DSP work is a FastDSP program whose input is the DMIC
rather than the I2S port (upstream's program takes I2S audio from the
phone) — a schematic choice in Lark Studio's FastDSP tab, per the
EVAL-ADAU1860 user guide (UG-2017). The one open **safety** item that no
amount of firmware fixes: the app's `level_db` values are nominal until
someone measures commanded level → actual dB SPL at the ear on real
hardware.

The `open_earable_flutter/` and `open_earable_app/` clones are **not**
part of Haven's product — they're reference material for seeing how
OpenEarable's own app talks to OpenEarable's own firmware, useful when
Haven's BLE protocol or sensor handling needs a working example to compare
against. `legacy_prototypes/` is where the DSP approach was first proven out
on a Teensy before the nRF5340/ADAU1860 hardware existed; it's kept for
reference, not built on top of.

## Where to start

- Building/running the app: `mobile_app/haven_custom_app/docs/README.md`.
- Understanding the wire protocol between app and firmware:
  `mobile_app/haven_custom_app/docs/ble-protocol.md`.
- Firmware status and TODOs: `firmware/haven_zephyr_app/README.md`.
- Output-safety invariants (read before touching any tone/level code):
  `mobile_app/haven_custom_app/docs/safety.md`.
- Swapping the website's logo, or seeing all seven designed marks:
  `website/README.md`. Live at https://pauliano22.github.io/haven-website/.
