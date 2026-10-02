# Patent landscape: real prior art exists in this exact space

Research prompted by a simple question that hadn't been asked yet despite
all the regulatory/funding/pricing research already done: does building
and selling "DSP-based, app-tunable active hearing protection" risk
infringing on someone else's patent, or is the space actually open?

**This is not legal advice and does not answer that question.** It
surfaces real, specific prior art that exists — the actual infringement
question (do Haven's specific claims fall inside any specific patent's
specific claim language) requires a real patent attorney doing a real
freedom-to-operate search, not an AI reading patent abstracts. Treat
everything below as "here's what's out there," not "here's whether it's
a problem."

## Two real, specific patents found, at very different points in their lifecycle

### Sonova AG — EP2127467B1 — expires December 18, 2026

A **major, real hearing-aid company** (Sonova owns Phonak, Unitron, and
others) already patented, in 2006, an active hearing protection system:
molded earplugs with mics + speakers + a body-worn processor, an "ambient
mode" (mic-through) and a "communication mode" (external audio mixed with
ambient), ≥10dB attenuation, level-dependent gain reduction, and a noise
dosimeter. **This is close to the general shape of an active hearing
protector** — but it's about three months from expiring as of this
writing (2026-09-17). By the time Haven could plausibly reach a
commercial launch, this specific reference will likely no longer be
enforceable — worth confirming the exact expiration mechanics (annuity
payments can occasionally lapse a patent earlier, or a company can
occasionally get extensions) rather than just trusting the calculated
date, but it's a genuinely good sign for this specific reference, not a
present blocker.

**Re-checked 2026-10-02, directly against the patent's own legal-status record
(Google Patents), not re-derived from the original search**: still tracking
exactly as expected — active, annuity fee paid for year 20 as of April 2026,
no litigation flag. One clarifying detail the original research didn't
narrow down: most European national designations (UK, France, Denmark, and
others) lapsed for non-payment/translation reasons back in 2015-2018 — the
patent is now only confirmed active in Germany specifically. Doesn't change
the conclusion (still expiring Dec 18, 2026, still not a present blocker),
just a sharper picture of where it was ever enforceable in the meantime.

### Eers Global Technologies Inc. — US10238546B2 — active through January 22, 2036

**This one is the real signal worth paying attention to.** Assigned to
Eers Global Technologies (originally developed at École de Technologie
Supérieure, a Quebec engineering school — a real academic-to-commercial
pipeline, not a shell filing), filed 2015/2016, **active and enforceable
for another decade**. Its claims are notably closer to Haven's own
approach than Sonova's older, more generic patent:

- Measures the **individual user's own ear-canal acoustic properties**
  via built-in mics and auto-designs a **personalized correction filter**
  — i.e., patented IP specifically around *per-user personalization* of
  an active hearing-protection earpiece, not just "active hearing
  protection" generically.
- Active occlusion-effect cancellation (the "boomy own-voice" problem —
  a real, well-known musician complaint).
- Frequency-dependent attenuation uniformity, accounting for loudness
  perception.
- User-adjustable attenuation level, an emphasis frequency, and auxiliary
  audio input.

**Eers Global Technologies is a real company Haven's own competitor list
never included** — worth researching directly (product name, current
market presence, price point) before assuming the existing musician-
hearing-protection competitor set (MEE Audio, Sensaphonics, Earasers,
Minuendo — see `MARKET_POSITIONING.md`) is complete. A company holding a
broad, decade-long-remaining patent specifically on personalized active
hearing protection is a materially different kind of competitor than a
passive-earplug maker.

**Follow-up, somewhat reassuring**: Eers (Montreal, founded 2014) appears
to have moved on from consumer/musician hearing protection specifically —
current search results describe them as focused on "high-noise IoT
hearing protection with in-ear communication and worker safety
monitoring" (industrial) and, per their own site's page title, an "MRI
Audio Platform" (medical imaging, a genuinely different market again).
Their own site (`eers.ca`) returned a server error when checked directly,
so this is search-snippet-level confidence, not a confirmed current
product lineup. **The patent itself doesn't care whether they still ship
a consumer product** — it's enforceable regardless of what Eers currently
sells — but this does mean they're less likely to currently be a *direct
market* competitor for Haven's specific consumer/musician positioning,
even though their IP could still matter.

**Two real, new, previously-unsurfaced findings, checked 2026-10-02 directly
against the patent's own legal-events record (Google Patents) rather than
re-running the original search:**

1. **Cook Medical Holdings LLC recorded a security interest against this
   patent on 2025-12-24.** Cook Medical is a large, real medical device
   company — a security interest is a financing instrument (the patent
   pledged as collateral, most likely for a loan to Eers), not necessarily
   a sale or license, since the assignee of record is still listed as Eers
   Global Technologies Inc. This doesn't by itself change the
   infringement-risk picture, but it's a concrete signal that a much
   larger, patent-experienced company now has a direct financial stake in
   this specific patent being valuable/enforceable — worth knowing before
   assuming this is a small, inactive academic spinout's dormant IP.
2. **Google Patents flags this patent's family as having litigation**
   ("Family has litigation," sourced from the Darts-ip global patent
   litigation database) — a real flag, not a false positive I could
   dismiss, but one I could not resolve to a specific case: no matching
   result in CourtListener (US federal courts) or general web search for
   "Eers Global Technologies" as a litigant. Darts-ip tracks litigation
   globally, and the flag is on the patent *family* (which includes
   non-US filings, e.g., a Canadian or PCT equivalent), so the likely
   explanation is litigation outside the US that free sources don't
   surface — but that's inference, not confirmation. **This is exactly
   the kind of thing a real freedom-to-operate search (already flagged
   below as needed) would resolve properly**; don't treat "no CourtListener
   hit" as "no litigation," and don't treat the unresolved flag as "this is
   definitely being actively enforced" either — it's a real open question,
   not a known answer in either direction.

## Why this specific claim area matters for Haven

Eers' patent personalizes based on **measured individual ear-canal
acoustics** (a physical/acoustic measurement). Haven's own approach
(per `haven_custom_app`'s features) personalizes based on **a
tinnitus/loudness pitch-matching *test*, not an ear-canal acoustic
measurement** — a real, substantive difference in mechanism, not just
wording. That distinction is worth leading with if this ever needs to be
argued, but it's exactly the kind of distinction that needs a real
attorney reading the actual claim language (not an abstract or an AI
summary) to know whether it actually clears the patent's claims or not.

## What this doesn't resolve

- No actual claim-language reading was done here — only AI-generated
  summaries of what Google Patents' own interface surfaced. Real
  infringement analysis requires reading the actual numbered claims
  (typically the least readable, most legally load-bearing part of a
  patent) with counsel, not the abstract/description.
- This was a narrow, keyword-driven search (two patents found, not a
  systematic prior-art or freedom-to-operate search). A real FTO search
  by a patent professional would search patent classifications
  systematically, not just web-search keywords, and would find far more
  than two references.
- ~~Didn't check whether Eers Global Technologies has since built and
  shipped an actual product~~ Partially addressed above (2026-10-02 re-check
  and the earlier follow-up): they appear to have moved to industrial/
  medical-imaging markets, search-snippet confidence only, their own site
  errored when checked directly. Current price point, if any, for a
  consumer product is still not known — not fully closed.
- Didn't check whether Haven's own approach (tinnitus-pitch-match-driven
  personalization, specifically) might itself be patentable — a real,
  separate, positive-direction question worth asking a patent attorney
  at the same time as the freedom-to-operate question, not just "are we
  infringing" in isolation.
- **New, 2026-10-02**: the "family has litigation" flag on the Eers patent
  is real but unresolved to a specific case — needs either a Darts-ip
  subscription or a patent attorney's access to proper litigation databases
  (PACER plus non-US equivalents) to actually identify what it refers to.
  This is now probably the single highest-value next research step in this
  doc, ahead of the general FTO search, since it's a specific, already-
  flagged lead rather than a blind search.
- Didn't investigate the nature or terms of Cook Medical's security
  interest (loan amount, maturity, whether it signals Eers is financially
  distressed or just doing normal venture debt) — UCC filing databases
  (state-level, where Eers is incorporated) would have this, not Google
  Patents.
