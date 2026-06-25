"""
Chart 36 — Hurst Exponent
Rolling Hurst exponent to identify trending (H>0.5) vs mean-reverting (H<0.5) regimes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, add_zero_line, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


ROLL_WINDOW = 252
LAG_RANGE   = range(2, 100)


def hurst(ts):
    """Rescaled range (R/S) method for Hurst exponent estimation."""
    n = len(ts)
    if n < 20:
        return np.nan

    lags = []
    rs   = []

    for lag in LAG_RANGE:
        if lag >= n:
            break

        chunks = n // lag
        if chunks < 1:
            break

        rs_vals = []
        for c in range(chunks):
            chunk = ts[c * lag : (c + 1) * lag]
            mean_chunk = np.mean(chunk)
            deviations = np.cumsum(chunk - mean_chunk)
            r = np.max(deviations) - np.min(deviations)
            s = np.std(chunk, ddof=1)
            if s > 0:
                rs_vals.append(r / s)

        if rs_vals:
            lags.append(lag)
            rs.append(np.mean(rs_vals))

    if len(lags) < 5:
        return np.nan

    log_lags = np.log(lags)
    log_rs   = np.log(rs)
    slope, _ = np.polyfit(log_lags, log_rs, 1)
    return slope


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values
    dates   = df.index

    hurst_values = np.full(len(returns), np.nan)
    for i in range(ROLL_WINDOW, len(returns)):
        hurst_values[i] = hurst(returns[i - ROLL_WINDOW : i])

    valid = ~np.isnan(hurst_values)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [1, 2]},
                                    sharex=True)

    ax1.plot(dates, df["Close"].values, color=COLOURS["primary"], linewidth=0.7)
    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{cfg['name']} — Rolling Hurst Exponent ({ROLL_WINDOW}-Day)")

    ax2.plot(dates[valid], hurst_values[valid], color=COLOURS["primary"], linewidth=0.8)
    ax2.axhline(0.5, color=COLOURS["red"], linewidth=1, linestyle="--", label="H = 0.5 (Random Walk)")
    ax2.fill_between(dates[valid], 0.5, hurst_values[valid],
                     where=hurst_values[valid] > 0.5,
                     alpha=0.15, color=COLOURS["green"], label="Trending (H > 0.5)")
    ax2.fill_between(dates[valid], 0.5, hurst_values[valid],
                     where=hurst_values[valid] < 0.5,
                     alpha=0.15, color=COLOURS["red"], label="Mean-Reverting (H < 0.5)")

    ax2.set_ylabel("Hurst Exponent")
    ax2.set_ylim(0.2, 0.8)
    ax2.legend(loc="upper left", fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "36_hurst_exponent")
