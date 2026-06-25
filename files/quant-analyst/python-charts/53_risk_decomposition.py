"""
Chart 53 — Risk Decomposition
Breakdown of total risk into systematic (market) and idiosyncratic components.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices, load_benchmark

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


ROLL_WINDOW = 252


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    merged = df[["Return"]].join(bench[["Return"]], rsuffix="_bench").dropna()

    total_var     = []
    systematic    = []
    idiosyncratic = []
    dates         = []

    for end in range(ROLL_WINDOW, len(merged)):
        window = merged.iloc[end - ROLL_WINDOW : end]
        x = window["Return_bench"].values
        y = window["Return"].values

        slope, intercept, r_value, _, _ = stats.linregress(x, y)
        r_sq = r_value ** 2

        total = np.var(y, ddof=1) * 252
        syst  = total * r_sq
        idio  = total * (1 - r_sq)

        total_var.append(total * 1e4)
        systematic.append(syst * 1e4)
        idiosyncratic.append(idio * 1e4)
        dates.append(merged.index[end])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

    # Stacked area
    ax1.fill_between(dates, 0, systematic, alpha=0.6,
                     color=COLOURS["primary"], label="Systematic (Market)")
    ax1.fill_between(dates, systematic, [s + i for s, i in zip(systematic, idiosyncratic)],
                     alpha=0.6, color=COLOURS["amber"], label="Idiosyncratic")
    ax1.plot(dates, total_var, color=COLOURS["red"], linewidth=0.8, label="Total Variance")
    ax1.set_ylabel("Annualised Variance (bps sq)")
    ax1.set_title(f"{cfg['name']} — Risk Decomposition ({ROLL_WINDOW}-Day Rolling)")
    ax1.legend(fontsize=8)
    format_date_axis(ax1)

    # R-squared over time (proportion systematic)
    r_sq_series = [s / t if t > 0 else 0 for s, t in zip(systematic, total_var)]
    ax2.plot(dates, r_sq_series, color=COLOURS["primary"], linewidth=0.8)
    ax2.fill_between(dates, 0, r_sq_series, alpha=0.15, color=COLOURS["primary"])
    ax2.axhline(np.mean(r_sq_series), color=COLOURS["red"], linewidth=1, linestyle="--",
                label=f"Mean R-sq: {np.mean(r_sq_series):.2f}")
    ax2.set_ylabel("R-squared")
    ax2.set_ylim(0, 1)
    ax2.set_title("Proportion of Systematic Risk")
    ax2.legend(fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "53_risk_decomposition")
