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
| Earasers | Passive, fixed-filter | ~$25-30 (per third-party comparison; exact current price not confirmed directly from earasers.net) | web comparison |
| Minuendo | Passive, **mechanically continuously-adjustable** acoustic filter (7-25dB, a real dial, not swappable filters) | $179-189 (currently on sale from $189) | shop.minuendo.com, fetched directly |
| Sensaphonics 3DME (universal fit) | **Active/electronic** — Bluetooth-controlled "Active Ambient" mixing | $799 | sensaphonics.com product pages |
| Sensaphonics 3D-U AARO | Active/electronic | $1,500 list | musicplayers.com / churchproduction.com reviews |
| Sensaphonics 3DME Custom Tour | Active/electronic, custom-molded | $2,000 MSRP | musicplayers.com |

## The real signal here

**There's roughly a 4-6x price jump from "passive, fixed" to "passive,
adjustable" ($25-30 → $179-189), and then another 4-10x jump from
"passive, adjustable" to "electronic/active" ($179 → $799-2,000).** That
second jump is the one that actually matters for Haven's positioning:
the market has already demonstrated real willingness to pay a large
premium specifically for *active/electronic* control over ambient sound,
not just a better passive filter. Sensaphonics' price point isn't a
custom-IEM tax alone either — their $799 *universal-fit* model, no
custom molding at all, is still 4x Minuendo's adjustable passive product.

This is a genuinely useful anchor for Haven's own pricing conversation:
positioning as "better passive" (competing with Minuendo's $179-189
tier) would badly undersell a DSP/app-controlled product relative to
what this exact market has already shown it will pay for active control
— Sensaphonics' $799-2,000 range is the more realistic reference class,
not the passive-earplug tier.

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
