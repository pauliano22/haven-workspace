# Haven v2 pod: bring-up plan for the first assembled board

Written 2026-11-07. **Plan only. No v2 board exists yet and nothing here has been run.** Facts come from
`hardware_kicad/kicad_v2_pod/README.md`, the exported netlist and the pod PCB. Where a step depends on a
datasheet I have not read, it says so.

Rule for the whole plan: **go one stage at a time, stop at the first thing that is wrong, write the
result down** in the log at the bottom. A pod is never put in anyone's ear until stage 7 passes.

## What you need on the bench

| Item | Why | Have it? |
|---|---|---|
| nRF5340 DK (as a J-Link debugger, via its debug-out header) | Flash and read logs over the pod's SWD pads | Yes |
| Bench supply with current limit, or a Li-ion cell plus a 100 ohm series resistor for first power-up | Stage 1 without risking a short | **Unpriced, ask Paul** |
| Multimeter | Rail voltages, shorts | Probably |
| Fine-tip tweezers/probes, a magnifier or USB microscope | The audio chip is 0.35 mm pitch | Ask Paul |
| 2 cm^3 coupler plus a calibrated measurement mic (or a borrowed sound level meter with an ear simulator) | Stage 7, the loudness limit | **No. Biggest gap.** |
| A second Bluetooth device, the app on a phone | Stage 4 | Yes |

Test points on the pod (from the PCB): SWDIO, SWCLK, RESET, VDD (+1V8), GND, SHPHLD, P1.13 (spare), BAT+, BAT-.
There is no test point on VSYS, the codec supply, or the PDM clock, so those need a probe on a component pad.

## Stages

| # | Stage | What you do | Pass looks like | If it fails |
|---|---|---|---|---|
| 0 | Look and measure, unpowered | Magnify every fine-pitch part (audio chip U15, power chip U2, module U1). Multimeter resistance, GND to +1V8 and GND to BAT+ | No visible solder bridges. No dead short (not under about 100 ohm) on any rail | Stop. Photograph it. Do not power it |
| 1 | First power, current limited | Battery pads (BAT+/BAT-) fed from the supply at 3.7 V, current limit 20 mA, **or** a cell through 100 ohm. Do not fit the real battery yet | Draw settles, nothing warms up. Measure +1V8 at the VDD pad | Heat or draw at the limit: unpower, look for the short around U2 |
| 2 | Regulator and charge path | Raise limit to 100 mA. Feed 5 V into the case pad (VBUS) through the supply, 100 mA limit. Check charge current with a series meter on the battery lead | Charge current about 40 mA (set by R111 = 15 kohm). Stops at 4.20 V. The datasheet-based expectation, **not measured** | Wrong current: R111 value or fit. **Never charge a real cell until the current is correct** |
| 3 | Flash over SWD | Wire the DK's debug-out to SWDIO/SWCLK/RESET/VDD/GND. `nrfjprog --recover` then flash the `haven_v2` build | Programmer sees an nRF5340. Firmware boots, the RTT log prints | Not found: check VDD at the pad, the RESET wire, the module's seat. Recover may need the network core flashed too |
| 4 | Bluetooth | Same test as the DK: `firmware/haven_zephyr_app/tools/ble_dk_windows_test.py` (14 checks) and the phone app | Advertises, connects, settings round-trip | Radio fault: see the crystal row below. A pod that cannot connect is a radio, antenna or crystal problem |
| 5 | Codec talks | Firmware reads the codec chip ID over I2C and powers it up | ID read, no error. Supply to the codec is switched by SENSORS_ENABLE (P1.11) | No ID: check the switched supply, the I2C pull-ups, the 24.576 MHz crystal |
| 6 | Tone out, still not in an ear | Play a tone at the lowest level into a **dummy load** (a 16 ohm resistor), scope the output | A clean tone at the right frequency, level steps follow the app | Distortion or noise: check codec clock and supply decoupling |
| 7 | Loudness limit | Speaker in a coupler. Command the loudest tone, then the loudest hear-through signal, and measure SPL. Test the limiter with a loud input | Peak output stays at or below the safety cap in `tone_safety.c`, and the limiter holds on loud input. **The numbers are written down before anyone wears it** | **Do not wear it.** Lower the limit in firmware or the codec, re-measure |
| 8 | Mic and hear-through | Fit the in-ear unit. Talk, clap, check the codec passes mic audio to the speaker. Measure latency (click test from `BENCH_TEST_PLAN.md` section 3) | Mic audio present, delay in the low hundreds of microseconds | Silent or noisy: PDM clock polarity (two mics share the line on opposite edges), cable length |
| 9 | Wear test, minutes | A volunteer, the lowest comfortable level, a hand on the volume. Stop at any discomfort | Comfortable, no pain, no tinnitus change reported | Stop. Back to stage 7 |

## Items that need a real measurement, not a guess

| Item | State today | How to settle it |
|---|---|---|
| Radio crystal load | Firmware sets 8 pF. The module maker's spec default is 12.5 pF (CAPVALUE 0x0C). **Mismatch, unresolved** | Stage 4. Measure Bluetooth carrier offset (a receiver with frequency readout, or watch connection reliability at both settings). Try 12.5 pF first on the board if the offset is high. Software change only, no board change |
| Low-frequency crystal | 32.768 kHz, external 9 pF caps | Check the sleep timing against a stopwatch over many minutes; wrong load shows as drift |
| Charge current | Computed from a rule of thumb, I = 600 V / R | Stage 2 |
| nPM1100 land pattern | Footprint not yet compared with Nordic's drawing | Compare before ordering (needs the Nordic document the browser helper is fetching) |
| Codec routing of mic audio to the serial output | Wiring verified in the netlist. Register setup untested, and the audio chip's full datasheet is not yet re-read | Needs the datasheet (queued) then a stage 8 test |
| Output ceiling in the finished device | **Not measured.** The 85 dB limit only covers hearing-test tones | Stage 7 |
| Battery safety | CoinPower cells have no protection circuit; the board has charge termination but no separate low-voltage cutoff | Do not leave a pod flat for weeks. Use a protected bench cell for early stages |

## Order of risk (what to check first, because it kills the most)

1. A short on a rail from the 0.35 mm audio chip or the power chip (stages 0 and 1).
2. The charge current being wrong for the battery (stage 2).
3. No radio because of the crystal setting (stage 4).
4. Loudness above a safe level (stage 7). This one is a safety risk, not a schedule risk.

## v3 pod: what is different (added 2026-11-14, plan only, no v3 board exists)

The stages above apply to the v3 pod (`hardware_kicad/kicad_v3_pod/`) with these changes and extra measurements.
Each one answers a specific doubt recorded in the v3 README or the shell brief.

| Stage | Change or extra measurement for v3 | Why | Pass looks like |
|---|---|---|---|
| 0 | Also inspect L2 against U2, C114, R5, R9 (0.14-0.25 mm gaps) and C117 beside the module | Parts are closer than on v2 | No bridges, no tombstoned 0201s |
| 1 | The real cell is a 40 mAh pouch with a 40 mA (1C) discharge limit. Before fitting it, log supply current during boot and Bluetooth connect with the bench supply (scope across a 1 ohm sense resistor) | Start-up and radio peaks were never measured | Peaks under 40 mA, or short enough that a 10 uF rail holds them: write the number down |
| 2 | Charge current should be about 20 mA (R111 = 30 kohm). Charge through the two spring pins, not a clip on the pad | 0.5C for the 40 mAh cell; checks the pins' contact | 20 mA +-20 %, stops at 4.20 V, pins make contact every time |
| 2 | Scope +1V8 at C114, AC coupled, 20 MHz limit, at idle and with audio running | The converter was re-laid; the old layout had a 4.4 mm switching line | Ripple under about 20 mV peak to peak. Higher: note it and compare the audio noise floor below |
| 2 | Low-battery shutdown: lower the bench supply slowly from 3.7 V with no charger | `battery_guard.c` has never run on hardware | The pod shuts down (ship mode) near 3.3 V after about 30 s below it, and wakes when the charger is connected |
| 3 | The RESET test pad is 0.6 mm (was 0.8); SWD works without it | Pad shrank to clear the spring-pin land | Programmer attaches with SWDIO / SWCLK / VDD / GND only |
| 3 | Status light: check that it lights at all | The LED's pad numbering is unsettled (datasheet and library disagree) | Lights. Dark and everything else works: the LED is reversed; turn it by hand or leave it |
| 4 | Bluetooth range with and without the spring pins fitted (same room, same phone, RSSI at 1 m and 5 m) | Two 3 mm metal posts sit 1 mm from the antenna keep-out | Less than about 3 dB difference. More: try shorter pins or move the contacts |
| 4 | This board has no 32 kHz crystal: confirm the `lfrc` firmware build is the one flashed, and that connections stay up for 30 minutes | The radio's slow clock runs from the internal oscillator | No drops |
| 6 | Codec noise floor into the dummy load with the DAC muted, converter running: FFT to 20 kHz, and look for tones near the converter's switching rate folded into the audio band | The inductor now sits 0.5 mm from the audio chip and 1.3 mm from the codec clock's capacitor | No discrete tones above the noise; A-weighted noise close to the data sheet's |
| 7 | Do stage 7 twice: with the series resistor at the speaker (220 ohm planned) and, on the bench only, without it. Command digital full scale once on purpose, in the coupler, never in an ear | The calculated worst case without the resistor is about 118 dB at 1 kHz | With the resistor, full scale stays under the level Paul and the audiologist set. Record both numbers |
| 8 | v3 has one microphone, on the pod (U14), and none in the ear. Feedback check: raise hear-through gain in the coupler until it howls and note the margin | Pod mic to ear speaker is a new acoustic path | Stable at the working gain with at least 6 dB to spare |

## What to expect honestly

First boards of a design this dense (6 layers, 0.35 mm pitch, 143 vias) often have one or two faults. Order
five boards, keep them unfitted until stage 0 and 1 pass on one, and keep notes of every fault. Rework
of a 0.35 mm chip needs hot air and practice; a failed audio chip is a lost board.

## Log (fill in at the bench)

| Date | Board # | Stage | Result | Notes |
|---|---|---|---|---|
| | | | | |
