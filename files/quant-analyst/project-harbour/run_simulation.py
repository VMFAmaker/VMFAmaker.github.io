"""
Run the full Project Harbour simulation.

    python run_simulation.py                  20,000 paths per scenario
    python run_simulation.py --sims 50000     more paths, slower, smoother
    python run_simulation.py --seed 7         a different random draw

Writes CSV files and charts to the outputs folder.
Edit retirement_sim/config.py to change any assumption.
"""

import argparse
import time
from pathlib import Path

import pandas as pd

from retirement_sim import charts
from retirement_sim import scenarios as sc
from retirement_sim.config import RunConfig, ScenarioConfig
from retirement_sim.market import unconditional_moments
from retirement_sim.metrics import best_mix_table, percentile_paths, sequence_risk_table, summarise

OUTPUT_DIR = Path(__file__).parent / "outputs"


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sims", type=int, default=RunConfig.n_sims, help="paths per scenario")
    parser.add_argument("--seed", type=int, default=RunConfig.seed, help="random seed")
    args = parser.parse_args()
    return RunConfig(n_sims=args.sims, seed=args.seed)


def calibration_table(base: ScenarioConfig) -> pd.DataFrame:
    """Regime assumptions and the long-run numbers they imply."""
    market = base.market
    moments = unconditional_moments(market)
    rows = [{
        "item": name, "share_of_years": share,
        "equity_mean": r.equity_mean, "equity_vol": r.equity_vol,
        "bond_mean": r.bond_mean, "bond_vol": r.bond_vol, "stock_bond_correlation": r.correlation,
    } for name, share, r in zip(("Expansion", "Bear", "Stagflation"), moments["regime_share"], market.regimes)]
    rows.append({
        "item": "Long-run mix", "share_of_years": 1.0,
        "equity_mean": moments["equity_mean"], "equity_vol": moments["equity_vol"],
        "bond_mean": moments["bond_mean"], "bond_vol": moments["bond_vol"],
        "stock_bond_correlation": moments["correlation"],
    })
    return pd.DataFrame(rows)


def main() -> None:
    run = parse_args()
    base = ScenarioConfig()
    OUTPUT_DIR.mkdir(exist_ok=True)
    started = time.time()

    sets = {
        "stress_ladder": sc.stress_ladder(base),
        "strategies": sc.strategy_comparison(base),
        "sequencing": sc.sequencing_comparison(base),
        "allocation": sc.allocation_sweep(base),
    }

    summaries, paths, results = [], [], {}
    for set_name, configs in sets.items():
        print(f"Running {set_name} ({len(configs)} scenarios, {run.n_sims:,} paths each)")
        set_results = sc.run_scenarios(configs, run)
        results[set_name] = set_results
        for result in set_results.values():
            summaries.append({"set": set_name, **summarise(result)})
            paths.append(percentile_paths(result))

    print("Running robustness sweep (5 variants, 2 rules, 11 weights)")
    cases = sc.robustness_sweep(base)
    sweep_results = sc.run_scenarios([case[3] for case in cases], run)
    robustness = pd.DataFrame([
        {"variant": variant, "strategy": strategy, "equity_weight": weight,
         "prob_ruin": summarise(sweep_results[cfg.name])["prob_ruin"]}
        for variant, strategy, weight, cfg in cases
    ])
    robustness.to_csv(OUTPUT_DIR / "robustness_sweep.csv", index=False)
    best_mix_table(robustness).to_csv(OUTPUT_DIR / "robustness_best_mix.csv", index=False)

    summary = pd.DataFrame(summaries)
    summary.to_csv(OUTPUT_DIR / "summary_metrics.csv", index=False)
    pd.concat(paths).to_csv(OUTPUT_DIR / "percentile_paths.csv", index=False)
    summary[summary["set"] == "allocation"].to_csv(OUTPUT_DIR / "allocation_sweep.csv", index=False)
    calibration_table(base).to_csv(OUTPUT_DIR / "market_calibration.csv", index=False)

    reference = results["stress_ladder"]["3. Regimes + health shocks"]
    sequence = sequence_risk_table(reference)
    sequence.to_csv(OUTPUT_DIR / "sequence_risk.csv", index=False)

    ladder = list(results["stress_ladder"].values())
    charts.save(charts.fan_chart(reference), "01_fan_chart", OUTPUT_DIR)
    charts.save(charts.ending_distribution(reference), "02_ending_wealth_distribution", OUTPUT_DIR)
    charts.save(charts.solvency_ladder(ladder), "03_solvency_by_stress_level", OUTPUT_DIR)
    charts.save(charts.strategy_chart(summary[summary["set"] == "strategies"]), "04_withdrawal_strategies", OUTPUT_DIR)
    charts.save(charts.sequencing_chart(summary[summary["set"] == "sequencing"]), "05_tax_sequencing", OUTPUT_DIR)
    charts.save(charts.allocation_chart(summary[summary["set"] == "allocation"]), "06_allocation_sweep", OUTPUT_DIR)
    charts.save(charts.sequence_risk_chart(sequence), "07_sequence_risk", OUTPUT_DIR)

    print(f"Done in {time.time() - started:.0f} seconds. Files are in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
