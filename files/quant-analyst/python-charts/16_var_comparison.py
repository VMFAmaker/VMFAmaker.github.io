"""
Chart 16 — VaR Comparison (Multiple Methods)
Historical, Parametric Normal, and Parametric Student-t VaR overlaid on returns.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, add_zero_line, save_chart
from _data   import load_prices

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


CONFIDENCE = 0.99


def plot(df, cfg=CONFIG):
    apply_style()

    returns = df["Return"].values

    hist_var  = np.percentile(returns, (1 - CONFIDENCE) * 100)
    norm_var  = stats.norm.ppf(1 - CONFIDENCE, loc=np.mean(returns), scale=np.std(returns, ddof=1))
    t_params  = stats.t.fit(returns)
    t_var     = stats.t.ppf(1 - CONFIDENCE, *t_params)

    fig, ax = plt.subplots(figsize=(14, 5))

    ax.bar(df.index, returns * 100,
           color=[COLOURS["muted"] if r >= hist_var else COLOURS["red"] for r in returns],
           width=1, alpha=0.5)

    ax.axhline(hist_var * 100, color=COLOURS["primary"], linewidth=1.5, linestyle="--",
               label=f"Historical VaR {CONFIDENCE:.0%}: {hist_var*100:.2f}%")
    ax.axhline(norm_var * 100, color=COLOURS["amber"],   linewidth=1.5, linestyle="--",
               label=f"Normal VaR {CONFIDENCE:.0%}: {norm_var*100:.2f}%")
    ax.axhline(t_var * 100,    color=COLOURS["green"],   linewidth=1.5, linestyle="--",
               label=f"Student-t VaR {CONFIDENCE:.0%}: {t_var*100:.2f}%")

    add_zero_line(ax)
    ax.set_title(f"{cfg['name']} — Value at Risk Comparison ({CONFIDENCE:.0%})")
    ax.set_ylabel("Daily Return (%)")
    ax.legend(loc="lower left")
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "16_var_comparison")
