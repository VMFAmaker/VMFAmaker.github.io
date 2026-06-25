"""
Chart 52 — Beta Scatter Plot
Asset vs benchmark returns with OLS regression line. Alpha and beta annotated.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices, load_benchmark

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    merged = df[["Return"]].join(bench[["Return"]], rsuffix="_bench").dropna()

    x = merged["Return_bench"].values * 100
    y = merged["Return"].values * 100

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(x, y, color=COLOURS["primary"], s=5, alpha=0.3)

    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, intercept + slope * x_line, color=COLOURS["red"],
            linewidth=1.5, label=f"Beta: {slope:.3f}")
    ax.plot(x_line, x_line, color=COLOURS["muted"], linewidth=0.5, linestyle=":",
            label="Beta = 1 line")

    ax.axhline(0, color=COLOURS["muted"], linewidth=0.3)
    ax.axvline(0, color=COLOURS["muted"], linewidth=0.3)

    note = (f"Alpha (daily): {intercept:.4f}%\n"
            f"Beta: {slope:.3f}\n"
            f"R-squared: {r_value**2:.3f}\n"
            f"p-value: {p_value:.2e}")
    ax.text(0.02, 0.98, note, transform=ax.transAxes, fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLOURS["muted"]))

    ax.set_xlabel(f"{cfg['benchmark_name']} Daily Return (%)")
    ax.set_ylabel(f"{cfg['name']} Daily Return (%)")
    ax.set_title(f"{cfg['name']} vs {cfg['benchmark_name']} — CAPM Beta")
    ax.legend(loc="lower right")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "52_beta_scatter")
