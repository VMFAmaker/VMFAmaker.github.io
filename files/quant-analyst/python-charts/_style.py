"""
Shared Chart Styling
====================
Keeps every chart visually consistent.
Import COLOURS and PALETTE for manual colour picks.
Call apply_style() at the top of every chart function.
Call save_chart(fig, name) to write to the output folder.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# ── Colour palette ──────────────────────────────────────────

COLOURS = {
    "primary":  "#2563EB",
    "red":      "#DC2626",
    "green":    "#16A34A",
    "amber":    "#F59E0B",
    "purple":   "#8B5CF6",
    "teal":     "#06B6D4",
    "muted":    "#94A3B8",
    "dark":     "#1E293B",
    "light":    "#F1F5F9",
}

PALETTE = [
    COLOURS["primary"],
    COLOURS["red"],
    COLOURS["green"],
    COLOURS["amber"],
    COLOURS["purple"],
    COLOURS["teal"],
]


# ── Style application ──────────────────────────────────────

def apply_style():
    """Set global matplotlib defaults for a clean, professional look."""
    plt.rcParams.update({
        "figure.facecolor":  "white",
        "axes.facecolor":    "#F8F9FA",
        "axes.grid":         True,
        "grid.alpha":        0.3,
        "grid.color":        "#CBD5E1",
        "font.family":       "sans-serif",
        "font.size":         10,
        "axes.titlesize":    13,
        "axes.titleweight":  "bold",
        "axes.labelsize":    11,
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "legend.fontsize":   9,
        "legend.framealpha": 0.9,
        "figure.dpi":        100,
    })


# ── Axis helpers ───────────────────────────────────────────

def format_date_axis(ax, interval_months=6):
    """Apply clean date formatting to a time-series x-axis."""
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval_months))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")


def add_zero_line(ax, **kwargs):
    """Draw a thin horizontal line at y = 0."""
    defaults = {"color": "black", "linewidth": 0.5, "zorder": 1}
    defaults.update(kwargs)
    ax.axhline(0, **defaults)


# ── Save helper ────────────────────────────────────────────

def save_chart(fig, name, cfg=None):
    """Save a figure to the configured output directory."""
    from _config import CONFIG
    cfg = cfg or CONFIG

    out_dir = cfg["output_dir"]
    os.makedirs(out_dir, exist_ok=True)

    filepath = os.path.join(out_dir, f"{name}.{cfg['format']}")
    fig.savefig(filepath, dpi=cfg["dpi"], bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {filepath}")
