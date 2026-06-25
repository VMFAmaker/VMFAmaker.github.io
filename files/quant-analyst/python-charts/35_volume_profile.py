"""
Chart 35 — Volume Profile
Horizontal volume distribution by price level. Shows support/resistance zones.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


N_BINS = 50


def plot(df, cfg=CONFIG):
    apply_style()

    close  = df["Close"].values
    volume = df["Volume"].values

    price_min = close.min()
    price_max = close.max()
    bins = np.linspace(price_min, price_max, N_BINS + 1)
    bin_centres = (bins[:-1] + bins[1:]) / 2

    vol_profile = np.zeros(N_BINS)
    for i in range(N_BINS):
        mask = (close >= bins[i]) & (close < bins[i + 1])
        vol_profile[i] = volume[mask].sum()

    poc_idx = np.argmax(vol_profile)
    poc_price = bin_centres[poc_idx]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7),
                                    gridspec_kw={"width_ratios": [3, 1]},
                                    sharey=True)

    ax1.plot(df.index, close, color=COLOURS["primary"], linewidth=0.7)
    ax1.axhline(poc_price, color=COLOURS["red"], linewidth=1, linestyle="--",
                label=f"POC: ${poc_price:.2f}")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price ($)")
    ax1.set_title(f"{cfg['name']} — Volume Profile")
    ax1.legend()
    format_date_axis(ax1)

    vol_normalised = vol_profile / vol_profile.max()
    bar_colours = [COLOURS["red"] if i == poc_idx else COLOURS["primary"]
                   for i in range(N_BINS)]

    ax2.barh(bin_centres, vol_normalised, height=(price_max - price_min) / N_BINS * 0.9,
             color=bar_colours, alpha=0.7)
    ax2.set_xlabel("Volume (normalised)")
    ax2.set_title("Volume at Price")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "35_volume_profile")
