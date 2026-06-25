"""
Chart 38 — Multi-Event CAR Grid
Side-by-side CAR plots for all configured events in _config.py.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices, load_benchmark

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


ESTIMATION_WINDOW = 252
EVENT_WINDOW      = 10


def compute_car(merged, event_date):
    if event_date not in merged.index:
        nearest = merged.index[merged.index.get_indexer([event_date], method="nearest")[0]]
        event_date = nearest

    event_loc = merged.index.get_loc(event_date)
    est_start = max(0, event_loc - ESTIMATION_WINDOW - EVENT_WINDOW)
    est_end   = event_loc - EVENT_WINDOW
    ev_start  = event_loc - EVENT_WINDOW
    ev_end    = min(len(merged), event_loc + EVENT_WINDOW + 1)

    est_data = merged.iloc[est_start:est_end]
    if len(est_data) < 30:
        return None

    slope, intercept, _, _, _ = stats.linregress(est_data["bench"], est_data["asset"])

    ev_data = merged.iloc[ev_start:ev_end].copy()
    ev_data["expected"] = intercept + slope * ev_data["bench"]
    ev_data["abnormal"] = ev_data["asset"] - ev_data["expected"]
    ev_data["car"]      = ev_data["abnormal"].cumsum()

    return ev_data


def plot(df, cfg=CONFIG):
    apply_style()

    events = cfg.get("events", [])
    if not events:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No events configured in _config.py",
                transform=ax.transAxes, ha="center", fontsize=14)
        return fig

    bench = load_benchmark()
    merged = pd.DataFrame({
        "asset": df["Return"],
        "bench": bench["Return"],
    }).dropna()

    n_events = len(events)
    cols = min(3, n_events)
    rows = (n_events + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)

    for idx, (date_str, name) in enumerate(events):
        r, c = divmod(idx, cols)
        ax = axes[r][c]

        ev_data = compute_car(merged, pd.Timestamp(date_str))

        if ev_data is None:
            ax.text(0.5, 0.5, "Insufficient data", transform=ax.transAxes, ha="center")
            ax.set_title(name, fontsize=9)
            continue

        days = np.arange(-EVENT_WINDOW, len(ev_data) - EVENT_WINDOW)
        car_pct = ev_data["car"].values * 100

        colour = COLOURS["green"] if car_pct[-1] >= 0 else COLOURS["red"]
        ax.plot(days, car_pct, color=colour, linewidth=1.5, marker="o", markersize=3)
        ax.fill_between(days, 0, car_pct, alpha=0.1, color=colour)
        ax.axvline(0, color=COLOURS["text"], linewidth=1, linestyle="-")
        ax.axhline(0, color=COLOURS["muted"], linewidth=0.5)

        ax.set_title(f"{name}\nCAR: {car_pct[-1]:+.2f}%", fontsize=9)
        ax.set_xlabel("Days", fontsize=8)
        ax.set_ylabel("CAR (%)", fontsize=8)

    for idx in range(n_events, rows * cols):
        r, c = divmod(idx, cols)
        axes[r][c].set_visible(False)

    fig.suptitle(f"{cfg['name']} — Event Study Grid", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "38_car_grid")
