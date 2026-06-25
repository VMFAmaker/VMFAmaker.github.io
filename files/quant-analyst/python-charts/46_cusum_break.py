"""
Chart 46 — CUSUM Structural Break Test
Cumulative sum of recursive residuals to detect structural breaks in the return series.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import breaks_cusumolsresid


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].dropna().values
    dates   = df["Return"].dropna().index

    n = len(returns)
    mean_r = np.mean(returns)
    std_r  = np.std(returns, ddof=1)

    cusum = np.cumsum(returns - mean_r) / std_r

    # Critical boundaries (5% significance, Brownian bridge)
    t_norm = np.arange(1, n + 1) / n
    boundary_upper =  1.358 * np.sqrt(n) * (t_norm + 0.01)  # approximate
    boundary_lower = -boundary_upper

    # Simple boundary: +/- a * sqrt(n) + 2*a*t/n
    a = 0.948
    upper = a * (np.sqrt(n) + 2 * np.arange(1, n + 1) / np.sqrt(n))
    lower = -upper

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [1, 2]},
                                    sharex=True)

    # Price
    ax1.plot(dates, df["Close"].reindex(dates).values, color=COLOURS["primary"], linewidth=0.7)
    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{cfg['name']} — CUSUM Structural Break Test")

    # CUSUM
    ax2.plot(dates, cusum, color=COLOURS["primary"], linewidth=0.8, label="CUSUM")
    ax2.plot(dates, upper, color=COLOURS["red"], linewidth=0.8, linestyle="--", label="5% Critical Boundary")
    ax2.plot(dates, lower, color=COLOURS["red"], linewidth=0.8, linestyle="--")
    ax2.fill_between(dates, lower, upper, alpha=0.05, color=COLOURS["red"])

    breaches = np.where(np.abs(cusum) > upper)[0]
    if len(breaches) > 0:
        first_breach = breaches[0]
        ax2.axvline(dates[first_breach], color=COLOURS["amber"], linewidth=1.5,
                    linestyle="-", label=f"First breach: {dates[first_breach].strftime('%Y-%m-%d')}")
        ax1.axvline(dates[first_breach], color=COLOURS["amber"], linewidth=1, linestyle="--", alpha=0.5)

    ax2.axhline(0, color=COLOURS["muted"], linewidth=0.5)
    ax2.set_ylabel("CUSUM Statistic")
    ax2.legend(loc="upper left", fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "46_cusum_break")
