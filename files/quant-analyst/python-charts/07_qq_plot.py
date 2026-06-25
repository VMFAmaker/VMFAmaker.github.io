"""
Chart 07 — QQ Plot
Quantile-quantile plots against Normal and Student-t distributions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # QQ vs Normal
    stats.probplot(returns, dist="norm", plot=ax1)
    ax1.get_lines()[0].set(color=COLOURS["primary"], markersize=3, alpha=0.5)
    ax1.get_lines()[1].set(color=COLOURS["red"], linewidth=1.5)
    ax1.set_title("QQ Plot vs Normal")

    # QQ vs Student-t (fit df first)
    t_params = stats.t.fit(returns)
    stats.probplot(returns, sparams=(t_params[0],), dist="t", plot=ax2)
    ax2.get_lines()[0].set(color=COLOURS["primary"], markersize=3, alpha=0.5)
    ax2.get_lines()[1].set(color=COLOURS["green"], linewidth=1.5)
    ax2.set_title(f"QQ Plot vs Student-t (df={t_params[0]:.1f})")

    fig.suptitle(f"{cfg['name']} — QQ Plots", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "07_qq_plot")
