"""
Chart 28 — Sensitivity Heatmap
Two-variable DCF sensitivity matrix (WACC vs Terminal Growth).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


WACC_RANGE     = np.arange(7.0, 14.5, 0.5)
TERM_G_RANGE   = np.arange(1.0, 4.5, 0.5)


def simple_dcf(wacc, term_g, base_revenue=400e9, rev_g=8.0,
               margin=30.0, tax=21.0, capex_pct=5.0, years=5):
    fcfs = []
    rev = base_revenue
    for _ in range(years):
        rev *= (1 + rev_g / 100)
        ebit = rev * (margin / 100)
        nopat = ebit * (1 - tax / 100)
        capex = rev * (capex_pct / 100)
        fcfs.append(nopat - capex)

    terminal = fcfs[-1] * (1 + term_g / 100) / (wacc / 100 - term_g / 100)
    pv_fcfs = sum(f / (1 + wacc / 100)**t for t, f in enumerate(fcfs, 1))
    pv_terminal = terminal / (1 + wacc / 100)**years

    return (pv_fcfs + pv_terminal) / 1e9


def plot(df=None, cfg=CONFIG):
    apply_style()

    matrix = np.zeros((len(TERM_G_RANGE), len(WACC_RANGE)))

    for i, tg in enumerate(TERM_G_RANGE):
        for j, w in enumerate(WACC_RANGE):
            if w / 100 <= tg / 100:
                matrix[i, j] = np.nan
            else:
                matrix[i, j] = simple_dcf(w, tg)

    fig, ax = plt.subplots(figsize=(14, 8))

    cmap = plt.cm.RdYlGn
    norm = mcolors.TwoSlopeNorm(
        vmin=np.nanmin(matrix),
        vcenter=np.nanmedian(matrix),
        vmax=np.nanmax(matrix),
    )

    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(np.arange(len(WACC_RANGE)))
    ax.set_yticks(np.arange(len(TERM_G_RANGE)))
    ax.set_xticklabels([f"{w:.1f}%" for w in WACC_RANGE], fontsize=8)
    ax.set_yticklabels([f"{g:.1f}%" for g in TERM_G_RANGE], fontsize=8)
    ax.set_xlabel("WACC")
    ax.set_ylabel("Terminal Growth Rate")

    for i in range(len(TERM_G_RANGE)):
        for j in range(len(WACC_RANGE)):
            val = matrix[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"${val:,.0f}B", ha="center", va="center", fontsize=7,
                        color="white" if val < np.nanpercentile(matrix, 30) else "black")

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Enterprise Value ($B)")

    ax.set_title(f"{cfg['name']} — DCF Sensitivity (WACC vs Terminal Growth)")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot()
    save_chart(fig, "28_sensitivity_heatmap")
