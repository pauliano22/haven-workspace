# Haven v3: making the pod the size of a real hearing aid (2026-11-11)

Task 2 of `FABLE_BRIEF.md`. Author: Claude (Fable 5.2). Nothing here is built, ordered or measured.
Sizes marked **generated** came out of the existing shell generator (`hardware/mechanical_cad/v3_slim/pod_v3.py`,
same construction as `v2_bte/bte.py`). Sizes marked **estimate** are arithmetic only.

## The target, from a real spec sheet

| Device | Length | Width (front-back) | Thickness (off the head) | Weight | Source |
|---|---|---|---|---|---|
| Audicus Omni (receiver-in-canal aid) | 28.4 | 12.2 | 8.7 | not given | maker's spec sheet, via search extract |
| Same sheet, second model | 27.8 | 11.6 | 7.4 | not given | same |
| Miracle-Ear Energy RIC R-S | not given | 12.8 | 7.8 | 2.3 g | maker's page, via search extract |
| **Haven v2 pod today** | **33.2** | **17.8** | **11.4** | 5.4 g est. | `v2_bte/bte_pod_R.stl`, measured |

So the target is about **28 × 12 × 8 mm and 2-3 g**. Haven v2 is 5 mm too wide, 3 mm too thick and twice the weight.
(Reconciling the two v2 numbers in the old brief: the STL is current. Its body is 17.8 mm wide; 19.5 mm includes the
cable boss. The 9.2 mm thickness quoted from the explorer does not match the STL's 11.4 mm; trust the STL.)

## Why v2 is fat

1. The battery is a 14.1 mm round can, 5.4 mm tall, sitting **on top of** a 13 mm board with parts **under** the board.
   Width is set by the can, thickness by can + board + parts.
2. The shell generator uses a 1.1 mm wall and 0.4 mm air gap: 3.0 mm added to every dimension.
   Real aids use thinner moulded walls.

## The idea common to concepts A and B: a flat sandwich

- A flat rectangular pouch cell (4 × 10 × 22 mm, "401020" class, about 50-60 mAh, with its own protection board)
  lies against the head-side face of a narrow board, full length.
- **Every** component, including the radio module, goes on the other face. Nothing under the board.
- Board 9.6 mm wide. Wall 0.8 mm, air gap 0.25 mm (**guess**: needs a test print for stiffness and light-tightness).

## Three concepts

| | A: sandwich, same radio module | B: sandwich, smaller radio module | C: keep the v2 board, shrink around it |
|---|---|---|---|
| Body size | **32.4 × 13.0 × 9.0 mm (generated)** | **29.2 × 12.8 × 8.8 mm (generated)** | about 31 × 15.5 × 10.5 mm (**estimate**) |
| Weight | 3.3 g (generated, cell mass estimated) | 3.0 g (same caveat) | about 4.5 g (estimate) |
| Volume vs v2 (convex hull) | 3.5 vs 5.2 cm³, 33 % smaller | 3.1 cm³, 41 % smaller | about 15-20 % smaller (estimate) |
| Vs the real aid | +4 mm long, +0.8 wide, +0.3 thick | +0.8 long, +0.6 wide, +0.1 thick | still clearly bigger |
| Radio | Raytac MDBT53V-1M, 12.4 × 7.8 × 1.85 (datasheet) | Insight SiP ISP2053-AX, 8 × 8 × 1.0 (maker's datasheet summary; drawing not read) | unchanged |
| Battery | 401020-class pouch, 50-60 mAh (seller listings only) | same | VARTA CP1254, 12.1 × 5.4, 60-77 mAh |
| Board | New: 9.6 × 27, 6 layers, parts on one face | New: 9.6 × 24, 6 layers, parts on one face | v2 board re-laid for the review fixes, narrowed to about 12.5 mm |
| Firmware | Unchanged apart from review fixes | New pin map; crystals and DC/DC parts are inside the module, so DC/DC mode becomes possible | Unchanged |
| Extra hardware work | New layout (needed anyway after the review) | New layout + new footprint + new board definition + antenna unknowns | Re-layout only |
| Main risk | Fitting about 78 parts on about 160 mm² of one face | Same density risk, plus antenna on a 9.6 mm wide ground (keep-out rules **not read**), LGA pad pitch not read | Low risk, but does not meet the goal |

Picture, same scale: `hardware/mechanical_cad/v3_slim/pod_size_v2_vs_v3.png`. Shells: `pod_v3_A_thin_R.stl`, `pod_v3_B_thin_R.stl`.

### What is verified and what is a guess

- **Verified from datasheets or measured files:** module sizes, v2 shell size, mic size (3.5 × 2.65 × 0.98), the shells are
  watertight with at least 0.26 mm clearance to every part.
- **From seller listings only:** the pouch cell. 401020 cells are listed at 50-60 mAh, 4 × 10 × 20-22 mm with protection
  board, by generic sellers. I found **no** listing from DigiKey, Mouser, Jauch, Renata or VARTA at this size (Jauch's
  smallest found is 22 mm wide). A battery worn on the head from an unknown seller is the same sourcing problem v2 has.
- **Guesses:** 0.8 mm wall; 0.3 mm swelling allowance; cell mass 1.3 g; that the parts fit one face. My area count:
  about 160 mm² free beside the module, chips and mic need about 60 mm² with spacing, about 55 small parts about 65 mm².
  That is about 78 % full. It needs a trial placement before anyone commits.
- **Battery life (datasheet estimate, never measured):** `POWER_BUDGET.md` gives about 3 mA quiet and 7 mA loud.
  55 mAh gives about 18 h quiet, 8 h loud, less with the phone connected. v2's 85-108 mAh gave about twice that.
- **A 3 mm cell** ("301020" class, maybe 40 mAh) would bring thickness to about 8.0 mm at about 13 h quiet. Not sourced.

### What the sandwich fixes for free

- The pouch cell has its own undervoltage and short-circuit protection: this closes most of review finding 4.
- Charge current drops to about 27 mA (0.5C of 55 mAh): R111 becomes about 22 kΩ (I ≈ 600 V / R, per the pod README).
- The new layout uses the corrected footprints, the right inductor and the slow load switch from the start.

### What it costs

- Parts on one face only makes the routing of the 0.35 mm audio chip harder, not easier. The 6-layer, filled-via process stays.
- The cell lies on bare board: needs an insulating film and no test pads under it.
- About half the battery life of v2.

## The in-ear piece

Haven is hearing **protection**, so it must seal the ear canal. It cannot use the open soft dome real aids use. The foam or
silicone tip stays. What can shrink is the hard body outside the canal (today 15 × 16 × 22 mm, 1.7 g).

| | I1: speaker only, mic on the pod | I2: speaker + mic in the ear |
|---|---|---|
| Parts in the ear | 4.9 × 4.15 mm speaker (Ole Wolff OWR-0504T-16, 16 Ω, DigiKey listing) | same speaker + mic + a 4 × 5 mm board |
| Hard body | about 7 mm across × 8 mm (**estimate**) | about 8 × 9 × 10 mm (**estimate**) |
| Cable | 2 wires, about 1.0 mm | 6 wires, about 1.5 mm |
| In-ear board | none (two wires soldered to the speaker) | needed; JLCPCB cannot assemble it alone |
| Sound | Mic hears from behind the ear, as on every commercial aid of this style; some loss of the outer ear's direction cues | Natural direction cues (Paul's 2026-11-04 decision) |

- The 4.9 mm speaker's loudness in a sealed ear was unknown when this was written (the listed 66.2 dBA at 1 mW / 10 mm is an open-air figure); see the maker's ear-simulator figure under "First draft of I1" below.
  It has to be measured in the ear simulator before it replaces the 9 mm part. A quieter speaker is not a safety problem; too quiet is a usability problem.
- The pod board already has the fallback pod mic (U14), so I1 needs no new electronics.

**First draft of I1 (2026-11-14):** `hardware/mechanical_cad/v3_slim/inear_v3.py` makes a two-part printable capsule
(`inear_v3_body`, `inear_v3_cap`, STEP and STL, both watertight) and `inear_v3_section.png`.
- Body 7.0 mm across x 7.7 mm long, plus the project's standard nozzle (5.4 mm x 5.5 mm, 0.35 mm lip, 2.6 mm bore, no
  vent): 13.2 mm of hard part on the axis, about 0.32 g printed (volume x 1.18 g/cm3) plus the 0.17 g speaker. v2's
  in-ear body is 15 x 16 x 22 mm, 1.7 g.
- The speaker drops in from the back, face to the nozzle; a cap closes the back and carries a 1.1 mm cable stub angled up.
- **Speaker drawing read (2026-11-14):** Ole Wolff preliminary specification Rev 00 (2022-08-25), copy in
  `~/.cache/haven_datasheets/speaker/owr-0504t-16.pdf`. Front cap 4.9 mm across with a 1.3 mm sound hole in its centre,
  widest point 5.1 mm, body 4.1 mm tall, two solder tabs reaching 0.8 mm past the back, 0.17 g. The capsule is sized to that.
- **Loudness in a sealed ear, from the same document: 104 +-2.5 dB SPL at 1 kHz for 0.179 V (2 mW into 16 ohm) in an
  IEC 60318-4 ear simulator**, about 116 dB at 100 Hz, distortion mask 2-6 %. Rated power test 5 mW (0.283 V). This
  replaces the open-air 66.2 dBA figure above as the planning number: the speaker is loud enough for Haven's
  output caps. It is the maker's figure in the maker's jig, a preliminary document, not a measurement in this housing.
- Not designed: wax guard, glue channel, strain relief; the sealed back volume (about 27 mm3) will raise the speaker's
  resonance and has not been modelled.
- It is symmetric, so one print serves both ears. Buy and measure a real speaker before printing.

**Worst-case loudness with this speaker (calculated 2026-11-14, nothing measured).**
**Status:** Paul was asked and answered "do whatever you think is best" (2026-11-14). The resistor is therefore IN the design: 220 ohm 0402 at one speaker tab inside the capsule. The value stays provisional until stage 7 of the bring-up plan and a word with the audiologist; it can be changed on any unit with a soldering iron.
- The audio chip can put 50 mW into 16 ohm (ADAU1860 data sheet, headphone output power), which is 0.89 V. The
  speaker gives 104 dB at 1 kHz for 0.179 V in a sealed ear simulator, and its response mask runs up to about 116 dB
  below 300 Hz and 119 dB near 7 kHz at that same voltage. 0.89 V is 14 dB more: **about 118 dB at 1 kHz and up to
  about 130 dB at the extremes if the chip's output ever went to full scale** (a firmware fault, a wrong register
  write, or feedback howl between the pod microphone and the ear). That is far above the 85 dB cap the app and
  firmware enforce, and those caps are all software.
- A plain resistor in series with the speaker is a limit no software fault can remove. With 220 ohm in series the
  full-scale figure drops by about 23 dB: **about 95 dB at 1 kHz**, roughly 107 dB at the low-frequency extreme.
  It also lowers the amplifier's hiss by the same amount. Cost: the speaker's response changes shape (it is driven
  through a high resistance), which the planned ear-simulator calibration has to correct anyway, and the top level
  available is lower. The value is a choice for Paul and the audiologist; 220 ohm is a starting point, not a result.
- Where: **inside the in-ear capsule, soldered to one speaker tab** (an 0402 resistor fits in the 1.2 mm space
  behind the speaker). Tried on the board on 2026-11-14: there is no legal spot beside the speaker pads W5 / W6,
  because the VBUS and VBAT lines run on inner layers directly under the only gap. A board position would need the
  speaker pads moved; do that only if the capsule position proves awkward.
- This does not replace the chip's own limiter or the software caps. It sits under them.

## Ranked recommendation

1. **Concept A + in-ear I1.** It gets within about 1 mm of a real aid in width and thickness and takes 2 g off, with the
   radio, antenna behaviour and firmware Paul already has. The board must be re-laid anyway.
2. **Concept B** as the following revision if A works and the extra 3 mm of length matters. It adds three unknowns at once
   (antenna, footprint, pin map); do not combine them with a first board.
3. **Concept C** only if a working prototype by a date matters more than size. It will still look big.

Not recommended and outside the brief's constraints, noted for later: a smaller radio chip family than the nRF5340 would
shrink the board further, since the audio path never passes through the radio chip. That is a firmware port.

## Decision (Paul, 2026-11-11): concept A, mic on the pod (I1), half of v2's battery life accepted

Progress since: trial placement passed (69 parts incl. pads on one face, 72 % of the free area, `hardware/mechanical_cad/v3_slim/trial_placement.png`); v3 schematic generated with 0 ERC violations (`hardware_kicad/kicad_v3_pod/README.md`). One consequence found: the pod mic must be a top-port part (SPK0641HT4H-1, 4 x 3 x 1 mm) because the cell covers the board's other face.

**Setback, same day:** placing the real footprints (`hardware_kicad/tools/gen_v3_pod_pcb.py`) fitted only 50 of 67 parts on the one face. The 72 % packing figure was too optimistic (it used smaller rectangles than the real land patterns). Concept A as drawn does not fit. Options: a 17 mm cell (about 40 mAh, about 13 h quiet / 6 h loud) to free part of the bottom face; the smaller radio module (concept B); a 4 mm longer pod; or a squeeze with no routing room. See `hardware_kicad/kicad_v3_pod/README.md`. Size stays about 32 x 13 x 9.2 mm with the shorter cell (board is 0.8 mm, not 0.6: JLCPCB's thinnest 6-layer).

## Printable test shell (2026-11-12, generated, not printed)

`hardware/mechanical_cad/v3_slim/pod_v3_shell.py` makes a hollow two-part shell from the rounded form: a head-side tray
(`pod_v3_shell_tray_R.stl`, about 0.6 g) and a lateral lid (`pod_v3_shell_lid_R.stl`, about 0.45 g), 0.8 mm wall, split
at the board plane with a 0.4 mm slip lip. Both meshes are watertight; every part envelope sits inside the cavity
(`pod_v3_shell_sections.png`). Outside 12.6 x 33.2 x 10.0 mm. Estimated pod weight with it: shell 1.05 g + cell 1.1 g +
board and parts about 1 g (**estimate**) = about 3.2 g.

Found while drawing it:
- **Charge contacts do not reach the outside.** The charge pads are on the board's bottom face, about 3.5 mm inside the
  head-side wall (the cell's thickness). The shell has two 1.4 mm holes there as placeholders, but a charger's pins
  would need to reach 4 mm into them. Options: spring pins or short posts soldered to the pads so they end flush with
  the shell; move the contacts to the pod's bottom end; or contacts on the lateral face. Undecided. This also affects
  the case design.
  **Decision (Paul, 2026-11-13): spring pins.** Two surface-mount spring pins soldered to the charge pads P1 / P2,
  ending flush with (or 0.3-0.5 mm proud of) the head-side shell face. Needed height: board bottom face (z = -0.4) to
  the outer surface there (z = -4.4, measured on the tray mesh) = **4.0 mm compressed**. Not yet done: choose a real
  pin (about 4.0-4.5 mm tall, body under 1.8 mm; no part number checked), check its land pattern against the 1.2 mm
  pads on the board, size the shell holes to it, and change the case to flat contacts. Skin contact: the pins sit
  against the head, so plating and recess depth need a look (`MATERIALS_AND_ASSEMBLY.md`).
  **Pin chosen in principle (2026-11-14).** Two LCSC parts with the same drawing, datasheets read: Xinyangze
  YZ160615045R-01 (C5157428) and Kinghelm KH-PG204505-DZ (C2842924). Base 2.0 mm x 0.5 mm, barrel 1.5 mm up to 3.0 mm,
  plunger 1.0 mm, 4.5 mm free, 3.5 mm working, 1 A, brass with gold over nickel. Stock and price not confirmed.
  The board's charge pads are now 2.0 mm lands for it. In this shell (4.0 mm from the board to the outside) the 4.5 mm
  pin stands 0.5 mm proud against the head and is pressed flush by a flat charger contact (half its working travel).
  A 4.0 mm pin of the same family would sit flush; whether one is stocked was not found. **Pick the length after
  the cell is measured**, because the cell's thickness sets that 4.0 mm. The shell's 1.4 mm holes already clear the
  1.0 mm plunger; the barrel ends 0.2 mm short of the wall. Open: comfort and nickel exposure of a proud metal tip
  on skin; effect of two 3 mm metal posts 1 mm from the antenna keep-out.
  **Contact land and cradle (2026-11-14).** The head-side face slopes about 25 degrees at the pins, so a flat charger
  pad would hit the shell first. The tray is now cut flat there (z = -4.4, 5.4 x 4.0 mm, `LAND_*` in
  `pod_v3_styled.py`) and thickened inside to keep 0.8 mm of wall. With the 4.5 mm pin the tip stands 0.5 mm proud
  of the land, so **the 4.5 mm pin is the one to buy** (no 4.0 mm pin needed). Charging cradle designed:
  `hardware_kicad/kicad_v3_cradle/README.md`.
- The module and the cell touch the wall in places (cover 0.75-0.77 mm against a 0.8 mm wall): there is no air gap
  there. With the cell's +-0.5 mm thickness tolerance, a thick cell will not fit. Measure a real cell first.
- Hole positions (wire, mic, contacts) follow the board drawing; left/right ear handedness is not checked.
- No latch, seal, magnet pocket or print-orientation work. It is for judging size and feel only.

## Decisions that were open (now settled above)

1. A, B or C.
2. Mic in the ear (I2, his earlier decision) or on the pod (I1, smaller and simpler).
3. Accept about half of v2's battery life for the size.

## Next steps if A is chosen (in order, none started)

1. Trial placement of all parts on one 9.6 × 27 mm face, no routing: proves or kills the density guess. About a day of scripting.
2. Find a pouch cell from a seller that publishes a real datasheet and safety certificates; ask Texim/VARTA and Jauch for a 10 mm wide cell.
3. Test print of the 0.8 mm wall shell (a few dollars at JLC3DP) to judge stiffness and feel behind the ear. Paul can wear an empty shell.
4. Full layout with the review fixes, handedness check, DRC, quote.
5. Add v3 to the website explorer next to v2 and the typical aid (publishing needs Paul's go-ahead).

## Sources

- Audicus Omni spec sheet: https://audicus.com/omni-spec-sheet
- Miracle-Ear Energy RIC R-S: https://www.miracle-ear.com/hearing-aids/features-benefits/rechargeable/meenergy-ric-r-s-bliss
- ISP2053: https://www.nordicsemi.com/Nordic-news/2021/12/The-ISP2053AX-from-Insight-SiP-employs-nRF5340-SoC , https://www.digikey.com/en/product-highlight/i/insight-sip/isp2053-dual-core-module (LCSC C5741989; prices seen $10-25)
- 401020 cells: https://www.ufinebattery.com/products/3-7-v-60mah-lithium-ion-battery-401020/ , https://ydlbattery.com/products/ydl-401020-55mah-3-7v-lithium-polymer-battery-4x10x22mm-with-ph2-0-connector
- Speaker: https://www.digikey.com/en/products/detail/ole-wolff-electronics-inc/OWR-0504T-16/19285332
