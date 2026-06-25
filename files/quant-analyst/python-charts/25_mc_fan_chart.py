"""
Chart 25 — Monte Carlo Fan Chart
Simulated price paths with percentile confidence bands.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


N_SIMS   = 10000
HORIZON  = 252
N_SAMPLE = 50


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values
    mu      = np.mean(returns)
    sigma   = np.std(returns, ddof=1)
    s0      = df["Close"].iloc[-1]

    rng = np.random.default_rng(42)
    sims = np.zeros((N_SIMS, HORIZON + 1))
    sims[:, 0] = s0

    for t in range(1, HORIZON + 1):
        z = rng.normal(mu, sigma, N_SIMS)
        sims[:, t] = sims[:, t - 1] * np.exp(z)

    days = np.arange(HORIZON + 1)

    fig, ax = plt.subplots(figsize=(14, 6))

    for i in range(N_SAMPLE):
        ax.plot(days, sims[i], color=COLOURS["muted"], linewidth=0.3, alpha=0.3)

    for pct, alpha in [(5, 0.15), (25, 0.20), (75, 0.20), (95, 0.15)]:
        band = np.percentile(sims, pct, axis=0)
        if pct <= 50:
            label = f"{pct}th pctile"
        else:
            label = f"{pct}th pctile"
        ax.plot(days, band, color=COLOURS["primary"], linewidth=0.6, alpha=0.5)

    ax.fill_between(days,
                    np.percentile(sims, 5, axis=0),
                    np.percentile(sims, 95, axis=0),
                    alpha=0.1, color=COLOURS["primary"], label="5th-95th")
    ax.fill_between(days,
                    np.percentile(sims, 25, axis=0),
                    np.percentile(sims, 75, axis=0),
                    alpha=0.2, color=COLOURS["primary"], label="25th-75th")

    median = np.median(sims, axis=0)
    ax.plot(days, median, color=COLOURS["red"], linewidth=1.5, label="Median")

    ax.axhline(s0, color=COLOURS["amber"], linewidth=0.8, linestyle=":", label=f"Current: ${s0:.2f}")

    ax.set_xlabel("Trading Days Ahead")
    ax.set_ylabel("Price ($)")
    ax.set_title(f"{cfg['name']} — Monte Carlo Simulation ({N_SIMS:,} paths, {HORIZON} days)")
    ax.legend(loc="upper left")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "25_mc_fan_chart")
