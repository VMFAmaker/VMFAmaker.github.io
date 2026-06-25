"""
Chart 31 — MACD (Moving Average Convergence Divergence)
MACD line, signal line, and histogram with price overlay.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


FAST   = 12
SLOW   = 26
SIGNAL = 9


def plot(df, cfg=CONFIG):
    apply_style()

    close = df["Close"]
    ema_fast = close.ewm(span=FAST, adjust=False).mean()
    ema_slow = close.ewm(span=SLOW, adjust=False).mean()

    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=SIGNAL, adjust=False).mean()
    histogram   = macd_line - signal_line

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [2, 1]},
                                    sharex=True)

    ax1.plot(close.index, close.values, color=COLOURS["primary"], linewidth=0.8)
    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{cfg['name']} — MACD ({FAST},{SLOW},{SIGNAL})")

    ax2.plot(macd_line.index, macd_line.values, color=COLOURS["primary"],
             linewidth=0.8, label="MACD")
    ax2.plot(signal_line.index, signal_line.values, color=COLOURS["red"],
             linewidth=0.8, label="Signal")

    colours = [COLOURS["green"] if v >= 0 else COLOURS["red"] for v in histogram.values]
    ax2.bar(histogram.index, histogram.values, color=colours, width=1, alpha=0.5)

    ax2.axhline(0, color=COLOURS["muted"], linewidth=0.5)
    ax2.set_ylabel("MACD")
    ax2.legend(loc="upper left", fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "31_macd")
