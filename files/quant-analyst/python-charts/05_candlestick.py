"""
Chart 05 — Candlestick Chart
OHLC candlesticks for the most recent 6 months.
Requires: pip install mplfinance
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import COLOURS, save_chart
from _data   import load_prices

import matplotlib.pyplot as plt

try:
    import mplfinance as mpf
except ImportError:
    mpf = None


LOOKBACK_DAYS = 126  # ~6 months


def plot(df, cfg=CONFIG):
    if mpf is None:
        print("mplfinance not installed. Run:  pip install mplfinance")
        return None

    recent = df.tail(LOOKBACK_DAYS).copy()

    mc = mpf.make_marketcolors(
        up=COLOURS["green"], down=COLOURS["red"],
        edge="inherit", wick="inherit", volume="inherit",
    )
    style = mpf.make_mpf_style(
        marketcolors=mc, gridcolor="#CBD5E1", gridstyle="--", gridaxis="both",
        facecolor="#F8F9FA", figcolor="white",
    )

    fig, axes = mpf.plot(
        recent, type="candle", volume=True, style=style,
        title=f"\n{cfg['name']} — Candlestick (Last {LOOKBACK_DAYS} Days)",
        figsize=(14, 7), returnfig=True,
    )

    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    if fig:
        save_chart(fig, "05_candlestick")
