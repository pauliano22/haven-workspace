# Regulatory positioning: why the marketing words matter as much as the hardware

Research prompted by the explicit project framing ("it's not a professional
hearing aid, we're marketing as a hearing protection device") and by the
project's own personal origin (wanting to help with a family member's
tinnitus and hyperacusis). Those two things pull in different regulatory
directions, and this doc is about that tension — not legal advice, and not
a substitute for a real conversation with an actual FDA regulatory
consultant or attorney before anything ships or is sold. Sources are the
FDA's own public materials, read directly, not summarized secondhand.

## The short version

**Whether Haven needs FDA clearance as a medical device is decided almost
entirely by what the marketing/labeling says, not by what the hardware
does.** Two products with identical circuit boards can land on opposite
sides of the line depending on word choice. This is not a loophole to be
clever about — it's literally how FDA's own guidance says it determines
intended use, in writing, examples included below.

## The actual rule (from FDA's own guidance)

Source: FDA/CDRH webinar transcript, "Hearing Aids and Personal Sound
Amplification Products," December 7, 2021 (covering the 2021 proposed OTC
hearing aid rule and the companion draft Hearing Aids vs. PSAPs guidance),
fda.gov/media/155020/download.

- **A hearing aid** is "a wearable device designed for and intended for
  aiding persons with impaired hearing or compensating for impaired
  hearing." It meets the FD&C Act §201(h) medical device definition
  ("intended for use in the diagnosis, cure, mitigation, treatment, or
  prevention of disease") and is regulated accordingly.
- **A PSAP (personal sound amplification product)** is for
  *non-hearing-impaired* consumers, to amplify sound in specific
  situations (hunting, birdwatching, a distant lecture, soft
  conversation) — not to aid impaired hearing. It does **not** meet the
  medical device definition and is **not** FDA-regulated as a device.
- FDA explicitly determines which bucket a product is in by looking at
  **intended use**, and intended use is established by "any written or
  oral claims or statements in any label, labeling, advertising, and/or
  promotion, by or on behalf of a manufacturer" — not by the circuitry.

FDA's guidance gives four concrete examples of claims that turn a PSAP
into a (regulated) hearing aid, quoted directly:

1. "If a product states it is for users with certain types of severity of
   hearing loss or impaired hearing, it is a hearing aid."
2. "If a product is suggested for use in situations typically where
   hearing loss is to be compensated for, it is a hearing aid."
3. "If a product is suggested as an alternative to, or a substitute for,
   a hearing aid for persons with hearing loss, then it's not a PSAP but
   a hearing aid."
4. "If a product has information conveyed to the user to optimize the
   product to their hearing loss or to their impaired hearing profile,
   for example, through use of software or other features, then the
   product is not a PSAP, but a hearing aid."

## Why #4 is the one that actually matters for Haven

This is the one worth sitting with, because it's not just a marketing-copy
problem — it describes a real feature already built. Per
`mobile_app/haven_custom_app/docs/roadmap.md`, the app has a "Match your
sound" tinnitus pitch/loudness matching flow and an LDL (loudness
discomfort level) test, both of which feed into **a personalized filter
band tuned to that specific user's profile.** That is close to a literal
match for FDA's example #4 ("software... to optimize the product to their
... impaired hearing profile"), depending entirely on how it's described
to the user and in any public materials.

**The good news: the app's existing product notes already got this half
right, seemingly by instinct rather than by regulatory analysis.**
Roadmap.md already frames "Match your sound" as "self-management, not a
cure" and cites weak/mixed clinical evidence for notched sound therapy as
the reason; the tolerance-building feature is described as "honest about
what Haven's hardware can and can't do... it has no broadband noise
generator, so this can't be real sound-generator-based hyperacusis
therapy." That instinct — don't claim to treat a condition — is exactly
the right one and should be treated as a hard rule going forward, not a
one-off note. **What's not yet resolved** is whether "personalizing a
filter to your own comfort/sound-matching results" reads to FDA the same
as "optimizing to your hearing/impairment profile" even without ever
using clinical language. That's a real open question a regulatory
consultant should answer, not something to guess at here.

## The words that are safe to use personally but not in any customer-facing material

The project's own founding motivation is completely reasonable to talk
about personally and even in an "our story" context handled carefully —
but specific words in that story are, almost verbatim, the FDA's own
medical-device trigger words:

- "**cure**" tinnitus/hyperacusis — this is literally one of the five
  words in the FD&C Act's own medical device definition ("diagnosis,
  cure, mitigation, treatment, or prevention of disease").
- "**treat**" or "**therapy**" for tinnitus/hyperacusis — same category.
- Describing tinnitus or hyperacusis as something the product
  *addresses* or *helps with* directly, rather than describing the
  product itself (sound dampening/protection) and letting the user infer
  their own reasons for using it.

None of this means the personal story has to be hidden — plenty of real
companies are founded on a personal health motivation. It means the
**product description, app copy, and any ads** need to stay in
protection/comfort/preference language (e.g., "reduces harsh or
overwhelming sounds," "adjustable sound comfort," "hearing protection for
loud environments") rather than condition-treatment language, consistently,
everywhere a customer could read it — not just on a website but in the app
UI, app store listing, and packaging.

## What "PSAP-safe" positioning would concretely look like

Based directly on FDA's own stated examples above, staying in
unregulated PSAP/hearing-protection territory would mean:

- Market to people in loud environments generally (musicians, concert-
  goers, factory/shop workers, people sensitive to noise) — **not** to
  people with a diagnosed hearing condition.
- Never claim the product is "for" tinnitus, hyperacusis, or hearing
  loss/impairment specifically — describe what the device does (filters/
  dampens sound), not what condition it's aimed at.
- Never position Haven as an alternative or substitute for a hearing aid.
- Frame any personalization (comfort test, preferred filter bands) as
  *preference tuning* (like an EQ or a volume curve), not as
  *optimizing to your hearing profile* — the same underlying feature,
  described differently, is the entire difference between the two
  regulatory buckets per FDA's own example #4 above.
- Keep the existing musician-hearing-protection competitive framing
  (MEE Audio, Sensaphonics, Ultimate Ears, Earasers, Minuendo — all
  already positioned as hearing protection, not medical devices) as the
  actual comparison set, not audiologist-dispensed hearing aids.

## What this doesn't resolve

- Whether tinnitus/hyperacusis sound-therapy apps (not hardware) have their
  own separate FDA digital-therapeutics pathway (some do, under different
  rules than hearing aids) wasn't researched here — a different question
  from the PSAP/hearing-aid line above, and worth its own pass if the app
  ever adds features explicitly framed as therapy.
- Whether existing musician-hearing-protection competitors with
  DSP/software features (if any emerge) have already tested this exact
  line with FDA — worth checking before assuming the safe framing above
  is bulletproof in practice, not just on paper.
- This is one FDA webinar transcript plus the underlying framework, not a
  full regulatory review. Treat this as "here's the shape of the real
  question," not "here's the final answer" — get real counsel before
  committing to final product copy, packaging, or app store descriptions.
