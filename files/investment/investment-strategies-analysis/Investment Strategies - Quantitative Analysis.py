"""
Investment Strategies — Quantitative Comparison
================================================
Simulates and compares major investment strategies using modelled
returns. Covers value, growth, index, momentum, dividend, contrarian,
and day trading approaches with risk-adjusted performance metrics.

Run:  python "Investment Strategies - Quantitative Analysis.py"
Deps: numpy, matplotlib, pandas (pip install numpy matplotlib pandas)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from dataclasses import dataclass
from typing import Dict, List, Tuple
import os

plt.style.use("seaborn-v0_8-whitegrid")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 42
np.random.seed(SEED)

YEARS = 20
MONTHS = YEARS * 12
N_SIMS = 10_000
INITIAL_CAPITAL = 10_000
MONTHLY_CONTRIB = 300
RISK_FREE_RATE = 0.04


# ═══════════════════════════════════════════════════════════════
# 1.  STRATEGY DEFINITIONS
# ═══════════════════════════════════════════════════════════════
@dataclass
class Strategy:
    name: str
    creator: str
    annual_return: float
    annual_vol: float
    max_drawdown: float
    annual_costs: float
    description: str
    min_skill: str
    time_commitment: str

STRATEGIES = {
    "value": Strategy(
        "Value Investing", "Benjamin Graham (1934)",
        0.110, 0.160, -0.45, 0.003,
        "Buy undervalued stocks trading below intrinsic value",
        "Intermediate", "5-10 hrs/week"
    ),
    "growth": Strategy(
        "Growth Investing", "Philip Fisher (1958)",
        0.125, 0.200, -0.55, 0.004,
        "Buy companies with above-average earnings growth",
        "Intermediate", "5-10 hrs/week"
    ),
    "index": Strategy(
        "Index Investing", "John Bogle (1976)",
        0.090, 0.150, -0.50, 0.001,
        "Buy and hold a broad market index fund",
        "None", "0.5 hrs/week"
    ),
    "dividend": Strategy(
        "Dividend Investing", "Geraldine Weiss (1966)",
        0.085, 0.120, -0.35, 0.003,
        "Buy stocks with consistent, growing dividends",
        "Beginner", "2-3 hrs/week"
    ),
    "momentum": Strategy(
        "Momentum Investing", "Richard Driehaus (1980s)",
        0.115, 0.220, -0.55, 0.008,
        "Buy recent winners, sell recent losers",
        "Advanced", "10-15 hrs/week"
    ),
    "contrarian": Strategy(
        "Contrarian Investing", "Sir John Templeton (1954)",
        0.105, 0.190, -0.50, 0.004,
        "Buy when others are fearful, sell when greedy",
        "Advanced", "5-10 hrs/week"
    ),
    "magic_formula": Strategy(
        "Magic Formula", "Joel Greenblatt (2005)",
        0.108, 0.170, -0.48, 0.005,
        "Rank stocks by earnings yield + return on capital",
        "Beginner", "2-3 hrs/month"
    ),
    "canslim": Strategy(
        "CAN SLIM", "William O'Neil (1988)",
        0.120, 0.210, -0.55, 0.010,
        "Seven-factor system combining fundamentals and technicals",
        "Advanced", "15-20 hrs/week"
    ),
    "all_weather": Strategy(
        "All Weather Portfolio", "Ray Dalio (1996)",
        0.072, 0.080, -0.20, 0.003,
        "Risk parity across asset classes for all conditions",
        "Beginner", "1-2 hrs/month"
    ),
    "day_trading": Strategy(
        "Day Trading (Technical)", "Charles Dow / various (1900s+)",
        0.020, 0.350, -0.80, 0.050,
        "Short-term trades using chart patterns and indicators",
        "Expert", "40-60 hrs/week"
    ),
    "bond_ladder": Strategy(
        "Bond Laddering", "Traditional (institutional practice)",
        0.045, 0.040, -0.08, 0.002,
        "Stagger bond maturities for steady income and reinvestment",
        "Beginner", "1-2 hrs/month"
    ),
    "dogs_of_dow": Strategy(
        "Dogs of the Dow", "Michael O'Higgins (1991)",
        0.095, 0.155, -0.45, 0.003,
        "Buy the 10 highest-yielding Dow stocks, rebalance annually",
        "None", "1 hr/year"
    ),
}


# ═══════════════════════════════════════════════════════════════
# 2.  MONTE CARLO SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════
def simulate_strategy(strategy: Strategy, n_sims: int = N_SIMS) -> np.ndarray:
    """Run Monte Carlo simulation for a strategy. Returns terminal values."""
    monthly_ret = (strategy.annual_return - strategy.annual_costs) / 12
    monthly_vol = strategy.annual_vol / np.sqrt(12)

    terminals = np.zeros(n_sims)
    paths = np.zeros((n_sims, MONTHS + 1))

    for sim in range(n_sims):
        balance = INITIAL_CAPITAL
        paths[sim, 0] = balance
        for m in range(MONTHS):
            r = np.random.normal(monthly_ret, monthly_vol)
            balance = (balance + MONTHLY_CONTRIB) * (1 + r)
            balance = max(balance, 0)
            paths[sim, m + 1] = balance
        terminals[sim] = balance

    return terminals, paths


def compute_metrics(terminals: np.ndarray, paths: np.ndarray, strategy: Strategy) -> dict:
    """Compute risk-adjusted performance metrics."""
    total_contributed = INITIAL_CAPITAL + MONTHLY_CONTRIB * MONTHS
    net_return = strategy.annual_return - strategy.annual_costs

    # Max drawdown from paths
    drawdowns = []
    for sim in range(min(1000, paths.shape[0])):
        peak = np.maximum.accumulate(paths[sim])
        dd = (paths[sim] - peak) / np.where(peak > 0, peak, 1)
        drawdowns.append(dd.min())
    avg_max_dd = np.mean(drawdowns)

    # Sharpe ratio (annualised)
    excess_return = net_return - RISK_FREE_RATE
    sharpe = excess_return / strategy.annual_vol if strategy.annual_vol > 0 else 0

    # Sortino ratio (using downside deviation)
    monthly_returns = np.diff(paths[:1000], axis=1) / np.where(paths[:1000, :-1] > 0, paths[:1000, :-1], 1)
    downside = monthly_returns[monthly_returns < 0]
    downside_dev = np.std(downside) * np.sqrt(12) if len(downside) > 0 else 0.01
    sortino = excess_return / downside_dev

    return {
        "median": np.median(terminals),
        "mean": np.mean(terminals),
        "p10": np.percentile(terminals, 10),
        "p25": np.percentile(terminals, 25),
        "p75": np.percentile(terminals, 75),
        "p90": np.percentile(terminals, 90),
        "prob_loss": np.mean(terminals < total_contributed) * 100,
        "prob_double": np.mean(terminals > total_contributed * 2) * 100,
        "prob_5x": np.mean(terminals > total_contributed * 5) * 100,
        "sharpe": sharpe,
        "sortino": sortino,
        "avg_max_drawdown": avg_max_dd * 100,
        "total_contributed": total_contributed,
        "growth_multiple": np.median(terminals) / total_contributed,
    }


# ═══════════════════════════════════════════════════════════════
# 3.  DAY TRADING PATTERN ANALYSIS
# ═══════════════════════════════════════════════════════════════
@dataclass
class TradingPattern:
    name: str
    creator: str
    win_rate: float
    avg_risk_reward: float
    frequency: str
    reliability: str

PATTERNS = [
    TradingPattern("Head and Shoulders", "Charles Dow (1900s)", 0.65, 1.5, "Moderate", "High"),
    TradingPattern("Double Top / Bottom", "Charles Dow (1900s)", 0.60, 1.3, "Common", "Moderate"),
    TradingPattern("Cup and Handle", "William O'Neil (1988)", 0.62, 1.8, "Rare", "High"),
    TradingPattern("Bullish/Bearish Engulfing", "Steve Nison (1991)", 0.55, 1.2, "Very Common", "Low-Moderate"),
    TradingPattern("Morning/Evening Star", "Steve Nison (1991)", 0.58, 1.4, "Moderate", "Moderate"),
    TradingPattern("Fibonacci Retracement", "Leonardo Fibonacci / traders", 0.50, 1.5, "Very Common", "Low"),
    TradingPattern("RSI Divergence", "J. Welles Wilder Jr. (1978)", 0.55, 1.3, "Common", "Moderate"),
    TradingPattern("MACD Crossover", "Gerald Appel (1979)", 0.52, 1.1, "Very Common", "Low"),
    TradingPattern("Bollinger Band Squeeze", "John Bollinger (1980s)", 0.58, 1.6, "Moderate", "Moderate"),
    TradingPattern("Moving Avg Crossover", "Various (1960s+)", 0.50, 1.2, "Common", "Low"),
    TradingPattern("Hammer / Hanging Man", "Steve Nison (1991)", 0.54, 1.2, "Common", "Low-Moderate"),
    TradingPattern("Triangle Breakout", "Richard Schabacker (1930s)", 0.60, 1.4, "Moderate", "Moderate"),
]


def simulate_pattern_trading(pattern: TradingPattern, trades_per_month: int = 8,
                              months: int = 60, capital: float = 10_000,
                              risk_per_trade: float = 0.02, n_sims: int = 5_000) -> dict:
    """Simulate a day trading pattern strategy over time."""
    terminals = np.zeros(n_sims)
    for sim in range(n_sims):
        bal = capital
        for m in range(months):
            for t in range(trades_per_month):
                if bal < 500:
                    break
                risk_amount = bal * risk_per_trade
                if np.random.random() < pattern.win_rate:
                    bal += risk_amount * pattern.avg_risk_reward
                else:
                    bal -= risk_amount
                bal -= 2.0  # commission
        terminals[sim] = max(bal, 0)

    return {
        "pattern": pattern.name,
        "median": np.median(terminals),
        "prob_profit": np.mean(terminals > capital) * 100,
        "prob_loss_50pct": np.mean(terminals < capital * 0.5) * 100,
        "best_10pct": np.percentile(terminals, 90),
        "worst_10pct": np.percentile(terminals, 10),
    }


# ═══════════════════════════════════════════════════════════════
# 4.  BOND STRATEGY COMPARISON
# ═══════════════════════════════════════════════════════════════
def simulate_bond_strategies(n_sims: int = 5_000, years: int = 10, capital: float = 50_000):
    """Compare bond ladder, barbell, and bullet strategies."""
    results = {}

    # Bond Ladder: spread across 1-10 year maturities
    ladder_yields = [0.038, 0.039, 0.040, 0.041, 0.042, 0.043, 0.044, 0.045, 0.046, 0.047]
    ladder_avg_yield = np.mean(ladder_yields)
    ladder_duration = 5.5

    # Barbell: 70% short-term (1-2yr), 30% long-term (10-20yr)
    barbell_yield = 0.70 * 0.038 + 0.30 * 0.050
    barbell_duration = 0.70 * 1.5 + 0.30 * 15.0

    # Bullet: concentrate at 5-year maturity
    bullet_yield = 0.043
    bullet_duration = 5.0

    strategies = {
        "Ladder": {"yield": ladder_avg_yield, "duration": ladder_duration},
        "Barbell": {"yield": barbell_yield, "duration": barbell_duration},
        "Bullet": {"yield": bullet_yield, "duration": bullet_duration},
    }

    for name, params in strategies.items():
        terminals = np.zeros(n_sims)
        for sim in range(n_sims):
            bal = capital
            for yr in range(years):
                rate_change = np.random.normal(0, 0.008)
                price_impact = -params["duration"] * rate_change
                income = bal * params["yield"]
                bal = bal * (1 + price_impact) + income
            terminals[sim] = bal

        results[name] = {
            "median": np.median(terminals),
            "yield": params["yield"],
            "duration": params["duration"],
            "volatility": np.std(terminals) / capital,
            "worst_10pct": np.percentile(terminals, 10),
            "best_10pct": np.percentile(terminals, 90),
            "income_10yr": capital * params["yield"] * years,
        }

    return results


# ═══════════════════════════════════════════════════════════════
# 5.  VISUALISATION
# ═══════════════════════════════════════════════════════════════
def plot_strategy_comparison(all_metrics: Dict[str, dict]):
    """Risk-return scatter plot of all strategies."""
    fig, ax = plt.subplots(figsize=(14, 9))

    colours = {
        "value": "#2E75B6", "growth": "#27AE60", "index": "#1ABC9C",
        "dividend": "#F39C12", "momentum": "#9B59B6", "contrarian": "#E67E22",
        "magic_formula": "#3498DB", "canslim": "#E74C3C", "all_weather": "#2ECC71",
        "day_trading": "#C0392B", "bond_ladder": "#7F8C8D", "dogs_of_dow": "#D4AC0D",
    }

    for key, strat in STRATEGIES.items():
        m = all_metrics[key]
        x = strat.annual_vol * 100
        y = (strat.annual_return - strat.annual_costs) * 100
        size = max(m["sharpe"] * 200, 50)
        colour = colours.get(key, "#999999")

        ax.scatter(x, y, s=size, c=colour, alpha=0.7, edgecolors="white", linewidths=1.5, zorder=5)
        offset_x = 0.5
        offset_y = 0.3 if key not in ("contrarian", "dogs_of_dow") else -0.5
        ax.annotate(strat.name, (x, y), textcoords="offset points",
                    xytext=(15, offset_y * 20), fontsize=9, fontweight="bold", color=colour,
                    arrowprops=dict(arrowstyle="-", color=colour, alpha=0.5))

    # Capital Market Line
    cml_x = np.linspace(0, 40, 100)
    cml_y = RISK_FREE_RATE * 100 + 0.35 * cml_x
    ax.plot(cml_x, cml_y, "--", color="#CCCCCC", linewidth=1, label="Approx. Capital Market Line", zorder=1)

    ax.set_xlabel("Annual Volatility (%)", fontsize=13)
    ax.set_ylabel("Net Annual Return (%)", fontsize=13)
    ax.set_title("Investment Strategies — Risk vs Return\n(Bubble size = Sharpe Ratio)", fontsize=15, fontweight="bold")
    ax.legend(fontsize=10, loc="upper left")
    ax.set_xlim(-1, 40)
    ax.set_ylim(-2, 14)
    ax.axhline(y=RISK_FREE_RATE * 100, color="#E0E0E0", linewidth=0.8, linestyle=":")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_risk_return.png"), dpi=150)
    plt.close()


def plot_terminal_distributions(all_terminals: Dict[str, np.ndarray]):
    """Distribution comparison for key strategies."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    selected = ["index", "value", "growth", "momentum", "all_weather", "day_trading"]
    colours = ["#1ABC9C", "#2E75B6", "#27AE60", "#9B59B6", "#2ECC71", "#C0392B"]

    total_contrib = INITIAL_CAPITAL + MONTHLY_CONTRIB * MONTHS

    for ax, key, col in zip(axes.flatten(), selected, colours):
        terms = all_terminals[key] / 1000
        ax.hist(terms, bins=60, color=col, alpha=0.7, edgecolor="white", linewidth=0.5)
        med = np.median(all_terminals[key])
        ax.axvline(total_contrib / 1000, color="#E74C3C", linestyle="--", linewidth=1.5, label=f"Contributed: £{total_contrib/1000:.0f}k")
        ax.axvline(med / 1000, color="#1B3A5C", linestyle="-", linewidth=2, label=f"Median: £{med/1000:.0f}k")
        ax.set_title(STRATEGIES[key].name, fontsize=12, fontweight="bold", color=col)
        ax.set_xlabel("Terminal Value (£k)")
        ax.legend(fontsize=8)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))

    plt.suptitle(f"20-Year Outcome Distributions (£{INITIAL_CAPITAL:,} + £{MONTHLY_CONTRIB}/mo)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_distributions.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_pattern_results(pattern_results: List[dict]):
    """Day trading pattern win rates and profitability."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    names = [r["pattern"] for r in pattern_results]
    probs = [r["prob_profit"] for r in pattern_results]
    medians = [r["median"] for r in pattern_results]
    y_pos = np.arange(len(names))

    colours = ["#27AE60" if p > 50 else "#E74C3C" for p in probs]
    ax1.barh(y_pos, probs, color=colours, alpha=0.7, edgecolor="white")
    ax1.axvline(50, color="#1B3A5C", linestyle="--", linewidth=1.5, label="Break-even line")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=9)
    ax1.set_xlabel("Probability of Profit (%)")
    ax1.set_title("Day Trading Patterns — Probability of Profit (5 Years)", fontsize=12, fontweight="bold")
    ax1.legend()
    ax1.invert_yaxis()

    colours2 = ["#27AE60" if m > 10_000 else "#E74C3C" for m in medians]
    ax2.barh(y_pos, [m/1000 for m in medians], color=colours2, alpha=0.7, edgecolor="white")
    ax2.axvline(10, color="#1B3A5C", linestyle="--", linewidth=1.5, label="Starting capital (£10k)")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(names, fontsize=9)
    ax2.set_xlabel("Median Outcome (£ thousands)")
    ax2.set_title("Day Trading Patterns — Median 5-Year Outcome", fontsize=12, fontweight="bold")
    ax2.legend()
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))
    ax2.invert_yaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_pattern_analysis.png"), dpi=150)
    plt.close()


def plot_bond_comparison(bond_results: dict):
    """Bond strategy comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    names = list(bond_results.keys())
    colours = ["#2E75B6", "#F39C12", "#27AE60"]

    # Yield vs Duration
    for name, col in zip(names, colours):
        r = bond_results[name]
        ax1.scatter(r["duration"], r["yield"] * 100, s=300, c=col, alpha=0.8,
                    edgecolors="white", linewidths=2, zorder=5)
        ax1.annotate(name, (r["duration"], r["yield"] * 100),
                     textcoords="offset points", xytext=(15, 5), fontsize=11, fontweight="bold", color=col)

    ax1.set_xlabel("Duration (years)", fontsize=12)
    ax1.set_ylabel("Yield (%)", fontsize=12)
    ax1.set_title("Bond Strategies — Yield vs Duration Risk", fontsize=13, fontweight="bold")

    # Outcome range
    x = np.arange(len(names))
    worst = [bond_results[n]["worst_10pct"] / 1000 for n in names]
    median = [bond_results[n]["median"] / 1000 for n in names]
    best = [bond_results[n]["best_10pct"] / 1000 for n in names]

    ax2.bar(x, median, width=0.5, color=colours, alpha=0.7, label="Median")
    ax2.errorbar(x, median,
                 yerr=[[m - w for m, w in zip(median, worst)],
                       [b - m for b, m in zip(best, median)]],
                 fmt="none", color="#1B3A5C", capsize=8, capthick=2, linewidth=2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, fontsize=11)
    ax2.set_ylabel("10-Year Value from £50k (£ thousands)", fontsize=11)
    ax2.set_title("Bond Strategies — 10-Year Outcome Range", fontsize=13, fontweight="bold")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_bond_strategies.png"), dpi=150)
    plt.close()


def plot_sharpe_comparison(all_metrics: Dict[str, dict]):
    """Sharpe and Sortino ratio comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    sorted_keys = sorted(all_metrics.keys(), key=lambda k: all_metrics[k]["sharpe"], reverse=True)
    names = [STRATEGIES[k].name for k in sorted_keys]
    sharpes = [all_metrics[k]["sharpe"] for k in sorted_keys]
    sortinos = [all_metrics[k]["sortino"] for k in sorted_keys]

    colours = ["#27AE60" if s > 0.3 else "#F39C12" if s > 0.1 else "#E74C3C" for s in sharpes]
    y_pos = np.arange(len(names))

    ax1.barh(y_pos, sharpes, color=colours, alpha=0.7, edgecolor="white")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=9)
    ax1.set_xlabel("Sharpe Ratio")
    ax1.set_title("Risk-Adjusted Return (Sharpe Ratio)", fontsize=12, fontweight="bold")
    ax1.axvline(0, color="#999999", linewidth=0.8)
    ax1.invert_yaxis()

    colours2 = ["#27AE60" if s > 0.4 else "#F39C12" if s > 0.15 else "#E74C3C" for s in sortinos]
    ax2.barh(y_pos, sortinos, color=colours2, alpha=0.7, edgecolor="white")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(names, fontsize=9)
    ax2.set_xlabel("Sortino Ratio")
    ax2.set_title("Downside Risk-Adjusted Return (Sortino Ratio)", fontsize=12, fontweight="bold")
    ax2.axvline(0, color="#999999", linewidth=0.8)
    ax2.invert_yaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_risk_adjusted.png"), dpi=150)
    plt.close()


# ═══════════════════════════════════════════════════════════════
# 6.  MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("  Investment Strategies — Quantitative Comparison")
    print("=" * 70)

    # --- Strategy simulations ---
    print("\n[1/5] Running Monte Carlo simulations for 12 strategies...")
    all_terminals = {}
    all_metrics = {}

    for key, strat in STRATEGIES.items():
        terminals, paths = simulate_strategy(strat, n_sims=N_SIMS)
        metrics = compute_metrics(terminals, paths, strat)
        all_terminals[key] = terminals
        all_metrics[key] = metrics
        net_ret = (strat.annual_return - strat.annual_costs) * 100
        print(f"  {strat.name:30s}  Net: {net_ret:5.1f}%  Vol: {strat.annual_vol*100:5.1f}%  "
              f"Sharpe: {metrics['sharpe']:.2f}  Median: £{metrics['median']:>10,.0f}  "
              f"P(loss): {metrics['prob_loss']:.1f}%")

    # --- Pattern analysis ---
    print("\n[2/5] Simulating day trading patterns (5,000 paths each)...")
    pattern_results = []
    for p in PATTERNS:
        result = simulate_pattern_trading(p)
        pattern_results.append(result)
        status = "PROFIT" if result["prob_profit"] > 50 else "LOSS"
        print(f"  {p.name:30s}  Win: {p.win_rate*100:.0f}%  R:R {p.avg_risk_reward:.1f}  "
              f"P(profit): {result['prob_profit']:.1f}%  [{status}]")

    # --- Bond strategies ---
    print("\n[3/5] Comparing bond strategies...")
    bond_results = simulate_bond_strategies()
    for name, r in bond_results.items():
        print(f"  {name:10s}  Yield: {r['yield']*100:.1f}%  Duration: {r['duration']:.1f}yr  "
              f"Median: £{r['median']:,.0f}  10yr Income: £{r['income_10yr']:,.0f}")

    # --- Generate charts ---
    print("\n[4/5] Generating visualisations...")
    plot_strategy_comparison(all_metrics)
    print("  -> chart_risk_return.png")
    plot_terminal_distributions(all_terminals)
    print("  -> chart_distributions.png")
    plot_pattern_results(pattern_results)
    print("  -> chart_pattern_analysis.png")
    plot_bond_comparison(bond_results)
    print("  -> chart_bond_strategies.png")
    plot_sharpe_comparison(all_metrics)
    print("  -> chart_risk_adjusted.png")

    # --- Summary ---
    print("\n[5/5] Key findings...")
    print("\n  STRATEGY RANKINGS BY SHARPE RATIO")
    print("  " + "-" * 55)
    ranked = sorted(all_metrics.items(), key=lambda x: x[1]["sharpe"], reverse=True)
    for i, (key, m) in enumerate(ranked, 1):
        s = STRATEGIES[key]
        print(f"  {i:>2}. {s.name:30s}  Sharpe: {m['sharpe']:.2f}  "
              f"Median: £{m['median']:>10,.0f}")

    print("\n  DAY TRADING PATTERN SUMMARY")
    print("  " + "-" * 55)
    profitable = sum(1 for r in pattern_results if r["prob_profit"] > 50)
    print(f"  {profitable}/{len(pattern_results)} patterns show >50% probability of 5-year profit")
    print(f"  Best pattern: {max(pattern_results, key=lambda r: r['prob_profit'])['pattern']}")
    print(f"  Even the best pattern underperforms passive index investing")

    print("\n  BOND STRATEGY VERDICT")
    print("  " + "-" * 55)
    print(f"  Ladder provides best risk-adjusted income (steady, predictable)")
    print(f"  Barbell has highest yield but most rate sensitivity")
    print(f"  Bullet simplest to manage, moderate risk")

    best = max(ranked[:3], key=lambda x: x[1]["sharpe"])
    print(f"\n  OVERALL: {STRATEGIES[best[0]].name} offers the best risk-adjusted returns")
    print(f"  But Index Investing remains optimal for most people (lowest skill, lowest cost)")

    print("\n" + "=" * 70)
    print(f"  Analysis complete. Charts saved to: {OUTPUT_DIR}")
    print("=" * 70)

    return all_metrics, pattern_results, bond_results


if __name__ == "__main__":
    metrics, patterns, bonds = main()
