"""
Chart 50 — Rolling Correlation
Time-varying correlation between the asset and its benchmark/peers.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, PALETTE, format_date_axis, save_chart
from _data   import load_prices, load_benchmark, load_peers

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROLL_WINDOW = 63


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    peers = load_peers()

    asset_ret = df["Return"]

    fig, ax = plt.subplots(figsize=(14, 6))

    bench_corr = asset_ret.rolling(ROLL_WINDOW).corr(bench["Return"])
    ax.plot(bench_corr.index, bench_corr.values, color=COLOURS["primary"],
            linewidth=1, label=cfg["benchmark_name"])

    for i, (ticker, peer_df) in enumerate(peers.items()):
        code_name = cfg["peers"].get(ticker, ticker)
        peer_corr = asset_ret.rolling(ROLL_WINDOW).corr(peer_df["Return"])
        colour = PALETTE[(i + 1) % len(PALETTE)]
        ax.plot(peer_corr.index, peer_corr.values, color=colour,
                linewidth=0.7, alpha=0.7, label=code_name)

    ax.axhline(0, color=COLOURS["muted"], linewidth=0.5, linestyle=":")
    ax.axhline(1, color=COLOURS["muted"], linewidth=0.3, linestyle=":")
    ax.set_ylim(-0.5, 1.1)
    ax.set_ylabel("Correlation")
    ax.set_title(f"{cfg['name']} — Rolling {ROLL_WINDOW}-Day Correlation")
    ax.legend(loc="lower left", fontsize=8, ncol=2)
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "50_rolling_correlation")
