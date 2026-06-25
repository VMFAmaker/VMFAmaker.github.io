"""
Chart 23 — GPD Tail Fit
Generalised Pareto Distribution fitted to exceedances above a threshold.
Shows empirical vs fitted survival function and PP/QQ diagnostic plots.
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


THRESHOLD_PERCENTILE = 95


def plot(df, cfg=CONFIG):
    apply_style()

    losses = -df["Return"].values
    threshold = np.percentile(losses, THRESHOLD_PERCENTILE)
    exceedances = losses[losses > threshold] - threshold
    exceedances = exceedances[exceedances > 0]

    shape, loc, scale = stats.genpareto.fit(exceedances, floc=0)
    n_exceed = len(exceedances)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Survival function
    ax = axes[0]
    exc_sorted = np.sort(exceedances)
    empirical_sf = 1 - np.arange(1, n_exceed + 1) / (n_exceed + 1)
    fitted_sf = stats.genpareto.sf(exc_sorted, shape, loc=0, scale=scale)

    ax.semilogy(exc_sorted * 100, empirical_sf, "o",
                color=COLOURS["primary"], markersize=3, label="Empirical")
    ax.semilogy(exc_sorted * 100, fitted_sf,
                color=COLOURS["red"], linewidth=1.5, label="GPD Fit")
    ax.set_xlabel("Excess Loss (%)")
    ax.set_ylabel("P(X > x)")
    ax.set_title("Survival Function")
    ax.legend()

    # PP Plot
    ax = axes[1]
    theoretical_p = stats.genpareto.cdf(exc_sorted, shape, loc=0, scale=scale)
    empirical_p = np.arange(1, n_exceed + 1) / (n_exceed + 1)
    ax.scatter(theoretical_p, empirical_p, color=COLOURS["primary"], s=8)
    ax.plot([0, 1], [0, 1], color=COLOURS["red"], linewidth=1, linestyle="--")
    ax.set_xlabel("Theoretical CDF")
    ax.set_ylabel("Empirical CDF")
    ax.set_title("PP Plot")
    ax.set_aspect("equal")

    # QQ Plot
    ax = axes[2]
    theoretical_q = stats.genpareto.ppf(empirical_p, shape, loc=0, scale=scale)
    ax.scatter(theoretical_q * 100, exc_sorted * 100, color=COLOURS["primary"], s=8)
    lims = [0, max(exc_sorted.max(), theoretical_q.max()) * 100 * 1.1]
    ax.plot(lims, lims, color=COLOURS["red"], linewidth=1, linestyle="--")
    ax.set_xlabel("Theoretical Quantile (%)")
    ax.set_ylabel("Empirical Quantile (%)")
    ax.set_title("QQ Plot")
    ax.set_aspect("equal")

    fig.suptitle(
        f"{cfg['name']} — GPD Tail Fit (xi={shape:.3f}, sigma={scale:.4f}, n={n_exceed})",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "23_gpd_fit")
