"""
Chart 24 — EVT Threshold Sensitivity
GPD shape parameter and VaR estimates across different threshold choices.
Reveals how stable the tail model is to threshold selection.
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


PERCENTILES = np.arange(85, 99, 0.5)
VAR_LEVEL   = 0.99


def plot(df, cfg=CONFIG):
    apply_style()

    losses = -df["Return"].values
    n = len(losses)

    shapes     = []
    scales     = []
    var_values = []
    n_exceed   = []

    for pct in PERCENTILES:
        threshold = np.percentile(losses, pct)
        exc = losses[losses > threshold] - threshold
        exc = exc[exc > 0]

        if len(exc) < 10:
            shapes.append(np.nan)
            scales.append(np.nan)
            var_values.append(np.nan)
            n_exceed.append(0)
            continue

        shape, _, scale = stats.genpareto.fit(exc, floc=0)
        shapes.append(shape)
        scales.append(scale)
        n_exceed.append(len(exc))

        p_exceed = len(exc) / n
        evt_var = threshold + (scale / shape) * ((p_exceed / (1 - VAR_LEVEL))**shape - 1)
        var_values.append(evt_var * 100)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Shape parameter
    ax = axes[0]
    ax.plot(PERCENTILES, shapes, "o-", color=COLOURS["primary"], markersize=3, linewidth=0.8)
    ax.axhline(0, color=COLOURS["muted"], linewidth=0.5, linestyle=":")
    ax.set_xlabel("Threshold Percentile")
    ax.set_ylabel("Shape (xi)")
    ax.set_title("GPD Shape Parameter")

    # EVT VaR
    ax = axes[1]
    ax.plot(PERCENTILES, var_values, "o-", color=COLOURS["red"], markersize=3, linewidth=0.8)
    ax.set_xlabel("Threshold Percentile")
    ax.set_ylabel(f"EVT VaR {VAR_LEVEL:.0%} (% loss)")
    ax.set_title(f"EVT VaR ({VAR_LEVEL:.0%})")

    # Sample size
    ax = axes[2]
    ax.bar(PERCENTILES, n_exceed, width=0.4, color=COLOURS["amber"], alpha=0.7)
    ax.set_xlabel("Threshold Percentile")
    ax.set_ylabel("Exceedances")
    ax.set_title("Tail Sample Size")

    fig.suptitle(f"{cfg['name']} — EVT Threshold Sensitivity Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "24_evt_threshold_sensitivity")
