"""
Chart 54 — Autocorrelation Function (ACF)
ACF of returns and squared returns. Significant lags in squared returns
indicate volatility clustering (ARCH effects).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt


MAX_LAGS = 40


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].dropna().values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    plot_acf(returns, ax=ax1, lags=MAX_LAGS, alpha=0.05,
             color=COLOURS["primary"],
             vlines_kwargs={"color": COLOURS["primary"]})
    ax1.set_title("ACF of Returns")
    ax1.set_xlabel("Lag (Days)")

    plot_acf(returns**2, ax=ax2, lags=MAX_LAGS, alpha=0.05,
             color=COLOURS["amber"],
             vlines_kwargs={"color": COLOURS["amber"]})
    ax2.set_title("ACF of Squared Returns")
    ax2.set_xlabel("Lag (Days)")

    fig.suptitle(f"{cfg['name']} — Autocorrelation Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "54_acf_plot")
