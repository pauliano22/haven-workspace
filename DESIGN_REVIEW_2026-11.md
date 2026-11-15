# Haven v2 pod: independent design review (2026-11-11)

Reviewer: Claude (Fable 5.2), task 1 of `FABLE_BRIEF.md`. Worked from the exported netlist
(`kicad-cli sch export netlist`), the board file read with pcbnew, and the datasheets in
`~/.cache/haven_datasheets/` (ADAU1860 Rev C, nPM1100 PS v1.5, Raytac MDBT53V-1M, AP22916 DS44758,
Knowles SPH0641LU4H-1). **The review was cut short by a usage limit; the "not reviewed" list at the end is real.**

## Recommendation: DO NOT ORDER. Fix finding 1 first; it makes every board dead.

## Findings, most severe first

### 1. FATAL: every footprint converted from the EasyEDA files is a mirror image

- **What:** the library footprints made by `hardware_kicad/extracted/gen_footprints.py` copy EasyEDA's pad
  coordinates without negating y. EasyEDA's footprint y axis points up, KiCad's points down, so each footprint is
  mirrored top to bottom. For symmetric 2-pin parts this does not matter. For the parts below it does.
- **Evidence (two independent datasheets):**
  - ADAU1860 Figure 8 (top view): A1 top-left, columns 1-8 to the right, rows A-G downward. Library file
    `BGA-56_...-TL.kicad_mod`: A1 at (-1.22, +1.05), G1 at (-1.22, -1.05), i.e. row A at the bottom. On the board U15 is
    on the bottom side with A1 (96.38, 103.55), A8 (98.83, 103.55), G1 (96.38, 105.65): seen from the top it looks like the
    datasheet's top view, so seen from the chip's own side it is mirrored.
  - Knowles land pattern (top view): pins 1/2 on the left, 5/4 on the right, port ring at the bottom. The library mic footprint
    is the mirror of that (cannot be matched by any rotation).
  - Control: U2 (nPM1100), U1 (module) and the case board's SOT parts use hand-made or KiCad-standard footprints and have the
    correct handedness. U15 and U2 sit on the same side with opposite handedness, so one of them must be wrong.
- **Parts affected on the pod:** U15 audio chip (rows A-G reversed: every ball on the wrong pad), U3 load switch (VIN/VOUT and
  GND/ON swapped), CRYSTAL1 (crystal terminals land on the ground pads), U14 pod mic, Q2 LED transistor (gate/source swapped).
  **In-ear board:** U13, the main microphone, same footprint, same fault.
- **Not affected:** U1, U2, passives, diodes, LED, X1, test pads. The case board is fine (its JLCPCB pin-1 warnings are
  placement-file rotations, a separate small issue).
- **Fix:** negate y in the generator (or mirror each affected footprint), re-place U15, U3, CRYSTAL1, U14, Q2 and U13, and
  re-route their connections. The U15 fan-out is the hardest routing on the board, so this is real layout work, then DRC,
  fab export and a new JLCDFM run. Add a check to `verify_v2_order_files.sh` that compares A1/pin-1 handedness per part.
- **Rev A (v1) board, NOT verified:** it uses the same library and its U15 (front side) shows the same mirrored pattern.
  The notes say pads matched the ported copper, which suggests the whole Rev A board may be a mirror image of the real
  OpenEarable board. Do not order Rev A either until someone checks one chip against its datasheet.

### 2. HIGH: buck inductor L2 is the wrong kind of part

- **What/where:** L2 = TDK MLZ1005M2R2WT000 (LCSC C383389), 0402 multilayer, on nPM1100 SW (A4) to +1V8.
- **Evidence:** nPM1100 PS Table 20 requires 2.2 uH, DCR <= 400 mohm, Isat >= 350 mA. LCSC lists this part as DCR 550 mohm
  and saturation current 60 mA (rated 350 mA is a heating limit). I read the LCSC listing, not the TDK datasheet.
- **Effect:** the inductor saturates at normal load; expect high ripple, poor efficiency, possibly an unstable 1.8 V rail.
- **Fix:** a power inductor meeting Table 20, e.g. an 0603/0806 metal-alloy 2.2 uH (Nordic's reference uses 0806). Needs a
  bigger footprint, so do it in the same layout pass as finding 1.

### 3. HIGH: switching on the codec rail will probably reset the radio

- **What/where:** U3 = AP22916**B** (fast version) switches +1V8 onto V_LS, which carries C33/C34/C41 (3 x 10 uF) plus about 3 uF more.
- **Evidence:** AP22916B slew rate at 1.8 V is 13 mV/us (datasheet timing table). 24-33 uF x 13,000 V/s = 0.3-0.4 A of inrush
  for about 100 us. The nPM1100 buck is limited to 400 mA and its own output capacitors are 14.7 uF nominal. The nRF5340
  needs VDD >= 1.7 V and the rail is 1.8 V (-2 %/+8 %, up to 80 mV ripple), so there is about 0.1 V of margin. Calculated, not measured.
- **Fix:** change U3 to **AP22916CCA4-7** (slow version, same package and pinout, 1 mV/us, inrush about 30 mA) and raise
  `supply-delay-us` in `haven_v2_nrf5340_cpuapp.dts` from 300 to about 6000 (turn-on time is 3.8 ms).

### 4. MEDIUM (safety): nothing stops the unprotected battery from over-discharging

- **Evidence:** nPM1100 PS section 3.7 says the battery pack must contain undervoltage and overcurrent protection. The CP1454
  has none. The buck only stops at VINT about 2.8 V, and the dividers and chip keep drawing after that. The firmware has no
  battery monitor or ship-mode code (`grep` of `src/` finds none; the devicetree only declares the pins).
- **Fix:** firmware must read VSYS_SENSE and enter ship mode (SHPACT high >= 200 ms) at about 3.3 V before anyone wears it.
  Better: a cell or small protection circuit with undervoltage cutoff. Until then, bench use only with a protected supply.

### 5. LOW: items to tidy or measure

- C102/C103 (1 uF on DECR/DECD) are fitted while L101/L102 are not. Raytac's LDO-mode reference leaves those pins
  unconnected. Mark C102/C103 not-fitted too, or fit the inductors and use DC/DC mode. Effect of the extra capacitance: unverified.
- VSYS and DEC capacitors are 0402 10 uF; at 4.2 V they lose a large part of their value (Nordic's reference uses 0603). Accept for a prototype, measure ripple.
- D1 (5.5 V signal ESD diode) on the 5 V charge pad has little margin and little energy rating. Acceptable for a prototype.
- LED transistor Q2 is driven with 1.8 V at the gate; its on-resistance at that voltage is not specified by me. LED brightness unverified.
- Battery can sits about 9 mm from the antenna, next to the head. Range unverified until measured.
- When V_LS is off, firmware must hold the codec's I2S, PD and clock pins low so they do not back-power the chip. Not checked in code.

### Status of the findings (updated 2026-11-12)

- Findings 1-3: fixed in the v3 pod design (`hardware_kicad/kicad_v3_pod/README.md`). The v2 pod files are unchanged and still must not be ordered.
- Finding 4: firmware now has `src/battery_guard.c` (on by default for the haven_v2 board, `CONFIG_HAVEN_BATTERY_GUARD`).
  It reads VSYS every 10 s and enters ship mode after 3 readings below 3.30 V with no charger attached. Decision rule
  has host tests (`tests/host/test_battery_guard.c`, 9 checks pass); firmware builds for haven_v2 and the dev kit.
  **Not run on hardware**: the threshold, the ADC reading with a 1 Mohm divider and whether SHPACT cuts power as
  expected all need a bench check. The v3 pouch cell also has its own protection circuit.

## Checked and found correct

- nPM1100: every ball matches PS Table 23; fixed 100 mA input limit (ISET = D- = AVSS, D+ open) matches Table 10; VTERMSET high = 4.20 V;
  10 kohm on NTC is the documented way to disable it; R111 = 15 kohm sits between the table's 11 kohm (50 mA) and 30 kohm (20 mA);
  capacitor set matches reference configuration 3; nRF drive levels meet VIH 1.1 V.
- ADAU1860: all 56 balls match Table 13; supplies within range (HPVDD_L 1.2 V to HPVDD); REG_EN to AVDD; CM 1 uF; PD has an
  internal pull-down; 2 kohm I2C pull-ups as the datasheet asks; address pins low matches firmware address 0x64.
- Crystals: X1 (C48615) is a 7 pF part and the 9 pF capacitors suit it; CRYSTAL1 (C7294677) is a 20 pF part and 33 pF capacitors suit it.
- Module: all 39 pins match the Raytac pin table; footprint handedness matches Raytac's top view; VDD and VDDH tied (normal-voltage mode);
  antenna keep-out is clear of copper (3.8 mm, full width); firmware regulators are in LDO mode, which matches the missing inductors.
- U3 pin assignment (A1 VOUT, A2 VIN, B1 GND, B2 ON) matches the datasheet; mic, ESD diode and Q2 pin numbers match their datasheets.
- Earlier fixes: U8 is now R116. nPM1100 LCSC C7016010: **not confirmed by me** to be NPM1100-CAAB-R7; check on JLCPCB's match screen.

## Not reviewed (ran out of budget)

Trace widths for the headphone and supply pins, decoupling placement distance, the 32 MHz load setting (8 pF vs 12.5 pF, needs a
measurement), the JLCDFM items one by one (they will change anyway after the re-layout), the hex of ROM_BOOT_MODE/SELFBOOT strapping
against OpenEarable, in-ear and case schematics beyond the mic and the two SOT parts.

## What would change the recommendation

Order only after: (1) footprints regenerated and the five pod parts plus the in-ear mic re-laid and re-checked against their
datasheets by handedness, (2) L2 replaced, (3) U3 changed to the C version. Finding 4 does not block an order but blocks wearing it.
