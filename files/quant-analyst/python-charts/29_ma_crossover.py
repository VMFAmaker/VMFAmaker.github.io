"""
Chart 29 — Moving Average Crossover
Price with SMA 50 and SMA 200. Golden cross / death cross signals marked.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


SHORT_WINDOW = 50
LONG_WINDOW  = 200


def plot(df, cfg=CONFIG):
    apply_style()

    close = df["Close"]
    sma_s = close.rolling(SHORT_WINDOW).mean()
    sma_l = close.rolling(LONG_WINDOW).mean()

    cross_up   = (sma_s > sma_l) & (sma_s.shift(1) <= sma_l.shift(1))
    cross_down = (sma_s < sma_l) & (sma_s.shift(1) >= sma_l.shift(1))

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(close.index, close.values, color=COLOURS["muted"], linewidth=0.6, alpha=0.7, label="Price")
    ax.plot(sma_s.index, sma_s.values, color=COLOURS["primary"], linewidth=1.2,
            label=f"SMA {SHORT_WINDOW}")
    ax.plot(sma_l.index, sma_l.values, color=COLOURS["amber"], linewidth=1.2,
            label=f"SMA {LONG_WINDOW}")

    golden = close.index[cross_up]
    death  = close.index[cross_down]

    ax.scatter(golden, close.loc[golden], marker="^", color=COLOURS["green"],
               s=80, zorder=5, label="Golden Cross")
    ax.scatter(death, close.loc[death], marker="v", color=COLOURS["red"],
               s=80, zorder=5, label="Death Cross")

    ax.set_title(f"{cfg['name']} — Moving Average Crossover ({SHORT_WINDOW}/{LONG_WINDOW})")
    ax.set_ylabel("Price ($)")
    ax.legend()
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "29_ma_crossover")
