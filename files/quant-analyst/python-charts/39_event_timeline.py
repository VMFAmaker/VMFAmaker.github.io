"""
Chart 39 — Event Timeline
Price chart with annotated event markers and shaded windows around each event.
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
import matplotlib.dates as mdates


EVENT_SHADE_DAYS = 5


def plot(df, cfg=CONFIG):
    apply_style()

    events = cfg.get("events", [])

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df.index, df["Close"].values, color=COLOURS["primary"], linewidth=0.8)

    colour_cycle = [COLOURS["red"], COLOURS["green"], COLOURS["amber"],
                    COLOURS["primary"], COLOURS["muted"]]

    for i, (date_str, name) in enumerate(events):
        event_date = pd.Timestamp(date_str)
        colour = colour_cycle[i % len(colour_cycle)]

        ax.axvline(event_date, color=colour, linewidth=1, linestyle="--", alpha=0.7)

        shade_start = event_date - pd.Timedelta(days=EVENT_SHADE_DAYS)
        shade_end   = event_date + pd.Timedelta(days=EVENT_SHADE_DAYS)
        ax.axvspan(shade_start, shade_end, alpha=0.05, color=colour)

        if event_date in df.index:
            y_val = df.loc[event_date, "Close"]
        else:
            nearest_idx = df.index.get_indexer([event_date], method="nearest")[0]
            y_val = df["Close"].iloc[nearest_idx]

        y_offset = 15 if i % 2 == 0 else -25
        ax.annotate(
            name, xy=(event_date, y_val),
            xytext=(0, y_offset), textcoords="offset points",
            fontsize=7, ha="center", color=colour, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=colour, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor=colour, alpha=0.8),
        )

    ax.set_ylabel("Price ($)")
    ax.set_title(f"{cfg['name']} — Event Timeline")
    format_date_axis(ax)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "39_event_timeline")
