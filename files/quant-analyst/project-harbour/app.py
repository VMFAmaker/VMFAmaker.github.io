"""
Project Harbour dashboard.

    streamlit run app.py

Move the sliders in the sidebar and every chart updates. Hover over any chart
to read the exact percentile values. All money is in today's money.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from retirement_sim import scenarios as sc
from retirement_sim.config import (HealthConfig, MarketConfig, PortfolioConfig, RunConfig, ScenarioConfig,
                                   TaxConfig, WithdrawalConfig, DEFAULT_REGIMES, SEQUENCING_RULES,
                                   shifted_regimes)
from retirement_sim.market import unconditional_moments
from retirement_sim.metrics import percentile_paths, solvency_curve, summarise

st.set_page_config(page_title="Project Harbour", layout="wide")

BLUE, RED, GREEN, AMBER, GREY, TEAL = "#2563EB", "#DC2626", "#16A34A", "#F59E0B", "#94A3B8", "#14B8A6"
STRATEGY_LABELS = {"static": "Static (fixed real amount)", "guardrails": "Guardrails (cut and raise)", "vpw": "Variable percentage (VPW)"}
SEQUENCING_LABELS = {
    "taxable_first": "Taxable first", "traditional_first": "Traditional first",
    "bracket_fill": "Fill low brackets", "proportional": "Pro rata",
}
LOWER_RETURNS = {"equity_shift": -0.015, "bond_shift": -0.0075}


# ── Sidebar ─────────────────────────────────────────────────

def sidebar_inputs() -> tuple[ScenarioConfig, RunConfig]:
    st.sidebar.header("You")
    retire = st.sidebar.slider("Retirement age", 50, 75, 65)
    end = st.sidebar.slider("Plan until age", 85, 100, 95)
    total = st.sidebar.number_input("Starting portfolio", 100_000, 10_000_000, 1_000_000, step=50_000)
    spending = st.sidebar.number_input("Yearly spending after tax", 10_000, 500_000, 40_000, step=1_000)
    equity = st.sidebar.slider("Share in stocks", 0, 100, 60, step=5) / 100

    st.sidebar.header("Accounts")
    taxable_pct = st.sidebar.slider("Taxable %", 0, 100, 30, step=5)
    trad_pct = st.sidebar.slider("Traditional (pre-tax) %", 0, 100 - taxable_pct, min(50, 100 - taxable_pct), step=5)
    roth_pct = 100 - taxable_pct - trad_pct
    st.sidebar.caption(f"Roth (tax free) {roth_pct}%")

    st.sidebar.header("Market")
    model = st.sidebar.radio("Return model", ["Regime switching", "Normal (textbook)"])
    returns = st.sidebar.radio("Return assumptions", ["Long-run history", "Lower (forward looking)"])
    bear_start = st.sidebar.checkbox("Bear market in year one", value=False)

    st.sidebar.header("Health shocks")
    health_on = st.sidebar.checkbox("Include health shocks", value=True)
    care_cost = st.sidebar.slider("Long-term care cost per year", 0, 150_000, 60_000, step=5_000)
    care_odds = st.sidebar.slider("Chance of care (1.0 = default)", 0.5, 2.0, 1.0, step=0.25)

    st.sidebar.header("Withdrawal rule")
    strategy = st.sidebar.selectbox("Rule", list(STRATEGY_LABELS), format_func=STRATEGY_LABELS.get)
    guard = {}
    if strategy == "guardrails":
        guard = {
            "guard_cut": st.sidebar.slider("Cut spending by", 0.05, 0.25, 0.10, step=0.05, format="%.2f"),
            "guard_raise": st.sidebar.slider("Raise spending by", 0.0, 0.25, 0.10, step=0.05, format="%.2f"),
            "guard_band": st.sidebar.slider("Trigger when withdrawal rate drifts by", 0.10, 0.40, 0.20, step=0.05, format="%.2f"),
        }
    if strategy == "vpw":
        guard = {"vpw_return": st.sidebar.slider("Real return assumed by VPW", 0.0, 0.05, 0.025, step=0.005, format="%.3f")}

    st.sidebar.header("Tax")
    tax_on = st.sidebar.checkbox("Include tax", value=True)
    sequencing = st.sidebar.selectbox("Withdrawal order", SEQUENCING_RULES, index=2, format_func=SEQUENCING_LABELS.get)

    st.sidebar.header("Simulation")
    sims = st.sidebar.select_slider("Paths", [2_000, 5_000, 10_000, 20_000], value=5_000)
    seed = st.sidebar.number_input("Random seed", 0, 9_999, 42)

    regimes = DEFAULT_REGIMES if returns == "Long-run history" else shifted_regimes(DEFAULT_REGIMES, **LOWER_RETURNS)
    base_health = HealthConfig()
    cfg = ScenarioConfig(
        name="Your scenario",
        portfolio=PortfolioConfig(
            retirement_age=retire, end_age=max(end, retire + 5), equity_weight=equity,
            taxable=total * taxable_pct / 100, traditional=total * trad_pct / 100, roth=total * roth_pct / 100,
        ),
        market=MarketConfig(
            model="regime" if model.startswith("Regime") else "normal", regimes=regimes,
            forced_start_regime="Bear" if bear_start else None, forced_start_years=1 if bear_start else 0,
        ),
        health=HealthConfig(
            enabled=health_on, ltc_annual_cost=care_cost,
            ltc_hazard_at_start=base_health.ltc_hazard_at_start * care_odds,
            ltc_hazard_at_95=base_health.ltc_hazard_at_95 * care_odds,
        ),
        tax=TaxConfig(enabled=tax_on, sequencing=sequencing),
        withdrawal=WithdrawalConfig(strategy=strategy, spending=spending, **guard),
    )
    return cfg, RunConfig(n_sims=sims, seed=int(seed))


# ── Cached simulation ───────────────────────────────────────

@st.cache_data(show_spinner="Simulating paths")
def simulate_one(cfg: ScenarioConfig, run: RunConfig) -> dict:
    result = sc.run_scenarios([cfg], run)[cfg.name]
    spend = result.spending / cfg.withdrawal.spending
    return {
        "summary": summarise(result),
        "paths": percentile_paths(result),
        "solvency": solvency_curve(result),
        "ages": result.ages,
        "ending": result.balance[:, -1],
        "spending": pd.DataFrame({
            "age": result.ages[:-1],
            **{f"p{p}": np.percentile(spend, p, axis=0) for p in (10, 25, 50, 75, 90)},
        }),
    }


@st.cache_data(show_spinner="Comparing scenarios")
def simulate_many(configs: tuple, run: RunConfig) -> pd.DataFrame:
    results = sc.run_scenarios(list(configs), run)
    return pd.DataFrame([summarise(r) for r in results.values()])


# ── Charts ──────────────────────────────────────────────────

def money(v: float) -> str:
    return f"${v:,.0f}"


def fan_figure(paths: pd.DataFrame, start: float) -> go.Figure:
    fig = go.Figure()
    bands = [(5, 95, 0.12), (10, 90, 0.18), (25, 75, 0.30)]
    for low, high, alpha in bands:
        fig.add_trace(go.Scatter(x=paths["age"], y=paths[f"balance_p{low}"], name=f"{low}th percentile",
                                 line=dict(width=0), hovertemplate="%{y:$,.0f}"))
        fig.add_trace(go.Scatter(x=paths["age"], y=paths[f"balance_p{high}"], name=f"{high}th percentile",
                                 line=dict(width=0), fill="tonexty", fillcolor=f"rgba(37,99,235,{alpha})",
                                 hovertemplate="%{y:$,.0f}"))
    fig.add_trace(go.Scatter(x=paths["age"], y=paths["balance_p50"], name="Median",
                             line=dict(color=TEAL, width=3), hovertemplate="%{y:$,.0f}"))
    fig.add_hline(y=start, line_dash="dash", line_color=AMBER, annotation_text="Starting value")
    fig.update_layout(hovermode="x unified", height=480, margin=dict(l=10, r=10, t=30, b=10),
                      xaxis_title="Age", yaxis_title="Portfolio value (today's money)", yaxis_tickprefix="$",
                      yaxis_range=[0, float(paths["balance_p90"].max()) * 1.05])
    return fig


def percentile_curve(ending: np.ndarray, start: float) -> go.Figure:
    pct = np.arange(1, 100)
    values = np.percentile(ending, pct)
    fig = go.Figure(go.Scatter(x=pct, y=values, mode="lines", line=dict(color=BLUE, width=3),
                               hovertemplate="%{x}% of paths end below %{y:$,.0f}<extra></extra>"))
    fig.add_hline(y=start, line_dash="dash", line_color=AMBER, annotation_text="Starting value")
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="Percentile of paths",
                      yaxis_title="Ending wealth", yaxis_tickprefix="$", hovermode="x")
    return fig


def solvency_figure(ages: np.ndarray, solvency: np.ndarray) -> go.Figure:
    fig = go.Figure(go.Scatter(x=ages, y=solvency, mode="lines", line=dict(color=GREEN, width=3),
                               hovertemplate="Age %{x}. Still solvent in %{y:.1%} of paths<extra></extra>"))
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="Age",
                      yaxis_title="Share of paths still solvent", yaxis_tickformat=".0%", yaxis_range=[0, 1.02])
    return fig


def spending_figure(table: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for low, high, alpha in [(10, 90, 0.15), (25, 75, 0.30)]:
        fig.add_trace(go.Scatter(x=table["age"], y=table[f"p{low}"], name=f"{low}th percentile", line=dict(width=0),
                                 hovertemplate="%{y:.0%}"))
        fig.add_trace(go.Scatter(x=table["age"], y=table[f"p{high}"], name=f"{high}th percentile", line=dict(width=0),
                                 fill="tonexty", fillcolor=f"rgba(22,163,74,{alpha})", hovertemplate="%{y:.0%}"))
    fig.add_trace(go.Scatter(x=table["age"], y=table["p50"], name="Median", line=dict(color=TEAL, width=3),
                             hovertemplate="%{y:.0%}"))
    fig.add_hline(y=1.0, line_dash="dash", line_color=AMBER, annotation_text="Target")
    fig.update_layout(hovermode="x unified", height=420, margin=dict(l=10, r=10, t=30, b=10),
                      xaxis_title="Age", yaxis_title="Spending as a share of target", yaxis_tickformat=".0%")
    return fig


def comparison_bars(table: pd.DataFrame, label_col: str) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(x=table[label_col], y=table["prob_ruin"], name="Chance the money runs out", marker_color=RED,
                hovertemplate="%{y:.1%}")
    fig.add_bar(x=table[label_col], y=table["prob_spending_below_80pct"], name="Chance spending is cut below 80%",
                marker_color=AMBER, hovertemplate="%{y:.1%}")
    fig.update_layout(barmode="group", height=380, margin=dict(l=10, r=10, t=30, b=10), yaxis_tickformat=".0%")
    return fig


def comparison_table(table: pd.DataFrame, label_col: str) -> pd.DataFrame:
    view = table[[label_col, "prob_ruin", "expected_ending_wealth", "ending_p50", "prob_spending_below_80pct",
                  "median_lifetime_tax"]].copy()
    view.columns = ["Scenario", "Chance of ruin", "Expected ending wealth", "Median ending wealth",
                    "Chance spending below 80%", "Median lifetime tax"]
    return view.style.format({
        "Chance of ruin": "{:.1%}", "Chance spending below 80%": "{:.1%}",
        "Expected ending wealth": "${:,.0f}", "Median ending wealth": "${:,.0f}", "Median lifetime tax": "${:,.0f}",
    })


# ── Page ────────────────────────────────────────────────────

def main() -> None:
    st.title("Project Harbour")
    st.caption("Retirement drawdown risk. Every number is in today's money. Hover over any chart for exact values.")

    cfg, run = sidebar_inputs()
    out = simulate_one(cfg, run)
    s = out["summary"]
    start = cfg.portfolio.total

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Chance the money runs out", f"{s['prob_ruin']:.1%}")
    k2.metric("Chance of ending below the start", f"{s['prob_real_capital_loss']:.1%}")
    k3.metric("Expected ending wealth", money(s["expected_ending_wealth"]))
    k4.metric("Median ending wealth", money(s["ending_p50"]))
    k5.metric("Chance the pot halves at some point", f"{s['prob_balance_halved']:.1%}")

    tabs = st.tabs(["Fan chart", "Probability curves", "Spending", "Compare rules", "Tax order", "Assumptions"])

    with tabs[0]:
        st.plotly_chart(fan_figure(out["paths"], start), width="stretch")
        st.caption("Bands show where 50%, 80% and 90% of paths sit at each age. Paths that run out of money stay at zero.")

    with tabs[1]:
        left, right = st.columns(2)
        left.subheader("Is the money still there?")
        left.plotly_chart(solvency_figure(out["ages"], out["solvency"]), width="stretch")
        right.subheader("Ending wealth by percentile")
        right.plotly_chart(percentile_curve(out["ending"], start), width="stretch")

    with tabs[2]:
        st.plotly_chart(spending_figure(out["spending"]), width="stretch")
        st.caption("Spending actually enjoyed, as a share of your target. Static spending only falls if the money runs out.")

    with tabs[3]:
        if st.toggle("Compare all three withdrawal rules on the same market paths"):
            configs = tuple(sc.tweak(cfg, STRATEGY_LABELS[k].split(" (")[0], withdrawal={"strategy": k})
                            for k in STRATEGY_LABELS)
            table = simulate_many(configs, run)
            st.plotly_chart(comparison_bars(table, "scenario"), width="stretch")
            st.dataframe(comparison_table(table, "scenario"), hide_index=True, width="stretch")
            st.caption("VPW spends the pot down by design, so look at spending and not at ending wealth.")

    with tabs[4]:
        if st.toggle("Compare withdrawal orders and a no-tax control"):
            configs = (sc.tweak(cfg, "No tax (control)", tax={"enabled": False}),) + tuple(
                sc.tweak(cfg, SEQUENCING_LABELS[r], tax={"enabled": True, "sequencing": r}) for r in SEQUENCING_RULES)
            table = simulate_many(configs, run)
            st.dataframe(comparison_table(table, "scenario"), hide_index=True, width="stretch")
            st.caption("Differences between orders are small compared with the spending rule and the market. See the summary note.")

    with tabs[5]:
        moments = unconditional_moments(cfg.market)
        regime_table = pd.DataFrame({
            "Regime": ["Expansion", "Bear", "Stagflation"],
            "Share of years": moments["regime_share"],
            "Stocks, mean real return": [r.equity_mean for r in cfg.market.regimes],
            "Stocks, volatility": [r.equity_vol for r in cfg.market.regimes],
            "Bonds, mean real return": [r.bond_mean for r in cfg.market.regimes],
            "Stock and bond correlation": [r.correlation for r in cfg.market.regimes],
        })
        st.dataframe(regime_table.style.format({c: "{:.1%}" for c in regime_table.columns[1:5]} | {"Stock and bond correlation": "{:.2f}"}),
                     hide_index=True, width="stretch")
        st.write(f"Long-run mix. Stocks {moments['equity_mean']:.1%} a year with {moments['equity_vol']:.1%} volatility. "
                 f"Bonds {moments['bond_mean']:.1%} a year with {moments['bond_vol']:.1%} volatility.")
        st.write("These are assumptions, not forecasts. The tax schedule is a US single filer. The plan runs to a fixed age, "
                 "with no early death. Edit retirement_sim/config.py to change any of it.")


main()
