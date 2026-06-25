"""
Chart 48 — Out-of-Sample Forecast
GARCH volatility forecast vs realised volatility on a holdout period.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, format_date_axis, save_chart
from _data   import load_prices

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from arch import arch_model
    HAS_ARCH = True
except ImportError:
    HAS_ARCH = False


TRAIN_FRAC = 0.70
REALISED_WINDOW = 5


def plot(df, cfg=CONFIG):
    apply_style()

    if not HAS_ARCH:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "Install 'arch' package: pip install arch",
                transform=ax.transAxes, ha="center", fontsize=14)
        return fig

    returns_pct = df["Return"].dropna() * 100
    n = len(returns_pct)
    split = int(n * TRAIN_FRAC)

    train = returns_pct.iloc[:split]
    test  = returns_pct.iloc[split:]

    model = arch_model(train, vol="Garch", p=1, q=1, dist="t", rescale=False)
    result = model.fit(disp="off", show_warning=False)

    forecasts = []
    for i in range(len(test)):
        expanding = returns_pct.iloc[:split + i]
        mod = arch_model(expanding, vol="Garch", p=1, q=1, dist="t", rescale=False)
        res = mod.fit(disp="off", show_warning=False, starting_values=result.params.values)
        fcast = res.forecast(horizon=1)
        forecasts.append(np.sqrt(fcast.variance.values[-1, 0]))

    forecast_vol = pd.Series(forecasts, index=test.index)
    realised_vol = test.rolling(REALISED_WINDOW).std()

    rmse = np.sqrt(np.nanmean((forecast_vol.values - realised_vol.values)**2))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                    gridspec_kw={"height_ratios": [2, 1]},
                                    sharex=True)

    ax1.plot(forecast_vol.index, forecast_vol.values, color=COLOURS["primary"],
             linewidth=0.8, label="GARCH Forecast")
    ax1.plot(realised_vol.index, realised_vol.values, color=COLOURS["amber"],
             linewidth=0.8, label=f"Realised ({REALISED_WINDOW}-day)")
    ax1.axvline(test.index[0], color=COLOURS["muted"], linewidth=1, linestyle=":",
                label="OOS Start")
    ax1.set_ylabel("Volatility (% daily)")
    ax1.set_title(f"{cfg['name']} — Out-of-Sample Volatility Forecast (RMSE: {rmse:.4f})")
    ax1.legend(fontsize=8)

    # Forecast error
    error = forecast_vol - realised_vol
    ax2.bar(error.index, error.values, color=COLOURS["muted"], width=1, alpha=0.6)
    ax2.axhline(0, color=COLOURS["text"], linewidth=0.5)
    ax2.set_ylabel("Forecast Error (%)")
    format_date_axis(ax2)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "48_oos_forecast")
