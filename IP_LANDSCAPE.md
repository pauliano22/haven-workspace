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
- Didn't check whether Eers Global Technologies has since built and
  shipped an actual product, what it costs, or how it's positioned —
  that's a real, separate competitor-research task this doc doesn't
  complete.
- Didn't check whether Haven's own approach (tinnitus-pitch-match-driven
  personalization, specifically) might itself be patentable — a real,
  separate, positive-direction question worth asking a patent attorney
  at the same time as the freedom-to-operate question, not just "are we
  infringing" in isolation.
