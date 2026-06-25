"""
Chart 30 — Relative Strength Index (RSI)
Price and RSI(14) with overbought/oversold bands.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


RSI_PERIOD = 14
OVERBOUGHT = 70
OVERSOLD   = 30


def compute_rsi(close, period=RSI_PERIOD):
    delta = close.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def plot(df, cfg=CONFIG):
    apply_style()

    rsi = compute_rsi(df["Close"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [2, 1]},
                                    sharex=True)

    ax1.plot(df.index, df["Close"], color=COLOURS["primary"], linewidth=0.8)
    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{cfg['name']} — RSI ({RSI_PERIOD})")

    ax2.plot(rsi.index, rsi.values, color=COLOURS["primary"], linewidth=0.8)
    ax2.axhline(OVERBOUGHT, color=COLOURS["red"],   linewidth=0.8, linestyle="--", label="Overbought")
    ax2.axhline(OVERSOLD,   color=COLOURS["green"], linewidth=0.8, linestyle="--", label="Oversold")
    ax2.axhline(50, color=COLOURS["muted"], linewidth=0.5, linestyle=":")
    ax2.fill_between(rsi.index, OVERBOUGHT, rsi.values,
                     where=rsi.values >= OVERBOUGHT, alpha=0.2, color=COLOURS["red"])
    ax2.fill_between(rsi.index, OVERSOLD, rsi.values,
                     where=rsi.values <= OVERSOLD, alpha=0.2, color=COLOURS["green"])
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    ax2.legend(loc="upper left", fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "30_rsi")
