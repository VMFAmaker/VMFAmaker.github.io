"""
Chart 14 — Volatility Cone
Distribution of realised volatility at multiple lookback periods.
Current vol overlaid as dots.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


LOOKBACKS = [10, 20, 30, 60, 90, 120, 252]
PERCENTILES = [10, 25, 50, 75, 90]


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"]
    cone = {p: [] for p in PERCENTILES}
    current = []

    for lb in LOOKBACKS:
        rolling = returns.rolling(lb).std() * np.sqrt(252) * 100
        rolling = rolling.dropna()
        for p in PERCENTILES:
            cone[p].append(np.percentile(rolling, p))
        current.append(float(rolling.iloc[-1]))

    fig, ax = plt.subplots(figsize=(12, 6))

    # Shaded bands
    ax.fill_between(LOOKBACKS, cone[10], cone[90], alpha=0.15, color=COLOURS["primary"], label="10th-90th")
    ax.fill_between(LOOKBACKS, cone[25], cone[75], alpha=0.25, color=COLOURS["primary"], label="25th-75th")

    # Percentile lines
    for p in PERCENTILES:
        ax.plot(LOOKBACKS, cone[p], color=COLOURS["primary"], linewidth=0.8, alpha=0.5)

    # Median
    ax.plot(LOOKBACKS, cone[50], color=COLOURS["primary"], linewidth=1.5, label="Median")

    # Current
    ax.plot(LOOKBACKS, current, "o-", color=COLOURS["red"], linewidth=1.5,
            markersize=6, label="Current", zorder=5)

    ax.set_title(f"{cfg['name']} — Volatility Cone")
    ax.set_xlabel("Lookback Period (Trading Days)")
    ax.set_ylabel("Annualised Volatility (%)")
    ax.set_xticks(LOOKBACKS)
    ax.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "14_volatility_cone")
