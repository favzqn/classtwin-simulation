"""
runner.py — Batch scenario runner with timestamped output directories.

Usage (CLI)::

    python -m src.experiments.runner                 # run all scenarios
    python -m src.experiments.runner baseline high_load   # specific scenarios
    python -m src.experiments.runner --output data/my_run

Usage (Python API)::

    from src.experiments.runner import ScenarioRunner
    runner = ScenarioRunner(output_root="data")
    results = runner.run_all()
    runner.save_comparison(results)
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from ..config import SimulationConfig
from ..model.classroom_model import ClassroomModel
from .scenarios import SCENARIOS, SCENARIO_LABELS, get_scenario


class ScenarioRunner:
    """
    Run one or more named scenarios, save results, and produce a
    comparison summary CSV.

    Parameters
    ----------
    output_root : str | Path
        Parent directory for all run outputs.  Each run gets a
        timestamped sub-folder.
    """

    def __init__(self, output_root: str | Path = "data") -> None:
        self.output_root = Path(output_root)
        self._run_dir: Optional[Path] = None

    # ------------------------------------------------------------------
    # Single scenario
    # ------------------------------------------------------------------

    def run_scenario(
        self,
        name: str,
        cfg: Optional[SimulationConfig] = None,
        save: bool = True,
    ) -> Dict:
        """
        Run one scenario by name (or pass an explicit config).

        Returns
        -------
        dict with keys: name, summary, student_df, weekly_df, run_dir
        """
        if cfg is None:
            cfg = get_scenario(name)

        model = ClassroomModel(cfg)
        t0 = time.perf_counter()
        model.run()
        elapsed = time.perf_counter() - t0

        summ = model.summary()
        summ["scenario"] = name
        summ["label"] = SCENARIO_LABELS.get(name, name)
        summ["run_time_s"] = round(elapsed, 3)

        result = {
            "name": name,
            "label": SCENARIO_LABELS.get(name, name),
            "config": cfg,
            "summary": summ,
            "student_df": model.student_dataframe(),
            "weekly_df": model.weekly_dataframe(),
            "model": model,
        }

        if save and self._run_dir is not None:
            scenario_dir = self._run_dir / name
            model.save(scenario_dir)
            result["run_dir"] = scenario_dir
        else:
            result["run_dir"] = None

        return result

    # ------------------------------------------------------------------
    # Batch runs
    # ------------------------------------------------------------------

    def run_all(
        self,
        scenario_names: Optional[List[str]] = None,
        tag: str = "",
    ) -> List[Dict]:
        """
        Run all (or specified) scenarios.  Creates a timestamped
        output directory under *output_root*.

        Returns
        -------
        List of result dicts (one per scenario).
        """
        if scenario_names is None:
            scenario_names = list(SCENARIOS.keys())

        # Create timestamped run directory
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"run_{ts}" + (f"_{tag}" if tag else "")
        self._run_dir = self.output_root / folder_name
        self._run_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for name in scenario_names:
            print(f"  Running scenario: {name} …", flush=True)
            res = self.run_scenario(name, save=True)
            results.append(res)
            print(f"    → mean_gpa={res['summary']['mean_gpa']:.3f}, "
                  f"failure_rate={res['summary']['failure_rate']:.1%}")

        self.save_comparison(results)
        return results

    # ------------------------------------------------------------------
    # Comparison output
    # ------------------------------------------------------------------

    def save_comparison(self, results: List[Dict]) -> Path:
        """Save a side-by-side comparison CSV + JSON to the run directory."""
        rows = [r["summary"] for r in results]
        df = pd.DataFrame(rows)

        if self._run_dir is None:
            self._run_dir = self.output_root / "comparison"
            self._run_dir.mkdir(parents=True, exist_ok=True)

        csv_path = self._run_dir / "scenario_comparison.csv"
        df.to_csv(csv_path, index=False)

        json_path = self._run_dir / "scenario_comparison.json"
        json_path.write_text(json.dumps(rows, indent=2))

        print(f"\nComparison saved → {self._run_dir}")
        return self._run_dir

    @property
    def run_dir(self) -> Optional[Path]:
        return self._run_dir


# ---------------------------------------------------------------------------
# Multi-seed robustness runner
# ---------------------------------------------------------------------------

class MultiSeedRunner:
    """
    Run one or more scenarios multiple times with different random seeds.

    Produces mean ± std and 95% CI for key metrics, allowing results to be
    reported as "mean ± CI" rather than single-seed point estimates.

    Parameters
    ----------
    n_runs : int
        Number of seeds per scenario (default: 20).
    base_seed : int
        Starting seed; runs use seeds base_seed, base_seed+1, …
    """

    def __init__(self, n_runs: int = 20, base_seed: int = 0) -> None:
        self.n_runs = n_runs
        self.base_seed = base_seed

    def run_scenario(self, name: str) -> Dict:
        """
        Run one scenario n_runs times.

        Returns
        -------
        Dict with keys: name, label, n_runs, and for each metric key k:
            {k}_mean, {k}_std, {k}_ci95
        """
        summaries = []
        for i in range(self.n_runs):
            cfg = get_scenario(name)
            cfg.seed = self.base_seed + i
            model = ClassroomModel(cfg)
            model.run()
            summaries.append(model.summary())
        return self._aggregate(name, summaries)

    def run_all(
        self,
        scenario_names: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Run all (or specified) scenarios, each n_runs times."""
        if scenario_names is None:
            scenario_names = list(SCENARIOS.keys())
        return [self.run_scenario(name) for name in scenario_names]

    def to_dataframe(self, aggregated: List[Dict]) -> pd.DataFrame:
        """Convert list of aggregated result dicts to a flat DataFrame."""
        return pd.DataFrame(aggregated)

    def _aggregate(self, name: str, summaries: List[Dict]) -> Dict:
        keys = [
            "mean_gpa", "failure_rate", "mean_final_stress",
            "mean_attendance_rate", "dropout_rate", "at_risk_rate",
            "mean_satisfaction",
        ]
        result: Dict = {
            "name": name,
            "label": SCENARIO_LABELS.get(name, name),
            "n_runs": self.n_runs,
        }
        for k in keys:
            vals = [s[k] for s in summaries if k in s]
            if vals:
                arr = np.array(vals)
                result[f"{k}_mean"] = round(float(arr.mean()), 4)
                result[f"{k}_std"] = round(float(arr.std()), 4)
                result[f"{k}_ci95"] = round(
                    float(1.96 * arr.std() / np.sqrt(len(vals))), 4
                )
        return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Run Classroom Digital Twin scenarios")
    parser.add_argument(
        "scenarios",
        nargs="*",
        default=list(SCENARIOS.keys()),
        help="Scenario names to run (default: all)",
    )
    parser.add_argument(
        "--output", "-o",
        default="data",
        help="Output root directory (default: data/)",
    )
    parser.add_argument(
        "--tag",
        default="",
        help="Optional tag appended to the run folder name",
    )
    args = parser.parse_args()

    print(f"Running {len(args.scenarios)} scenario(s): {', '.join(args.scenarios)}")
    runner = ScenarioRunner(output_root=args.output)
    runner.run_all(scenario_names=args.scenarios, tag=args.tag)


if __name__ == "__main__":
    _cli()
