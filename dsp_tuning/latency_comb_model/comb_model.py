"""Hear-through latency vs comb-filter ripple for a sealed earpiece.

Eardrum pressure (relative to the open ear) is modelled as the sum of two paths:
  leak:      sound passing the seal, attenuated by the earplug's insertion loss A(f), no delay
  processed: mic -> DSP -> speaker, gain G (dB re open ear), delayed by tau
  H(f) = 10^(-A(f)/20) + 10^(G/20) * exp(-j 2 pi f tau)
The ripple a listener could hear is the peak-to-notch swing of |H| inside each
1/3-octave band (a notch only matters if it falls where the ear resolves it).

Attenuation curves (dB at 125, 250, 500, 1k, 2k, 4k, 8k Hz):
  good      3M 1100 foam plug, manufacturer mean attenuation (3M 1100 TDS)
  mediocre  same curve minus 8 dB (about one standard deviation of that data:
            a real-world earbud tip / imperfect fit) -- assumption
  vented    open-ish fit: little low-frequency attenuation -- assumption,
            in line with vented hearing-aid domes
Run: python comb_model.py  (writes PNGs + results.md next to this file)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
ATT_F = np.array([125, 250, 500, 1000, 2000, 4000, 8000], dtype=float)
SEALS = {
    "good (foam)": np.array([20.3, 20.6, 23.2, 26.5, 32.3, 32.0, 41.1]),
    "mediocre (-8 dB)": np.array([20.3, 20.6, 23.2, 26.5, 32.3, 32.0, 41.1]) - 8,
    "vented / poor": np.array([3.0, 3.0, 5.0, 8.0, 14.0, 18.0, 22.0]),
}
TAUS_MS = [0.05, 0.1, 0.3, 0.5, 1, 2, 3, 5, 10]
GAINS_DB = {"transparency (G=0 dB)": 0.0, "protection (G=-10 dB)": -10.0}
F = np.geomspace(100, 10000, 20000)
BANDS = 1000 * 2.0 ** (np.arange(-10, 11) / 3)  # 1/3-octave centres ~100 Hz-10 kHz
BANDS = BANDS[(BANDS >= 125) & (BANDS <= 8000)]


def attenuation(curve):
    return np.interp(np.log10(F), np.log10(ATT_F), curve)


def response_db(curve, gain_db, tau_s):
    h = 10 ** (-attenuation(curve) / 20) + 10 ** (gain_db / 20) * np.exp(-2j * np.pi * F * tau_s)
    return 20 * np.log10(np.abs(h))


def worst_band_ripple(mag_db):
    worst = 0.0
    for fc in BANDS:
        sel = (F >= fc / 2 ** (1 / 6)) & (F < fc * 2 ** (1 / 6))
        worst = max(worst, mag_db[sel].max() - mag_db[sel].min())
    return worst


def main():
    rows = []
    for gname, g in GAINS_DB.items():
        for sname, curve in SEALS.items():
            rows.append((gname, sname, [worst_band_ripple(response_db(curve, g, t / 1e3)) for t in TAUS_MS]))

    lines = [
        "| gain | seal | " + " | ".join(f"{t} ms" for t in TAUS_MS) + " |",
        "|---|---|" + "---|" * len(TAUS_MS),
    ]
    for gname, sname, r in rows:
        lines.append(f"| {gname} | {sname} | " + " | ".join(f"{x:.1f}" for x in r) + " |")
    table = "\n".join(lines)
    (HERE / "results.md").write_text(
        "Worst 1/3-octave peak-to-notch ripple (dB), 125 Hz-8 kHz\n\n" + table + "\n"
    )
    print(table)

    for gname, g in GAINS_DB.items():
        fig, axes = plt.subplots(len(SEALS), 1, figsize=(9, 9), sharex=True)
        for ax, (sname, curve) in zip(axes, SEALS.items()):
            for t in (0.1, 0.3, 1, 3, 10):
                ax.semilogx(F, response_db(curve, g, t / 1e3), lw=0.8, label=f"{t} ms")
            ax.set_title(f"{sname} seal, {gname}")
            ax.set_ylabel("dB re open ear")
            ax.grid(True, which="both", alpha=0.3)
            ax.set_xlim(100, 10000)
        axes[0].legend(ncol=5, fontsize=8)
        axes[-1].set_xlabel("Frequency (Hz)")
        fig.tight_layout()
        fig.savefig(HERE / f"response_{'transparency' if g == 0 else 'protection'}.png", dpi=110)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for gname, sname, r in rows:
        ax.semilogx(TAUS_MS, r, marker="o", ls="-" if "transp" in gname else "--",
                    label=f"{sname}, {gname.split(' ')[0]}")
    ax.axhline(3, color="grey", lw=0.8, ls=":")
    ax.set_xlabel("Hear-through latency (ms)")
    ax.set_ylabel("Worst 1/3-oct ripple (dB)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(HERE / "ripple_vs_latency.png", dpi=110)


if __name__ == "__main__":
    main()
