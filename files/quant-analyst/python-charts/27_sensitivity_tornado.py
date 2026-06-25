"""
Chart 27 — Sensitivity Tornado Chart
Shows how DCF valuation changes when each input is varied by +/- one standard deviation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


BASE_CASE = {
    "Revenue Growth (%)":    8.0,
    "Operating Margin (%)": 30.0,
    "WACC (%)":             10.0,
    "Terminal Growth (%)":   2.5,
    "Tax Rate (%)":         21.0,
    "Capex / Revenue (%)":   5.0,
}

SWING = {
    "Revenue Growth (%)":    3.0,
    "Operating Margin (%)":  5.0,
    "WACC (%)":              1.5,
    "Terminal Growth (%)":   1.0,
    "Tax Rate (%)":          3.0,
    "Capex / Revenue (%)":   2.0,
}


def simple_dcf(rev_g, margin, wacc, term_g, tax, capex_pct,
               base_revenue=400e9, years=5):
    """Simplified DCF for sensitivity demonstration."""
    fcfs = []
    rev = base_revenue
    for _ in range(years):
        rev *= (1 + rev_g / 100)
        ebit = rev * (margin / 100)
        nopat = ebit * (1 - tax / 100)
        capex = rev * (capex_pct / 100)
        fcf = nopat - capex
        fcfs.append(fcf)

    terminal = fcfs[-1] * (1 + term_g / 100) / (wacc / 100 - term_g / 100)
    pv_fcfs = sum(f / (1 + wacc / 100)**t for t, f in enumerate(fcfs, 1))
    pv_terminal = terminal / (1 + wacc / 100)**years

    return (pv_fcfs + pv_terminal) / 1e9


def plot(df=None, cfg=CONFIG):
    apply_style()

    base_val = simple_dcf(**BASE_CASE)

    labels = []
    lows   = []
    highs  = []

    for param in BASE_CASE:
        params_low  = BASE_CASE.copy()
        params_high = BASE_CASE.copy()
        params_low[param]  -= SWING[param]
        params_high[param] += SWING[param]

        val_low  = simple_dcf(**params_low)
        val_high = simple_dcf(**params_high)

        labels.append(param)
        lows.append(min(val_low, val_high))
        highs.append(max(val_low, val_high))

    spreads = [h - l for h, l in zip(highs, lows)]
    order = np.argsort(spreads)[::-1]

    labels = [labels[i] for i in order]
    lows   = [lows[i]   for i in order]
    highs  = [highs[i]  for i in order]

    fig, ax = plt.subplots(figsize=(12, 7))

    y = np.arange(len(labels))
    ax.barh(y, [h - base_val for h in highs], left=base_val,
            color=COLOURS["green"], height=0.6, label="Upside")
    ax.barh(y, [l - base_val for l in lows], left=base_val,
            color=COLOURS["red"], height=0.6, label="Downside")

    ax.axvline(base_val, color=COLOURS["text"], linewidth=1.5, linestyle="-")
    ax.text(base_val, len(labels) - 0.5, f"  Base: ${base_val:,.0f}B",
            fontsize=9, fontweight="bold")

    for i, (lo, hi) in enumerate(zip(lows, highs)):
        ax.text(lo - 5, i, f"${lo:,.0f}B", ha="right", va="center", fontsize=8)
        ax.text(hi + 5, i, f"${hi:,.0f}B", ha="left", va="center", fontsize=8)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Enterprise Value ($B)")
    ax.set_title(f"{cfg['name']} — DCF Sensitivity (Tornado Chart)")
    ax.legend(loc="lower right")
    ax.invert_yaxis()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot()
    save_chart(fig, "27_sensitivity_tornado")
