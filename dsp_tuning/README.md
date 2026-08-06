# dsp_tuning

SigmaStudio project files and filter/limiter configurations for the ADAU1860
DSP live here once they exist.

**Status (2026-08-06): empty.** No SigmaStudio project (`.dspproj`) or exported
filter files have been created yet — a filesystem-wide search turned up
nothing. The biquad notch/peaking-cut math has so far only been implemented
directly in C (see `../legacy_prototypes/tinnitus_dsp` and
`../firmware/haven_zephyr_app/src/adau1860.c`), not authored in SigmaStudio.

When a SigmaStudio project for the ADAU1860 is started, it belongs here:

- `haven_dsp.dspproj` (or similar) — the SigmaStudio project itself.
- Exported parameter/coefficient files used by `haven_zephyr_app`'s
  `adau1860_apply_filters()` to know the parameter RAM address map.
- Any limiter/safety-cap configuration exported from SigmaStudio — this is
  the **firmware-side counterpart** to the app's hard-coded output ceiling
  (`haven_custom_app/src/constants/safety.ts`); see that project's
  `docs/safety.md` for why an independent hardware limiter is required, not
  optional.
