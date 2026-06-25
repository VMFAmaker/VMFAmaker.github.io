"""
Chart 10 — Rolling Statistics
Rolling mean, std, skewness, and kurtosis of returns (252-day window).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


WINDOW = 252  # 1 year


def plot(df, cfg=CONFIG):
    apply_style()

    r = df["Return"]

    roll_mean = r.rolling(WINDOW).mean() * 252 * 100
    roll_std  = r.rolling(WINDOW).std()  * np.sqrt(252) * 100
    roll_skew = r.rolling(WINDOW).skew()
    roll_kurt = r.rolling(WINDOW).kurt()

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), sharex=True)

    panels = [
        (axes[0, 0], roll_mean, "Annualised Mean (%)",     r.mean() * 252 * 100),
        (axes[0, 1], roll_std,  "Annualised Volatility (%)", r.std() * np.sqrt(252) * 100),
        (axes[1, 0], roll_skew, "Skewness",                  float(r.skew())),
        (axes[1, 1], roll_kurt, "Excess Kurtosis",           float(r.kurt())),
    ]

    for ax, series, ylabel, full_sample in panels:
        ax.plot(series.index, series.values, color=COLOURS["primary"], linewidth=0.8)
        ax.axhline(full_sample, color=COLOURS["red"], linewidth=1, linestyle="--",
                    label=f"Full sample: {full_sample:.2f}")
        ax.set_ylabel(ylabel)
        ax.legend(fontsize=8)

    format_date_axis(axes[1, 0])
    format_date_axis(axes[1, 1])

    fig.suptitle(f"{cfg['name']} — Rolling Statistics ({WINDOW}-Day Window)",
                 fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "10_rolling_statistics")
