"""
Chart 43 — Historical Multiples
Trailing P/E, P/B, and EV/EBITDA over time. Shows whether current valuation
is cheap or expensive relative to history.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices, load_financials

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    ticker = yf.Ticker(cfg["ticker"])
    info = ticker.info

    current_pe = info.get("trailingPE", np.nan)
    current_pb = info.get("priceToBook", np.nan)

    close = df["Close"]
    returns_annual = close.pct_change(252)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    # Price / 52-week range
    ax = axes[0, 0]
    rolling_high = close.rolling(252).max()
    rolling_low  = close.rolling(252).min()
    pct_range = (close - rolling_low) / (rolling_high - rolling_low) * 100

    ax.plot(pct_range.index, pct_range.values, color=COLOURS["primary"], linewidth=0.7)
    ax.axhline(50, color=COLOURS["muted"], linewidth=0.5, linestyle=":")
    ax.fill_between(pct_range.index, 80, pct_range.values,
                    where=pct_range.values >= 80, alpha=0.2, color=COLOURS["red"])
    ax.fill_between(pct_range.index, 20, pct_range.values,
                    where=pct_range.values <= 20, alpha=0.2, color=COLOURS["green"])
    ax.set_ylabel("% of 52-Week Range")
    ax.set_title("Position in 52-Week Range")
    ax.set_ylim(0, 100)
    format_date_axis(ax)

    # Rolling PE proxy (price / trailing earnings estimate)
    ax = axes[0, 1]
    if not np.isnan(current_pe):
        implied_eps = close.iloc[-1] / current_pe
        pe_series = close / implied_eps
        ax.plot(pe_series.index, pe_series.values, color=COLOURS["primary"], linewidth=0.7)
        ax.axhline(pe_series.median(), color=COLOURS["amber"], linewidth=1, linestyle="--",
                   label=f"Median: {pe_series.median():.1f}x")
        ax.axhline(current_pe, color=COLOURS["red"], linewidth=1, linestyle=":",
                   label=f"Current: {current_pe:.1f}x")
        ax.set_title("Implied P/E (Proxy)")
        ax.legend(fontsize=8)
    else:
        ax.text(0.5, 0.5, "P/E data not available", transform=ax.transAxes, ha="center")
        ax.set_title("P/E Ratio")
    ax.set_ylabel("P/E Ratio")
    format_date_axis(ax)

    # Annual returns distribution
    ax = axes[1, 0]
    annual_ret = returns_annual.dropna() * 100
    ax.hist(annual_ret, bins=50, color=COLOURS["primary"], alpha=0.7, edgecolor="white", linewidth=0.3)
    if len(annual_ret) > 0:
        current_annual = annual_ret.iloc[-1]
        ax.axvline(current_annual, color=COLOURS["red"], linewidth=1.5,
                   label=f"Current: {current_annual:.1f}%")
    ax.set_xlabel("1-Year Return (%)")
    ax.set_ylabel("Frequency")
    ax.set_title("Rolling 1-Year Return Distribution")
    ax.legend(fontsize=8)

    # Earnings yield (1/PE) vs risk-free proxy
    ax = axes[1, 1]
    if not np.isnan(current_pe):
        ey_series = 100 / pe_series
        ax.plot(ey_series.index, ey_series.values, color=COLOURS["primary"], linewidth=0.7,
                label="Earnings Yield")
        ax.axhline(ey_series.median(), color=COLOURS["amber"], linewidth=1, linestyle="--")
        ax.set_title("Earnings Yield")
        ax.legend(fontsize=8)
    else:
        ax.text(0.5, 0.5, "Data not available", transform=ax.transAxes, ha="center")
        ax.set_title("Earnings Yield")
    ax.set_ylabel("Yield (%)")
    format_date_axis(ax)

    fig.suptitle(f"{cfg['name']} — Historical Valuation Metrics", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "43_historical_multiples")
