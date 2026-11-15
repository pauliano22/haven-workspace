# Haven v2 BTE: what to order for one pair + case

> **2026-11-11: DO NOT ORDER the v2 pod, the in-ear board or Rev A.** An independent review found that every footprint
> converted from the EasyEDA files is a mirror image (audio chip, load switch, codec crystal, both microphones, LED transistor),
> plus an under-rated power inductor and a load switch that is too fast. Details and fixes: `DESIGN_REVIEW_2026-11.md`.
> The library and generator are fixed; the boards are not re-laid yet. `hardware_kicad/tools/verify_v2_order_files.sh` now fails
> until they are (it runs `check_footprint_handedness.py`). All earlier "DRC clean / ready to quote" statements are superseded.


Status 2026-11-05. Prices are not filled in: get them from the JLCPCB / LCSC / DigiKey quotes when
ordering (no quote requests sent yet, per Paul). Board BOMs are exported from the schematics:
`kicad-cli sch export bom` on `hardware_kicad/kicad_v2_{pod,inear,case}/`.

## Boards (JLCPCB, PCB + assembly)

| Board | Qty in a pair | Spec | Files | State |
|---|---|---|---|---|
| Pod | 2 (order 5, assemble 2–3) | 13 × 27 mm, **6-layer**, 0.8 mm, **via-in-pad filled and capped (POFV)**, 0.09 mm track, 0.2/0.35 mm via, ENIG | `kicad_v2_pod/`  | Routed, DRC 0/0/0 |
| In-ear | 2 (order 5) | 6 × 6 mm, 2-layer, 0.6 mm, ENIG | `kicad_v2_inear/` (merged) | Routed, DRC 0/0/0 |
| Case | 1 (order 5, assemble 2) | 44 × 15.5 mm, 2-layer, 1.0 mm, HASL ok | `kicad_v2_case/` | Routed, DRC 0/0/0 |

Gerbers, drill, BOM and placement files: `hardware_kicad/fab/v2_{pod,inear,case}/` (
`tools/export_v2_fab.py`). Check every part rotation in JLC's placement preview before paying.

## Parts JLCPCB can't place from LCSC stock (buy separately)

| Part | Per pair | Where | Note |
|---|---|---|---|
| Raytac MDBT53V-1M | 2 | DigiKey Marketplace (sold by Raytac) | Checked 2026-11-07: 30 in stock, $7.00 each, **+$25 flat shipping**, ~14 days. Not at Mouser. Consign to JLC or hand-solder (LGA, 39 pads: hard by hand) |
| Nordic nPM1100-CAAB-R | 2 | Mouser (949-NPM1100-CAAB-R) or DigiKey | Checked 2026-11-07: in stock at both (6,221 / 6,374), $1.92 / $2.17 each. 0.4 mm WLCSP-25: consign to JLC, not hand-solderable |
| VARTA CP1454 (85–120 mAh) | 2 | **Source unresolved** | Checked 2026-11-07: not at DigiKey or Mouser. Retail resellers only (rechargeable Li-ion, sold as headset battery, $10–25), unvetted, and the tabbed version is unconfirmed. Ask VARTA or Texim directly. Avoid unknown marketplace cells for a battery worn on the head |
| 8 mm 16–32 Ω dynamic driver | 2 + spares | AliExpress: [NSC Audio 8 mm 16 Ω PU+Ti](https://www.aliexpress.us/item/3256811665047808.html) $12.80 / pair (4.9★, 4k sold), or [JCD 10-pc 8 mm 32 Ω TWS](https://www.aliexpress.us/item/3256810394275219.html) ~$5 / 10 | Thickness not listed: ask seller / measure. OWR-0860T-16 dropped: DigiKey only sells 10,000-pc reels (2026-11-06). Shell rebuilds for any size: `HAVEN_DRIVER=8.0x3.9 python3 bte.py`; 8 mm fits better (mean worst 1.53 vs 1.76 mm) |
| 6-conductor cable, ~1.5 mm OD, 55 mm + ends | 2 | Hand-built (38–40 AWG litz/magnet wire in sleeve) | No catalog part this thin |
| Ear tips S/M/L, 4.5 mm bore | 1 set each | SpinFit CP145 or generic IEM silicone | |
| 3 × 2 mm N52 disc magnets | 4 (2 pods + 2 case) | Any | |
| Pod charge contacts, Ø1.5 × 3.5 mm pins, **gold-plated on a nickel-free base** (decided 2026-11-07; was "cut brass rod": brass can contain nickel and these touch skin) | 4 | Ask the supplier to confirm no nickel underplate. Fallback: 316L stainless | Flush with the pod shell (see case notes) |
| Case spring pins | 4 + spares | Kinghelm KH-PG2011005-DZ, LCSC C2842935 (SMD, 11 mm, 2 mm base) | Stroke unpublished: measure one and set `POGO_WORK_H` in case.py |
| 1S LiPo ~800 mAh with protection board, 603040 class, JST-SH 1.0 mm lead | 1 | Any reputable cell vendor | Check lead polarity |

## Case board
Every placed part has an LCSC number checked on lcsc.com (2026-11-05). JLC can place the whole board.

## Prints (resin, JLC3DP or a local printer)
JLC3DP quote 2026-11-06 (9600 resin, not signed in): **$0.32 per part**, 3-day build; shipping needs sign-in. JLC3DP has **no flexible resin**: print sleeves in 9600 for the fit test (rigid = worst case).
- Pod shells L/R, in-ear shells L/R: `hardware/mechanical_cad/v2_bte/bte_*_{L,R}.stl`.
- Case base, lid, bottom plate: `case_*.stl` (merged).
- In-ear shells: the reshaped body (driver up 3 mm, nozzle 8.5 mm). Print one cheap test pair first
  and try it in a real ear before the full order.
- Optional: 8 mm-driver earpiece shells (`inear8_{L,R}.stl` in the test-print zip) to compare fit side by side.
- Comfort sleeves M / L: `sleeve_{M,L}_{L,R}.stl`, in flexible resin for the test (silicone later).

## Rough cost (ballpark, NOT a quote)
Typical JLCPCB / distributor pricing from memory; real numbers come from the quote step.

| Item | Rough range |
|---|---|
| Pod PCB, 6-layer, ENIG, POFV, 5 pcs | $60–150 (POFV is the big adder) |
| Pod assembly, 3 boards, both sides, setup + extended-part fees + parts (ADAU1860 etc.) | $100–200 |
| MDBT53V-1M ×3 + nPM1100 ×3 from DigiKey/Mouser, shipped to JLC | $35–60 |
| In-ear PCB + assembly (mic, 2 passives) | $30–50 |
| Case PCB + assembly | $30–50 |
| Resin prints: pods, in-ear units, sleeves, case | $30–60 |
| CP1454 ×2, drivers ×2, LiPo, spring pins, magnets, ear tips, wire | $50–90 |
| Shipping (2–3 orders) | $40–70 |
| **Total** | **~$375–730** |

This is likely **over the $300 budget**. The pod board is most of it. Ways down, in order:
cheapest first-article only (2 pods, skip spares); skip POFV by moving to a 0.4 mm-pitch-friendly
codec/PMIC fan-out (a redesign, not recommended); hand-assemble the case board.

## Known small things
- Pod BOM "U8" is a 1 MΩ resistor (kept v1's reference).
- Pod nRF DC/DC inductors L101/L102 are DNP on the first build (module runs in LDO mode).


## Real JLCPCB quotes (2026-11-07 23:35, quote only, nothing ordered)

Pod: PCB $103.83 (5) + assembly $165.45 (2 boards, without radio module, power chip and mic) = **$269.28**.
In-ear: bare PCB **$44.07** (5); JLCPCB will not assemble a 6 x 6 mm board (10 x 10 minimum, panels force 240+ boards).
Case: PCB $28.34 + economic assembly $39.42 = **$67.76**.
Boards alone: about **$381** before shipping and before the radio module, power chip, battery, drivers, shells and tips.
Details, fix list and the missing design-check verdict: `ORDER_READINESS.md`. This replaces the earlier $60-150 pod PCB
guess in the table above: the pod is the largest single cost, about 71% of the board spend.
