# Haven v2 BTE: what to order for one pair + case

Status 2026-11-05. Prices are not filled in: get them from the JLCPCB / LCSC / DigiKey quotes when
ordering (no quote requests sent yet, per Paul). Board BOMs are exported from the schematics:
`kicad-cli sch export bom` on `hardware_kicad/kicad_v2_{pod,inear,case}/`.

## Boards (JLCPCB, PCB + assembly)

| Board | Qty in a pair | Spec | Files | State |
|---|---|---|---|---|
| Pod | 2 (order 5, assemble 2–3) | 13 × 27 mm, **6-layer**, 0.8 mm, **via-in-pad filled and capped (POFV)**, 0.09 mm track, 0.2/0.35 mm via, ENIG | `kicad_v2_pod/` (kicad PR #19) | Routed, DRC 0/0/0 |
| In-ear | 2 (order 5) | 6 × 6 mm, 2-layer, 0.6 mm, ENIG | `kicad_v2_inear/` (merged) | Routed, DRC 0/0/0 |
| Case | 1 (order 5, assemble 2) | 44 × 15.5 mm, 2-layer, 1.0 mm, HASL ok | `kicad_v2_case/` (kicad PR #20) | Routed, DRC 0/0/0 |

Gerbers, drill, BOM and placement files: `hardware_kicad/fab/v2_{pod,inear,case}/` (kicad PR #21,
`tools/export_v2_fab.py`). Check every part rotation in JLC's placement preview before paying.

## Parts JLCPCB can't place from LCSC stock (buy separately)

| Part | Per pair | Where | Note |
|---|---|---|---|
| Raytac MDBT53V-1M | 2 | DigiKey / Mouser | Low stock is the risk. Consign to JLC or hand-solder (LGA, 39 pads: hard by hand) |
| Nordic nPM1100-CAAB-R | 2 | DigiKey / Mouser / Future | 0.4 mm WLCSP-25: consign to JLC, not hand-solderable |
| VARTA CP1454 (85–120 mAh) | 2 | Texim / VARTA distributors | Tabbed version for TP8/TP9 |
| 8 mm 16–32 Ω dynamic driver | 2 + spares | Ole Wolff OWR-0860T-16 class | Not yet sourced/measured |
| 6-conductor cable, ~1.5 mm OD, 55 mm + ends | 2 | Hand-built (38–40 AWG litz/magnet wire in sleeve) | No catalog part this thin |
| Ear tips S/M/L, 4.5 mm bore | 1 set each | SpinFit CP145 or generic IEM silicone | |
| 3 × 2 mm N52 disc magnets | 4 (2 pods + 2 case) | Any | |
| Pod charge contacts, Ø1.5 × 3.5 mm brass pins | 4 | Any (cut brass rod) or gold pogo targets | Flush with the pod shell (see case notes) |
| Case spring pins | 4 + spares | Kinghelm KH-PG2011005-DZ, LCSC C2842935 (SMD, 11 mm, 2 mm base) | Stroke unpublished: measure one and set `POGO_WORK_H` in case.py |
| 1S LiPo ~800 mAh with protection board, 603040 class, JST-SH 1.0 mm lead | 1 | Any reputable cell vendor | Check lead polarity |

## Case board
Every placed part has an LCSC number checked on lcsc.com (2026-11-05). JLC can place the whole board.

## Prints (resin, JLC3DP or a local printer)
- Pod shells L/R, in-ear shells L/R: `hardware/mechanical_cad/v2_bte/bte_*_{L,R}.stl`.
- Case base, lid, bottom plate: `case_*.stl` (haven-hardware PR #7).
- In-ear shells: the reshaped body (driver up 3 mm, nozzle 8.5 mm). Print one cheap test pair first
  and try it in a real ear before the full order.
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
