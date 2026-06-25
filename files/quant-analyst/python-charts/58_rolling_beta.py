"""
Chart 58 — Rolling Beta
Time-varying CAPM beta estimated on a rolling window.
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


ROLL_WINDOW = 126


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    merged = df[["Return"]].join(bench[["Return"]], rsuffix="_bench").dropna()

    rolling_beta  = []
    rolling_alpha = []
    rolling_r_sq  = []
    dates         = []

    for end in range(ROLL_WINDOW, len(merged)):
        window = merged.iloc[end - ROLL_WINDOW : end]
        slope, intercept, r_value, _, _ = stats.linregress(
            window["Return_bench"], window["Return"]
        )
        rolling_beta.append(slope)
        rolling_alpha.append(intercept * 252 * 100)
        rolling_r_sq.append(r_value**2)
        dates.append(merged.index[end])

    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

    # Beta
    ax = axes[0]
    ax.plot(dates, rolling_beta, color=COLOURS["primary"], linewidth=0.8)
    ax.axhline(1.0, color=COLOURS["red"], linewidth=0.8, linestyle="--", label="Beta = 1")
    ax.axhline(np.mean(rolling_beta), color=COLOURS["amber"], linewidth=0.8, linestyle=":",
               label=f"Mean: {np.mean(rolling_beta):.2f}")
    ax.set_ylabel("Beta")
    ax.set_title(f"{cfg['name']} — Rolling Beta ({ROLL_WINDOW}-Day)")
    ax.legend(fontsize=8)

    # Alpha
    ax = axes[1]
    ax.plot(dates, rolling_alpha, color=COLOURS["green"], linewidth=0.8)
    ax.axhline(0, color=COLOURS["muted"], linewidth=0.5, linestyle=":")
    ax.fill_between(dates, 0, rolling_alpha,
                    where=[a >= 0 for a in rolling_alpha],
                    alpha=0.15, color=COLOURS["green"])
    ax.fill_between(dates, 0, rolling_alpha,
                    where=[a < 0 for a in rolling_alpha],
                    alpha=0.15, color=COLOURS["red"])
    ax.set_ylabel("Alpha (% ann.)")
    ax.set_title("Rolling Jensen's Alpha")

    # R-squared
    ax = axes[2]
    ax.plot(dates, rolling_r_sq, color=COLOURS["amber"], linewidth=0.8)
    ax.axhline(np.mean(rolling_r_sq), color=COLOURS["red"], linewidth=0.8, linestyle="--",
               label=f"Mean: {np.mean(rolling_r_sq):.2f}")
    ax.set_ylabel("R-squared")
    ax.set_ylim(0, 1)
    ax.set_title("Rolling R-squared (Market Explanatory Power)")
    ax.legend(fontsize=8)
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "58_rolling_beta")
