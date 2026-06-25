"""
Chart 62 — Option Greeks Sensitivity
Delta, Gamma, Theta, Vega as functions of underlying price for a vanilla call.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats as sp_stats
import matplotlib.pyplot as plt


T     = 0.25
R     = 0.04
SIGMA = 0.25


def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def delta(S, K, T, r, sigma):
    return sp_stats.norm.cdf(d1(S, K, T, r, sigma))


def gamma(S, K, T, r, sigma):
    return sp_stats.norm.pdf(d1(S, K, T, r, sigma)) / (S * sigma * np.sqrt(T))


def theta(S, K, T, r, sigma):
    d1_val = d1(S, K, T, r, sigma)
    d2_val = d2(S, K, T, r, sigma)
    term1 = -(S * sp_stats.norm.pdf(d1_val) * sigma) / (2 * np.sqrt(T))
    term2 = -r * K * np.exp(-r * T) * sp_stats.norm.cdf(d2_val)
    return (term1 + term2) / 365


def vega(S, K, T, r, sigma):
    return S * sp_stats.norm.pdf(d1(S, K, T, r, sigma)) * np.sqrt(T) / 100


def plot(df, cfg=CONFIG):
    apply_style()

    current = df["Close"].iloc[-1]
    K = round(current, -1)
    S_range = np.linspace(current * 0.7, current * 1.3, 300)

    greeks = {
        "Delta":       delta(S_range, K, T, R, SIGMA),
        "Gamma":       gamma(S_range, K, T, R, SIGMA),
        "Theta ($/day)": theta(S_range, K, T, R, SIGMA),
        "Vega ($/1% vol)": vega(S_range, K, T, R, SIGMA),
    }

    colours = [COLOURS["primary"], COLOURS["amber"], COLOURS["red"], COLOURS["green"]]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    for ax, (name, vals), colour in zip(axes.flat, greeks.items(), colours):
        ax.plot(S_range, vals, color=colour, linewidth=1.5)
        ax.axvline(K, color=COLOURS["muted"], linewidth=0.8, linestyle=":",
                   label=f"Strike: ${K:.0f}")
        ax.axvline(current, color=COLOURS["red"], linewidth=0.8, linestyle="--",
                   label=f"Current: ${current:.2f}")
        ax.set_xlabel("Stock Price ($)")
        ax.set_ylabel(name)
        ax.set_title(name)
        ax.legend(fontsize=8)

    fig.suptitle(
        f"{cfg['name']} — Option Greeks (Call, K=${K:.0f}, T={T:.2f}yr, sigma={SIGMA:.0%})",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "62_greeks_sensitivity")
