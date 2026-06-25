"""
Chart 04 — Drawdown Profile
Percentage decline from the running peak at every point in time.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import matplotlib.pyplot as plt


def compute_drawdown(df):
    cumulative  = (1 + df["Return"]).cumprod()
    running_max = cumulative.cummax()
    drawdown    = (cumulative - running_max) / running_max
    return drawdown


def plot(df, cfg=CONFIG):
    apply_style()

    dd = compute_drawdown(df) * 100
    max_dd_date = dd.idxmin()
    max_dd_val  = dd.min()

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.fill_between(dd.index, dd.values, 0, color=COLOURS["red"], alpha=0.4)
    ax.plot(dd.index, dd.values, color=COLOURS["red"], linewidth=0.6)

    ax.annotate(
        f"Max: {max_dd_val:.1f}%\n{max_dd_date.strftime('%Y-%m-%d')}",
        xy=(max_dd_date, max_dd_val),
        xytext=(max_dd_date, max_dd_val + 5),
        fontsize=9, ha="center",
        arrowprops=dict(arrowstyle="->", color=COLOURS["dark"]),
    )

    ax.set_title(f"{cfg['name']} — Drawdown Profile")
    ax.set_ylabel("Drawdown (%)")
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "04_drawdown")
