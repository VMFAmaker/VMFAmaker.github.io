"""
Chart 20 — Stress Test Scenario Comparison
Portfolio impact under historical and hypothetical stress scenarios.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


SCENARIOS = {
    "COVID Crash (Mar 2020)":      -0.34,
    "2022 Rate Shock":             -0.28,
    "Flash Crash (2010)":          -0.09,
    "GFC Peak (Oct 2008)":         -0.40,
    "Dot-Com Burst (2000-02)":     -0.49,
    "Black Monday (1987)":         -0.22,
    "1 Std Dev Move":              None,
    "2 Std Dev Move":              None,
    "3 Std Dev Move":              None,
}


def plot(df, cfg=CONFIG):
    apply_style()

    daily_std = df["Return"].std()

    impacts = {}
    for label, shock in SCENARIOS.items():
        if shock is None:
            multiplier = int(label[0])
            impacts[label] = -multiplier * daily_std * np.sqrt(21) * 100
        else:
            impacts[label] = shock * 100

    labels   = list(impacts.keys())
    values   = list(impacts.values())
    bar_cols = [COLOURS["red"] if v < -20 else COLOURS["amber"] if v < -10
                else COLOURS["green"] for v in values]

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(labels, values, color=bar_cols, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, values):
        x_pos = val - 1 if val < -5 else val + 0.5
        ha = "right" if val < -5 else "left"
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", ha=ha, fontsize=9, fontweight="bold")

    ax.axvline(0, color=COLOURS["text"], linewidth=0.5)
    ax.set_xlabel("Impact (%)")
    ax.set_title(f"{cfg['name']} — Stress Test Scenarios")
    ax.invert_yaxis()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "20_stress_test")
