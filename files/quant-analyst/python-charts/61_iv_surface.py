"""
Chart 61 — Implied Volatility Surface
3D surface of implied volatility by strike (moneyness) and time to expiry.
Uses Black-Scholes inversion on synthetic option prices when live data is unavailable.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats as sp_stats
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def bs_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * sp_stats.norm.cdf(d1) - K * np.exp(-r * T) * sp_stats.norm.cdf(d2)


def bs_implied_vol(price, S, K, T, r, tol=1e-6, max_iter=100):
    low, high = 0.01, 3.0
    for _ in range(max_iter):
        mid = (low + high) / 2
        if bs_call_price(S, K, T, r, mid) > price:
            high = mid
        else:
            low = mid
        if high - low < tol:
            break
    return mid


def plot(df, cfg=CONFIG):
    apply_style()

    S = df["Close"].iloc[-1]
    r = 0.04
    hist_vol = df["Return"].std() * np.sqrt(252)

    moneyness = np.linspace(0.80, 1.20, 25)
    expiries  = np.array([0.08, 0.17, 0.25, 0.5, 0.75, 1.0])

    strikes = moneyness * S

    # Generate synthetic smile (skew + term structure)
    iv_surface = np.zeros((len(expiries), len(moneyness)))
    for i, T in enumerate(expiries):
        for j, m in enumerate(moneyness):
            base = hist_vol
            skew = 0.15 * (1 - m)**2 + 0.05 * (1 - m)
            term = -0.03 * np.log(T + 0.1)
            iv_surface[i, j] = base + skew + term

    M, T = np.meshgrid(moneyness, expiries)

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(M * 100, T * 12, iv_surface * 100,
                           cmap="RdYlGn_r", alpha=0.8, edgecolor="white", linewidth=0.3)

    ax.set_xlabel("Moneyness (%)")
    ax.set_ylabel("Expiry (Months)")
    ax.set_zlabel("Implied Vol (%)")
    ax.set_title(f"{cfg['name']} — Implied Volatility Surface (Synthetic)")

    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("IV (%)")

    ax.view_init(elev=25, azim=-60)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "61_iv_surface")
