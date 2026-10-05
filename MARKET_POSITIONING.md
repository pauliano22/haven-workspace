# Competitor pricing: what "smart" is actually worth in this market

Real, current prices pulled directly from manufacturer sites (not
secondhand estimates), to answer a question the earlier competitive
framing hadn't: given musician hearing-protection competitors are
identified as "all passive/swappable physical filters, not software-
adjustable DSP" — what does the market actually pay across that passive-
to-active spectrum, and where would a DSP/app-controlled product like
Haven plausibly sit?

## Real prices found

| Product | Type | Price | Source |
|---|---|---|---|
| Earasers | Passive, fixed-filter | ~~~$25-30~~ **$49.99**, confirmed directly 2026-10 | earasers.net/products/earasers, fetched directly |
| Minuendo (Adjustable) | Passive, **mechanically continuously-adjustable** acoustic filter (7-25dB, a real dial, not swappable filters) | $179-189 (currently on sale from $189) | shop.minuendo.com, fetched directly |
| Sensaphonics 3DME BT Gen2 (universal fit) | **Active/electronic** — Bluetooth-controlled "Active Ambient" mixing | $799 | sensaphonics.com, fetched directly 2026-10 |
| ~~Sensaphonics 3D-U AARO~~ | ~~Active/electronic~~ | ~~$1,500 list~~ **Discontinued** — not in the current product lineup (checked 2026-10) | — |
| Sensaphonics 3DME Custom Tour Gen2 | Active/electronic, custom-molded | $2,000 | sensaphonics.com, fetched directly 2026-10 |

## The real signal here

**There's roughly a 3.5-4x price jump from "passive, fixed" to "passive,
adjustable" ($49.99 → $179-189), and then another 4-10x jump from
"passive, adjustable" to "electronic/active" ($179 → $799-2,000).** (The
first jump is smaller than an earlier draft of this doc had it — see the
2026-10 update below — but the conclusion is the same.) That second jump
is the one that actually matters for Haven's positioning: the market has
already demonstrated real willingness to pay a large premium specifically
for *active/electronic* control over ambient sound, not just a better
passive filter. Sensaphonics' price point isn't a custom-IEM tax alone
either — their $799 *universal-fit* model, no custom molding at all, is
still 4x Minuendo's adjustable passive product.

This is a genuinely useful anchor for Haven's own pricing conversation:
positioning as "better passive" (competing with Minuendo's $179-189
tier) would badly undersell a DSP/app-controlled product relative to
what this exact market has already shown it will pay for active control
— Sensaphonics' $799-2,000 range is the more realistic reference class,
not the passive-earplug tier.

## Update 2026-10: three real changes found re-checking every price directly

All three competitor sites fetched directly this pass, not re-trusted from
the original research:

1. **Earasers was wrong, not just unconfirmed.** The original ~$25-30
   estimate was a third-party comparison the doc itself flagged as never
   verified directly — turns out that was the price of a **single
   replacement earplug for one ear** ($25.00), not the actual product.
   The real product (a pair, in a presentation box with a carry case,
   12 size/filter combinations) is **$49.99**. This makes the
   "fixed → adjustable" price jump smaller than originally stated (~3.5-4x,
   not ~4-6x) — doesn't change the overall conclusion, but the number
   was simply wrong, not just imprecise.
2. **Minuendo has added a second, cheaper product line not in the original
   research**: "LIVE 17dB Earplugs," $119-129 (vs. the original
   "Adjustable" line's $179-189, still current and accurately priced).
   LIVE is a fixed 17dB attenuation (not continuously adjustable like the
   Adjustable line) — a real middle tier between Earasers' $49.99 and the
   Adjustable line's $179-189 that didn't exist (or wasn't found) before.
   Worth knowing as another real data point on the passive-to-adjustable
   price curve.
3. **Sensaphonics' 3D-U AARO ($1,500) appears discontinued.** Checked the
   full current product listing directly (sensaphonics.com/collections/all)
   — it's not there. The current 3DME lineup is just two tiers: "3DME BT
   Gen2" (the renamed universal-fit model, still $799, matching the
   original figure) and "3DME Custom Tour Gen2" (still $2,000, matching).
   The three-tier $799/$1,500/$2,000 ladder this doc described is now a
   two-tier $799/$2,000 one — a real simplification of the actual
   competitive landscape, not just a renamed SKU (nothing in the current
   lineup sits near $1,500).

## Real, important differences from Sensaphonics worth being honest about

- Sensaphonics' "Active Ambient" is built for **performers monitoring
  their own mix on stage** (musicians who need to hear the room *and*
  their in-ear mix simultaneously) — a professional tool sold into a
  narrow, low-volume, high-touch (often custom-molded) channel. Haven's
  target use case (general hearing protection/comfort, tinnitus-adjacent
  self-management framing per `REGULATORY_POSITIONING.md`) is a
  different, likely larger and more price-sensitive consumer market —
  the $799-2,000 tier may not be directly achievable for a consumer
  product even if it's the right *category* anchor.
- Sensaphonics sells direct to a professional-audio audience already
  primed to spend on IEMs; Haven doesn't have that built-in premium-
  audio-buyer context and would need its own case for the price point,
  not just "we're also active/electronic."

## What this doesn't resolve

- No real consumer willingness-to-pay data for Haven's actual target
  buyer (a musician/noise-sensitive consumer, not a touring professional)
  — this is competitor pricing, not primary market research.
- Manufacturing/BOM cost isn't reconciled against any of these price
  points here — `haven_dev_board_kicad/HARDWARE_COST_ALTERNATIVES.md`
  has the real component-cost findings for the dev board specifically,
  not a production-unit cost estimate at any particular volume.
- Didn't check whether any of these competitors, especially Sensaphonics
  (the only genuinely electronic one), disclose real unit sales volume
  or margin — pricing alone doesn't confirm market size.
