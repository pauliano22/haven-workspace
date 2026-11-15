# Infrastructure, tools and what's missing

Written 2026-11-07 from what I hit while working on Haven today. Items marked **built** exist now,
**proposed** are my recommendation, **unchecked** are things I have not researched (no prices or
availability claimed).

## What I built or found today

| Thing | State | Why it matters |
|---|---|---|
| `hardware_kicad/tools/verify_v2_order_files.sh` | **built**, runs in about 15 s | One command before any board order: DRC and schematic parity on all three boards, a check that the fab files match the boards, and JLCPCB's published limits as an informational extra |
| `firmware/haven_zephyr_app/tools/dk_regression.sh` | **built**, tested | Flash the DK, boot it, run 14 Bluetooth checks from Windows, cross-check against the board's own log, reset it. No browser, no clicking |
| `tools/ble_dk_windows_test.py` | **built** | The Bluetooth checks themselves, using Windows Python with `bleak` in an isolated environment (`C:\Users\pmi\claude-bridge\files\blevenv`) |
| Datasheet cache `~/.cache/haven_datasheets/` | **built**, 1 file | Raytac's module spec is saved there. Many notes in the repo cite datasheet tables, but the PDFs were never on disk, and some sites (analog.com, Texim, Nordic's docs) block automated downloads |

## Things to be aware of

1. **Local-only work.** Nothing from today is pushed. Uncommitted in `haven_workspace`: the new docs
   (`MATERIALS_AND_ASSEMBLY.md`, `ADAPTIVE_PROTECTION_DESIGN.md`, `ORDER_READINESS.md`, this file) and
   edits to `PROJECT_STATUS.md` and `V2_ORDER.md`; in `website`: five wording fixes; in `hardware`: a
   `.gitignore` and the colorway renderer; in `firmware`: the sound-signature prototype and the scripts
   above. Committed on a local branch only: the trigger diary (`feature/trigger-diary`, app repo).
   Pushing the website publishes it live.
2. **Bluetooth from WSL is impossible.** The WSL kernel has no Bluetooth support, so every Bluetooth test
   has to come from Windows. That is why the tests use Windows Python.
3. **Chrome's device picker can't be automated.** Browser Web Bluetooth tests need a person to click the
   device. Use the `bleak` route for protocol tests; the app's own screen needs a person or a phone build.
4. **The browser agent stalls when nobody is at the computer.** Tasks I queued while you were away
   (the JLCPCB quotes) were not picked up: the Windows session was probably waiting on a permission
   prompt. Only one Windows Claude can hold Chrome, and a second window can take it from the first.
   Fix options: keep one window open running `/loop /bridge`, and pre-approve its Chrome and file
   permissions. **Proposed**, not done.
5. **The board can end up stuck "connected".** After a Windows client disconnected, the DK did not
   re-advertise for 2+ minutes. Unknown whether that's Windows or firmware. Needs a phone to settle.
6. **No hardware CI.** GitHub builds the firmware and type-checks the app, but nothing checks the KiCad
   boards on a pull request. **Proposed:** run `verify_v2_order_files.sh` in KiCad's official Docker image
   on every hardware pull request. Not set up; I have not confirmed the image has the Python module the
   export script needs.

## Bench equipment the first build will need (unchecked: no prices or models researched)

- Something to read the pod's current draw (the power budget is a datasheet estimate, never measured).
- A way to program and debug the pod through its SWD pads (the DK's debug-out covers this; the pads need a
  probe or a clip that fits them).
- A calibrated measurement microphone setup for the loudness limit (see `MATERIALS_AND_ASSEMBLY.md`).
- A scope or logic analyzer for the microphone clock and data and the I2S lines.
- A way to measure the Bluetooth module's carrier frequency error (see the crystal item in `ORDER_READINESS.md`).
- Magnification and fine tweezers for the 0.35 mm-pitch chips and the hand-built cable.

## Agentic tools: what would help most (proposed, in order)

1. **A weekly stock and price check** of the Bluetooth module, power chip, battery and speaker, written to a
   file in the repo. Part availability is what blocked v1. Needs either the browser bridge or a distributor's
   public API (unchecked).
2. **A nightly run of the two scripts above** when the DK is plugged in, with the result written to
   `PROJECT_STATUS.md`'s evidence column, so "tested" claims stay current.
3. **A pull-request watcher** for the Haven repos that reads new contributions the way I reviewed them in
   September (run the tests, check the claim) and leaves a summary for you.
4. **A datasheet shelf**: a folder of the PDFs the project depends on, converted to text, so claims about
   registers, pads and limits can be checked on the spot. Needs your browser once for the sites that block
   downloads (Analog Devices, Nordic, VARTA).

I do not recommend more tools than this yet. The project's limit is hardware that does not exist, not
tooling.
