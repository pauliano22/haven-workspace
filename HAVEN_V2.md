# Haven v2: compact earbud + charging case

Naming (Paul, 2026-10-29): **v1** = the trimmed OpenEarable board (earlier called "Rev A"),
**v2** = this compact bud + case (earlier "Rev B"). Branch and PR names keep the old labels.

Started 2026-10-29. v1 (OpenEarable's native board, trimmed; `haven-dev-board-kicad#15`) is
parked until its Bluetooth module and charger are back in stock. v2 is a new, smaller board
and a charging case. Status and decisions also live in `PROJECT_STATUS.md`.

## Goals (working assumptions, Paul can change these)
- Bud about AirPods Pro size.
- At least 6 h of hear-through per charge.
- Keep the ADAU1860 codec (driver and tests exist) and the SPH0641 mic.
- Sealed nozzle for standard 4.5 mm-bore tips (see the seal spec in `PROJECT_STATUS.md`).
- Charging through the case with 2 pogo pins; no USB-C on the bud.
- Keep a certified nRF5340 module (a bare chip + own antenna loses FCC/IC certification).

## Power and battery
Datasheet-based budget (`hardware_kicad/POWER_BUDGET.md`): ~3.5 mA quiet hear-through,
~7.5 mA loud. 6 h loud needs ~45 mAh; with 20% margin, at least 60 mAh.

## Component picks (research 2026-10-29; stock figures are snapshots)

| Role | Lead pick | Size | Supply | Alternatives |
|---|---|---|---|---|
| nRF5340 module | Raytac MDBT53V-1M (chip antenna) | 7.8 × 12.4 × 1.85 mm | DigiKey 25, $7.00, Active. Low stock is the risk; buy early once chosen. | Insight SiP ISP2053-AX, 8 × 8 × 1 mm, supply unknown (needs a quote). u-blox NORA-B106, 10.4 × 14.2 mm, DigiKey 8,519, $10.89 (safe supply, no size win). |
| Charger / PMIC | Nordic nPM1100 | 2.1 × 2.1 mm WLCSP | Future 6,000; not at LCSC (consignment) | Keep BQ25120A (2.5 × 2.6; LCSC 4) |
| Battery | VARTA CoinPower CP1254 | Ø12.1 × 5.4 mm | 60–77 mAh; Texim "in stock, price on request" | CP1454 (Ø14.1, 85–120 mAh) for longer life; generic 1254 cells need vetting |
| Speaker | Pending: 6–8 mm dynamic driver, or Knowles ED-29689 BA (6.3 × 4.3 mm, 10.2 Ω, ~€26) | | | BA only if the ADAU1860 output can drive 10 Ω |
| Case contacts | 2 pogo pins (VBAT/charge+data, GND) + N52 disc magnets ~3 × 2 mm | ~2.5 mm pitch | Common on LCSC | |

Charging case: USB-C → IP5306 (cheap charger + 5 V boost) or TI BQ25619 (TI's TWS case
reference, SLUAA04) → TPS22910A load switch per bud → pogo pins. 300–500 mAh LiPo pouch
(502030 / 602035 class). Optional DRV5032 lid hall sensor. No microcontroller for a
charge-only first version.

## Size estimate (before CAD)
PCB about 9 × 13 mm (MDBT53V) or 9 × 9 mm (ISP2053), module on top, everything else on the
bottom. Stack: battery 5.4 + board ~3.5–4 + speaker 3–4 mm. Bud about 17 × 20 × 21 mm head
plus nozzle, vs OpenEarable's 16.6 × 34.6 × 21.2 mm shell (35–40% shorter).

## Fit study result (2026-10-29, `haven-hardware#3`, draft)
Packaging models with real part envelopes; all interference checks pass. Previews in
`hardware/mechanical_cad/rev_b_fit_study/`.
- **Bud head 16.7 × 18.9 × 17.5 mm**; with nozzle 22.0–23.5 mm tall depending on module and
  driver (MDBT53V + 8 mm driver: 16.7 × 18.9 × 23.5). About 40% smaller than v1's OpenEarable
  shell by bounding box.
- **The CP1254 battery sets the footprint, not the module.** ISP2053 saves only ~0.9 mm of height,
  so pick the module for supply and radio performance.
- **Speaker: 16–32 Ω dynamic driver.** The ADAU1860 headphone output is only specified at 16/24/32 Ω
  (~30–50 mW); the 10.2 Ω Knowles BA is out. No small 16–32 Ω earbud driver is listed at
  DigiKey/Mouser/PUI, so a real part needs sourcing and measuring.
- **Case 53.5 × 45.5 × 25.5 mm** (1.2 mm walls bring it under 25 mm). A 502030 cell (~250 mAh)
  gives ~1.5 recharges of both buds; a larger cell gives ~3 for a few mm more.
- Assumes a 0.8 mm board (v1 is 1.6 mm; 1.6 adds 0.8 mm height) and that the codec, PMIC and
  passives fit within 1.0 mm on the underside of a 9 × 13 mm board; real placement must confirm.
- Charging pads/magnet sit beside the speaker and the mic stands beside the board; both need a
  short flex or spring contact. The shell is a rounded block for now; the nicer v3 surface comes later.

## Decisions (Paul, 2026-10-29)
- Module: Raytac MDBT53V-1M is the lead. Don't buy now; wait for stock when it's time to order.
- Speaker: 8 mm, 16–32 Ω dynamic driver (more output headroom; only 0.6 mm taller than 6 mm).
- Case: size doesn't matter; use a larger case battery (~3 full recharges of both buds).

## Schematic (2026-10-29, `haven-dev-board-kicad#16`, draft, `kicad_v2/`)
67 parts, 46 nets, ERC 0 (all pins typed passive, so ERC checks wiring only); netlist matches
the intended 46 nets; BOM export works. MDBT53V-1M (39 pins) and nPM1100 (25 balls) checked pin
by pin against Raytac spec Ver.D and Nordic PS v1.2.
- Power: case pogo → nPM1100 (100 mA input limit, 20 mA charge to 4.20 V, 1.8 V buck, ship
  mode) → nRF5340 + ADAU1860. Battery level and in-case detect via ADC dividers. No fuel gauge.
- No button: wake on case insertion, control from the app. One red status LED.
- 11 test/wire pads (SWD, battery, speaker, ship-mode hold, spare GPIO).
- **Firmware needs a new `haven_v2` board target**: codec I2C, I2S and LED move to new pins
  (pin map in `kicad_v2/README.md`); the codec driver itself doesn't change.
- **Finding: v1's schematic is wired wrong** (e.g., the mic DATA pin on GND, the module
  unconnected). The v1 Rev A *board* is correct (checked pad-to-copper), so v2 circuits came from
  the board's verified pad-to-net map, not from v1's schematic. v1's schematic needs fixing before
  it's used as a reference.
- Open: ESD clamp part, a few LCSC numbers, nPM1100 land-pattern check against Nordic's reference
  layout, 8 mm driver part, data over the charge pin (deferred), MDBT53V and nPM1100 must be
  supplied to JLCPCB.

## Firmware board target (2026-10-29, `haven-zephyr-app#25`, draft)
`haven_v2` builds locally (app 156 KB flash / 62 KB RAM; net core 143 KB / 46 KB). No pin
conflicts: P0.05 = AIN1, P0.25 = AIN4, P1.02/P1.03 are the 1 Mbit/s TWIM pins. No button
(`wake_button_init()` returns 0 without `sw0`), console over RTT (no UART). Codec driver
unchanged. Charger CHG/ERR/ship-mode and the two ADC channels are declared but not yet used in code.
To confirm: the 32 MHz crystal load setting against the MDBT53V-1M spec.

## Ergonomic shell (2026-10-30, haven-hardware#4)
The rounded-block fit-study bud was replaced by an organic body fitted against six real ear scans
(HUTUBS HRTF database, TU Berlin, CC BY 4.0; concha widths 11.4–21.6 mm). Files and method in
`hardware/mechanical_cad/v2_ergonomic_shell/`.

| Shape | Worst skin compression | Mean area pressed > 1 mm | Mean contact | Mean protrusion past tragus | Mass |
|---|---|---|---|---|---|
| **Stacked** (driver on canal axis, battery behind, board on top) | 4.5 mm | 323 mm² | 562 mm² | +7.8 mm | 4.63 g |
| Nestled (battery beside driver) | 5.7 mm | 451 mm² | 443 mm² | +7.9 mm | 4.61 g |
| Fit-study block | 5.7 mm | 711 mm² | 598 mm² | +7.8 mm | 5.12 g |

Stacked halves the block's tissue interference; nestled spans ~26 mm, longer than most conchas.
No shape fits every ear yet: 3–5 mm compression remains in the smaller ears (pessimistic near
the nozzle, since the scans close the canal). The parts (Ø12.1 mm battery + 8 mm driver) are the
limit now, not the shell.

**Decision (Paul, 2026-10-30):** keep the current size and the long battery life: CP1254 + 8 mm
driver, stacked layout. No smaller battery, 6 mm driver or second body size for now. Next check is a
real-ear print test (S/M/L tips). The 3D explorer and website now show this shell in the pp3 scan.

## Form factor decision: behind-the-ear (Paul, 2026-11-03)
After comparing five shapes in a scanned ear (stacked pebble, two stems, bean+wing, BTE;
`haven-hardware#5`), v2 is **behind-the-ear (BTE)**: a pod behind the ear holds the battery and
main board; a thin fixed cable runs over the top of the ear to a small in-ear unit with the
speaker, nozzle and tip. It also charges in a case (pads + magnet on the pod).
Why: least pressure in the ear of any concept (1.6 mm in pp3 vs 1.8 for the pebble, 2.7–3.8 for
the rest), sits inside the ear, longest battery (CP1454 in the pod), and the pod's ~18 × 33 mm
board is much easier to lay out than the pebble's ~9 × 13 mm one. Trade-off accepted: it looks like
a hearing aid / pro in-ear monitor, not an earbud.
Defaults to confirm during design: outer mic in the in-ear unit (keeps natural pinna cues for
hear-through; PDM over the cable, ~6 conductors), fixed cable (no connector), CP1454 battery.
Supersedes the pebble-based sizing above.
Confirmed (Paul, 2026-11-04): mic stays in the in-ear unit for better hear-through sound, with a
hand-built 6-conductor cable for the first pair (no catalog cable that thin exists). Fallback if the
harness proves unworkable: mic on the pod, 2-conductor standard receiver wire.

## BTE schematic (2026-11-03, `haven-dev-board-kicad#17`, draft)
Two boards from `tools/gen_v2_bte_schematic.py`:
- **Pod** (`kicad_v2_pod/`, 76 parts): radio, PMIC, codec, LED, charge pads, SWD pads.
  - CP1454 battery at about 40 mA charge.
  - nRF DC/DC inductors not fitted on the first build.
- **In-ear** (`kicad_v2_inear/`, 11 parts, about 6 × 6 mm): mic, decoupling, 33 Ω data resistor,
  cable and speaker pads.
- **Cable** (6 conductors): mic supply, GND, PDM clock and data, speaker pair.
  - The mic stays at the ear for natural hear-through cues. Its PDM clock is 3.072 MHz, with 33 Ω
    source termination on both PDM lines.
  - Fallback: put the mic on the pod (2-conductor cable).
- **ESD:** TI TPD1E05U06 on every cable line and on VBUS.

**Two mic positions (Paul, 2026-11-04):** the in-ear mic is primary. A fallback SPH0641 sits on the
pod (U14) on the same PDM pair, opposite channel: in-ear SELECT low = DMIC0 (the channel firmware
already uses), pod SELECT high = DMIC1 (firmware picks the input). Either or both can be fitted.
Build variants: **6-wire** (in-ear mic) or **2-wire** (speaker-only in-ear unit, pod mic), from
the same boards. The pod mic's port must face outward through the pod shell, away from the head.
ERC 0 on both boards (pod 79 parts/48 nets), and netlists match. nRF pins are unchanged.
Open: TVS LCSC number, a real cable part, speaker part, and the DMIC_CTRL2 edge mapping at bring-up.

## Open risks
1. Module supply (MDBT53V 25 in stock; ISP2053 unknown).
2. nPM1100 and CP1254 aren't easy small-quantity LCSC/DigiKey parts: consignment or another
   distributor.
3. Speaker choice depends on the ADAU1860's minimum load impedance.
4. No programming port on an earbud: plan SWD test pads.
5. Layout at this density is the hardest step; the autorouter failed even on the 5× board.
   Quilter (AI layout) is worth one trial here.

## Plan
1. Size-setting parts (done above).
2. 3D fit study of bud + case with real part envelopes, both module variants
   (`hardware/mechanical_cad/rev_b_fit_study/`, in progress).
3. Paul picks module, speaker, battery.
4. Schematic (new module + charging path + pogo pins), then layout.
5. Case board and shell.

## BTE mechanics result (2026-11-04, hardware PR #6)

- Pod is 19.5 × 33.2 × 11.4 mm and 5.4 g, with a 13 × 27 mm board outline (DXF with keepouts). It compresses < 0.5 mm into all six scanned heads. Done for layout.
- In-ear unit A (mic in ear) is 13.7 × 15.8 × 17.6 mm and 1.6 g, with a 6 × 6 mm mic board. Variant B (speaker only) fits about the same.
- In-ear compression is still 2.2–3.9 mm at the worst spot. That beats the earbud shells but isn't finished. Open item: shrink the concha body or make S/M/L sizes. This doesn't block the board layouts, because the 6 × 6 board fits any of those.
- Cable is 46–56 mm over the helix root. Plan a 55 mm harness, or 50 / 56 mm sizes.
- Next: in-ear board layout (2-layer, 6 × 6), then the pod board layout (6-layer, 13 × 27).

## 2026-11-05: merges, website live, pod board routed
- Paul approved: all open draft PRs merged (hardware #2–#6, kicad #15–#18, zephyr #24/#25, app #16);
  kicad #11 (TAC5301 swap, superseded) left open. Website `main` fast-forwarded to Sanctuary, live.
- Pod board fully routed (kicad PR #19, draft): DRC 0 / unconnected 0 / parity 0. Order with POFV.
- Seal = standard S/M/L ear tip on the 5.4 mm nozzle (unchanged). Next: swappable silicone
  concha sleeves (S/M/L) over the in-ear body for comfort, then the charging case board + shell,
  BOM, and the v2 quote. Paul said no quote emails for now.

## 2026-11-05 (later): earpiece reshape, case, fab files
- **In-ear body moved 3 mm up, nozzle 5.5 → 8.5 mm** (sweep of 6 body offsets on the six HUTUBS
  ears; up was the only direction that helped). Mean worst compression 3.35 → 1.77 mm, mean area
  pressed 201 → 46 mm². Cost: sticks out ~2–3 mm more. pp48 still 2.9 mm, so a real-ear test
  print decides. The bore now meets the driver face at its edge (fine for a sealed IEM, check by ear).
- **Comfort sleeves S/M/L:** S = bare shell; M/L = 0.8 / 1.5 mm soft band over the concha part of
  the body (`sleeves.py`). Seal is still the standard S/M/L ear tip on the nozzle.
- **Case** 48.6 × 50.6 × 49.9 mm (haven-hardware #7) + case board (kicad #20): USB-C → MCP73831 →
  800 mAh LiPo → TPS61023 5 V → spring pins 5.0 mm apart. IP5306 / BQ25619 rejected (light-load
  shutoff / needs an MCU). Spring pin candidate KH-PG2011005-DZ.
- **Pod charge contacts** should be 3.5 mm brass pins, flush with the shell (were recessed 2.3 mm).
- **Fab files** for all three boards: kicad #21. Order list + rough cost: `V2_ORDER.md`
  (ballpark $375–730, likely over the $300 budget; pod board is most of it).
