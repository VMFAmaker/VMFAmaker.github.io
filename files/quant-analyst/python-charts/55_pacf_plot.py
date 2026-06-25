"""
Chart 55 — Partial Autocorrelation Function (PACF)
PACF of returns and squared returns for AR/GARCH order selection.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from statsmodels.graphics.tsaplots import plot_pacf
import matplotlib.pyplot as plt


MAX_LAGS = 40


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].dropna().values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    plot_pacf(returns, ax=ax1, lags=MAX_LAGS, alpha=0.05,
              method="ywm",
              color=COLOURS["primary"],
              vlines_kwargs={"color": COLOURS["primary"]})
    ax1.set_title("PACF of Returns")
    ax1.set_xlabel("Lag (Days)")

    plot_pacf(returns**2, ax=ax2, lags=MAX_LAGS, alpha=0.05,
              method="ywm",
              color=COLOURS["amber"],
              vlines_kwargs={"color": COLOURS["amber"]})
    ax2.set_title("PACF of Squared Returns")
    ax2.set_xlabel("Lag (Days)")

    fig.suptitle(f"{cfg['name']} — Partial Autocorrelation Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "55_pacf_plot")
