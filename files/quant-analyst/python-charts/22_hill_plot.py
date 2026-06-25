"""
Chart 22 — Hill Plot
Hill estimator of the tail index as a function of the number of order statistics.
Stable region indicates a reliable tail index estimate.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


def hill_estimator(losses_sorted_desc, k):
    """Hill estimator using the top k order statistics."""
    log_ratios = np.log(losses_sorted_desc[:k]) - np.log(losses_sorted_desc[k])
    return np.mean(log_ratios)


def plot(df, cfg=CONFIG):
    apply_style()

    losses = -df["Return"].values
    losses = losses[losses > 0]
    losses_sorted = np.sort(losses)[::-1]

    k_min = 20
    k_max = min(len(losses_sorted) - 1, 500)
    k_range = np.arange(k_min, k_max + 1)

    hill_values = np.array([hill_estimator(losses_sorted, k) for k in k_range])
    alpha_values = 1.0 / hill_values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(k_range, hill_values, color=COLOURS["primary"], linewidth=0.8)
    ax1.axhline(np.median(hill_values), color=COLOURS["red"], linewidth=1, linestyle="--",
                label=f"Median: {np.median(hill_values):.3f}")
    ax1.set_xlabel("Number of Order Statistics (k)")
    ax1.set_ylabel("Hill Estimator (gamma)")
    ax1.set_title("Hill Estimator")
    ax1.legend()

    ax2.plot(k_range, alpha_values, color=COLOURS["amber"], linewidth=0.8)
    ax2.axhline(np.median(alpha_values), color=COLOURS["red"], linewidth=1, linestyle="--",
                label=f"Median: {np.median(alpha_values):.2f}")
    ax2.set_xlabel("Number of Order Statistics (k)")
    ax2.set_ylabel("Tail Index (alpha = 1/gamma)")
    ax2.set_title("Tail Index")
    ax2.legend()

    fig.suptitle(f"{cfg['name']} — Hill Plot", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "22_hill_plot")
