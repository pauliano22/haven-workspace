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
