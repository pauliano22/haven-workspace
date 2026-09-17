# Project status — start here

A single map of everything in flight across all 5 repos, written because
there are now two substantial, independent bodies of work sitting in 15
open PRs plus 4 new research docs, and reconstructing that from scratch
every time you sit down is real overhead. This is the orientation doc —
read this first, then follow the links into whichever PR/doc actually
needs your decision.

## Decided: keep the ADAU1860. Don't merge my redesign.

The codec question is settled — the parallel effort's case
(`haven-dev-board-kicad#6`, `haven-zephyr-app#9`) is right: the "we can't
know this chip" problem was solvable (they ported a real, working driver
from upstream OpenEarable, 120+ tests, independently re-verified by me),
and my redesign never checked hear-through latency at all, which is close
to the actual point of the product. Don't merge `haven-dev-board-kicad#8`.

**A real consequence of that decision, worth knowing**: the charger swap
in that same PR (TP4056/TPS62822/TPS22917 replacing BQ25120A) *also*
shouldn't be merged for now — not because it's wrong, but because keeping
the ADAU1860 (the single worst fine-pitch offender of the original three)
means the board stays in the same expensive fab tier regardless of what
happens to the charger. Verified this is real (PCB fab pricing is set by
the whole board's worst-case feature size, not per-component), so the
charger swap wouldn't actually reduce the ~$500 quote that started this
investigation — and it's also unrouted and untested. Full reasoning in
`haven-dev-board-kicad/HARDWARE_COST_ALTERNATIVES.md`'s "Decided" section.

**The fastest real path to an orderable board**: merge just the
crystal-placement fixes (`#3`→`#5`→`#7` below), skip the codec and charger
work entirely for this first order, ship close to the stock design.

## What needs your click, right now

I've fully reviewed all of the parallel effort's PRs myself — read the
actual code, independently reproduced their key technical claims, ran
their real test suites (not just trusted the PR descriptions). They're
good. I can't merge or close PRs myself; Claude Code's own permission
system blocks that regardless of what you tell me verbally, and working
around it isn't something I'll do. **On `haven-dev-board-kicad`, merge
`#3`, then `#5`, then `#7`, in that order** (each builds on the last) —
that's the crystal-placement fix, the one thing actually blocking an
order. Everything else below is real and good but not blocking.

## The two bodies of work

### Mine, this session — narrower, mostly paused pending the above

| Repo | PR | What | Status |
|---|---|---|---|
| haven-dev-board-kicad | [#8](https://github.com/pauliano22/haven-dev-board-kicad/pull/8) | Charger swap + codec/mic swap | **Superseded, close it** — see "Decided" above |
| haven-zephyr-app | [#15](https://github.com/pauliano22/haven-zephyr-app/pull/15) | NUS TX acks, firmware side | **Redundant** — close, `#12` below does this better |
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

1. Merge `haven-dev-board-kicad#3` → `#5` → `#7` — unblocks ordering a
   working board. This is the one time-sensitive item.
2. Close `haven-dev-board-kicad#8` (my redesign) — superseded by the
   decision above, on both the codec and charger halves.
3. Merge the firmware stack (`haven-zephyr-app#8`→`#9`→`#10`→`#13`→`#14`)
   and the app stack (`haven-app#6`→`#7`→`#8`) whenever convenient — real,
   tested, good work, but doesn't block ordering the PCB itself.
4. Resolve the NUS-ack duplication: close my `haven-zephyr-app#15`, merge
   `#12` instead; then decide whether my `haven-app#9` needs reworking to
   match `#12`'s wire format or can also close.
5. Business docs are read-when-convenient, no blocking dependency on
   anything else.
