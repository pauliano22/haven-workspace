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

Gerbers, drill, BOM and placement files are not exported yet; that's the step before quoting.

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
| Case spring pins, SMD, ~9.8 mm tall, ≥ 1 mm travel | 4 + spares | Mill-Max / LCSC "pogo pin" | Part not chosen; check against the 2.2 mm seat |
| 1S LiPo ~800 mAh with protection board, 603040 class, JST-SH 1.0 mm lead | 1 | Any reputable cell vendor | Check lead polarity |

## Case board gaps
LCSC numbers still blank for: 4.7 µF 0603, 10 µF / 22 µF 0805, 0402 resistors (5.1k, 4.02k 1%,
1k, 732k 1%, 100k 1%), red 0603 LED, JST-SH SM02B-SRSS-TB, 1 µH 2520 inductor (≥ 1.5 A sat).
All are common basic parts; pick them in JLC's part search when quoting.

## Prints (resin, JLC3DP or a local printer)
- Pod shells L/R, in-ear shells L/R: `hardware/mechanical_cad/v2_bte/bte_*_{L,R}.stl`.
- Case base, lid, bottom plate: `case_*.stl` (haven-hardware PR #7).
- **Before printing the in-ear shells:** the current in-ear body presses too hard into all six
  scanned ears (see HAVEN_V2.md). A reshaped body (driver moved up ~3 mm and a ~3 mm longer
  nozzle) is being evaluated; print that one, plus one cheap test print first.

## Known small things
- Pod BOM "U8" is a 1 MΩ resistor (kept v1's reference).
- Pod nRF DC/DC inductors L101/L102 are DNP on the first build (module runs in LDO mode).
