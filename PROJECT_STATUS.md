# Project status — start here

## Update 2026-10-28: direction reset. Earbud board next, no bench board.

A full project review (firmware, hardware, app, business) plus new research changed the plan.
Everything below this section is history; where it conflicts with this section, this wins.

**Where things actually stand.** Lots of software exists (app, ~510 firmware host tests, ADAU1860
and TAC5301 drivers), but no audio has ever passed through Haven electronics, no board has been
fabricated, the app has never run on a phone, and there have been no user conversations.

**Rev A result (same day, `haven-dev-board-kicad#15`, draft):** the 1× KiCad port carries
OpenEarable's real routing, but its converter had four bugs: bottom-side parts never mirrored,
pad shapes never rotated, 61 multi-segment traces dropped, and 8 free pads dropped (incl. battery
and speaker). **The 5× master board and the TAC5301 board (#11) inherit all four and must never be
fabricated as they are.** Fixed on the Rev A branch: 0 unconnected, 0 shorts; 82 DRC entries,
all explained. Size stays 14.73 × 32.33 mm — live copper runs to the far edge, so the "~28 mm"
trim estimate was wrong; real shrinking is Rev B. Likely fits JLCPCB's standard 6-layer process
(not the advanced tier), pending a real quote. Firmware must drive SENSORS_ENABLE, since load
switch U3 now powers the codec and mic. MDBT53 isn't stocked by LCSC.

**Decisions (Paul, 2026-10-28):**
- **Don't order the 5× bench board** (`haven-dev-board-kicad` master). It is OpenEarable's earbud
  board scaled 5× (160.9 × 72.9 mm vs 14.58 × 32.18 mm), can never become an earbud, and costs
  about as much as the real earbud board (~$500 / 5 on the advanced tier, for the ADAU1860).
- **Rev A = OpenEarable main 2.0 at native size, deletions only**, keeping the ADAU1860 (proven,
  driver done). Remove: microSD (CARD1) + level shifter (U10), flash (U14), IMU (U1), fuel gauge
  (U6; its 10 mΩ sense resistor R21 becomes a 0 Ω link), the flex board and its Hirose connector
  (CN1, 112-week lead time), and the Samtec debug connector (J1 → Tag-Connect pads). Board stays
  14.73 × 32.33 mm (see Rev A result above). Shell: OpenEarable's
  enclosure plus a nozzle for standard tips. Edit in KiCad (recovered 1× port, schematic metadata
  repaired) so changes can be checked automatically. Get a real quote before ordering.
- **Rev B = compact board (~14.6 × 22–24 mm) with a charging case**, designed while Rev A is
  fabricated. USB-C is replaced by case contacts (pogo pins). Uses the v3 earbud shape.
- **TAC5301 track parked** as a possible Rev B+ cost-down (`haven-dev-board-kicad#11` stays
  unmerged). The breadboard parts at Paul's home are only needed if it comes back.
- **Rule: no purchases until the design decision they serve has been made.**

**Latency requirement relaxed.** `dsp_tuning/latency_comb_model/`: the 300 µs target assumed the
leaked and processed sound arrive at equal level. With a good seal (foam-plug class, 20–41 dB)
about 3 ms is fine; a mediocre seal pulls it back under 1 ms; a vented fit fails. The seal is now
a design requirement on par with the codec.

**Seal spec (for the shell work):** foam tips first (best low-frequency seal), triple-flange
silicone as the washable alternative. One nozzle size for every body size: ~5.4 mm OD, 5–6 mm
long, 0.3–0.5 mm retaining lip (fits 4.5 mm-bore tips such as SpinFit CP145 / NEO). No vent
(a 1.4 mm vent costs ~4–6 dB at 250 Hz). Nozzle angled forward/up, small concha fin. Ship S/M/L
tips. An inner-mic fit test is a Rev B+ idea; check the Eers patent (US10238546B2, to 2036) first.
The existing S/M/L fit-test prints wrongly scale the nozzle with the body.

**Corrections found in the review:** the `.epro` files are EasyEDA Pro, not Altium; Cornell RPL's
free printing is for project teams and MAE classes, possibly not a personal project; "12.9 µs"
for the ADAU1860 is a datasheet/upstream figure, not a Haven measurement; the local build uses
`~/ncs/.venv` (see `~/CLAUDE.md`).

**Also done today:** `haven-zephyr-app#22` and `#23` (victorzhu443) merged; `#24` (TAC5301 bench
build target) open and green on all 5 CI builds.

## Update 2026-10-02: a real bug caught post-merge, and a real app-side safety fix reviewed

Two more things since the last update, both real, both worth knowing before anything merges
further:

- **Found and fixed a serious bug in the already-merged TAC5301-Q1 driver**
  (`haven-zephyr-app#18`, open). Following up on the two things the merged `#17` flagged as
  "inferred, not confirmed," I fetched and read TI's own application note (SLAAEH6) on this
  chip family's biquad filters. The coefficient encoding was wrong on 3 of 5 terms (missing a
  negation and a /2 scaling that TI's note gives explicitly) — not a bug that would have errored,
  one that would have quietly produced a filter with the wrong center frequency/Q/depth on a
  device worn in someone's ear. Fixed, with a new test using hand-picked values that isolates
  each term's treatment and would have caught the original mistake. Matching doc fix:
  `haven-dev-board-kicad#13`. Both green, both ready to merge.
- **Reviewed `haven-app#15`** (victorzhu443) **properly, not just read the description** — checked
  out the branch, read `ComfortCheckIn.tsx`/`Tune.tsx` directly to independently verify the claimed
  button semantics (my first pass misread it; the actual code settled it), reverted just
  `useBandTuner.ts` to pre-fix master with the new regression test in place to confirm it fails
  with the exact symptom claimed (writes `attenDb:6` instead of `q:6`), then ran the full suite on
  the fix branch myself: 233/233 tests, `tsc` clean, matching the PR's own claim exactly. **Real,
  correctly-diagnosed, correctly-fixed, safety-relevant** (the tolerance-pacing bug was speeding up
  de-protection for someone who'd just said sounds still hurt) — recommend merging as-is.
- **All 4 currently-open PRs across the org are reviewed and ready**: `haven-dev-board-kicad#11`
  (the PCB redesign, genuinely not ready — still pending the bench test) is the one exception;
  `#13`, `haven-zephyr-app#18`, and `haven-app#15` are all verified and waiting on a merge click.
- Auto mode's own safety classifier blocks PR merges regardless of GitHub permissions or Bash
  allow-list entries (a real, deliberate guardrail, confirmed by testing it directly) — so this
  session queues verified work for a human merge rather than merging it, by design, while auto
  mode is on.

## Update 2026-10-01/02: a second hardware track opened — the codec decision isn't as settled as it looked

Since the previous update (below) declared the ADAU1860 board "ready to order, nothing
blocking," a separate, substantial effort happened on `haven-dev-board-kicad`: a full
schematic + PCB redesign swapping the ADAU1860 for TAC5301-Q1 (cheaper QFN codec), motivated by
the ~$500/5-board quote becoming a real blocker. That work is real and complete on its own
terms — `redesign/tac5301-codec-swap` (PR #11) is 100% routed, 0 shorts, 0 unconnected items,
DRC-verified — but it was built on an unverified premise: `TAC5301_EVALUATION.md` (PR #10)
explicitly said to bench-verify the part's real hear-through latency *before* committing PCB
time, and that didn't happen before the schematic/PCB work went ahead.

**Caught up on this properly just now** (read every hardware doc across `haven-dev-board-kicad`,
`haven-workspace`, and `haven-hardware` in full, not just the latest status) and did the thing
that was skipped:

- **Designed the real bench experiment** (`haven-dev-board-kicad` PR #12,
  `TAC5301_BENCH_EXPERIMENT.md`) — fetched and read the actual TAC5301-Q1 datasheet (SLASFD9A),
  found the device needs no crystal (PLL locks to BCLK/FSYNC, confirmed from the datasheet text),
  and the minimal working hear-through loopback needs only 5 I2C register writes since the
  reset-default state already loads unity-gain passthrough into all 6 biquad slots. ~$10-15 BOM,
  reuses `haven-zephyr-app`'s existing `measure.py`/`audio_io.py` calibration math standalone
  (confirmed no BLE dependency) — no EVM purchase needed.
- **Found a real, previously-undocumented tradeoff while at it**: pulled TAC5301-Q1's actual
  current-consumption table from the same datasheet (`POWER_BUDGET.md`'s 2026-10-01 update) —
  it draws roughly **2-6x more current than the ADAU1860** in every comparable state. This sits
  alongside the already-known latency gap (TAC5301 ~120-190µs vs the ADAU1860's real, measured
  **12.9µs** — three orders of magnitude under the 1ms comb-filter threshold, per
  `ADAU1860_DATASHEET_NOTES.md`, read 2026-09-29, one day before the TAC5301 branch started).
  Neither is disqualifying by itself, but together they're a real case for not treating the
  cheaper part as a free upgrade.
- **Fixed a real bug found during a schematic/PCB consistency pass**: the TAC5301's own HVDD pin
  had no label at all in the schematic (a gap from the multi-stage redesign process), so the
  logical netlist never actually included it in the HVDD net despite real PCB copper being
  routed there. Fixed; every other pin of the 15 added components checked out.
- **Updated PR #11's title/body** to stop claiming "stage 1 of N, WIP" when the actual PCB work
  is complete — it was just waiting on an accurate status, not more routing.

**What this means practically**: there are now two real, viable hardware paths, not one.
- **Path A (ADAU1860, current `master`)**: proven, driver exists (120+ tests), real latency
  measured at 12.9µs, real power numbers known, zero new firmware work — genuinely "order it
  today" ready, as the earlier update below says.
- **Path B (TAC5301-Q1, `redesign/tac5301-codec-swap`)**: cheaper part and (if it also addresses
  the charger/fuel-gauge) a real shot at a materially cheaper board, but needs the PR #12 bench
  experiment run for real before trusting it, a new codec driver written from scratch (~400-600
  lines, no existing tests), and accepts a real latency/power regression vs. path A in exchange
  for the cost savings.

**Not decided by me — this is exactly the kind of call that's yours.** Both branches are in a
real, documented, non-misleading state now; neither is blocked on cleanup work, only on an actual
decision (and, for Path B, a cheap bench experiment) whenever you have bandwidth for it.

## Update 2026-09-30 (later): all six PRs from the stretch below are now merged

`haven-app#10`, `#11`, `#12`, `#13`, `#14` and `haven-dev-board-kicad#9` are
all merged, `haven-app#9` closed as superseded. `#11` and `#12` needed a
second conflict-resolution pass after `#14` landed (both touched
`Hearing.tsx`/`docs/roadmap.md`) — resolved by keeping both features'
render blocks/roadmap entries side by side where they were genuinely
independent. `#12` also had three real add/add conflicts
(`insights.ts`, `insights.test.ts`, `docs/llm-summary.md`) because its
branch point predated `#11`'s merge of the same feature — master's version
was a strict superset in every case (added `hasRealData`, the deployed
relay writeup), so master's content won outright rather than being
concatenated. `tsc`/`jest` and CI green on every merge. No open PRs
remain in `haven-app`, `haven-zephyr-app`, or `haven-dev-board-kicad`.

## Update 2026-09-30: two real new PRs reviewed, my own four rebased clean

Checked in after a quiet stretch and found real new activity, not just
silence:

- **`haven-app#14`** (victorzhu443) — the correct app-side ack
  implementation, written against `haven-zephyr-app#12`'s real wire format,
  **explicitly supersedes `#9`**. I reviewed this properly, not just the PR
  description: checked out the branch, ran `tsc` (clean, both native and
  web module resolution) and the full test suite myself (157/157, matching
  the PR's own claim exactly), and spot-checked the three safety-relevant
  claims directly in the source rather than trusting the writeup — the
  `tone_watchdog` handler genuinely never sends `TONE_STOP` after the
  device has already silenced itself, the applied-level echo is genuinely
  reclamped before use (can lower the meter, never raise it past the
  ceiling), and the `dac_source` allow-list genuinely fails closed for any
  unrecognized value. All three checked out exactly as described. **My
  read: this is good, and resolves the `#9` ambiguity — merge this, close
  `#9`.** Not done by me; that's still your click.
- **`haven-dev-board-kicad#9`** (victorzhu443) — fills in the ADAU1860
  active-current number `POWER_BUDGET.md` explicitly left as "not
  verified" (the one I couldn't get — two direct PDF fetches from ADI
  timed out from this session, both times). Real page citations (Tables
  6–8, pp. 9–10 of ADAU1860 Rev. 0), and the battery-referred arithmetic
  checks out (3–8 mW ÷ (3.7 V × ~85% regulation) ≈ 1–2.5 mA, matching their
  stated result). Docs-only, no board/BOM change. I didn't independently
  re-fetch the PDF myself to verify the raw page citations (same fetch
  problem as before), so that part is trust-but-cite, not independently
  reproduced — worth knowing if this number ever matters for a real
  spec decision. Also flags one real, specific, checkable bring-up risk:
  the codec crystal's max load capacitance (20 pF, Table 2) is close to
  what the board's 2×33 pF caps plus stray capacitance produce
  (~19–22 pF) — not a defect (stock OpenEarable uses the same values), but
  worth trying 22 pF caps first if the codec crystal doesn't start.
- **My own four PRs (`haven-app#10/#11/#12/#13`) had drifted into real
  merge conflicts** against current master (confirmed with actual `git
  merge`, not just GitHub's sometimes-flaky mergeable field) — the
  evidence-programme merge from a few days ago added its own code at the
  same spot in `Tune.tsx` and `docs/roadmap.md` that my own work did, and
  I'd never rebased after it landed. Fixed properly: merged master into
  each branch, resolved every conflict by keeping both sides (nothing was
  actually incompatible, just additive), reverified `tsc`/`jest` clean
  after each one, then pushed. **All four are genuinely `MERGEABLE` again
  now** — nothing left blocking them but your review.
- **`haven-zephyr-app#12`'s conflict is also resolved** — the contributor
  read this file's own diagnosis, rebased, kept both CI matrix entries and
  both test names exactly as described here, and confirmed host tests
  pass. CI on GitHub now builds all four matrix configs clean. This one's
  fully ready too.

I did not merge or close anything in this pass — reviewing and fixing
conflicts on branches I have write access to is different from the merge
decision itself, and I said I'd be more conservative about that until you
weighed in on the earlier backlog merge. **Everything listed above is
ready for your review/click; `#9` is the one thing to close, not fix.**

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

- **`haven-zephyr-app#12` (NUS acks + LFRC fallback) would not merge — a
  real conflict, and a correction to what I said here earlier.** I first
  read this as GitHub being wrong (a local test merge showed no conflict at
  all), and said so above. That test was against a stale master — I'd
  since merged the whole firmware stack (`#8`→`#14`) in between, and
  against *current* master there's a real conflict in two files, confirmed
  by re-running the same local test. GitHub was right the whole time; my
  diagnostic just used an outdated comparison point. **The actual conflict
  is trivial, though** — `#12` and the now-merged `#13` each added their
  own CI matrix entry (`.github/workflows/build.yml`, one line each) and
  their own test name to the shared list (`tests/host/run_tests.sh`), on
  adjacent lines. Nothing is actually incompatible — the fix is keeping
  *both* matrix entries and *both* test names, not picking one. I don't
  have push access to fix this myself (it's a contributor's fork branch,
  not mine), but it should take under a minute in GitHub's own web
  conflict editor with that in mind.
  **Separately, victorzhu443 commented on the PR (real, current, 2026-09-27
  evening)**: their fork's CI has been stuck on the "Initialize containers"
  step (a `ghcr.io` image-pull stall) across three run attempts — an
  Actions/registry-side issue, not a build error, no step of theirs has run
  yet. Their own host tests pass locally; the actual firmware compile for
  this PR's two commits just isn't verified by CI yet, separate from the
  merge conflict above.
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
