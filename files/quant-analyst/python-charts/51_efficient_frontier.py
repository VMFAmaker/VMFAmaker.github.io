"""
Chart 51 — Efficient Frontier
Mean-variance frontier using the asset and its peers. Shows optimal portfolios.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from _config import CONFIG
from _style  import apply_style, COLOURS, save_chart
from _data   import load_prices, load_peers

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


N_PORTFOLIOS = 10000


def plot(df, cfg=CONFIG):
    apply_style()

    peers = load_peers()
    returns = pd.DataFrame({cfg["name"]: df["Return"]})

    for ticker, peer_df in peers.items():
        code_name = cfg["peers"].get(ticker, ticker)
        returns[code_name] = peer_df["Return"]

    returns = returns.dropna()
    n_assets = returns.shape[1]

    mean_ret = returns.mean() * 252
    cov      = returns.cov() * 252

    rng = np.random.default_rng(42)

    port_returns = []
    port_vols    = []
    port_sharpes = []
    all_weights  = []

    for _ in range(N_PORTFOLIOS):
        w = rng.random(n_assets)
        w /= w.sum()

        ret = np.dot(w, mean_ret)
        vol = np.sqrt(np.dot(w, np.dot(cov, w)))
        sr  = ret / vol

        port_returns.append(ret * 100)
        port_vols.append(vol * 100)
        port_sharpes.append(sr)
        all_weights.append(w)

    port_returns = np.array(port_returns)
    port_vols    = np.array(port_vols)
    port_sharpes = np.array(port_sharpes)

    max_sr_idx = np.argmax(port_sharpes)
    min_vol_idx = np.argmin(port_vols)

    fig, ax = plt.subplots(figsize=(12, 8))

    scatter = ax.scatter(port_vols, port_returns, c=port_sharpes, cmap="RdYlGn",
                         s=3, alpha=0.5)
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.8)
    cbar.set_label("Sharpe Ratio")

    ax.scatter(port_vols[max_sr_idx], port_returns[max_sr_idx],
               marker="*", s=300, color=COLOURS["red"], zorder=5,
               label=f"Max Sharpe ({port_sharpes[max_sr_idx]:.2f})")
    ax.scatter(port_vols[min_vol_idx], port_returns[min_vol_idx],
               marker="D", s=100, color=COLOURS["amber"], zorder=5,
               label="Min Variance")

    for i, name in enumerate(returns.columns):
        ret_i = mean_ret.iloc[i] * 100
        vol_i = np.sqrt(cov.iloc[i, i]) * 100
        ax.scatter(vol_i, ret_i, marker="o", s=80, color=COLOURS["primary"],
                   edgecolor="white", zorder=5)
        ax.annotate(name, (vol_i, ret_i), textcoords="offset points",
                    xytext=(8, 5), fontsize=8)

    ax.set_xlabel("Annualised Volatility (%)")
    ax.set_ylabel("Annualised Return (%)")
    ax.set_title(f"{cfg['name']} & Peers — Efficient Frontier ({N_PORTFOLIOS:,} portfolios)")
    ax.legend(loc="upper left")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    fig = plot(load_prices())
    save_chart(fig, "51_efficient_frontier")
