"""
Chart 59 — Alpha Decomposition
Cumulative alpha vs cumulative market contribution to total return.
Shows where returns came from: market exposure or stock-specific alpha.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices, load_benchmark

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    merged = df[["Return"]].join(bench[["Return"]], rsuffix="_bench").dropna()

    slope, intercept, _, _, _ = stats.linregress(
        merged["Return_bench"], merged["Return"]
    )

    market_contrib = slope * merged["Return_bench"]
    alpha_contrib  = merged["Return"] - market_contrib

    cum_total  = merged["Return"].cumsum() * 100
    cum_market = market_contrib.cumsum() * 100
    cum_alpha  = alpha_contrib.cumsum() * 100

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(cum_total.index, cum_total.values, color=COLOURS["primary"],
            linewidth=1.2, label="Total Return")
    ax.plot(cum_market.index, cum_market.values, color=COLOURS["amber"],
            linewidth=0.8, label=f"Market Component (beta={slope:.2f})")
    ax.plot(cum_alpha.index, cum_alpha.values, color=COLOURS["green"],
            linewidth=0.8, label=f"Alpha Component ({cum_alpha.iloc[-1]:+.1f}%)")

    ax.fill_between(cum_alpha.index, 0, cum_alpha.values,
                    where=cum_alpha.values >= 0, alpha=0.1, color=COLOURS["green"])
    ax.fill_between(cum_alpha.index, 0, cum_alpha.values,
                    where=cum_alpha.values < 0, alpha=0.1, color=COLOURS["red"])

    ax.axhline(0, color=COLOURS["muted"], linewidth=0.5)
    ax.set_ylabel("Cumulative Return (%)")
    ax.set_title(f"{cfg['name']} — Return Attribution (Alpha vs Market)")
    ax.legend(loc="upper left")
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "59_alpha_decomposition")
