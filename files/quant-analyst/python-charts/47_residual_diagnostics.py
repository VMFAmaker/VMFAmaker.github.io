"""
Chart 47 — Residual Diagnostics
Four-panel diagnostic for GARCH standardised residuals: histogram, QQ, ACF, ACF-squared.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt

try:
    from arch import arch_model
    HAS_ARCH = True
except ImportError:
    HAS_ARCH = False


def plot(df, cfg=CONFIG):
    apply_style()

    if not HAS_ARCH:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "Install 'arch' package: pip install arch",
                transform=ax.transAxes, ha="center", fontsize=14)
        return fig

    returns_pct = df["Return"].dropna().values * 100

    model = arch_model(returns_pct, vol="Garch", p=1, q=1, dist="t", rescale=False)
    result = model.fit(disp="off", show_warning=False)

    resid = result.std_resid
    resid = resid[~np.isnan(resid)]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    # Histogram
    ax = axes[0, 0]
    ax.hist(resid, bins=80, density=True, color=COLOURS["primary"], alpha=0.7,
            edgecolor="white", linewidth=0.3)
    x_range = np.linspace(resid.min(), resid.max(), 200)
    ax.plot(x_range, stats.norm.pdf(x_range), color=COLOURS["red"],
            linewidth=1.5, label="Normal")
    ax.set_title("Standardised Residuals")
    ax.set_xlabel("Residual")
    ax.legend()

    # QQ Plot
    ax = axes[0, 1]
    sorted_resid = np.sort(resid)
    theoretical = stats.norm.ppf(np.arange(1, len(resid) + 1) / (len(resid) + 1))
    ax.scatter(theoretical, sorted_resid, color=COLOURS["primary"], s=3, alpha=0.5)
    lim = max(abs(sorted_resid.min()), abs(sorted_resid.max()), abs(theoretical.min()), abs(theoretical.max()))
    ax.plot([-lim, lim], [-lim, lim], color=COLOURS["red"], linewidth=1, linestyle="--")
    ax.set_xlabel("Theoretical Quantile")
    ax.set_ylabel("Sample Quantile")
    ax.set_title("QQ Plot (vs Normal)")

    # ACF of residuals
    ax = axes[1, 0]
    plot_acf(resid, ax=ax, lags=40, alpha=0.05,
             color=COLOURS["primary"], vlines_kwargs={"color": COLOURS["primary"]})
    ax.set_title("ACF of Residuals")

    # ACF of squared residuals
    ax = axes[1, 1]
    plot_acf(resid**2, ax=ax, lags=40, alpha=0.05,
             color=COLOURS["amber"], vlines_kwargs={"color": COLOURS["amber"]})
    ax.set_title("ACF of Squared Residuals")

    fig.suptitle(f"{cfg['name']} — GARCH Residual Diagnostics", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "47_residual_diagnostics")
