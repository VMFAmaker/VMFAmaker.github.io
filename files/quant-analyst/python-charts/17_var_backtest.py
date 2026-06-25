"""
Chart 17 — VaR Backtest
Actual returns vs VaR forecasts with violation markers and coverage statistics.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


CONFIDENCE  = 0.99
ROLL_WINDOW = 252


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values
    dates   = df.index

    hist_var = np.full(len(returns), np.nan)
    norm_var = np.full(len(returns), np.nan)

    for i in range(ROLL_WINDOW, len(returns)):
        window = returns[i - ROLL_WINDOW : i]
        hist_var[i] = np.percentile(window, (1 - CONFIDENCE) * 100)
        norm_var[i] = stats.norm.ppf(1 - CONFIDENCE,
                                     loc=np.mean(window),
                                     scale=np.std(window, ddof=1))

    valid = ~np.isnan(hist_var)
    d   = dates[valid]
    r   = returns[valid]
    hv  = hist_var[valid]
    nv  = norm_var[valid]

    hist_violations = r < hv
    norm_violations = r < nv

    expected_rate = 1 - CONFIDENCE
    hist_rate = hist_violations.sum() / len(r)
    norm_rate = norm_violations.sum() / len(r)

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(d, r * 100,  color=COLOURS["muted"],   linewidth=0.5, alpha=0.6, label="Returns")
    ax.plot(d, hv * 100, color=COLOURS["primary"],  linewidth=0.8, label="Historical VaR")
    ax.plot(d, nv * 100, color=COLOURS["amber"],    linewidth=0.8, label="Normal VaR")

    ax.scatter(d[hist_violations], r[hist_violations] * 100,
               color=COLOURS["red"], s=15, zorder=5, label="Violations (Historical)")
    ax.scatter(d[norm_violations], r[norm_violations] * 100,
               color=COLOURS["red"], s=15, zorder=5, marker="x", label="Violations (Normal)")

    note = (f"Expected: {expected_rate:.1%} | "
            f"Historical: {hist_rate:.1%} ({hist_violations.sum()}) | "
            f"Normal: {norm_rate:.1%} ({norm_violations.sum()})")
    ax.text(0.02, 0.97, note, transform=ax.transAxes, fontsize=8,
            verticalalignment="top", bbox=dict(boxstyle="round,pad=0.3",
            facecolor="white", edgecolor=COLOURS["muted"], alpha=0.8))

    ax.set_title(f"{cfg['name']} — VaR Backtest ({CONFIDENCE:.0%}, {ROLL_WINDOW}-Day Rolling)")
    ax.set_ylabel("Daily Return (%)")
    ax.legend(loc="lower left", fontsize=7)
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "17_var_backtest")
