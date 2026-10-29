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
