"""
insights.py — Campus Board Insights module for the Classroom Digital Twin.

Transforms raw scenario results into executive-ready summaries, policy ROI
tables, equity analyses, and ranked recommendations for university administrators.

Usage::

    from src.insights import CampusBoardInsights
    from src.experiments.runner import ScenarioRunner

    runner = ScenarioRunner()
    results = runner.run_all(['baseline', 'slow_feedback', 'ses_diverse'])
    cb = CampusBoardInsights(results)
    print(cb.ranked_recommendations())
    cb.generate_report(Path("data/report"))
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Policy metadata — used for ROI table
# ---------------------------------------------------------------------------

_POLICY_META: Dict[str, Dict] = {
    "baseline": {
        "policy_name": "Status Quo",
        "ease": "N/A",
        "cost_level": "—",
        "description": "No change from current practice",
    },
    "fast_feedback": {
        "policy_name": "Immediate Feedback System",
        "ease": "Medium",
        "cost_level": "Low",
        "description": "Online submission with auto-feedback or weekly TA marking",
    },
    "slow_feedback": {
        "policy_name": "Delayed Feedback (current worse-case)",
        "ease": "—",
        "cost_level": "—",
        "description": "Represents resource-constrained grading",
    },
    "low_load": {
        "policy_name": "Reduced Assignment Load",
        "ease": "High",
        "cost_level": "None",
        "description": "Reduce weekly assignments from 2 to 1; focus on quality",
    },
    "high_load": {
        "policy_name": "Increased Assignment Load",
        "ease": "High",
        "cost_level": "None",
        "description": "Add third weekly assignment to increase practice",
    },
    "large_class": {
        "policy_name": "Large Lecture (60 students)",
        "ease": "—",
        "cost_level": "—",
        "description": "Scaling without additional support structures",
    },
    "small_class": {
        "policy_name": "Small Class Section (15 students)",
        "ease": "Low",
        "cost_level": "High",
        "description": "Split large lectures into smaller sections",
    },
    "intervention": {
        "policy_name": "Tutoring Intervention (weeks 7–10)",
        "ease": "Medium",
        "cost_level": "Medium",
        "description": "Targeted tutoring for bottom 25% students mid-semester",
    },
    "adaptive_lecturer": {
        "policy_name": "Adaptive Teaching Protocol",
        "ease": "Medium",
        "cost_level": "Low",
        "description": "Lecturer monitors class progress and adjusts delivery",
    },
    "ses_diverse": {
        "policy_name": "High SES Diversity Context",
        "ease": "—",
        "cost_level": "—",
        "description": "Simulation with high socioeconomic variance in cohort",
    },
    "no_peer_learning": {
        "policy_name": "No Study Groups",
        "ease": "—",
        "cost_level": "—",
        "description": "Students study independently without structured peer learning",
    },
    "combined_intervention": {
        "policy_name": "Combined Best-Practice Policy",
        "ease": "Low",
        "cost_level": "Medium",
        "description": "Fast feedback + low load + tutoring + adaptive teaching",
    },
    "morning_class": {
        "policy_name": "Morning Schedule",
        "ease": "—",
        "cost_level": "—",
        "description": "Class scheduled in early morning slot",
    },
    "evening_class": {
        "policy_name": "Evening Schedule",
        "ease": "—",
        "cost_level": "—",
        "description": "Class scheduled in evening slot",
    },
    "stress_test": {
        "policy_name": "Worst-Case Configuration",
        "ease": "—",
        "cost_level": "—",
        "description": "60 students + maximum load + maximum feedback delay",
    },
    "hot_classroom": {
        "policy_name": "Hot Classroom (no AC)",
        "ease": "Low",
        "cost_level": "Low",
        "description": "Classroom at 32°C due to broken or absent HVAC",
    },
    "cold_classroom": {
        "policy_name": "Over-cooled Classroom",
        "ease": "Low",
        "cost_level": "Low",
        "description": "Classroom over-airconditioned to 16°C",
    },
    "online_class": {
        "policy_name": "Fully Online Delivery",
        "ease": "High",
        "cost_level": "Low",
        "description": "All sessions delivered online; reduced peer interaction and teaching effectiveness",
    },
    "hybrid_class": {
        "policy_name": "Hybrid Delivery",
        "ease": "Medium",
        "cost_level": "Low",
        "description": "Mix of in-person and online sessions",
    },
}


# ---------------------------------------------------------------------------
# CampusBoardInsights
# ---------------------------------------------------------------------------

class CampusBoardInsights:
    """
    Converts a list of scenario results into campus-board-ready insights.

    Parameters
    ----------
    results : List[Dict]
        Result dicts from ScenarioRunner.run_scenario() or run_all().
        Each dict must have: 'name', 'label', 'summary', 'model',
        'student_df', 'weekly_df'.
    baseline_name : str
        Name of the scenario to treat as the reference/baseline for
        computing deltas.  Defaults to 'baseline'.
    """

    def __init__(
        self,
        results: List[Dict],
        baseline_name: str = "baseline",
    ) -> None:
        self.results = results
        self.baseline_name = baseline_name
        self._baseline = self._find_baseline()

    def _find_baseline(self) -> Optional[Dict]:
        for r in self.results:
            if r.get("name") == self.baseline_name:
                return r
        # Fall back to first result
        return self.results[0] if self.results else None

    # ------------------------------------------------------------------
    # Executive summary
    # ------------------------------------------------------------------

    def executive_summary(self) -> str:
        """
        Return a 5-bullet executive summary comparing key scenarios.
        Suitable for a slide or brief printed handout.
        """
        if not self.results:
            return "No results available."

        lines = ["CLASSROOM DIGITAL TWIN — EXECUTIVE SUMMARY", "=" * 50, ""]

        # 1. Best and worst GPA scenario
        summaries = [(r["label"], r["summary"]) for r in self.results]
        best = max(summaries, key=lambda x: x[1].get("mean_gpa", 0))
        worst = min(summaries, key=lambda x: x[1].get("mean_gpa", 0))
        lines.append(f"• GPA range: {worst[1]['mean_gpa']:.2f} ({worst[0]}) "
                     f"→ {best[1]['mean_gpa']:.2f} ({best[0]}) — "
                     f"a {best[1]['mean_gpa'] - worst[1]['mean_gpa']:.2f} point spread.")

        # 2. Failure rate range
        best_fail = min(summaries, key=lambda x: x[1].get("failure_rate", 1))
        worst_fail = max(summaries, key=lambda x: x[1].get("failure_rate", 0))
        lines.append(f"• Failure rates: {best_fail[1]['failure_rate']:.0%} ({best_fail[0]}) "
                     f"to {worst_fail[1]['failure_rate']:.0%} ({worst_fail[0]}). "
                     f"Policy choice is the primary driver.")

        # 3. Dropout
        max_dropout = max(summaries, key=lambda x: x[1].get("dropout_rate", 0))
        if max_dropout[1].get("dropout_rate", 0) > 0:
            lines.append(f"• Dropout risk: Up to {max_dropout[1]['dropout_rate']:.0%} "
                         f"of students drop out under {max_dropout[0]} conditions. "
                         f"Proactive intervention can eliminate this.")
        else:
            lines.append("• No dropouts observed across all scenarios with current parameters.")

        # 4. Equity
        ses_result = next((r for r in self.results if r.get("name") == "ses_diverse"), None)
        if ses_result:
            eq_df = ses_result["model"].equity_dataframe()
            if len(eq_df) >= 2:
                q1 = eq_df[eq_df["ses_quartile"] == 0]
                q4 = eq_df[eq_df["ses_quartile"] == 3]
                if len(q1) and len(q4):
                    gap = float(q4["mean_gpa"].iloc[0]) - float(q1["mean_gpa"].iloc[0])
                    lines.append(f"• Equity gap: Under high SES-diversity conditions, "
                                 f"Q4 students score {gap:.2f} GPA points above Q1 on average. "
                                 f"Targeted support for low-SES students is warranted.")

        # 5. Top recommendation
        recs = self.ranked_recommendations()
        if recs:
            lines.append(f"• Top recommendation: {recs[0]}")

        lines.append("")
        lines.append("Full policy analysis below.")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Policy ROI table
    # ------------------------------------------------------------------

    def policy_roi_table(self) -> pd.DataFrame:
        """
        DataFrame comparing each scenario to baseline.

        Columns: scenario, policy_name, mean_gpa, gpa_delta, failure_rate,
                 failure_rate_delta, dropout_rate, gini_gpa, ease,
                 cost_level, at_risk_rate.
        """
        baseline_summ = self._baseline["summary"] if self._baseline else {}
        base_gpa = baseline_summ.get("mean_gpa", 0)
        base_fail = baseline_summ.get("failure_rate", 0)

        rows = []
        for r in self.results:
            name = r.get("name", "?")
            summ = r["summary"]
            meta = _POLICY_META.get(name, {})

            rows.append({
                "scenario": name,
                "policy_name": meta.get("policy_name", name),
                "mean_gpa": summ.get("mean_gpa", 0),
                "gpa_delta": round(summ.get("mean_gpa", 0) - base_gpa, 4),
                "failure_rate": summ.get("failure_rate", 0),
                "failure_rate_delta": round(
                    summ.get("failure_rate", 0) - base_fail, 4
                ),
                "dropout_rate": summ.get("dropout_rate", 0),
                "at_risk_rate": summ.get("at_risk_rate", 0),
                "gini_gpa": summ.get("gini_gpa", 0),
                "mean_satisfaction": summ.get("mean_satisfaction", 0),
                "ease": meta.get("ease", "—"),
                "cost_level": meta.get("cost_level", "—"),
                "description": meta.get("description", ""),
            })

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Equity analysis
    # ------------------------------------------------------------------

    def equity_analysis(self) -> pd.DataFrame:
        """
        SES Q1 vs Q4 outcome comparison for each scenario.

        Returns a tidy DataFrame with columns:
            scenario, label, ses_quartile, mean_gpa, failure_rate,
            dropout_rate, mean_satisfaction, gpa_gap (Q4 - Q1)
        """
        rows = []
        for r in self.results:
            model = r.get("model")
            if model is None:
                continue
            try:
                eq_df = model.equity_dataframe()
            except Exception:
                continue

            q1 = eq_df[eq_df["ses_quartile"] == 0]
            q4 = eq_df[eq_df["ses_quartile"] == 3]
            q1_gpa = float(q1["mean_gpa"].iloc[0]) if len(q1) else 0.0
            q4_gpa = float(q4["mean_gpa"].iloc[0]) if len(q4) else 0.0

            for _, row in eq_df.iterrows():
                rows.append({
                    "scenario": r.get("name", "?"),
                    "label": r.get("label", r.get("name", "?")),
                    "ses_quartile": int(row["ses_quartile"]),
                    "ses_quartile_label": row.get("ses_quartile_label", ""),
                    "mean_gpa": row.get("mean_gpa", 0),
                    "failure_rate": row.get("failure_rate", 0),
                    "dropout_rate": row.get("dropout_rate", 0),
                    "mean_satisfaction": row.get("mean_satisfaction", 0),
                    "at_risk_rate": row.get("at_risk_rate", 0),
                    "gpa_gap_q4_minus_q1": round(q4_gpa - q1_gpa, 4),
                })
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # At-risk report
    # ------------------------------------------------------------------

    def at_risk_report(self) -> pd.DataFrame:
        """
        Which scenarios produce the most at-risk students at week 5.

        Returns DataFrame: scenario, label, at_risk_rate, at_risk_count,
        n_students, sorted by at_risk_rate descending.
        """
        rows = []
        for r in self.results:
            summ = r["summary"]
            n = summ.get("n_students", 0)
            rate = summ.get("at_risk_rate", 0)
            rows.append({
                "scenario": r.get("name", "?"),
                "label": r.get("label", r.get("name", "?")),
                "at_risk_rate": rate,
                "at_risk_count": round(rate * n),
                "n_students": n,
                "dropout_rate": summ.get("dropout_rate", 0),
                "mean_gpa": summ.get("mean_gpa", 0),
            })
        df = pd.DataFrame(rows)
        return df.sort_values("at_risk_rate", ascending=False).reset_index(drop=True)

    # ------------------------------------------------------------------
    # Ranked recommendations
    # ------------------------------------------------------------------

    def ranked_recommendations(self) -> List[str]:
        """
        Return a ranked list of actionable policy recommendations.

        Rankings are based on GPA improvement over baseline, failure rate
        reduction, ease of implementation, and equity impact.
        """
        if not self.results:
            return []

        baseline_summ = self._baseline["summary"] if self._baseline else {}
        base_gpa = baseline_summ.get("mean_gpa", 0)
        base_fail = baseline_summ.get("failure_rate", 0)
        base_dropout = baseline_summ.get("dropout_rate", 0)

        scored: List[tuple[float, str]] = []

        for r in self.results:
            name = r.get("name", "?")
            if name == self.baseline_name:
                continue
            meta = _POLICY_META.get(name, {})
            if meta.get("ease") in ("—", None):
                continue  # skip non-actionable scenarios

            summ = r["summary"]
            gpa_gain = summ.get("mean_gpa", 0) - base_gpa
            fail_reduction = base_fail - summ.get("failure_rate", 0)
            dropout_reduction = base_dropout - summ.get("dropout_rate", 0)

            # Ease multiplier: High=1.5, Medium=1.0, Low=0.5
            ease_mult = {"High": 1.5, "Medium": 1.0, "Low": 0.5}.get(
                meta.get("ease", "Medium"), 1.0
            )

            score = (gpa_gain * 2 + fail_reduction * 3 + dropout_reduction * 2) * ease_mult

            label = r.get("label", name)
            policy = meta.get("policy_name", label)

            # Build readable recommendation
            parts = [f"{policy}"]
            if gpa_gain > 0.01:
                parts.append(f"+{gpa_gain:.2f} GPA")
            elif gpa_gain < -0.01:
                parts.append(f"{gpa_gain:.2f} GPA")
            if fail_reduction > 0.005:
                parts.append(f"−{fail_reduction:.0%} failures")
            if dropout_reduction > 0.005:
                parts.append(f"−{dropout_reduction:.0%} dropout")
            if meta.get("ease"):
                parts.append(f"[ease: {meta['ease']}, cost: {meta.get('cost_level','?')}]")

            scored.append((score, " · ".join(parts)))

        # Sort descending by score
        scored.sort(reverse=True, key=lambda x: x[0])
        return [f"{i+1}. {rec}" for i, (_, rec) in enumerate(scored)]

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, output_dir: Path) -> Path:
        """
        Save a full text/CSV report to *output_dir*.

        Files written:
          - executive_summary.txt
          - policy_roi.csv
          - equity_analysis.csv
          - at_risk_report.csv
          - recommendations.txt
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        (output_dir / "executive_summary.txt").write_text(
            self.executive_summary(), encoding="utf-8"
        )

        self.policy_roi_table().to_csv(output_dir / "policy_roi.csv", index=False)
        self.equity_analysis().to_csv(output_dir / "equity_analysis.csv", index=False)
        self.at_risk_report().to_csv(output_dir / "at_risk_report.csv", index=False)

        recs = self.ranked_recommendations()
        (output_dir / "recommendations.txt").write_text(
            "RANKED POLICY RECOMMENDATIONS\n"
            + "=" * 40 + "\n"
            + "\n".join(recs),
            encoding="utf-8",
        )

        print(f"Campus Board report saved → {output_dir}")
        return output_dir
