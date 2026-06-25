"""
Chart 60 — Option Payoff Diagram
Payoff at expiry for common option strategies (long call, long put, straddle, etc.).
Edit the STRATEGIES list to show different combinations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, PALETTE, save_chart
from _data   import load_prices

import numpy as np
import matplotlib.pyplot as plt


def call_payoff(S, K, premium, position=1):
    return position * (np.maximum(S - K, 0) - premium)


def put_payoff(S, K, premium, position=1):
    return position * (np.maximum(K - S, 0) - premium)


def plot(df, cfg=CONFIG):
    apply_style()

    current_price = df["Close"].iloc[-1]
    K = round(current_price, -1)

    strategies = {
        "Long Call":      lambda S: call_payoff(S, K, K * 0.03),
        "Long Put":       lambda S: put_payoff(S, K, K * 0.025),
        "Covered Call":   lambda S: (S - current_price) + call_payoff(S, K * 1.05, K * 0.015, -1),
        "Straddle":       lambda S: call_payoff(S, K, K * 0.03) + put_payoff(S, K, K * 0.025),
        "Bull Call Spread": lambda S: call_payoff(S, K * 0.95, K * 0.05) + call_payoff(S, K * 1.05, K * 0.015, -1),
    }

    price_range = np.linspace(current_price * 0.7, current_price * 1.3, 300)

    n_strats = len(strategies)
    cols = min(3, n_strats)
    rows = (n_strats + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)

    for idx, (name, payoff_fn) in enumerate(strategies.items()):
        r, c = divmod(idx, cols)
        ax = axes[r][c]

        payoff = payoff_fn(price_range)

        ax.plot(price_range, payoff, color=COLOURS["primary"], linewidth=1.5)
        ax.fill_between(price_range, 0, payoff,
                        where=payoff >= 0, alpha=0.15, color=COLOURS["green"])
        ax.fill_between(price_range, 0, payoff,
                        where=payoff < 0, alpha=0.15, color=COLOURS["red"])
        ax.axhline(0, color=COLOURS["muted"], linewidth=0.5)
        ax.axvline(current_price, color=COLOURS["amber"], linewidth=0.8, linestyle=":")

        max_profit = payoff.max()
        max_loss   = payoff.min()
        breakevens = price_range[np.where(np.diff(np.sign(payoff)))[0]]

        note = f"Max P: ${max_profit:.0f}\nMax L: ${max_loss:.0f}"
        if len(breakevens) > 0:
            be_str = ", ".join([f"${b:.0f}" for b in breakevens[:2]])
            note += f"\nBE: {be_str}"
        ax.text(0.02, 0.98, note, transform=ax.transAxes, fontsize=7,
                verticalalignment="top",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=COLOURS["muted"], alpha=0.8))

        ax.set_title(name, fontsize=10)
        ax.set_xlabel("Stock Price ($)")
        ax.set_ylabel("P&L ($)")

    for idx in range(n_strats, rows * cols):
        r, c = divmod(idx, cols)
        axes[r][c].set_visible(False)

    fig.suptitle(f"{cfg['name']} — Option Payoff Diagrams (K ~ ${K:.0f})",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "60_payoff_diagram")
