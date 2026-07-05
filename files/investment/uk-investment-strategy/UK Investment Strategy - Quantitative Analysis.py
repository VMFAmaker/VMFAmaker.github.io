"""
UK Personal Investment Strategy — Quantitative Analysis
========================================================
Monte Carlo simulations, compound growth modelling, and portfolio
optimisation for the average UK investor across age brackets and
income levels. All figures in GBP unless stated otherwise.

Run:  python "UK Investment Strategy - Quantitative Analysis.py"
Deps: numpy, matplotlib, pandas (pip install numpy matplotlib pandas)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import warnings, os

warnings.filterwarnings("ignore", category=FutureWarning)
plt.style.use("seaborn-v0_8-whitegrid")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 42
np.random.seed(SEED)


# ═══════════════════════════════════════════════════════════════
# 1.  UK SALARY DATA (ONS 2025/26, median gross annual)
# ═══════════════════════════════════════════════════════════════
UK_SALARIES = pd.DataFrame({
    "age_band":     ["18-21","22-29","30-39","40-49","50-59","60+"],
    "median_gross": [21_500, 28_800, 36_200, 39_500, 37_400, 31_000],
    "take_home":    [19_100, 24_200, 28_600, 30_500, 29_100, 25_200],
})

NATIONAL_MEDIAN_GROSS = 34_963
NATIONAL_MEDIAN_NET   = 27_756


# ═══════════════════════════════════════════════════════════════
# 2.  ASSET CLASS ASSUMPTIONS (nominal, pre-tax)
# ═══════════════════════════════════════════════════════════════
@dataclass
class AssetClass:
    name: str
    expected_return: float
    volatility: float
    description: str

ASSETS = {
    "global_equity":  AssetClass("Global Equities (MSCI World)", 0.090, 0.155, "Broad developed-market stocks"),
    "uk_equity":      AssetClass("UK Equities (FTSE All-Share)",  0.075, 0.148, "UK-listed companies"),
    "uk_gilts":       AssetClass("UK Gilts",                      0.040, 0.062, "Government bonds"),
    "corporate_bond": AssetClass("Investment-Grade Corporate",    0.052, 0.075, "Corporate bonds"),
    "property":       AssetClass("UK Property (REIT proxy)",      0.065, 0.105, "Real estate exposure via REITs"),
    "cash":           AssetClass("Cash / Money Market",           0.035, 0.008, "Savings accounts, money market funds"),
}

INFLATION_RATE = 0.030
ISA_ALLOWANCE  = 20_000
PENSION_MATCH  = 0.05


# ═══════════════════════════════════════════════════════════════
# 3.  PORTFOLIO ALLOCATIONS BY LIFE STAGE
# ═══════════════════════════════════════════════════════════════
PORTFOLIOS = {
    "Aggressive (18-30)": {
        "global_equity": 0.70, "uk_equity": 0.15, "property": 0.10, "corporate_bond": 0.05,
    },
    "Growth (30-45)": {
        "global_equity": 0.50, "uk_equity": 0.15, "property": 0.10,
        "corporate_bond": 0.15, "uk_gilts": 0.10,
    },
    "Balanced (45-55)": {
        "global_equity": 0.35, "uk_equity": 0.10, "property": 0.10,
        "corporate_bond": 0.20, "uk_gilts": 0.20, "cash": 0.05,
    },
    "Conservative (55+)": {
        "global_equity": 0.20, "uk_equity": 0.05, "property": 0.05,
        "corporate_bond": 0.25, "uk_gilts": 0.35, "cash": 0.10,
    },
}

def portfolio_stats(weights: Dict[str, float]) -> Tuple[float, float]:
    ret = sum(w * ASSETS[k].expected_return for k, w in weights.items())
    vol = sum(w * ASSETS[k].volatility for k, w in weights.items())
    return ret, vol


# ═══════════════════════════════════════════════════════════════
# 4.  MONTE CARLO ENGINE
# ═══════════════════════════════════════════════════════════════
def monte_carlo(
    monthly_contribution: float,
    years: int,
    port_return: float,
    port_vol: float,
    n_sims: int = 10_000,
    contribution_growth: float = 0.02,
) -> np.ndarray:
    """Simulate portfolio growth with monthly contributions.
    Returns array of shape (n_sims,) with terminal values."""
    months = years * 12
    monthly_ret = port_return / 12
    monthly_vol = port_vol / np.sqrt(12)

    terminals = np.zeros(n_sims)
    for sim in range(n_sims):
        balance = 0.0
        contrib = monthly_contribution
        for m in range(months):
            if m > 0 and m % 12 == 0:
                contrib *= (1 + contribution_growth)
            r = np.random.normal(monthly_ret, monthly_vol)
            balance = (balance + contrib) * (1 + r)
        terminals[sim] = balance
    return terminals


def quick_compound(monthly: float, years: int, annual_rate: float) -> float:
    """Deterministic compound growth (no volatility)."""
    months = years * 12
    monthly_rate = annual_rate / 12
    total = 0.0
    for m in range(months):
        total = (total + monthly) * (1 + monthly_rate)
    return total


# ═══════════════════════════════════════════════════════════════
# 5.  DAY TRADING vs PASSIVE — PROBABILITY MODEL
# ═══════════════════════════════════════════════════════════════
def day_trading_simulation(
    starting_capital: float = 5_000,
    daily_trades: int = 3,
    win_rate: float = 0.48,
    avg_win: float = 0.012,
    avg_loss: float = 0.010,
    trading_days: int = 252,
    years: int = 5,
    n_sims: int = 10_000,
    commission_per_trade: float = 2.0,
    spread_cost: float = 0.0005,
) -> np.ndarray:
    """Simulate retail day trading outcomes."""
    total_days = trading_days * years
    terminals = np.zeros(n_sims)

    for sim in range(n_sims):
        capital = starting_capital
        for day in range(total_days):
            for trade in range(daily_trades):
                if capital <= 100:
                    break
                if np.random.random() < win_rate:
                    pnl = capital * avg_win
                else:
                    pnl = -capital * avg_loss
                capital += pnl - commission_per_trade - (capital * spread_cost)
            if capital <= 100:
                break
        terminals[sim] = max(capital, 0)
    return terminals


# ═══════════════════════════════════════════════════════════════
# 6.  SCENARIO ANALYSIS (Bull / Base / Bear)
# ═══════════════════════════════════════════════════════════════
@dataclass
class MarketScenario:
    name: str
    probability: float
    equity_return_adj: float
    bond_return_adj: float
    description: str

SCENARIOS = [
    MarketScenario("Bull",  0.25,  0.030, 0.005, "Strong growth, low inflation, AI productivity boom"),
    MarketScenario("Base",  0.55,  0.000, 0.000, "Moderate growth, normalising rates, steady earnings"),
    MarketScenario("Bear",  0.20, -0.035,-0.010, "Recession, rate cuts, earnings compression"),
]


# ═══════════════════════════════════════════════════════════════
# 7.  ANALYSIS FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def analyse_starting_age():
    """How starting age affects terminal wealth (same monthly amount)."""
    monthly = 200
    target_age = 65
    results = {}

    for start_age in [18, 25, 30, 35, 40, 50]:
        years = target_age - start_age
        if years <= 0:
            continue
        port_name = (
            "Aggressive (18-30)" if start_age < 30
            else "Growth (30-45)" if start_age < 45
            else "Balanced (45-55)" if start_age < 55
            else "Conservative (55+)"
        )
        ret, vol = portfolio_stats(PORTFOLIOS[port_name])
        terminals = monte_carlo(monthly, years, ret, vol, n_sims=5_000)
        results[start_age] = {
            "years": years,
            "total_contributed": monthly * 12 * years,
            "median": np.median(terminals),
            "p25": np.percentile(terminals, 25),
            "p75": np.percentile(terminals, 75),
            "p10": np.percentile(terminals, 10),
            "p90": np.percentile(terminals, 90),
        }
    return results


def analyse_savings_rates():
    """Optimal savings rate by income bracket."""
    results = []
    for _, row in UK_SALARIES.iterrows():
        net_monthly = row["take_home"] / 12
        for rate in [0.05, 0.10, 0.15, 0.20, 0.25]:
            saving = net_monthly * rate
            remaining = net_monthly - saving
            terminal_30y = quick_compound(saving, 30, 0.075)
            results.append({
                "age_band": row["age_band"],
                "gross": row["median_gross"],
                "net_monthly": round(net_monthly),
                "savings_rate": rate,
                "monthly_saving": round(saving),
                "monthly_remaining": round(remaining),
                "terminal_30y": round(terminal_30y),
            })
    return pd.DataFrame(results)


def compare_strategies():
    """Compare passive index investing vs day trading over 5 years."""
    capital = 10_000
    monthly_addition = 200

    passive_ret, passive_vol = portfolio_stats(PORTFOLIOS["Growth (30-45)"])
    passive_terminals = monte_carlo(monthly_addition, 5, passive_ret, passive_vol, n_sims=10_000)
    passive_terminals += capital * (1 + passive_ret) ** 5

    day_trade_terminals = day_trading_simulation(
        starting_capital=capital + (monthly_addition * 60),
        years=5, n_sims=10_000
    )

    return passive_terminals, day_trade_terminals


# ═══════════════════════════════════════════════════════════════
# 8.  VISUALISATION
# ═══════════════════════════════════════════════════════════════
def plot_starting_age(results: dict):
    fig, ax = plt.subplots(figsize=(12, 7))
    ages = sorted(results.keys())
    medians = [results[a]["median"] for a in ages]
    contribs = [results[a]["total_contributed"] for a in ages]
    p25 = [results[a]["p25"] for a in ages]
    p75 = [results[a]["p75"] for a in ages]

    x = np.arange(len(ages))
    w = 0.35
    bars1 = ax.bar(x - w/2, [m/1000 for m in medians], w, label="Median Portfolio Value", color="#2E75B6")
    bars2 = ax.bar(x + w/2, [c/1000 for c in contribs], w, label="Total Contributed", color="#BDD7EE")

    ax.errorbar(x - w/2, [m/1000 for m in medians],
                yerr=[[((m - p)/1000) for m, p in zip(medians, p25)],
                      [((p - m)/1000) for m, p in zip(medians, p75)]],
                fmt="none", color="#1B3A5C", capsize=4)

    ax.set_xlabel("Starting Age", fontsize=12)
    ax.set_ylabel("Value at Age 65 (£ thousands)", fontsize=12)
    ax.set_title("The Power of Starting Young — £200/month to Age 65", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Age {a}" for a in ages])
    ax.legend(fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))

    for bar, med in zip(bars1, medians):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f"£{med/1000:,.0f}k", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_starting_age.png"), dpi=150)
    plt.close()


def plot_strategy_comparison(passive, day_trade):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax1 = axes[0]
    ax1.hist(passive / 1000, bins=60, alpha=0.7, color="#2E75B6", label="Passive Index")
    ax1.hist(day_trade / 1000, bins=60, alpha=0.7, color="#E74C3C", label="Day Trading")
    ax1.set_xlabel("Terminal Value (£ thousands)")
    ax1.set_ylabel("Frequency")
    ax1.set_title("5-Year Outcome Distribution (£10k start + £200/mo)")
    ax1.legend()
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))

    ax2 = axes[1]
    categories = ["Lost Money", "Below Inflation", "Beat Inflation", "Doubled+"]
    total_invested = 10_000 + 200 * 60
    inflation_adj = total_invested * (1.03 ** 5)

    passive_pcts = [
        np.mean(passive < total_invested) * 100,
        np.mean((passive >= total_invested) & (passive < inflation_adj)) * 100,
        np.mean((passive >= inflation_adj) & (passive < total_invested * 2)) * 100,
        np.mean(passive >= total_invested * 2) * 100,
    ]
    dt_pcts = [
        np.mean(day_trade < total_invested) * 100,
        np.mean((day_trade >= total_invested) & (day_trade < inflation_adj)) * 100,
        np.mean((day_trade >= inflation_adj) & (day_trade < total_invested * 2)) * 100,
        np.mean(day_trade >= total_invested * 2) * 100,
    ]

    x = np.arange(len(categories))
    w = 0.35
    ax2.bar(x - w/2, passive_pcts, w, label="Passive Index", color="#2E75B6")
    ax2.bar(x + w/2, dt_pcts, w, label="Day Trading", color="#E74C3C")
    ax2.set_ylabel("% of Simulations")
    ax2.set_title("Probability of Outcomes — Passive vs Day Trading")
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, fontsize=9)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_strategy_comparison.png"), dpi=150)
    plt.close()


def plot_savings_rate_impact(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 7))
    age_bands = df["age_band"].unique()
    colours = ["#2E75B6", "#27AE60", "#F39C12", "#E74C3C", "#9B59B6", "#1ABC9C"]

    for i, band in enumerate(age_bands):
        subset = df[df["age_band"] == band]
        ax.plot(
            [f"{int(r*100)}%" for r in subset["savings_rate"]],
            subset["terminal_30y"] / 1000,
            marker="o", linewidth=2, color=colours[i], label=f"{band} (£{subset.iloc[0]['gross']:,})"
        )

    ax.set_xlabel("Savings Rate (% of take-home pay)", fontsize=12)
    ax.set_ylabel("Portfolio Value After 30 Years (£ thousands)", fontsize=12)
    ax.set_title("Terminal Wealth by Savings Rate and Income Bracket", fontsize=14, fontweight="bold")
    ax.legend(title="Age Band (Median Gross)", fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_savings_rate.png"), dpi=150)
    plt.close()


def plot_scenario_analysis():
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly = 300
    years = 20

    for scenario in SCENARIOS:
        base_ret, base_vol = portfolio_stats(PORTFOLIOS["Growth (30-45)"])
        adj_ret = base_ret + scenario.equity_return_adj * 0.65 + scenario.bond_return_adj * 0.25
        adj_vol = base_vol * (1.3 if scenario.name == "Bear" else 0.85 if scenario.name == "Bull" else 1.0)

        terminals = monte_carlo(monthly, years, adj_ret, adj_vol, n_sims=5_000)
        colour = "#27AE60" if scenario.name == "Bull" else "#E74C3C" if scenario.name == "Bear" else "#2E75B6"
        ax.hist(terminals / 1000, bins=50, alpha=0.5, color=colour,
                label=f"{scenario.name} ({int(scenario.probability*100)}%) — Median: £{np.median(terminals)/1000:,.0f}k")

    ax.set_xlabel("Portfolio Value After 20 Years (£ thousands)")
    ax.set_ylabel("Frequency")
    ax.set_title("Market Scenario Impact — £300/month for 20 Years", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"£{v:,.0f}k"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_scenario_analysis.png"), dpi=150)
    plt.close()


def plot_allocation_glide():
    fig, ax = plt.subplots(figsize=(12, 6))
    ages = list(range(18, 70))
    categories = ["Equities", "Property", "Corp Bonds", "Gilts", "Cash"]
    cat_colours = ["#2E75B6", "#F39C12", "#27AE60", "#9B59B6", "#BDC3C7"]

    data = {c: [] for c in categories}
    for age in ages:
        if age < 30:
            w = PORTFOLIOS["Aggressive (18-30)"]
        elif age < 45:
            w = PORTFOLIOS["Growth (30-45)"]
        elif age < 55:
            w = PORTFOLIOS["Balanced (45-55)"]
        else:
            w = PORTFOLIOS["Conservative (55+)"]

        data["Equities"].append((w.get("global_equity", 0) + w.get("uk_equity", 0)) * 100)
        data["Property"].append(w.get("property", 0) * 100)
        data["Corp Bonds"].append(w.get("corporate_bond", 0) * 100)
        data["Gilts"].append(w.get("uk_gilts", 0) * 100)
        data["Cash"].append(w.get("cash", 0) * 100)

    ax.stackplot(ages, [data[c] for c in categories], labels=categories, colors=cat_colours, alpha=0.85)
    ax.set_xlabel("Age", fontsize=12)
    ax.set_ylabel("Portfolio Allocation (%)", fontsize=12)
    ax.set_title("Recommended Asset Allocation Glide Path by Age", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.set_xlim(18, 69)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "chart_allocation_glide.png"), dpi=150)
    plt.close()


# ═══════════════════════════════════════════════════════════════
# 9.  MAIN — RUN ALL ANALYSES
# ═══════════════════════════════════════════════════════════════
def main():
    print("=" * 65)
    print("  UK Personal Investment Strategy — Quantitative Analysis")
    print("=" * 65)

    # --- Starting age analysis ---
    print("\n[1/6] Analysing impact of starting age...")
    age_results = analyse_starting_age()
    print(f"      {'Start':>5}  {'Years':>5}  {'Contributed':>12}  {'Median':>12}  {'Growth':>8}")
    for age, r in sorted(age_results.items()):
        growth = r["median"] / r["total_contributed"]
        print(f"      {age:>5}  {r['years']:>5}  £{r['total_contributed']:>10,}  £{r['median']:>10,.0f}  {growth:>7.1f}x")
    plot_starting_age(age_results)
    print("      -> chart_starting_age.png saved")

    # --- Savings rate analysis ---
    print("\n[2/6] Modelling optimal savings rates...")
    savings_df = analyse_savings_rates()
    print(savings_df[savings_df["savings_rate"].isin([0.10, 0.20])].to_string(index=False))
    plot_savings_rate_impact(savings_df)
    print("      -> chart_savings_rate.png saved")

    # --- Strategy comparison ---
    print("\n[3/6] Simulating passive vs day trading (10,000 paths each)...")
    passive, day_trade = compare_strategies()
    total_invested = 10_000 + 200 * 60
    print(f"      Passive Index — Median: £{np.median(passive):,.0f}, "
          f"Prob of loss: {np.mean(passive < total_invested)*100:.1f}%")
    print(f"      Day Trading  — Median: £{np.median(day_trade):,.0f}, "
          f"Prob of loss: {np.mean(day_trade < total_invested)*100:.1f}%")
    plot_strategy_comparison(passive, day_trade)
    print("      -> chart_strategy_comparison.png saved")

    # --- Market scenarios ---
    print("\n[4/6] Running market scenario analysis...")
    for s in SCENARIOS:
        ret, _ = portfolio_stats(PORTFOLIOS["Growth (30-45)"])
        adj = ret + s.equity_return_adj * 0.65
        print(f"      {s.name:>4} ({int(s.probability*100):>2}%) — Adj return: {adj*100:.1f}%, {s.description}")
    plot_scenario_analysis()
    print("      -> chart_scenario_analysis.png saved")

    # --- Allocation glide path ---
    print("\n[5/6] Generating allocation glide path...")
    plot_allocation_glide()
    print("      -> chart_allocation_glide.png saved")

    # --- Summary statistics ---
    print("\n[6/6] Computing summary statistics...")
    print("\n  KEY FINDINGS")
    print("  " + "-" * 50)

    age_18 = age_results[18]["median"]
    age_35 = age_results[35]["median"]
    print(f"  Starting at 18 vs 35 (£200/mo): £{age_18:,.0f} vs £{age_35:,.0f}")
    print(f"  That is {age_18/age_35:.1f}x more wealth from starting 17 years earlier")

    print(f"\n  Day trading probability of losing money: {np.mean(day_trade < total_invested)*100:.0f}%")
    print(f"  Passive investing probability of losing:  {np.mean(passive < total_invested)*100:.0f}%")

    for _, row in UK_SALARIES.iterrows():
        net_m = row["take_home"] / 12
        saving_10 = net_m * 0.10
        terminal = quick_compound(saving_10, 30, 0.075)
        print(f"\n  {row['age_band']:>5} earner (£{row['median_gross']:,}) saving 10% = "
              f"£{saving_10:,.0f}/mo -> £{terminal:,.0f} in 30 years")

    print("\n" + "=" * 65)
    print("  Analysis complete. Charts saved to:", OUTPUT_DIR)
    print("=" * 65)

    return {
        "age_results": age_results,
        "savings_df": savings_df,
        "passive_terminals": passive,
        "day_trade_terminals": day_trade,
    }


if __name__ == "__main__":
    results = main()
