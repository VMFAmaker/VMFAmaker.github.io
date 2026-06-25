"""
Chart 18 — CVaR (Expected Shortfall) Comparison
Historical, Normal, and Student-t CVaR at multiple confidence levels.
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


CONFIDENCE_LEVELS = [0.90, 0.95, 0.975, 0.99, 0.995]


def historical_cvar(returns, alpha):
    var = np.percentile(returns, (1 - alpha) * 100)
    return returns[returns <= var].mean()


def normal_cvar(returns, alpha):
    mu    = np.mean(returns)
    sigma = np.std(returns, ddof=1)
    z     = stats.norm.ppf(1 - alpha)
    return mu - sigma * stats.norm.pdf(z) / (1 - alpha)


def t_cvar(returns, alpha):
    df_t, loc, scale = stats.t.fit(returns)
    x = stats.t.ppf(1 - alpha, df_t)
    pdf_x = stats.t.pdf(x, df_t)
    return loc + scale * (-pdf_x / (1 - alpha)) * ((df_t + x**2) / (df_t - 1))


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values

    hist_vals = [historical_cvar(returns, a) * 100 for a in CONFIDENCE_LEVELS]
    norm_vals = [normal_cvar(returns, a) * 100     for a in CONFIDENCE_LEVELS]
    t_vals    = [t_cvar(returns, a) * 100           for a in CONFIDENCE_LEVELS]

    labels = [f"{a:.1%}" for a in CONFIDENCE_LEVELS]
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width, hist_vals, width, label="Historical",  color=COLOURS["primary"])
    ax.bar(x,         norm_vals, width, label="Normal",       color=COLOURS["amber"])
    ax.bar(x + width, t_vals,    width, label="Student-t",    color=COLOURS["green"])

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Confidence Level")
    ax.set_ylabel("CVaR (%)")
    ax.set_title(f"{cfg['name']} — Conditional VaR (Expected Shortfall) Comparison")
    ax.legend()

    for i, (h, n, t) in enumerate(zip(hist_vals, norm_vals, t_vals)):
        ax.text(i - width, h - 0.15, f"{h:.2f}%", ha="center", va="top", fontsize=7)
        ax.text(i,         n - 0.15, f"{n:.2f}%", ha="center", va="top", fontsize=7)
        ax.text(i + width, t - 0.15, f"{t:.2f}%", ha="center", va="top", fontsize=7)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "18_cvar_comparison")
