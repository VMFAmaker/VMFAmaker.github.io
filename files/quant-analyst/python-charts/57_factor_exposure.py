"""
Chart 57 — Factor Exposure Bar Chart
Estimated factor betas (Market, Size, Value, Momentum) from a multi-factor regression.
Uses peer returns as proxy factors when Fama-French data is unavailable.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, PALETTE, save_chart
from _data   import load_prices, load_benchmark, load_peers

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def plot(df, cfg=CONFIG):
    apply_style()

    bench = load_benchmark()
    peers = load_peers()

    # Build factor proxies
    factors = pd.DataFrame({"Market": bench["Return"]})

    peer_returns = pd.DataFrame()
    for ticker, peer_df in peers.items():
        code_name = cfg["peers"].get(ticker, ticker)
        peer_returns[code_name] = peer_df["Return"]

    if peer_returns.shape[1] >= 2:
        sorted_cols = peer_returns.columns.tolist()
        half = len(sorted_cols) // 2
        factors["HML Proxy"] = peer_returns[sorted_cols[:half]].mean(axis=1) - \
                                peer_returns[sorted_cols[half:]].mean(axis=1)

    if peer_returns.shape[1] >= 1:
        mom = peer_returns.mean(axis=1).rolling(252).mean() - \
              peer_returns.mean(axis=1).rolling(21).mean()
        factors["Momentum Proxy"] = mom

    asset_ret = df["Return"]
    combined = factors.join(asset_ret, rsuffix="_asset").dropna()

    y = combined["Return"].values
    X = combined.drop(columns=["Return"]).values
    factor_names = [c for c in combined.columns if c != "Return"]

    X_with_const = np.column_stack([np.ones(len(X)), X])
    betas, residuals, _, _ = np.linalg.lstsq(X_with_const, y, rcond=None)

    intercept = betas[0]
    factor_betas = betas[1:]

    y_pred = X_with_const @ betas
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_sq = 1 - ss_res / ss_tot

    fig, ax = plt.subplots(figsize=(10, 6))

    x_pos = np.arange(len(factor_names))
    bar_colours = [COLOURS["green"] if b >= 0 else COLOURS["red"] for b in factor_betas]

    bars = ax.bar(x_pos, factor_betas, color=bar_colours, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, factor_betas):
        y_pos = val + 0.01 if val >= 0 else val - 0.03
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                f"{val:.3f}", ha="center", fontsize=10, fontweight="bold")

    ax.axhline(0, color=COLOURS["text"], linewidth=0.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(factor_names)
    ax.set_ylabel("Factor Beta")
    ax.set_title(f"{cfg['name']} — Factor Exposures (R-sq: {r_sq:.3f}, Alpha: {intercept*252*100:.2f}% ann.)")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "57_factor_exposure")
