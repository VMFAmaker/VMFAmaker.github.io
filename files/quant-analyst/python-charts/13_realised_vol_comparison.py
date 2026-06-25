"""
Chart 13 — Realised Volatility Comparison
Close-to-close, Parkinson, and Garman-Klass estimators on a rolling window.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


WINDOW = 30


def parkinson_vol(high, low):
    return np.sqrt((1 / (4 * np.log(2))) * (np.log(high / low) ** 2))


def garman_klass_vol(op, hi, lo, cl):
    return np.sqrt(
        0.5 * (np.log(hi / lo) ** 2)
        - (2 * np.log(2) - 1) * (np.log(cl / op) ** 2)
    )


def plot(df, cfg=CONFIG):
    apply_style()

    # Close-to-close
    cc = df["Return"].rolling(WINDOW).std() * np.sqrt(252) * 100

    # Parkinson (rolling)
    pk = pd.Series(
        [parkinson_vol(df["High"].iloc[i], df["Low"].iloc[i]) for i in range(len(df))],
        index=df.index,
    ).rolling(WINDOW).mean() * np.sqrt(252) * 100

    # Garman-Klass (rolling)
    gk = pd.Series(
        [garman_klass_vol(df["Open"].iloc[i], df["High"].iloc[i],
                          df["Low"].iloc[i],  df["Close"].iloc[i])
         for i in range(len(df))],
        index=df.index,
    ).rolling(WINDOW).mean() * np.sqrt(252) * 100

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(cc.index, cc.values, color=COLOURS["primary"], linewidth=0.8, label="Close-to-Close")
    ax.plot(pk.index, pk.values, color=COLOURS["amber"],   linewidth=0.8, label="Parkinson")
    ax.plot(gk.index, gk.values, color=COLOURS["green"],   linewidth=0.8, label="Garman-Klass")

    ax.set_title(f"{cfg['name']} — Realised Volatility Estimators ({WINDOW}-Day Rolling, Annualised)")
    ax.set_ylabel("Volatility (%)")
    ax.legend()
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "13_realised_vol_comparison")
