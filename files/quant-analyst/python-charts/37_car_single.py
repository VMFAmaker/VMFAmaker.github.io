"""
Chart 37 — Single Event CAR (Cumulative Abnormal Return)
Market model event study for a single event with estimation and event windows.
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


def plot(df, cfg=CONFIG):
    apply_style()

    events = cfg.get("events", [])
    if not events:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No events configured in _config.py",
                transform=ax.transAxes, ha="center", fontsize=14)
        return fig

    event_date, event_name = events[0]
    event_date = pd.Timestamp(event_date)

    bench = load_benchmark()
    merged = pd.DataFrame({
        "asset": df["Return"],
        "bench": bench["Return"],
    }).dropna()

    if event_date not in merged.index:
        nearest = merged.index[merged.index.get_indexer([event_date], method="nearest")[0]]
        event_date = nearest

    event_loc = merged.index.get_loc(event_date)
    est_start = max(0, event_loc - ESTIMATION_WINDOW - EVENT_WINDOW)
    est_end   = event_loc - EVENT_WINDOW
    ev_start  = event_loc - EVENT_WINDOW
    ev_end    = min(len(merged), event_loc + EVENT_WINDOW + 1)

    est_data = merged.iloc[est_start:est_end]
    slope, intercept, _, _, _ = stats.linregress(est_data["bench"], est_data["asset"])

    ev_data = merged.iloc[ev_start:ev_end].copy()
    ev_data["expected"] = intercept + slope * ev_data["bench"]
    ev_data["abnormal"] = ev_data["asset"] - ev_data["expected"]
    ev_data["car"]      = ev_data["abnormal"].cumsum()

    days = np.arange(-EVENT_WINDOW, len(ev_data) - EVENT_WINDOW)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))

    # Abnormal returns
    colours = [COLOURS["green"] if v >= 0 else COLOURS["red"] for v in ev_data["abnormal"].values]
    ax1.bar(days, ev_data["abnormal"].values * 100, color=colours, alpha=0.7)
    ax1.axvline(0, color=COLOURS["text"], linewidth=1.5, linestyle="-", label="Event Day")
    ax1.axhline(0, color=COLOURS["muted"], linewidth=0.5)
    ax1.set_ylabel("Abnormal Return (%)")
    ax1.set_title(f"{cfg['name']} — Event Study: {event_name}")
    ax1.legend()

    # CAR
    ax2.plot(days, ev_data["car"].values * 100, color=COLOURS["primary"], linewidth=1.5, marker="o", markersize=4)
    ax2.fill_between(days, 0, ev_data["car"].values * 100, alpha=0.1, color=COLOURS["primary"])
    ax2.axvline(0, color=COLOURS["text"], linewidth=1.5, linestyle="-")
    ax2.axhline(0, color=COLOURS["muted"], linewidth=0.5)

    final_car = ev_data["car"].iloc[-1] * 100
    ax2.text(0.98, 0.95, f"CAR: {final_car:+.2f}%",
             transform=ax2.transAxes, ha="right", va="top", fontsize=11, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLOURS["muted"]))

    ax2.set_xlabel("Days Relative to Event")
    ax2.set_ylabel("CAR (%)")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "37_car_single")
