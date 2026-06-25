"""
Chart 45 — Parameter Stability
Rolling GARCH parameters (alpha, beta, persistence) over time to check stability.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt

try:
    from arch import arch_model
    HAS_ARCH = True
except ImportError:
    HAS_ARCH = False


ROLL_WINDOW = 504
STEP        = 21


def plot(df, cfg=CONFIG):
    apply_style()

    if not HAS_ARCH:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "Install 'arch' package: pip install arch",
                transform=ax.transAxes, ha="center", fontsize=14)
        return fig

    returns = df["Return"].values * 100
    dates   = df.index

    roll_dates = []
    alphas     = []
    betas      = []
    persistence = []

    for end in range(ROLL_WINDOW, len(returns), STEP):
        window = returns[end - ROLL_WINDOW : end]

        try:
            model = arch_model(window, vol="Garch", p=1, q=1, dist="t", rescale=False)
            result = model.fit(disp="off", show_warning=False)
            a = result.params.get("alpha[1]", np.nan)
            b = result.params.get("beta[1]", np.nan)
        except Exception:
            a, b = np.nan, np.nan

        roll_dates.append(dates[end - 1])
        alphas.append(a)
        betas.append(b)
        persistence.append(a + b if not (np.isnan(a) or np.isnan(b)) else np.nan)

    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

    axes[0].plot(roll_dates, alphas, color=COLOURS["primary"], linewidth=0.8)
    axes[0].set_ylabel("Alpha")
    axes[0].set_title(f"{cfg['name']} — GARCH(1,1) Parameter Stability ({ROLL_WINDOW}-Day Rolling)")

    axes[1].plot(roll_dates, betas, color=COLOURS["amber"], linewidth=0.8)
    axes[1].set_ylabel("Beta")

    axes[2].plot(roll_dates, persistence, color=COLOURS["red"], linewidth=0.8)
    axes[2].axhline(1.0, color=COLOURS["muted"], linewidth=0.5, linestyle=":", label="Persistence = 1")
    axes[2].set_ylabel("Persistence (a+b)")
    axes[2].legend(fontsize=8)
    format_date_axis(axes[2])

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "45_parameter_stability")
