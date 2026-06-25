"""
Chart 41 — Peer Comparison (Multiples)
Grouped bar chart comparing valuation multiples across peers.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, PALETTE, save_chart
from _data   import load_peer_fundamentals

import numpy as np
import matplotlib.pyplot as plt


MULTIPLES = ["P/E", "Forward P/E", "P/B", "EV/EBITDA"]


def plot(df=None, cfg=CONFIG):
    apply_style()

    fundamentals = load_peer_fundamentals()

    tickers = [cfg["ticker"]] + list(cfg["peers"].keys())
    names   = [cfg["name"]]   + list(cfg["peers"].values())

    data = {m: [] for m in MULTIPLES}
    valid_names = []

    for ticker, name in zip(tickers, names):
        info = fundamentals.get(ticker, {})
        if not info:
            continue

        valid_names.append(name)
        data["P/E"].append(info.get("trailingPE", np.nan))
        data["Forward P/E"].append(info.get("forwardPE", np.nan))
        data["P/B"].append(info.get("priceToBook", np.nan))
        data["EV/EBITDA"].append(info.get("enterpriseToEbitda", np.nan))

    if not valid_names:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No peer data available", transform=ax.transAxes, ha="center")
        return fig

    n_names = len(valid_names)
    n_mult  = len(MULTIPLES)
    x = np.arange(n_names)
    width = 0.8 / n_mult

    fig, ax = plt.subplots(figsize=(14, 7))

    for i, mult in enumerate(MULTIPLES):
        vals = data[mult]
        offset = (i - n_mult / 2 + 0.5) * width
        colour = PALETTE[i % len(PALETTE)]
        bars = ax.bar(x + offset, vals, width, label=mult, color=colour, alpha=0.8)

        for bar, val in zip(bars, vals):
            if not np.isnan(val):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                        f"{val:.1f}", ha="center", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels(valid_names, rotation=30, ha="right")
    ax.set_ylabel("Multiple")
    ax.set_title(f"{cfg['name']} — Peer Valuation Comparison")
    ax.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot()
    save_chart(fig, "41_peer_comparison")
