"""
Chart 08 — Empirical CDF vs Theoretical CDF
Step function of actual returns against Normal and Student-t CDFs.
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

    returns = np.sort(df["Return"].values)
    n = len(returns)
    ecdf = np.arange(1, n + 1) / n

    norm_params = stats.norm.fit(returns)
    t_params    = stats.t.fit(returns)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.step(returns * 100, ecdf, color=COLOURS["primary"], linewidth=1.2, label="Empirical CDF")
    ax.plot(returns * 100, stats.norm.cdf(returns, *norm_params),
            color=COLOURS["red"], linewidth=1.5, linestyle="--", label="Normal CDF")
    ax.plot(returns * 100, stats.t.cdf(returns, *t_params),
            color=COLOURS["green"], linewidth=1.5, linestyle="--",
            label=f"Student-t CDF (df={t_params[0]:.1f})")

    ax.set_title(f"{cfg['name']} — Empirical vs Theoretical CDF")
    ax.set_xlabel("Daily Return (%)")
    ax.set_ylabel("Cumulative Probability")
    ax.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "08_empirical_cdf")
