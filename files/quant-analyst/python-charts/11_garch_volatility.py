"""
Chart 11 — GARCH Conditional Volatility
GARCH(1,1)-t and GJR-GARCH(1,1,1)-t conditional volatility overlaid.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model


def plot(df, cfg=CONFIG):
    apply_style()

    scaled = df["Return"].values * 100

    # GARCH(1,1)-t
    garch = arch_model(scaled, vol="Garch", p=1, q=1, dist="t", mean="Constant")
    garch_res = garch.fit(disp="off")
    garch_vol = np.array(garch_res.conditional_volatility).flatten() / 100 * np.sqrt(252) * 100

    # GJR-GARCH(1,1,1)-t
    gjr = arch_model(scaled, vol="Garch", p=1, o=1, q=1, dist="t", mean="Constant")
    gjr_res = gjr.fit(disp="off")
    gjr_vol = np.array(gjr_res.conditional_volatility).flatten() / 100 * np.sqrt(252) * 100

    dates = df.index[:len(garch_vol)]

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(dates, garch_vol, color=COLOURS["primary"], linewidth=0.8, label="GARCH(1,1)-t")
    ax.plot(dates, gjr_vol,   color=COLOURS["purple"],  linewidth=0.8, label="GJR-GARCH-t", alpha=0.8)

    median_vol = np.median(garch_vol)
    ax.axhline(median_vol, color=COLOURS["muted"], linestyle="--", linewidth=0.8,
               label=f"Median: {median_vol:.1f}%")

    ax.set_title(f"{cfg['name']} — GARCH Conditional Volatility (Annualised)")
    ax.set_ylabel("Volatility (%)")
    ax.legend()
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "11_garch_volatility")
