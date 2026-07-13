"""
sensitivity.py — One-at-a-time (OAT) parameter sensitivity analysis.

Varies each key policy parameter individually while holding all others at
their baseline values, measures the change in a target metric, and returns
a ranked DataFrame suitable for a tornado chart.

Usage::

    from src.experiments.sensitivity import SensitivityAnalyzer

    sa = SensitivityAnalyzer(metric="mean_gpa")
    df = sa.analyze()           # OAT sensitivity — ranked by impact
    cv = sa.convergence_test()  # convergence across class sizes
"""

from __future__ import annotations

from copy import deepcopy
from typing import List, Optional

import numpy as np
import pandas as pd

from ..config import SimulationConfig
from ..model.classroom_model import ClassroomModel
from .scenarios import SCENARIO_LABELS, get_scenario


# ---------------------------------------------------------------------------
# Parameter sweep table
# ---------------------------------------------------------------------------
# Each entry: (param_id, label, low_value, high_value, setter)
# setter(cfg, value) mutates the config in place.

def _make_parameters() -> list:
    return [
        (
            "n_students", "Class Size",
            15, 60,
            lambda cfg, v: setattr(cfg, "n_students", int(v)),
        ),
        (
            "feedback_delay", "Feedback Delay (weeks)",
            0, 4,
            lambda cfg, v: setattr(cfg.lecturer, "feedback_delay_weeks", int(v)),
        ),
        (
            "assignment_load", "Assignment Load",
            1, 3,
            lambda cfg, v: setattr(cfg.lecturer, "assignment_load", int(v)),
        ),
        (
            "teaching_effectiveness", "Teaching Effectiveness",
            0.7, 1.3,
            lambda cfg, v: setattr(cfg.lecturer, "teaching_effectiveness", float(v)),
        ),
        (
            "ses_mean", "Mean SES Score",
            0.25, 0.75,
            lambda cfg, v: setattr(cfg.students, "ses_score_mean", float(v)),
        ),
        (
            "room_temp", "Room Temperature (°C)",
            16.0, 32.0,
            lambda cfg, v: setattr(cfg.environment, "room_temp_celsius", float(v)),
        ),
        (
            "peer_learning", "Peer Learning (on/off)",
            False, True,
            lambda cfg, v: setattr(cfg.social, "enable_peer_learning", bool(v)),
        ),
        (
            "class_mode", "Class Mode (in-person vs online)",
            "in_person", "online",
            lambda cfg, v: setattr(cfg.environment, "class_mode", str(v)),
        ),
    ]


# ---------------------------------------------------------------------------
# SensitivityAnalyzer
# ---------------------------------------------------------------------------

class SensitivityAnalyzer:
    """
    One-at-a-time (OAT) sensitivity analysis for the Classroom Digital Twin.

    For each parameter, varies it from a low to a high value while holding
    all other parameters at their baseline values.  Reports the change in
    the target metric relative to the unmodified baseline.

    Parameters
    ----------
    base_scenario : str
        Named scenario used as the reference (default: 'baseline').
    metric : str
        Key from model.summary() to measure (default: 'mean_gpa').
    n_runs : int
        Seeds per configuration.  1 = fast (single run).
        Use 3–5 for smoother, more reliable estimates.
    """

    def __init__(
        self,
        base_scenario: str = "baseline",
        metric: str = "mean_gpa",
        n_runs: int = 1,
    ) -> None:
        self.base_scenario = base_scenario
        self.metric = metric
        self.n_runs = n_runs

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_cfg(self, cfg: SimulationConfig) -> float:
        """Run cfg n_runs times with consecutive seeds; return mean metric."""
        vals = []
        for offset in range(self.n_runs):
            c = deepcopy(cfg)
            c.seed = cfg.seed + offset
            model = ClassroomModel(c)
            model.run()
            vals.append(model.summary().get(self.metric, 0.0))
        return float(np.mean(vals))

    # ------------------------------------------------------------------
    # OAT sensitivity
    # ------------------------------------------------------------------

    def analyze(self) -> pd.DataFrame:
        """
        Run OAT analysis over all defined parameters.

        Returns
        -------
        pd.DataFrame sorted by max_abs_delta descending, with columns:
            param_id, label, low_value, high_value,
            metric_baseline, metric_at_low, metric_at_high,
            delta_low, delta_high, max_abs_delta
        """
        parameters = _make_parameters()
        base_cfg = get_scenario(self.base_scenario)
        baseline_metric = self._run_cfg(base_cfg)

        rows = []
        for param_id, label, low_val, high_val, setter in parameters:
            cfg_low = get_scenario(self.base_scenario)
            setter(cfg_low, low_val)
            m_low = self._run_cfg(cfg_low)

            cfg_high = get_scenario(self.base_scenario)
            setter(cfg_high, high_val)
            m_high = self._run_cfg(cfg_high)

            d_low = round(m_low - baseline_metric, 4)
            d_high = round(m_high - baseline_metric, 4)

            rows.append({
                "param_id": param_id,
                "label": label,
                "low_value": str(low_val),
                "high_value": str(high_val),
                "metric_baseline": round(baseline_metric, 4),
                "metric_at_low": round(m_low, 4),
                "metric_at_high": round(m_high, 4),
                "delta_low": d_low,
                "delta_high": d_high,
                "max_abs_delta": round(max(abs(d_low), abs(d_high)), 4),
            })

        df = pd.DataFrame(rows)
        return df.sort_values("max_abs_delta", ascending=False).reset_index(drop=True)

    # ------------------------------------------------------------------
    # Convergence test
    # ------------------------------------------------------------------

    def convergence_test(
        self,
        student_counts: Optional[List[int]] = None,
        n_seeds: int = 10,
    ) -> pd.DataFrame:
        """
        Test whether results stabilise as class size N increases.

        For each N, runs the scenario n_seeds times with different seeds
        and records mean ± std of the target metric.

        Returns
        -------
        pd.DataFrame with columns: n_students, mean, std, ci95
        """
        if student_counts is None:
            student_counts = [10, 15, 20, 30, 45, 60, 90, 120]

        rows = []
        for n in student_counts:
            vals = []
            for seed in range(n_seeds):
                cfg = get_scenario(self.base_scenario)
                cfg.n_students = n
                cfg.seed = seed
                model = ClassroomModel(cfg)
                model.run()
                vals.append(model.summary().get(self.metric, 0.0))
            rows.append({
                "n_students": n,
                "mean": round(float(np.mean(vals)), 4),
                "std": round(float(np.std(vals)), 4),
                "ci95": round(float(1.96 * np.std(vals) / np.sqrt(n_seeds)), 4),
            })
        return pd.DataFrame(rows)
