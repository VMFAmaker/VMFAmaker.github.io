"""
Chart 32 — Bollinger Bands
Price with 20-day SMA and +/- 2 standard deviation bands. Width panel below.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import matplotlib.pyplot as plt


WINDOW = 20
NUM_SD = 2


def plot(df, cfg=CONFIG):
    apply_style()

    close = df["Close"]
    sma   = close.rolling(WINDOW).mean()
    std   = close.rolling(WINDOW).std()

    upper = sma + NUM_SD * std
    lower = sma - NUM_SD * std
    width = (upper - lower) / sma * 100

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [3, 1]},
                                    sharex=True)

    ax1.plot(close.index, close.values, color=COLOURS["primary"], linewidth=0.7, label="Price")
    ax1.plot(sma.index, sma.values, color=COLOURS["amber"], linewidth=0.8, label=f"SMA {WINDOW}")
    ax1.plot(upper.index, upper.values, color=COLOURS["muted"], linewidth=0.5)
    ax1.plot(lower.index, lower.values, color=COLOURS["muted"], linewidth=0.5)
    ax1.fill_between(close.index, lower, upper, alpha=0.1, color=COLOURS["primary"],
                     label=f"Bollinger Band ({NUM_SD}sd)")

    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{cfg['name']} — Bollinger Bands ({WINDOW},{NUM_SD})")
    ax1.legend(loc="upper left", fontsize=8)

    ax2.plot(width.index, width.values, color=COLOURS["primary"], linewidth=0.8)
    ax2.fill_between(width.index, 0, width, alpha=0.15, color=COLOURS["primary"])
    ax2.set_ylabel("Band Width (%)")
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "32_bollinger_bands")
