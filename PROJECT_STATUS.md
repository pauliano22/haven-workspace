# Project status — start here

A single map of everything in flight across all 5 repos, written because
there are now two substantial, independent bodies of work sitting in 15
open PRs plus 4 new research docs, and reconstructing that from scratch
every time you sit down is real overhead. This is the orientation doc —
read this first, then follow the links into whichever PR/doc actually
needs your decision.

## The one thing that actually needs a decision from you

**Two competing analyses of the codec question, both substantive.** Read
`haven-dev-board-kicad#6` and `haven-zephyr-app#9` before merging anything
codec-related on either side. Short version: my own redesign
(`haven-dev-board-kicad#8`) replaces the ADAU1860 to escape its fine-pitch
BGA package and its "we can't know this chip" tooling problem. A parallel
effort shows that problem was solvable (ported a real, working driver from
upstream OpenEarable) and raises something my redesign never checked at
all — hear-through latency, which is close to the actual point of the
product. Full trace in `haven-dev-board-kicad/HARDWARE_COST_ALTERNATIVES.md`'s
"STOP" section near the end.

**What's *not* in question**: the charger swap (`haven-dev-board-kicad#8`'s
commits 1-2, TP4056/TPS62822/TPS22917 replacing BQ25120A) stands on its
own regardless of how the codec question resolves.

## The two bodies of work

### Mine, this session — narrower, mostly paused pending the above

| Repo | PR | What | Status |
|---|---|---|---|
| haven-dev-board-kicad | [#8](https://github.com/pauliano22/haven-dev-board-kicad/pull/8) | Charger swap (sound) + codec/mic swap (contested, see above) | Charger half ready for review; codec half paused |
| haven-zephyr-app | [#15](https://github.com/pauliano22/haven-zephyr-app/pull/15) | NUS TX acks, firmware side | **Redundant** — `#12` below does this better |
| haven-app | [#9](https://github.com/pauliano22/haven-app/pull/9) | NUS TX acks, app side | Needs rework if `#12` merges instead (different wire format) |

### The parallel effort (victorzhu443) — broader, deep, mostly ADAU1860-keeping

Real, substantial, well-tested work spanning ~a week
(2026-09-11 → 2026-09-15). Each repo's PRs mostly stack in order.

**haven-dev-board-kicad** — foundational research, then placement fixes:
- [#3](https://github.com/pauliano22/haven-dev-board-kicad/pull/3) Hardware review resolved against upstream OpenEarable firmware (register map, I2S master/slave direction, DIN/DOUT — found the original port had this backwards)
- [#5](https://github.com/pauliano22/haven-dev-board-kicad/pull/5) → [#7](https://github.com/pauliano22/haven-dev-board-kicad/pull/7) Crystal/decoupling placement fixes (the exact issue flagged earlier this session, actually fixed here)
- [#6](https://github.com/pauliano22/haven-dev-board-kicad/pull/6) The architecture memo — **read this one**

**haven-zephyr-app** — a complete ADAU1860 bring-up path:
- [#8](https://github.com/pauliano22/haven-zephyr-app/pull/8) Coefficient format verified (Q5.27) — closes a real roadmap item
- [#9](https://github.com/pauliano22/haven-zephyr-app/pull/9) The real driver, ported from upstream — **read this one**
- [#10](https://github.com/pauliano22/haven-zephyr-app/pull/10) LDL tone path over the real driver
- [#11](https://github.com/pauliano22/haven-zephyr-app/pull/11) Calibration rig (turns `level_db` into measured dB SPL) — closes another real roadmap item
- [#12](https://github.com/pauliano22/haven-zephyr-app/pull/12) NUS acks (better version of my `#15`) + an LFRC clock fallback
- [#13](https://github.com/pauliano22/haven-zephyr-app/pull/13) A second hear-through path via the codec's EQ engine, as a fallback if the FastDSP route is silent
- [#14](https://github.com/pauliano22/haven-zephyr-app/pull/14) Hardware output ceiling (third safety layer, after app clamp + firmware watchdog)

**haven-app** — docs alignment + a real clinical-evidence framework:
- [#6](https://github.com/pauliano22/haven-app/pull/6) Docs realigned to the real ADAU1860 path; new `calibration.md` and `clinical-basis.md` (cites real literature, and **21 CFR 874.3400** — a tinnitus-masker device category worth knowing about, now in `REGULATORY_POSITIONING.md`)
- [#7](https://github.com/pauliano22/haven-app/pull/7) Clinical-review follow-ups (octave check for pitch matching, LDL-aware match level, LDL drift warning)
- [#8](https://github.com/pauliano22/haven-app/pull/8) A real evidence programme — weekly VAS, THI, a proper 4-week N-of-1 trial with randomized blocks

**haven-workspace / hardware** — one README-alignment PR each, both about
the same "codec owns the audio path, mic is PDM not I2S" correction.

None of this is merged. All of it compiles/tests clean on the
contributor's own fork CI, none of it has run on real hardware yet.

## The 4 business/research docs (this workspace root)

- **`REGULATORY_POSITIONING.md`** — marketing language, not the hardware,
  decides whether this needs FDA clearance. Three real buckets identified:
  PSAP, hearing protector (probably the best fit), tinnitus masker (a
  fourth-wall the app's tinnitus features could accidentally hit).
- **`FUNDING_RESEARCH.md`** — a real company with a recent (2023) NIOSH/CDC
  SBIR track record in almost exactly this concept; real contact names.
- **`MARKET_POSITIONING.md`** — real competitor prices; active/electronic
  hearing protection commands 4-10x what passive/adjustable does.
- **`IP_LANDSCAPE.md`** — a real, active patent (through 2036) on
  personalized active hearing protection exists; not a blocker necessarily,
  but real counsel should see this before commercializing.

## A reasonable order to go through all this, whenever you have time

1. Read `haven-dev-board-kicad#6` and `haven-zephyr-app#9` (30-45 min) —
   this unblocks everything else hardware/firmware-related.
2. Decide: keep-and-fix-the-ADAU1860 (the parallel effort's direction) or
   replace-the-codec (my direction) — or measure first, per `#6`'s own
   suggested ~$200/one-week latency experiment.
3. Once decided, the losing side's PRs can close and the winning side's
   can start getting real review/merge attention.
4. The charger swap (`haven-dev-board-kicad#8` commits 1-2) can be
   reviewed independently of all of the above, any time.
5. Business docs are read-when-convenient, no blocking dependency on
   anything else.
