"""
Chart 21 — Mean Excess Plot
Mean residual life plot for threshold selection in Extreme Value Theory.
An upward slope suggests heavy tails (GPD with positive shape parameter).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    losses = -df["Return"].values
    losses_sorted = np.sort(losses)

    thresholds = []
    mean_excess = []

    for u in np.linspace(np.percentile(losses, 80), np.percentile(losses, 99), 100):
        exceedances = losses[losses > u] - u
        if len(exceedances) >= 10:
            thresholds.append(u * 100)
            mean_excess.append(np.mean(exceedances) * 100)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(thresholds, mean_excess, color=COLOURS["primary"], linewidth=1.2)
    ax.scatter(thresholds, mean_excess, color=COLOURS["primary"], s=8, zorder=5)

    z = np.polyfit(thresholds, mean_excess, 1)
    trend = np.poly1d(z)
    ax.plot(thresholds, trend(thresholds), color=COLOURS["red"],
            linewidth=1, linestyle="--", label=f"Linear trend (slope={z[0]:.3f})")

    ax.set_xlabel("Threshold (% loss)")
    ax.set_ylabel("Mean Excess (% loss)")
    ax.set_title(f"{cfg['name']} — Mean Excess Plot")
    ax.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "21_mean_excess")
