"""
Chart 19 — Loss Exceedance Curve
Empirical probability of losses exceeding a given threshold, with fitted GPD tail.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


THRESHOLD_PERCENTILE = 5


def plot(df, cfg=CONFIG):
    apply_style()

    losses = -df["Return"].values
    losses_sorted = np.sort(losses)[::-1]

    n = len(losses_sorted)
    exceedance_prob = np.arange(1, n + 1) / n

    threshold = np.percentile(losses, 100 - THRESHOLD_PERCENTILE)
    exceedances = losses[losses > threshold] - threshold

    if len(exceedances) > 10:
        shape, loc, scale = stats.genpareto.fit(exceedances, floc=0)

        tail_x = np.linspace(threshold, losses_sorted[0], 200)
        tail_prob = (THRESHOLD_PERCENTILE / 100) * stats.genpareto.sf(
            tail_x - threshold, shape, loc=0, scale=scale
        )
    else:
        tail_x = None

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.semilogy(losses_sorted, exceedance_prob,
                color=COLOURS["primary"], linewidth=0.8, label="Empirical")

    if tail_x is not None:
        ax.semilogy(tail_x, tail_prob,
                    color=COLOURS["red"], linewidth=1.5, linestyle="--",
                    label=f"GPD Tail (xi={shape:.3f})")

    ax.axvline(threshold, color=COLOURS["amber"], linewidth=1, linestyle=":",
               label=f"Threshold ({THRESHOLD_PERCENTILE}th pctile)")

    ax.set_xlabel("Loss (as positive fraction)")
    ax.set_ylabel("P(Loss > x)")
    ax.set_title(f"{cfg['name']} — Loss Exceedance Curve")
    ax.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "19_loss_exceedance")
