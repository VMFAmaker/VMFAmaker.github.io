"""
Chart 49 — Correlation Heatmap
Pairwise return correlations across the asset and its peers.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices, load_peers

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    peers = load_peers()
    returns = pd.DataFrame({cfg["name"]: df["Return"]})

    for ticker, peer_df in peers.items():
        code_name = cfg["peers"].get(ticker, ticker)
        returns[code_name] = peer_df["Return"]

    returns = returns.dropna()
    corr = returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1)

    n = len(corr)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(corr.columns, fontsize=9)

    for i in range(n):
        for j in range(n):
            val = corr.values[i, j]
            colour = "white" if abs(val) > 0.7 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=9, color=colour, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Correlation")

    ax.set_title(f"{cfg['name']} — Peer Correlation Matrix")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "49_correlation_heatmap")
