"""
Chart 33 — Momentum Bars
Multi-period return momentum (1M, 3M, 6M, 12M) as a grouped bar chart.
Rolling version shows momentum regime changes over time.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


PERIODS = {"1M": 21, "3M": 63, "6M": 126, "12M": 252}


def plot(df, cfg=CONFIG):
    apply_style()

    close = df["Close"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7))

    # Current momentum snapshot
    labels = list(PERIODS.keys())
    values = []
    for name, days in PERIODS.items():
        if len(close) > days:
            ret = (close.iloc[-1] / close.iloc[-days] - 1) * 100
        else:
            ret = 0
        values.append(ret)

    bar_cols = [COLOURS["green"] if v >= 0 else COLOURS["red"] for v in values]
    bars = ax1.bar(labels, values, color=bar_cols, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, values):
        y_pos = val + 0.5 if val >= 0 else val - 1.5
        ax1.text(bar.get_x() + bar.get_width() / 2, y_pos,
                 f"{val:+.1f}%", ha="center", fontsize=10, fontweight="bold")

    ax1.axhline(0, color=COLOURS["text"], linewidth=0.5)
    ax1.set_ylabel("Return (%)")
    ax1.set_title(f"{cfg['name']} — Current Momentum Snapshot")

    # Rolling momentum over time
    period_colours = [COLOURS["primary"], COLOURS["amber"], COLOURS["green"], COLOURS["red"]]
    for (name, days), col in zip(PERIODS.items(), period_colours):
        rolling_mom = (close / close.shift(days) - 1) * 100
        ax2.plot(rolling_mom.index, rolling_mom.values, color=col,
                 linewidth=0.7, label=name, alpha=0.8)

    ax2.axhline(0, color=COLOURS["muted"], linewidth=0.5)
    ax2.set_ylabel("Return (%)")
    ax2.set_title("Rolling Momentum")
    ax2.legend(loc="upper left", fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "33_momentum_bars")
