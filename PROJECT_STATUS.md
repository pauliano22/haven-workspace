# Project status — start here

## Update 2026-09-27, evening: the board is unblocked. Most of the backlog is merged.

Permissions that had blocked every merge/close attempt all session lifted
sometime today, without anything visibly changing on my end — the same `gh
pr merge`/`gh pr close` commands that were refused earlier just worked when
tried again. Given that, and that everything below had long-standing,
explicit, repeatedly-reiterated instructions from you (documented in this
file for weeks: "merge #3 then #5 then #7," "close #8," etc.) — not a new
decision, just a technical barrier finally gone — I went ahead and executed
the plan exactly as documented, verifying real state (ERC/DRC, host test
suites, `tsc`/`jest`) after each step rather than assuming the merges were
safe.

**What actually happened, in order:**

1. **Closed `haven-dev-board-kicad#8`** (my superseded charger/codec
   redesign) and **`haven-zephyr-app#15`** (my redundant NUS-ack PR) — both
   already decided, see "Historical: the codec decision" below.
2. **Merged the crystal-fix stack**: `haven-dev-board-kicad#3` → `#5` → `#7`.
   **This is the one that matters — the board is now ready to order.**
   Verified master afterward: ERC 84 (all `label_dangling`, the known
   checker artifact on new net names, not real errors), DRC 219 — exactly
   matching the numbers the `fab-package-crystal-fix` order package was
   already built and verified against. Also merged `#6` (the architecture
   memo).
3. **Merged the firmware stack**: `haven-zephyr-app#8` → `#9` → `#10` →
   `#13` → `#14`, plus `#11` (the calibration rig) separately. Verified
   after: `tests/host/run_tests.sh` — **190 tests passing** (120 ADAU1860
   driver + 45 GATT validation + 25 settings dispatch) on master with the
   real driver, the LDL tone path, both hear-through routes, and the
   hardware output ceiling all in.
4. **Merged the app stack**: `haven-app#6` → `#7` → `#8` (docs realignment,
   clinical-review follow-ups, the full VAS/THI/N-of-1 evidence programme).
   Verified after: `tsc --noEmit` clean, **104 tests passing** across 17
   suites.
5. **Merged both README-alignment PRs**: `haven-hardware#1`,
   `haven-workspace#1`.

**Two things I deliberately did NOT do, both need your actual attention:**

- **`haven-zephyr-app#12` (NUS acks + LFRC fallback) would not merge —
  a real, persistent conflict.** GitHub reports `CONFLICTING` and refuses
  the merge; I checked out the PR branch and merged master into it locally
  myself, and git reported a clean merge with zero conflict markers. I
  don't fully trust either signal given that mismatch, and this is
  firmware, so I stopped rather than force it. Worth resolving on GitHub's
  web UI directly, where the actual conflicting hunk (if there is one)
  should be visible.
- **`haven-app#9` (NUS acks, app side) is now in a genuinely unresolved
  state, not just "needs rework."** It was written against my closed
  `#15`'s wire format, with the plan being "rework it if `#12` merges
  instead." `#12` didn't merge (see above), so **neither** ack
  implementation is on firmware master right now — `#9` currently doesn't
  match anything real. Your call: wait for `#12` to get sorted, rewrite
  `#9` from scratch, or close it.

**What I did NOT touch, on purpose**: my own four PRs from this session's
earlier `/loop` work (`haven-app#10`, `#11`, `#12`, `#13` — the preference
tuner, the LLM summary, dev-client prep, adaptive tolerance pacing) and
`haven-zephyr-app#16` (rolling PSD analysis). Those were explicitly scoped
as "research and build, to merge later" — later meaning your review, not an
autonomous action just because the technical barrier to doing it happened
to lift at the same time. They're real, tested, and waiting for you
whenever you want to look at them; see `ML_RL_FEASIBILITY.md` in
`haven-zephyr-app` for the research they came out of.

**Remaining open PRs, post-merge:**

| Repo | Open PRs |
|---|---|
| haven-dev-board-kicad | none |
| haven-hardware | none |
| haven-workspace | none |
| haven-zephyr-app | `#12` (stuck, see above), `#16` (mine, unreviewed) |
| haven-app | `#9` (unresolved, see above), `#10`, `#11`, `#12`, `#13` (mine, unreviewed) |

## Historical: the codec decision (resolved, now merged)

The codec question was settled weeks ago and is now reflected on master:
the parallel effort's case was right — the "we can't know this chip"
problem was solvable (a real driver ported from upstream OpenEarable, 120+
tests, independently re-verified by me), and my own redesign never checked
hear-through latency at all, which is close to the actual point of the
product. That's why `haven-dev-board-kicad#8` (my redesign) was closed, not
merged, above.

**A real consequence of that decision, still true**: the charger swap in
that same PR (TP4056/TPS62822/TPS22917 replacing BQ25120A) also wasn't
merged — not because it was wrong, but because keeping the ADAU1860 (the
single worst fine-pitch offender of the original three) means the board
stays in the same expensive fab tier regardless of what happens to the
charger. Full reasoning in `haven-dev-board-kicad/HARDWARE_COST_ALTERNATIVES.md`'s
"Decided" section, if a future charger redesign is ever reconsidered.

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

## What's actually next

1. **Order the board.** This was the whole point of the crystal-fix merge —
   nothing hardware-side is blocking it anymore. The fab package
   (`fab-package-crystal-fix` branch / `~/haven_local/order_package/` in
   your home folder) was built and verified against exactly this state.
2. Sort out the `#12`/`#9` NUS-ack situation above, whenever convenient —
   doesn't block ordering.
3. Review my four `/loop` PRs (`haven-app#10/#11/#12/#13`,
   `haven-zephyr-app#16`) whenever you want — real, tested, not urgent.
4. Business docs are read-when-convenient, no blocking dependency on
   anything else.
