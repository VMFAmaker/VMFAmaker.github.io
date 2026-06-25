"""
Chart 15 — Implied vs Realised Volatility
VIX (implied) vs S&P 500 realised vol. Requires ^VIX data from Yahoo Finance.
Adapt the tickers in _config.py if analysing a single stock with IV data.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


VIX_TICKER = "^VIX"
REALISED_WINDOW = 30


def plot(df, cfg=CONFIG):
    apply_style()

    # Realised vol (30-day)
    realised = df["Return"].rolling(REALISED_WINDOW).std() * np.sqrt(252) * 100

    # Download VIX as implied vol proxy
    vix = yf.download(VIX_TICKER, start=cfg["start"], end=cfg["end"], progress=False)
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)

    # Align dates
    combined = pd.DataFrame({
        "Realised": realised,
        "Implied (VIX)": vix["Close"],
    }).dropna()

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(combined.index, combined["Realised"],      color=COLOURS["primary"], linewidth=0.8, label="Realised (30-day)")
    ax.plot(combined.index, combined["Implied (VIX)"], color=COLOURS["red"],     linewidth=0.8, label="Implied (VIX)")
    ax.fill_between(
        combined.index,
        combined["Implied (VIX)"], combined["Realised"],
        alpha=0.1, color=COLOURS["amber"], label="Volatility Risk Premium",
    )

    ax.set_title(f"{cfg['name']} — Implied vs Realised Volatility")
    ax.set_ylabel("Volatility (%)")
    ax.legend()
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "15_implied_vs_realised")
