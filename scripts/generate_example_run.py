"""
generate_example_run.py — Produce example_run outputs for the README.

Runs: baseline + high_load + stress_test + intervention
Saves to: data/example_run/
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root on path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import pandas as pd

from src.experiments.runner import ScenarioRunner
from src.viz.plots import save_all_plots

EXAMPLE_SCENARIOS = ["baseline", "high_load", "slow_feedback", "intervention"]


def main() -> None:
    output_root = root / "data" / "example_run"
    print(f"Generating example run → {output_root}")

    runner = ScenarioRunner(output_root=str(output_root))
    # Override the timestamped folder — write directly into example_run/
    runner._run_dir = output_root
    output_root.mkdir(parents=True, exist_ok=True)

    results = []
    for name in EXAMPLE_SCENARIOS:
        print(f"  Scenario: {name}")
        res = runner.run_scenario(name, save=True)
        results.append(res)
        summ = res["summary"]
        print(f"    GPA={summ['mean_gpa']:.3f}  fail={summ['failure_rate']:.1%}  stress={summ['mean_final_stress']:.3f}")

    # Comparison CSV
    comp_rows = [r["summary"] for r in results]
    comp_df = pd.DataFrame(comp_rows)
    runner.save_comparison(results)

    # Plots
    plots_dir = output_root / "plots"
    save_all_plots(results, plots_dir, comparison_df=comp_df)

    print(f"\nDone!  Example outputs in: {output_root}")


if __name__ == "__main__":
    main()
