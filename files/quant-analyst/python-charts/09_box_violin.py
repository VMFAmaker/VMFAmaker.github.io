"""
Chart 09 — Box and Violin Plots
Return distributions grouped by year, showing how volatility changes over time.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    df = df.copy()
    df["Year"] = df.index.year
    years = sorted(df["Year"].unique())
    data  = [df.loc[df["Year"] == y, "Return"].values * 100 for y in years]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Box plot
    bp = ax1.boxplot(data, labels=years, patch_artist=True, showfliers=True,
                     flierprops=dict(marker="o", markersize=3, alpha=0.4))
    for patch in bp["boxes"]:
        patch.set_facecolor(COLOURS["primary"])
        patch.set_alpha(0.5)
    ax1.set_title("Box Plot by Year")
    ax1.set_ylabel("Daily Return (%)")

    # Violin plot
    vp = ax2.violinplot(data, positions=range(len(years)), showmedians=True, showextrema=True)
    for body in vp["bodies"]:
        body.set_facecolor(COLOURS["purple"])
        body.set_alpha(0.5)
    ax2.set_xticks(range(len(years)))
    ax2.set_xticklabels(years)
    ax2.set_title("Violin Plot by Year")
    ax2.set_ylabel("Daily Return (%)")

    fig.suptitle(f"{cfg['name']} — Annual Return Distributions", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "09_box_violin")
