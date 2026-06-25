"""
Chart 44 — Bootstrap Distribution
Block bootstrap confidence intervals for key statistics (mean, std, VaR, Sharpe).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


N_BOOTSTRAP = 1000
BLOCK_SIZE  = 20
CONFIDENCE  = 0.95


def block_bootstrap(returns, block_size, rng):
    n = len(returns)
    n_blocks = int(np.ceil(n / block_size))
    starts = rng.integers(0, n - block_size, size=n_blocks)
    blocks = [returns[s : s + block_size] for s in starts]
    return np.concatenate(blocks)[:n]


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values
    rng = np.random.default_rng(42)

    stats_names = ["Annualised Mean (%)", "Annualised Vol (%)", "99% VaR (%)", "Sharpe Ratio"]
    boot_results = {s: [] for s in stats_names}

    for _ in range(N_BOOTSTRAP):
        sample = block_bootstrap(returns, BLOCK_SIZE, rng)
        mu  = np.mean(sample) * 252 * 100
        vol = np.std(sample, ddof=1) * np.sqrt(252) * 100
        var = np.percentile(sample, 1) * 100
        sr  = (np.mean(sample) * 252) / (np.std(sample, ddof=1) * np.sqrt(252))

        boot_results[stats_names[0]].append(mu)
        boot_results[stats_names[1]].append(vol)
        boot_results[stats_names[2]].append(var)
        boot_results[stats_names[3]].append(sr)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    point_estimates = {
        stats_names[0]: np.mean(returns) * 252 * 100,
        stats_names[1]: np.std(returns, ddof=1) * np.sqrt(252) * 100,
        stats_names[2]: np.percentile(returns, 1) * 100,
        stats_names[3]: (np.mean(returns) * 252) / (np.std(returns, ddof=1) * np.sqrt(252)),
    }

    alpha = (1 - CONFIDENCE) / 2
    for ax, name in zip(axes.flat, stats_names):
        vals = np.array(boot_results[name])
        lo = np.percentile(vals, alpha * 100)
        hi = np.percentile(vals, (1 - alpha) * 100)
        point = point_estimates[name]

        ax.hist(vals, bins=50, color=COLOURS["primary"], alpha=0.7,
                edgecolor="white", linewidth=0.3)
        ax.axvline(point, color=COLOURS["red"], linewidth=1.5,
                   label=f"Point: {point:.2f}")
        ax.axvline(lo, color=COLOURS["amber"], linewidth=1, linestyle="--",
                   label=f"{CONFIDENCE:.0%} CI: [{lo:.2f}, {hi:.2f}]")
        ax.axvline(hi, color=COLOURS["amber"], linewidth=1, linestyle="--")

        ax.set_title(name)
        ax.legend(fontsize=7, loc="upper right")

    fig.suptitle(f"{cfg['name']} — Bootstrap Distributions (n={N_BOOTSTRAP}, block={BLOCK_SIZE})",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "44_bootstrap_distribution")
