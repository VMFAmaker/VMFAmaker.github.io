"""
Chart 34 — Relative Strength vs Benchmark
Ratio of asset price to benchmark price. Rising line means outperformance.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices, load_benchmark

import numpy as np
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    aligned = df["Close"].reindex(bench.index).dropna()
    bench_aligned = bench["Close"].reindex(aligned.index)

    ratio = aligned / bench_aligned
    ratio_norm = ratio / ratio.iloc[0] * 100

    sma_50 = ratio_norm.rolling(50).mean()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [1, 1]},
                                    sharex=True)

    # Cumulative relative performance
    asset_cum = (1 + df["Return"]).cumprod().reindex(aligned.index)
    bench_cum = (1 + bench["Return"]).cumprod().reindex(aligned.index)
    ax1.plot(asset_cum.index, asset_cum.values * 100, color=COLOURS["primary"],
             linewidth=0.8, label=cfg["name"])
    ax1.plot(bench_cum.index, bench_cum.values * 100, color=COLOURS["amber"],
             linewidth=0.8, label=cfg["benchmark_name"])
    ax1.set_ylabel("Growth of $100")
    ax1.set_title(f"{cfg['name']} vs {cfg['benchmark_name']} — Relative Strength")
    ax1.legend()

    # Relative strength ratio
    ax2.plot(ratio_norm.index, ratio_norm.values, color=COLOURS["primary"],
             linewidth=0.8, label="Relative Strength Ratio")
    ax2.plot(sma_50.index, sma_50.values, color=COLOURS["red"],
             linewidth=0.8, linestyle="--", label="50-Day SMA")
    ax2.axhline(100, color=COLOURS["muted"], linewidth=0.5, linestyle=":")
    ax2.set_ylabel("Ratio (Indexed to 100)")
    ax2.legend(loc="upper left", fontsize=8)
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "34_relative_strength")
