"""
Chart 02 — Returns Time Series
Daily percentage returns over time, showing volatility clustering and outliers.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, add_zero_line, save_chart
from _data   import load_prices

import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.bar(
        df.index, df["Return"] * 100,
        color=[COLOURS["green"] if r >= 0 else COLOURS["red"] for r in df["Return"]],
        width=1, alpha=0.6,
    )
    add_zero_line(ax)

    ax.set_title(f"{cfg['name']} — Daily Returns")
    ax.set_ylabel("Return (%)")
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "02_returns_series")
