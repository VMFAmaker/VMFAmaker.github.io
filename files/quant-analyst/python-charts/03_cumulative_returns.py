"""
Chart 03 — Cumulative Returns
Growth of $1 for the asset vs the benchmark.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_aligned

import matplotlib.pyplot as plt


def plot(aligned, cfg=CONFIG):
    apply_style()

    cum_asset = (1 + aligned["asset"]).cumprod()
    cum_bench = (1 + aligned["benchmark"]).cumprod()

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(cum_asset.index, cum_asset.values, color=COLOURS["primary"], linewidth=1.2, label=cfg["name"])
    ax.plot(cum_bench.index, cum_bench.values, color=COLOURS["amber"],  linewidth=1.2, label=cfg["benchmark_name"])

    ax.set_title(f"Cumulative Returns — {cfg['name']} vs {cfg['benchmark_name']}")
    ax.set_ylabel("Growth of $1")
    ax.legend()
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_aligned())
    save_chart(fig, "03_cumulative_returns")
