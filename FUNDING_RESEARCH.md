# Federal SBIR funding: real precedent for exactly this space

Research prompted by wanting to find funding that doesn't depend on Cornell-
specific programs or deadlines (those are tracked in
`haven_dev_board_kicad/HARDWARE_COST_ALTERNATIVES.md`'s "Cornell startup/
pitch programs" section instead — this doc is federal SBIR/STTR only).

## The headline finding: this exact concept is already a proven, funded category

Searched for prior SBIR awards in "smart"/active hearing protection rather
than starting from a generic funding-agency list, and found a real company
with a multi-year, still-active track record in almost exactly Haven's
space — not a one-off grant, a genuine funding lane:

**Speech Technology and Applied Research Corporation** (Lexington, MA —
23 Phase I + 6 Phase II awards since 1995, $11.5M total SBIR funding,
per sbir.gov's own public award database):

| Year | Phase | Amount | Agency | Project |
|---|---|---|---|---|
| 2020 | I | $149,949 | HHS/CDC (NIOSH) | "Factory Noise Removal to Preserve Situational Awareness" |
| 2023 | I | $295,671 | HHS/CDC (NIOSH) | "Scrubbing Complex Sound Sources for Factory Situational Awareness" |
| 2022 | I | $259,566 | HHS/NIDCD | "Hear What I Want: Acoustically Smart Personalized Common Room" |
| 2023 | I | $275,389 | HHS/NIDCD | "Clarity in Motion: Motion-Tolerant Hearing Aid" |

The 2020→2023 CDC/NIOSH pair (a fresh Phase I on the *same underlying
concept* three years later, not a Phase II continuation of the first) is
the important signal here: NIOSH is still actively funding "let dangerous/
unwanted sound through selectively, preserve situational awareness" work
as of 2023, not a program that existed once and closed. That's real,
current-enough precedent that this general concept is fundable, not just
theoretically eligible.

**What their actual product concept is** (per public summaries — worth
reading their full proposal abstracts on sbir.gov directly before treating
this as more than a starting point): multi-microphone, DSP-based system
that identifies and removes hazardous factory/machinery noise while
preserving audibility of safety-critical sounds (alarms, a supervisor's
voice, a reversing forklift). That's functionally adjacent to Haven, not
identical — Haven's differentiator is personal/wearable + app-tunable per-
user comfort profile vs. their more environment/factory-floor framing —
which is a real, defensible point of difference to lead with in any
proposal rather than positioning Haven as "the same thing."

## Two different agencies, two different framings — pick deliberately

This matters given the regulatory-positioning research
(`REGULATORY_POSITIONING.md`) already found that framing changes which
regulatory bucket Haven falls into. The same tension shows up here in
which agency to target:

- **NIOSH (via CDC)**: occupational hearing *protection* framing —
  preventing hearing damage from hazardous noise exposure, situational
  awareness preservation. This is the same lane as the "hearing
  protector" (EPA/ANSI, not FDA) regulatory framing already identified as
  probably the better fit — **the funding and regulatory framings point
  the same direction**, which is a real point in favor of leading with
  this angle over the alternative below.
- **NIDCD** (National Institute on Deafness and Other Communication
  Disorders, part of NIH): hearing-*health*/communication-disorder
  framing — the "Motion-Tolerant Hearing Aid" and "Acoustically Smart...
  Common Room" titles both read as assistive/hearing-health technology,
  closer to the "hearing aid" FDA bucket than "hearing protector." Applying
  here would push toward exactly the medical-device framing
  `REGULATORY_POSITIONING.md` recommends avoiding for the actual product
  positioning — worth being deliberate about, not defaulting to whichever
  agency's topic list happens to read as the easier match on paper.

**Net recommendation**: NIOSH/CDC is the more coherent target — it matches
both the intended hearing-*protection* product positioning and has a
proven, recent (2023) track record funding closely related DSP/smart-
hearing-protection work.

## Real budget/process numbers found

From the HHS SBIR Program Descriptions document (seed.nih.gov, the
current official one — replaces an older cached PDF some search results
still point to):

- NIOSH: "typically supports Phase I awards at the maximum allowable total
  cost as stated in the funding announcement"; **Phase II capped at $1M
  total for the two-year period** (this is NIOSH-specific — don't assume
  the general HHS SBIR Phase II ceiling of ~$2.1M applies here, an earlier,
  less careful pass at this research conflated the two).
- Programmatic contact for NIOSH SBIR as of this document: Steve Dearwent,
  PhD (sdearwent@cdc.gov, 404-498-6382) — a real named contact, not just a
  general inbox; worth reaching out to directly with a one-paragraph
  concept pitch before writing a full proposal, standard SBIR practice.
- NIOSH also runs a **Small Research Grant Program (R03)**: up to $50,000/
  year in direct costs over 2 years, ~5-10 awards/year — a smaller, lower-
  commitment option if a full SBIR proposal feels premature.
- **NORA Hearing Loss Prevention Cross-Sector Council**: a real NIOSH-
  convened industry/researcher network for hearing-loss-prevention
  stakeholders (per NIOSH's own Hearing Loss Prevention Program page) —
  worth investigating as a visibility/partnership channel independent of
  applying for money directly, especially before a first SBIR application
  where having a credible existing connection in the space helps.
  **Real, current co-chairs found** (cdc.gov/nora/councils/hlp/members.html):
  Laurie Wells (3M), and NIOSH's own HLP program co-coordinators Amanda
  Azman and Elizabeth Masterson — the latter two are directly-reachable
  NIOSH staff who literally run the program the SBIR precedent above was
  funded under, a real warm-ish path to the same "reach out before writing
  a full proposal" step already recommended. Most other private-sector
  members (Caterpillar, Komatsu Mining, Milwaukee Tools) are large
  industrial/occupational-PPE companies, not close analogs to a consumer
  wearable — useful for the network and NIOSH access, not as direct peers.

## What this doesn't resolve

- Haven's actual differentiators (consumer/musician/personal-wearable
  framing, app-based per-user tuning, tinnitus/hyperacusis-adjacent origin
  even though that specific framing needs to stay out of the product
  description itself per `REGULATORY_POSITIONING.md`) vs. this company's
  more industrial/factory-floor framing — a real proposal would need to
  articulate this distinction clearly, not just cite their precedent as
  "someone else does something similar."
- Whether NIOSH's *current* (not historical) solicitation actually lists
  a topic this fits — the specific topics document referenced in NIOSH's
  own funding page (pages 180-184 of an older combined PDF) wasn't
  locatable in this pass; the current seed.nih.gov document is shorter and
  administrative rather than topic-listing. Confirming this needs checking
  the live NIOSH homepage/current solicitation directly, or just asking
  the programmatic contact above.
- Full abstracts of the cited prior awards weren't read directly (sbir.org
  blocked the fetch; sbir.gov's award database was used instead, which
  gave real amounts/titles but not full technical abstracts) — worth
  pulling those before citing this precedent in an actual application.
