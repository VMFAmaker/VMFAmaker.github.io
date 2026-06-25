"""
Chart 56 — Ljung-Box Test
P-values from Ljung-Box test at multiple lag orders for returns and squared returns.
Low p-values indicate significant serial correlation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
import matplotlib.pyplot as plt


LAG_RANGE = list(range(1, 41))


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].dropna().values

    lb_returns = acorr_ljungbox(returns, lags=LAG_RANGE, return_df=True)
    lb_squared = acorr_ljungbox(returns**2, lags=LAG_RANGE, return_df=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Returns
    ax1.bar(LAG_RANGE, lb_returns["lb_pvalue"].values,
            color=COLOURS["primary"], alpha=0.7, width=0.8)
    ax1.axhline(0.05, color=COLOURS["red"], linewidth=1, linestyle="--", label="5% Significance")
    ax1.axhline(0.01, color=COLOURS["red"], linewidth=0.8, linestyle=":", label="1% Significance")
    ax1.set_xlabel("Lag")
    ax1.set_ylabel("p-value")
    ax1.set_title("Ljung-Box: Returns")
    ax1.set_ylim(0, 1)
    ax1.legend(fontsize=8)

    # Squared returns
    ax2.bar(LAG_RANGE, lb_squared["lb_pvalue"].values,
            color=COLOURS["amber"], alpha=0.7, width=0.8)
    ax2.axhline(0.05, color=COLOURS["red"], linewidth=1, linestyle="--", label="5% Significance")
    ax2.axhline(0.01, color=COLOURS["red"], linewidth=0.8, linestyle=":", label="1% Significance")
    ax2.set_xlabel("Lag")
    ax2.set_ylabel("p-value")
    ax2.set_title("Ljung-Box: Squared Returns (ARCH Effects)")
    ax2.set_ylim(0, max(0.1, lb_squared["lb_pvalue"].max() * 1.1))
    ax2.legend(fontsize=8)

    fig.suptitle(f"{cfg['name']} — Ljung-Box Serial Correlation Test", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "56_ljung_box")
