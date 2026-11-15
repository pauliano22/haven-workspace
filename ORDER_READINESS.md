# Can we order the first v2 build? Readiness checklist

> **2026-11-11: DO NOT ORDER the v2 pod, the in-ear board or Rev A.** An independent review found that every footprint
> converted from the EasyEDA files is a mirror image (audio chip, load switch, codec crystal, both microphones, LED transistor),
> plus an under-rated power inductor and a load switch that is too fast. Details and fixes: `DESIGN_REVIEW_2026-11.md`.
> The library and generator are fixed; the boards are not re-laid yet. `hardware_kicad/tools/verify_v2_order_files.sh` now fails
> until they are (it runs `check_footprint_handedness.py`). All earlier "DRC clean / ready to quote" statements are superseded.


Started 2026-11-07. One line per thing that has to be true before money is spent. Status words:
**Verified** (checked, evidence given), **Open** (not yet checked), **Blocked** (needs Paul or an outside answer).
Nothing has been ordered. Cost figures are labelled as quote or estimate.

## Boards

| Check | Status | Evidence / what's left |
|---|---|---|
| Pod, in-ear and case boards pass KiCad DRC, zero unconnected pads, zero schematic mismatches | **Verified** 2026-11-07 | Re-run by me on KiCad 9.0.9: 0 / 0 / 0 on all three |
| Fab files (gerbers, drill, parts list, placement) are current with the board files | **Verified** 2026-11-07 | Export script re-run in a scratch copy; every layer, parts list and placement file identical (drill and job files differ only by date). The case board was edited after the first export (its USB-C footprint and part numbers), so I regenerated it: the output is identical |
| Pod module pin wiring matches the firmware's board file | **Verified** 2026-11-06 | 39 of 39 pins, netlist diff |
| Mic audio can reach the microcontroller (codec to nRF I2S) without a board change | **Verified** 2026-11-07 | Net `/DOUT`: codec ball B1 to nRF pin P0.31, declared in the `haven_v2` pin file |
| JLCPCB can build the pod to the design's numbers | **Open: browser quote task running** | See "What the stricter rules found" below. Only JLCPCB's own review settles it |
| Every placed part has an LCSC number | **Verified** | Only U1 (Bluetooth module) and U2 (power chip) have none, on purpose: bought separately |
| LCSC stock for every placed part today | **Open: browser quote task** | Last seen stock figure for the audio chip: 116 (2026-10-29) |
| How JLCPCB handles U1 and U2 (supplied by us) | **Open: browser quote task** | |
| Part rotations right in JLCPCB's placement preview | **Open: browser quote task** | Script warns WLCSPs, SOT-23/563 and the USB-C differ from KiCad's zero |
| Power chip footprint matches Nordic's land pattern | **Open** | Our pads: 25 at 0.2 mm, 0.4 mm pitch (0.2 mm gap). Nordic's drawing could not be fetched (their site redirects to an index). Download the nPM1100 product specification and app note nAN-038 in a browser |
| 32 MHz crystal load setting matches the Bluetooth module's spec | **Open: a mismatch found 2026-11-07, firmware only** | Raytac's MDBT53V-1M spec (Ver.D, section 3, p.17) lists the crystal as 32 MHz, CL 8 pF, 20 ppm, inside the module, and says the default on-chip load capacitor is **12.5 pF** (CAPVALUE 0x0C). The `haven_v2` board file sets **8 pF** (`load-capacitance-femtofarad = <8000>`), copied from OpenEarable's board. Not changed blind: OpenEarable may have tuned its value, and layout strays differ. A wrong value shifts the radio frequency a little and can hurt Bluetooth reliability. No board change needed. Resolve at bring-up by measuring the carrier frequency error on the first pod, or by asking Raytac. Spec copy: `~/.cache/haven_datasheets/raytac_MDBT53V-1M_spec.pdf` |
| 32.768 kHz crystal | **Verified consistent** | Raytac: the module has no 32.768 kHz crystal inside, an external one is expected; their reference uses internal load caps (6 pF default). Haven fits the crystal with external 9 pF caps and the firmware says `external`, so board and firmware agree. Fallback exists: the firmware's "LFRC fallback" build (internal RC oscillator, see the firmware README). Measure at bring-up |

### What the stricter rules found (pod)
KiCad's DRC passes under the project's own rules. I added JLCPCB's published multilayer limits as extra
rules (copy of the board in a scratch folder, nothing changed in the repo):
- **Audio chip (ADAU1860, U15) is 56 balls at 0.35 mm pitch with 0.25 mm pads.** Gaps between pads are
  0.10 mm, against JLCPCB's general 0.15 mm pad-to-pad figure. 92 hits, all on this chip. JLCPCB's
  page allows tighter track spacing locally at BGA pads but states no pad-to-pad exception, so this
  needs their answer.
- **Via hole to track or copper fill: 0.15 to 0.195 mm, against a published 0.2 mm.** About 205 hits (79 with
  tracks, 97 with fill). The vias are the smallest JLCPCB allows (0.15 mm hole, 0.25 mm pad).
  Whether JLCPCB treats this as a fail, a warning, or fine is unknown.
- Track width 0.09 mm sits exactly on JLCPCB's minimum for 1 oz copper. No margin.
- Not a violation: filled-and-capped vias are the default on 6-layer boards, and the 0.8 mm thickness and
  ENIG finish are available.
Worst case: JLCPCB asks for a redesign or a more expensive process tier. That would be found before paying.

## Parts and money

| Check | Status | Evidence / what's left |
|---|---|---|
| Bluetooth module (MDBT53V-1M) obtainable | **Verified** 2026-11-07 | DigiKey Marketplace: 30 in stock, $7.00 each plus $25 flat shipping, about 14 days |
| Power chip (nPM1100) obtainable | **Verified** 2026-11-07 | Mouser 6,221 at $1.92, DigiKey 6,374 at $2.17 |
| Battery (VARTA CP1454, tabbed) obtainable from a source worth trusting | **Blocked** | No DigiKey or Mouser listing; retail resellers are unvetted. Leads found 2026-11-07: Texim Europe (VARTA distributor) lists the CP1454 A3, 85 mAh, 14.1 mm wide, 5.4 mm high, part 63145101501-VAR, listed without tabs ([datasheet](https://texim-europe.com/getfile.ashx?id=110796)). The newer **A4X** is 108 mAh and 5.1 mm high ([datasheet](https://www.texim-europe.com/Cmsfile/VAR-CP1454%20A4X-DS-230703-TE.pdf)), a better fit if the tag version exists. **No source confirms a tabbed version of either.** Do not solder wires to a lithium cell. Needs a question to Texim (draft below), which Paul has to approve sending |
| Pod charge current is safe for the battery | **Verified against a secondary source** 2026-11-07 | Pod charges at about 40 mA (R111 15 kΩ; Nordic's table gives 30 kΩ = 20 mA, 12 kΩ = 50 mA). The CP1454 A3 datasheet (an older version, read through a search extraction) lists standard charge 42.5 mA (0.5C), fast 85 mA (1C), 4.20 V, charge temperature 0 to 45 °C. The pod has a battery temperature sensor input. Re-check against VARTA's current datasheet, and against the A4X sheet if that cell is chosen |
| 8 mm speaker chosen and measured | **Open** | Candidates listed in `V2_ORDER.md`; thickness unknown until one is in hand |
| Over-ear cable (6 wires, hand-built) | **Open** | Needs a build and a bend test. Fallback exists: 2-wire cable with the mic on the pod |
| Case spring-pin stroke | **Open** | Measure one pin, set `POGO_WORK_H` |
| Real total price | **Open: browser quote task** | Estimate only: $375 to $730 against a $300 budget |
| Shipping for printed test shells | **Blocked** | JLC3DP needs a sign-in (Paul) |

## Pod board price drivers (real JLCPCB quote, 2026-11-07, PCB only, 5 boards, not signed in)

Total $101.86 + about $26.60 shipping, 7-8 day build. Lines: base $32.00, ENIG $16.60, Tg155 $3.32 (forced),
**0.15 mm via $33.17**, **4-wire Kelvin test $16.57 (forced by the 0.15 mm via)**, deburring $0.20.
Choosing the 0.15 mm via is therefore worth about $50 of the $102.

Via census of `haven_v2_pod.kicad_pcb` (counted with pcbnew): 96 vias with a 0.15 mm drill (0.25 mm pad),
47 with 0.20 mm (0.35 mm pad). The 0.15 mm vias: 28 near the audio chip (U15), 21 near the radio module (U1),
19 near the power chip (U2), and about 28 single vias beside small parts. Only the singles look easy to
enlarge. The ones under the chips are fan-out for the 0.35 mm pitch parts, so going to 0.20 mm would mean
rerouting. **Not done, no layout change made.** If budget forces it, this is the lever to price after
JLCPCB's own design review says whether 0.20 mm is even possible there.

Not yet quoted: in-ear board, case board, assembly (JLCPCB standard assembly pads the board to 71 x 71 mm,
2-5 boards), shipping for JLC3DP. The sign-in page blocked the browser helper, so no design-review verdict yet.

## Real JLCPCB quotes, 2026-11-07 23:35 (signed in as Paul; quote only, nothing in cart, nothing ordered)

Full text and screenshots: `/mnt/c/Users/pmi/claude-bridge/done/2026-11-07-2010-haven-jlcpcb-quotes.md` and its `screens/` folder.
Projects are auto-saved in Paul's JLCPCB account (pod, inear, case).

| Board | What was quoted | Total (before shipping) |
|---|---|---|
| Pod (6L, 27 x 13 mm) | 5 PCBs $103.83 + assembly of 2 boards $165.45 (setup $51.50, 24 parts $34.97, extended-part fee $37.20, stencil, fixture, X-ray). **Excludes** radio module U1, power chip U2, mic U14 | **$269.28** (380 g) |
| In-ear (2L, 6 x 6 mm) | 5 bare PCBs $44.07. JLCPCB refuses to assemble anything under 10 x 10 mm; on its V-cut panel it forces 240+ boards. Quoted $121.47 with the mic short on stock | **$44.07 bare**; assembly impractical, hand-solder 3 parts or panel it |
| Case (2L, 15.5 x 44 mm) | 5 PCBs $28.34 + economic assembly of 2 boards $39.42 | **$67.76** |

**Answers to the open questions**
- JLCPCB will fabricate all three as drawn at the instant-quote level. No rejection. The 0.15 mm via and filled vias force Tg155 and a Kelvin test; still no track/space option to choose for 6 layers.
- **No design-check verdict exists yet.** JLCPCB's engineers review after payment. JLCDFM (jlcdfm.com, separate free tool) is the pre-check and has **not** been run. That is the next thing to try for the 0.35 mm audio chip and the 0.09 mm tracks.
- Shipping is not known until checkout; the web estimate of $26.60 was for a 0.14 kg parcel.

**Fix list found by the quote**
1. Pod `R112,U8`: a resistor labelled U8 mixes prefixes; JLCPCB left it unplaced. Rename it. (File edit, not yet done.)
2. Pod mic U14 (SPH0641LU4H-1, C2879853): flagged "difficult"; extra fees possible after review. The in-ear mic has the same part and JLCPCB had 181 of the 240 needed.
3. Pod U1 (radio) has no stock at JLCPCB; U2 (power chip) has 1. Both must be bought elsewhere and sent in (consignment) or hand-fitted.
4. Case: JLCPCB's pin-1 marks for U1 (MCP73831) and U2 (TPS61023) disagree with the silkscreen. Check the placement file rotations or tick "confirm parts placement" when ordering.
5. Case R5 (732 kohm): JLCPCB has 11, needs 20. Pick another stocked 732 kohm 0402.
6. Radio module footprint, audio chip and battery are untouched by any of this.

**Budget, honestly:** boards alone (pod $269 + in-ear $44 + case $68) are about **$381**, before shipping, before the radio module, power chip, battery, drivers, shells, tips and tax. That is more than the $300 target without anything else. The pod is 71% of the board spend.

## JLCDFM, consignment, codec region, test print (browser task of 2026-11-08 01:10; nothing ordered)

Full text: `/mnt/c/Users/pmi/claude-bridge/tasks/2026-11-08-0010-haven-prechecks.md`. Screenshots in `screens/`.

**JLCDFM (JLCPCB's free design checker) on the pod: no overall pass/fail, only counts, and many are "danger".**
It lists (danger / warning): annular ring 100/0 (tool itself says via flags can be ignored), trace width 53/8
(the 0.09 and 0.10 mm tracks), pad spacing 58/41 (0.10 mm between 0.25 mm via pads, worst 0.05 mm), hole-to-trace
clearance 30/70 (0.16 mm), via to pad 2/50. It found the audio chip's 0.2 mm ball pads as "BGA pads" with no BGA-specific
error, no via-in-pad flags and no soldermask sliver flags. **Read:** the board sits at JLCPCB's 6-layer limits. Nothing says
"cannot be made", but expect their engineers to query it after payment, which can add days. The two via-to-pad spots at 0.05 and
0.06 mm and the 0.05 mm pad gap are the ones worth fixing or accepting knowingly. Case: 2 via-to-pad and 4 hole-spacing
dangers around the USB-C footprint plus silkscreen clipping.

**Radio module and power chip.**
- Power chip nPM1100: JLCPCB stocks the reel variant `-R7`, LCSC **C7016010**, 1,323 in stock at $1.94. I set U2's LCSC field to it and
  rebuilt the pod files (DRC 0, files current). **Confirm in JLCPCB's match screen that C7016010 really is NPM1100-CAAB-R.**
  That should remove the power chip from the "bring your own parts" list.
- Radio module MDBT53V-1M: JLCPCB part C6300378, 0 in stock, **pre-order at about $23.50 each**. Consigning my own (DigiKey $7 + $25
  shipping) means shipping to JLCPCB's Hong Kong warehouse with 2% handling (min $10), customs paperwork and extra days, so pre-order may be
  the simpler route. Not decided; U1's LCSC number is still blank in the files.
- JLCPCB does not hand-place parts it doesn't stock. It machine-places consigned parts.

**ADAU1860 region question, answered.** The datasheet (Rev. C) says the two variants share all specs and features and the
same package; only the ordering region differs. Plain ADAU1860 = for customers in China; ADAU1860-1 = outside China. In practice
the US channel sells only the plain part: DigiKey lists the "-1" as discontinued (0 stock), Mouser says it does not sell it in our region,
and ADI's own Sample & Buy for the US lists only `ADAU1860BCBZRL` (about $9.24 at 1k). Our BOM part (LCSC C17592940, 116 in
stock, $12.49) is the plain one. So the order is practical, but I have not seen anything on whether ADI minds a non-PRC buyer. ADI also
points to a newer part, **ADAU1797A**; not evaluated. Datasheet also confirms a microphone-to-serial-output path exists (graphs
labelled "DMICxx to SDATAO_x").

**Shell test print.** All 10 parts are in the JLC3DP cart (not checked out): $3.20 of parts, shipping about $6.19 to your saved address,
coupons currently bring the subtotal to $0.00. The two `sleeve_M` parts carry a thin-wall warning; the helper did NOT accept the risk box.
Ships about 11 Nov if ordered. Needs Paul's go-ahead.

## Chip research, 2026-11-07 night (web search only; pages that timed out are marked)

**Audio chip variant and price (NEW, needs checking before any order).**
- Our pod BOM uses `ADAU1860BCBZRL` (LCSC C17592940). Mouser's product page says the **ADAU1860 is orderable only by customers in China, and the ADAU1860-1 by customers outside China**. DigiKey lists `ADAU1860BCBZRL` at **$20.20 each** (LCSC $12.49, 116 in stock, JLCPCB charged $24.73 for the 2 on the pod quote) (3,310 in stock) and shows the `-1` reel part as discontinued there.
- I could not read ADI's FAQ or Mouser's page (both timed out), so I do not know whether the two parts differ in silicon or only in sales region, or whether a buyer in the US can legally order the non-"-1" one. **Open: ask ADI, or check at the JLCPCB BOM match stage.**
- $20 per chip makes the audio chip the most expensive single part on the pod, more than the module ($7) and power chip ($2) combined. Not yet in the budget table.

**Radio module alternatives (all nRF5340, so the firmware and pinout logic carry over, but the board footprint does not):**
- Insight SiP ISP2053-AX, 8 x 8 x 1 mm, about $14 at Mouser (316 in stock, page undated).
- u-blox NORA-B1 family, 10.4 x 14.3 x 1.7 mm (about 3,100 NORA-B100 at DigiKey, undated).
- Ezurio (ex-Laird) BL5340, as small as 15 x 10 x 2.2 mm.
- Fanstel BT40 family; smallest (BT40C/M) 8.4 x 12.3 x 1.5 mm.
- The nRF54L15 is not an option for Bluetooth audio: it has no audio PLL (Nordic forum).
- None is cheaper than the Raytac MDBT53V-1M ($7). Reason to look later: stock (the Raytac is only 30 units, from a marketplace seller with 14 days and $25 shipping) and size. Changing it means redoing the pod layout. **No change recommended for the first order.**

**Audio chip alternatives:** the search found nothing new. Same-family ADAU1797A (recommended for new designs per ADI) is a possible swap; its package was not shown, so unverified. Earlier work already compared TLV320AIC3100/AIC3254/TAC5301 (see `hardware_kicad/TAC5301_EVALUATION.md`, `HARDWARE_COST_ALTERNATIVES.md`) and decided to keep the ADAU1860 for latency.

**Power chip:** nPM1300 (QFN, charger + fuel gauge + two bucks) exists as a bigger sibling of the nPM1100. Nothing found that needs it. Its DigiKey price shown in the search was a reel price, ignore it.

## Software and safety

| Check | Status | Evidence / what's left |
|---|---|---|
| Firmware for the v2 board compiles | **Verified** 2026-11-06 | Local build at `9915c56` |
| Firmware logic tests | **Verified** 2026-11-07 | 9 suites pass, run against fake hardware |
| Current firmware still runs on real hardware | **Verified** 2026-11-07 | Nordic dev board boots, advertises, restores settings |
| Receiving mic audio on the microcontroller | **Open** | Firmware transmits only today; receive not written |
| App running on a real phone | **Open** | Never done |
| Loudness limit measured on the built device | **Open, required before anyone wears it** | Needs a measurement setup and a chosen limit |
| ADAU1860 datasheet on disk to check register behaviour | **Open: browser task** | The PDF is not on this machine |

## Reading this honestly
Nothing found so far says the boards cannot be ordered. The unknowns that could stop an order are
JLCPCB's verdict on the pod, the battery source, and the budget. The first two are being resolved
now. Even after an order, the largest risk is unchanged: no sound has gone through Haven electronics.

## Draft message to Texim (NOT sent; Paul decides)
Subject: VARTA CP1454 A3 / A4X with solder tags, small quantity to the US

Hello, I am building a small prototype wearable and want the VARTA CoinPower CP 1454 (A3 85 mAh, or the
A4X 108 mAh) with SMD or PCB solder tags, for a first run of 4 to 10 cells. Do you stock a tagged version,
and what is its part number? Can you ship to the United States, and what are the unit price and minimum
order? If you do not sell tagged cells in small quantities, can you recommend a distributor who does?
Thank you.
