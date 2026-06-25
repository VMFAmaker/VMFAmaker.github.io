"""
Chart 40 — DCF Valuation Distribution
Monte Carlo DCF with simulated growth, margins, WACC. Histogram of fair values.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


N_SIMS       = 50000
YEARS        = 5
BASE_REVENUE = 400e9
SHARES       = 15.4e9

PARAMS = {
    "rev_growth":   (0.05, 0.08, 0.12),
    "margin":       (0.25, 0.30, 0.35),
    "wacc":         (0.08, 0.10, 0.13),
    "terminal_g":   (0.02, 0.025, 0.035),
    "tax_rate":     (0.18, 0.21, 0.24),
}


def run_dcf_sim(rng):
    rev_g = rng.triangular(*PARAMS["rev_growth"], N_SIMS)
    margin = rng.triangular(*PARAMS["margin"], N_SIMS)
    wacc = rng.normal(PARAMS["wacc"][1], 0.01, N_SIMS)
    wacc = np.clip(wacc, 0.05, 0.20)
    term_g = rng.triangular(*PARAMS["terminal_g"], N_SIMS)
    tax = rng.triangular(*PARAMS["tax_rate"], N_SIMS)

    ev = np.zeros(N_SIMS)
    for _ in range(YEARS):
        rev = BASE_REVENUE * (1 + rev_g)
        ebit = rev * margin
        nopat = ebit * (1 - tax)
        fcf = nopat * 0.9
        ev += fcf / (1 + wacc)**(_ + 1)

    terminal = fcf * (1 + term_g) / (wacc - term_g)
    terminal = np.where(wacc > term_g, terminal, 0)
    ev += terminal / (1 + wacc)**YEARS

    return ev / SHARES


def plot(df, cfg=CONFIG):
    apply_style()

    rng = np.random.default_rng(42)
    fair_values = run_dcf_sim(rng)
    fair_values = fair_values[fair_values > 0]

    current_price = df["Close"].iloc[-1]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.hist(fair_values, bins=150, color=COLOURS["primary"], alpha=0.7,
            edgecolor="white", linewidth=0.2, density=True)

    ax.axvline(current_price, color=COLOURS["red"], linewidth=2, linestyle="-",
               label=f"Market Price: ${current_price:.2f}")
    ax.axvline(np.median(fair_values), color=COLOURS["amber"], linewidth=1.5, linestyle="--",
               label=f"Median Fair Value: ${np.median(fair_values):.2f}")
    ax.axvline(np.percentile(fair_values, 25), color=COLOURS["muted"], linewidth=1, linestyle=":",
               label=f"25th pctile: ${np.percentile(fair_values, 25):.2f}")
    ax.axvline(np.percentile(fair_values, 75), color=COLOURS["muted"], linewidth=1, linestyle=":",
               label=f"75th pctile: ${np.percentile(fair_values, 75):.2f}")

    pct_overvalued = (fair_values < current_price).sum() / len(fair_values) * 100

    ax.text(0.02, 0.95,
            f"Sims below market: {pct_overvalued:.1f}%\nMean: ${np.mean(fair_values):.2f}",
            transform=ax.transAxes, fontsize=9, verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLOURS["muted"]))

    ax.set_xlabel("Fair Value per Share ($)")
    ax.set_ylabel("Density")
    ax.set_title(f"{cfg['name']} — Monte Carlo DCF Distribution ({N_SIMS:,} simulations)")
    ax.legend(loc="upper right", fontsize=8)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "40_dcf_distribution")
