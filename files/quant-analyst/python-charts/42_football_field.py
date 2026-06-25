"""
Chart 42 — Football Field Valuation Chart
Range of implied valuations from different methods shown as horizontal bars.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, PALETTE, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    current_price = df["Close"].iloc[-1]

    methods = [
        ("DCF (Bull)",       current_price * 0.85, current_price * 1.25),
        ("DCF (Base)",       current_price * 0.65, current_price * 0.95),
        ("DCF (Bear)",       current_price * 0.45, current_price * 0.70),
        ("Peer P/E",         current_price * 0.80, current_price * 1.10),
        ("Peer EV/EBITDA",   current_price * 0.75, current_price * 1.15),
        ("52-Week Range",    df["Close"].min(),     df["Close"].max()),
        ("Analyst Consensus", current_price * 0.90, current_price * 1.20),
    ]

    fig, ax = plt.subplots(figsize=(12, 7))

    labels = [m[0] for m in methods]
    y = np.arange(len(labels))

    for i, (name, low, high) in enumerate(methods):
        mid = (low + high) / 2
        colour = PALETTE[i % len(PALETTE)]
        ax.barh(i, high - low, left=low, height=0.6,
                color=colour, alpha=0.7, edgecolor="white")
        ax.plot(mid, i, "o", color="white", markersize=6, zorder=5)
        ax.text(low - 2, i, f"${low:.0f}", ha="right", va="center", fontsize=8)
        ax.text(high + 2, i, f"${high:.0f}", ha="left", va="center", fontsize=8)

    ax.axvline(current_price, color=COLOURS["red"], linewidth=2, linestyle="-",
               label=f"Current: ${current_price:.2f}", zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Price ($)")
    ax.set_title(f"{cfg['name']} — Valuation Football Field")
    ax.legend(loc="lower right")
    ax.invert_yaxis()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "42_football_field")
