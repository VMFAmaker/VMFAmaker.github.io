"""
Chart 12 — EWMA Volatility
Exponentially Weighted Moving Average volatility (RiskMetrics lambda=0.94).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


LAMBDA = 0.94


def compute_ewma(returns, lam=LAMBDA):
    n = len(returns)
    var = np.zeros(n)
    var[0] = returns[0] ** 2
    for i in range(1, n):
        var[i] = lam * var[i - 1] + (1 - lam) * returns[i - 1] ** 2
    return np.sqrt(var)


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values
    ewma = compute_ewma(returns) * np.sqrt(252) * 100
    rolling_30 = df["Return"].rolling(30).std() * np.sqrt(252) * 100

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(df.index, ewma,       color=COLOURS["primary"], linewidth=0.8,
            label=f"EWMA (lambda={LAMBDA})")
    ax.plot(df.index, rolling_30, color=COLOURS["amber"],   linewidth=0.8,
            label="30-Day Rolling Std", alpha=0.7)

    ax.set_title(f"{cfg['name']} — EWMA Volatility (Annualised)")
    ax.set_ylabel("Volatility (%)")
    ax.legend()
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "12_ewma_volatility")
