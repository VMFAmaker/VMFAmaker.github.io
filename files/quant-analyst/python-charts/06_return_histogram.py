"""
Chart 06 — Return Histogram with Fitted Distributions
Empirical histogram overlaid with Normal and Student-t fits.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, PALETTE, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values * 100
    x = np.linspace(returns.min(), returns.max(), 300)

    # Fit distributions
    norm_params = stats.norm.fit(returns)
    t_params    = stats.t.fit(returns)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.hist(returns, bins=80, density=True, color=COLOURS["primary"],
            alpha=0.5, edgecolor="white", linewidth=0.3, label="Actual")

    ax.plot(x, stats.norm.pdf(x, *norm_params),
            color=COLOURS["red"], linewidth=1.5, label="Normal fit")
    ax.plot(x, stats.t.pdf(x, *t_params),
            color=COLOURS["green"], linewidth=1.5,
            label=f"Student-t fit (df={t_params[0]:.1f})")

    ax.set_title(f"{cfg['name']} — Return Distribution")
    ax.set_xlabel("Daily Return (%)")
    ax.set_ylabel("Density")
    ax.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "06_return_histogram")
