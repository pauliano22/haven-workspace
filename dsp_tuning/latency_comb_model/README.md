# Hear-through latency vs. comb filtering (sealed earpiece)

This model asks whether Haven really needs the 300 µs hear-through latency target from
`HARDWARE_ARCHITECTURE_DECISION.md` §2 (haven-dev-board-kicad). That target came from
counting where comb-filter notches land (`f = (2k+1)/2Δt`). It assumed the leaked sound and
the processed sound arrive at **equal level**. How deep the notches are depends on the level
ratio between the two paths, and a seal makes the leaked path 20–40 dB quieter.

Run with `python comb_model.py` (needs numpy and matplotlib). It writes `results.md`,
`ripple_vs_latency.png`, `response_transparency.png` and `response_protection.png`.

## Model
`H(f) = 10^(-A(f)/20) + 10^(G/20)·e^(-j2πfτ)`, relative to the open ear.

- `A(f)` is the seal's attenuation.
- `G` is the hear-through gain.
- `τ` is the latency.

The metric is the worst peak-to-notch swing inside any 1/3-octave band from 125 Hz to 8 kHz.

Seal curves:

- **good**: the manufacturer's mean attenuation for the 3M 1100 foam plug, 20–41 dB
  ([3M 1100 TDS](https://multimedia.3m.com/mws/media/836362O/3m-1100-tds-pdf.pdf)).
- **mediocre**: the same curve minus 8 dB, roughly one standard deviation of that data
  (assumed).
- **vented/poor**: 3–22 dB (assumed).

## Results: worst ripple (dB)

| gain | seal | 0.05 | 0.1 | 0.3 | 0.5 | 1 | 2 | 3 | 5 | 10 ms |
|---|---|---|---|---|---|---|---|---|---|---|
| transparency, G=0 | good | 0.1 | 0.1 | 0.3 | 0.3 | 0.5 | 0.8 | 0.9 | 1.3 | 1.4 |
| transparency, G=0 | mediocre | 0.2 | 0.3 | 0.7 | 0.9 | 1.3 | 2.1 | 2.2 | 3.1 | 3.7 |
| transparency, G=0 | vented | 0.5 | 0.7 | 1.6 | 3.0 | 5.1 | 7.2 | 8.6 | 11.4 | 13.5 |
| protection, G=−10 | good | 0.2 | 0.3 | 0.9 | 1.1 | 1.6 | 2.7 | 2.7 | 3.9 | 4.7 |
| protection, G=−10 | mediocre | 0.5 | 0.8 | 2.2 | 2.8 | 4.9 | 7.5 | 9.7 | 11.9 | 14.8 |
| protection, G=−10 | vented | 1.2 | 2.6 | 8.3 | 8.7 | 18.5 | 46.2 | 27.8 | 36.5 | 45.2 |

I found no published dB threshold for audible ripple. Sources say coloration is most noticeable when
the two paths are within about ±10 dB of each other, which works out to roughly 6 dB of ripple
([Hearing Review 2020](https://hearingreview.com/hearing-products/hearing-aids/bte/reducing-hearing-aid-delay-for-optimal-sound-quality-a-new-paradigm-in-processing)).
This README uses **3 dB** as a conservative working limit. That's an assumption, not a measured number.

Separately, delay is noticed as an echo or doubled sound once it passes about 14–30 ms in closed
fittings (Stone &amp; Moore 2005, summarized in the
[Goehring et al. manuscript](https://eprints.soton.ac.uk/414900/1/Goehring_DelayTolerance_Manuscript.docx)).

## Verdict
With a good seal, every latency up to 10 ms stays under 1.5 dB of ripple at transparency
gain. Up to 3 ms stays under 3 dB even in protection mode, where the processed sound is turned
down and the leaked sound counts for relatively more. The 300 µs target is only needed if the fit
is vented or leaky.

The result depends heavily on the seal. A mediocre fit in protection mode passes 3 dB at
about 0.5 ms, and a vented fit fails almost everywhere. Low-frequency leak around a poorly
fitted tip is the main risk, so fit matters as much as the codec choice.

Not modeled: the user's own voice (bone-conducted sound mixing with the delayed hear-through
signal; real data puts own-voice tolerance on the lower end of the 14–30 ms range), the
receiver's own acoustics, and differences between individual ears. Verify with a quick
listening test on a sealed tip.
