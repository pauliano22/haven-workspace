# Shell options: what we could put Haven in

Researched 2026-09-21 from web search snippets only. No dimensions or prices
below were verified against a product page; treat every item as a lead to check.

Two different problems get called "the shell":

## A. A case for the dev board (73 x 161 mm) - needed now

The dev board is a bench board, not a wearable. It doesn't need a designed
shell. Options, cheapest first:
1. **No case.** Standoffs on a plastic base plate for bring-up. Normal for a first board.
2. **Off-the-shelf project box** at least ~80 x 170 mm inside, with the USB and
   battery connectors cut out. Check inner dimensions before buying; I have not
   verified any specific model.
3. **3D-printed tray or box** from the board's outline. I can generate this from
   the KiCad board file if you want it.

## B. The wearable earpiece (final product) - later

The existing CAD (`hardware/mechanical_cad/haven_dev_board_enclosure_v1/`) and
the S/M/L fit-test prints are size studies for a universal in-ear shape. Real
options for the final part:

| Route | What it is | Good for | Catch |
|---|---|---|---|
| **3D-printed universal shell** (ours) | Print our own shape in resin or nylon, foam tip on the nozzle | Fastest iteration, cheap, matches our electronics exactly | Comfort and acoustic seal vary per ear; resin biocompatibility matters for skin contact |
| **Blank DIY IEM shells** (Alibaba, eBay, Thingiverse "Universal IEM Shell") | Ready-made hollow shells sold for DIY earphones | Cheap way to test fit with real hardware | Sized for small drivers, not our PCB; likely too small |
| **Custom-molded earpieces** (ear impression, as audiologists and monitor makers do) | Shell made from an impression or 3D scan of each ear | Best seal and comfort | Slow, needs per-person scan, expensive for a prototype |
| **Custom sleeves on a universal shell** (e.g. Sensaphonics-style sleeves) | Molded silicone sleeve over a standard body | Good comfort without custom electronics housing | Adds a supplier and a fitting step |

## Recommendation

- Now: no case, or a printed tray for the dev board.
- First wearable test: 3D-print our own S/M/L shells (already done) and check
  fit on real ears. This uses no outside supplier and answers the first
  question: does the size work?
- Later: only if the size works, look at 3D-scan-based custom shells.

## Things to check before any of this

- Skin-contact materials: resin used for anything worn in the ear needs a
  biocompatible grade. Ask the print service; don't assume.
- Acoustics: the seal and vent design change hear-through sound. Test with the
  Teensy or the board, not by ear alone.
- Fit is per person. Test on your dad if he will.

## Sources (search results, unverified)
- https://3dprint.com/270363/are-3d-printed-headphones-finally-here-moondrops-3d-printed-earbuds-for-professional-in-ear-monitoring/
- https://formlabs.com/blog/custom-fit-ear-tips-3d-printing/
- https://www.thingiverse.com/thing:3116121
- https://www.sensaphonics.com/collections/plugs-sleeves
- https://www.head-fi.org/threads/diy-shell-making-re-shell-guide-w-some-pictures-new-finished-ciem-pics.656122/
