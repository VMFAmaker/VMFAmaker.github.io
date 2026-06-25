"""
Chart 01 — Price History with Volume
Two-panel chart: closing price on top, daily volume below.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    fig, (ax_price, ax_vol) = plt.subplots(
        2, 1, figsize=(14, 7),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )

    # Price
    ax_price.plot(df.index, df["Close"], color=COLOURS["primary"], linewidth=1)
    ax_price.set_title(f"{cfg['name']} — Price History")
    ax_price.set_ylabel("Price ($)")

    # Volume
    ax_vol.bar(df.index, df["Volume"], color=COLOURS["muted"], width=1, alpha=0.6)
    ax_vol.set_ylabel("Volume")
    format_date_axis(ax_vol)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "01_price_history")
