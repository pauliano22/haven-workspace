# dsp_tuning

Lark Studio projects and exported FastDSP / EQ memory images for the
ADAU1860 live here once they exist.

**Status (2026-09-10): empty, but the picture has changed.** The ADAU1860 is
not programmed with SigmaStudio — ADI's tool for this chip ("Lark") is
**Lark Studio** (www.analog.com/ADAU1860; see the EVAL-ADAU1860 User Guide,
UG-2017). Its "Download to Target" step writes plain `uint32_t` memory
images to the FastDSP program/parameter banks; upstream OpenEarable checked
exactly such an export in as `open-earable-2/src/drivers/Lark-fdsp.c` (five
biquad slots, then expander, volume, mute, mixer, limiter). There is no
`.dspproj`, no parameter-RAM address map to discover, and no `ADISIGM` blob:
the slot addresses are fixed by the chip (program at `0x40008000`, banks at
`0x40008100 + bank*0x500 + slot*0x100`) and coefficients are written at
runtime via the safeload registers in Q5.27 fixed point.

What belongs here once someone with a Windows machine opens Lark Studio:

- `haven_fastdsp.<lark project ext>` — a FastDSP schematic whose **input is
  the DMIC (PDM mic) path**, not I2S/ASRCI as upstream's is, so the
  mic → 5 biquads → limiter → DAC hear-through loop runs entirely inside
  the codec. Set the schematic `fs` equal to `FDSP_RATE_SOURCE` (UG-2017):
  upstream frame-clocks FastDSP from the 192 kHz DMIC stream.
- The exported `uint32_t` arrays (program + three parameter banks), dropped
  into `haven_zephyr_app/src/` in place of the upstream Lark program.
- The limiter slot's parameters — this is the **firmware-side counterpart**
  to the app's hard-coded output ceiling
  (`haven_custom_app/src/constants/safety.ts`); see that project's
  `docs/safety.md` for why an independent hardware limiter is required, not
  optional. Note the ceiling is not physically calibrated until commanded
  level has been measured against dB SPL on real hardware.

Alternative worth testing before building the above: the codec's separate
hardware EQ engine has an explicit input-select register (`EQ_ROUTE`); if the
DMIC/FDEC channel can be routed into it, hear-through may need only register
writes. Unverified — see `HAVEN_HARDWARE_REVIEW.md` §0 in
`haven-dev-board-kicad`.
