"""
Chart 26 — Monte Carlo Terminal Distribution
Histogram of simulated terminal prices/returns with key percentile markers.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


N_SIMS  = 50000
HORIZON = 252


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values
    mu      = np.mean(returns)
    sigma   = np.std(returns, ddof=1)
    s0      = df["Close"].iloc[-1]

    rng = np.random.default_rng(42)
    cumulative = rng.normal(mu, sigma, (N_SIMS, HORIZON)).sum(axis=1)
    terminal_prices = s0 * np.exp(cumulative)
    terminal_returns = (terminal_prices / s0 - 1) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Price distribution
    ax1.hist(terminal_prices, bins=100, color=COLOURS["primary"], alpha=0.7, edgecolor="white", linewidth=0.3)
    for pct, label in [(5, "5th"), (50, "Median"), (95, "95th")]:
        val = np.percentile(terminal_prices, pct)
        ax1.axvline(val, color=COLOURS["red"], linewidth=1, linestyle="--")
        ax1.text(val, ax1.get_ylim()[1] * 0.9, f"  {label}: ${val:.0f}",
                 fontsize=8, color=COLOURS["red"])

    ax1.axvline(s0, color=COLOURS["amber"], linewidth=1.5, linestyle=":",
                label=f"Current: ${s0:.2f}")
    ax1.set_xlabel("Terminal Price ($)")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Terminal Price Distribution")
    ax1.legend()

    # Return distribution
    ax2.hist(terminal_returns, bins=100, color=COLOURS["amber"], alpha=0.7, edgecolor="white", linewidth=0.3)
    ax2.axvline(0, color=COLOURS["text"], linewidth=0.5)

    prob_loss = (terminal_returns < 0).sum() / N_SIMS * 100
    ax2.text(0.02, 0.95, f"P(loss): {prob_loss:.1f}%\nMean: {np.mean(terminal_returns):.1f}%",
             transform=ax2.transAxes, fontsize=9, verticalalignment="top",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLOURS["muted"]))

    ax2.set_xlabel("1-Year Return (%)")
    ax2.set_ylabel("Frequency")
    ax2.set_title("Terminal Return Distribution")

    fig.suptitle(f"{cfg['name']} — Monte Carlo Terminal Distribution ({N_SIMS:,} sims)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "26_mc_terminal_distribution")
