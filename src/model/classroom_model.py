"""
classroom_model.py — Orchestration engine for the Classroom Digital Twin.

ClassroomModel initialises agents from SimulationConfig, runs the
semester week-by-week, and produces structured DataFrames for analysis.

Simulation loop (per week):
  1. Check for exam week (stress spike + knowledge consolidation, no new learning)
  2. For each active (non-dropout) student:
       a. Draw attendance
       b. Draw assignment outcomes
       c. Update feedback counter
       d. Update stress (+ SES relief + grit recovery)
       e. Update topic knowledge OR consolidate (exam week)
       f. Apply peer learning delta
       g. Update motivation (+ schedule effect)
       h. Update fatigue
       i. Update satisfaction
       j. Apply intervention if applicable
       k. Snapshot history
  3. Adaptive lecturer adjustment
  4. Check dropouts
  5. At-risk detection at the designated week
  6. Compute class-level weekly aggregate
  After week n_weeks: compute GPA proxy for each student
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from ..config import SimulationConfig
from .agents import LecturerAgent, StudentAgent
from .dynamics import (
    apply_intervention,
    check_dropout,
    compute_gini,
    compute_gpa_proxy,
    compute_peer_learning_delta,
    consolidate_exam_knowledge,
    did_receive_feedback,
    draw_assignment_outcomes,
    draw_attendance,
    effective_feedback_quality,
    grit_recovery,
    mid_semester_slump_factor,
    ses_stress_adjustment,
    update_fatigue,
    update_motivation,
    update_satisfaction,
    update_stress,
    update_topic_knowledge,
)


class ClassroomModel:
    """
    Agent-based classroom simulation.

    Parameters
    ----------
    cfg : SimulationConfig
        Full configuration object; controls all parameters.

    Usage
    -----
    >>> model = ClassroomModel(cfg)
    >>> model.run()
    >>> df_students = model.student_dataframe()
    >>> df_weekly = model.weekly_dataframe()
    """

    def __init__(self, cfg: SimulationConfig) -> None:
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.seed)
        self._ran = False

        # Instantiate agents
        self.lecturer = self._make_lecturer()
        self.students: List[StudentAgent] = self._make_students()

        # Study groups (assigned at start)
        self._study_groups: Dict[int, List[StudentAgent]] = {}

        # Weekly class-level aggregates (populated during run)
        self._weekly_records: List[Dict] = []

        # Form study groups (uses RNG, so after students are created)
        if cfg.social.enable_peer_learning:
            self._form_study_groups()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _make_lecturer(self) -> LecturerAgent:
        lc = self.cfg.lecturer
        return LecturerAgent(
            teaching_effectiveness=lc.teaching_effectiveness,
            feedback_delay_weeks=lc.feedback_delay_weeks,
            assignment_load=lc.assignment_load,
            strictness=lc.strictness,
            adaptivity=lc.adaptivity,
            adaptation_threshold=lc.adaptation_threshold,
            adaptation_boost=lc.adaptation_boost,
        )

    def _make_students(self) -> List[StudentAgent]:
        sd = self.cfg.students
        n = self.cfg.n_students
        n_topics = self.cfg.curriculum.n_topics
        schedule_mod = self.cfg.environment.schedule_motivation_modifier

        # Learning capacity: uniform in [min, max]
        capacities = self.rng.uniform(sd.learning_capacity_min,
                                      sd.learning_capacity_max, n)

        # Motivation: truncated normal, clamped
        motivations = np.clip(
            self.rng.normal(sd.motivation_mean, sd.motivation_std, n), 0.01, 0.99
        )

        # Stress: truncated normal, clamped
        stresses = np.clip(
            self.rng.normal(sd.stress_mean, sd.stress_std, n), 0.0, 1.0
        )

        # Knowledge: truncated normal, clamped
        knowledges = np.clip(
            self.rng.normal(sd.knowledge_mean, sd.knowledge_std, n), 0.0, 1.0
        )

        # SES scores: truncated normal [0,1]
        ses_scores = np.clip(
            self.rng.normal(sd.ses_score_mean, sd.ses_score_std, n), 0.0, 1.0
        )

        # Grit scores: truncated normal [0,1]
        grits = np.clip(
            self.rng.normal(sd.grit_mean, sd.grit_std, n), 0.0, 1.0
        )

        students = []
        for i in range(n):
            # Attendance base: slight individual variation + schedule effect
            att_base = float(np.clip(
                self.rng.normal(sd.base_attendance_prob, 0.08) + schedule_mod,
                0.3, 0.99
            ))
            late_base = float(np.clip(
                self.rng.normal(sd.base_late_work_prob, 0.06), 0.0, 0.6
            ))
            # SES also slightly boosts attendance (resources / fewer outside obligations)
            att_base = float(np.clip(att_base + ses_scores[i] * 0.05, 0.3, 0.99))

            # Initial topic knowledge: all topics start at the same sampled level
            k0 = float(knowledges[i])
            topic_k = [k0] * n_topics

            s = StudentAgent(
                student_id=i,
                learning_capacity=float(capacities[i]),
                attendance_prob=att_base,
                late_work_prob=late_base,
                ses_score=float(ses_scores[i]),
                grit=float(grits[i]),
                motivation=float(motivations[i]),
                stress=float(stresses[i]),
                topic_knowledge=topic_k,
            )
            students.append(s)
        return students

    # ------------------------------------------------------------------
    # Study group formation
    # ------------------------------------------------------------------

    def _form_study_groups(self) -> None:
        """
        Assign students to study groups of approximately study_group_size.

        formation='mixed' (heterogeneous): sort by knowledge, then interleave
        so each group has a spread of abilities.
        formation='random': random assignment.
        formation='homogeneous': sort by knowledge, assign consecutively.
        """
        sc = self.cfg.social
        n = len(self.students)
        size = sc.study_group_size

        if sc.formation == "mixed":
            # Sort by initial knowledge, then round-robin into groups
            ordered = sorted(self.students, key=lambda s: s.knowledge)
            n_groups = max(1, n // size)
            for i, student in enumerate(ordered):
                student.study_group_id = i % n_groups
        elif sc.formation == "homogeneous":
            ordered = sorted(self.students, key=lambda s: s.knowledge)
            n_groups = max(1, n // size)
            for i, student in enumerate(ordered):
                student.study_group_id = i // size
        else:  # random
            indices = self.rng.permutation(n)
            n_groups = max(1, n // size)
            for rank, i in enumerate(indices):
                self.students[i].study_group_id = rank % n_groups

        # Build group → members lookup
        self._study_groups = {}
        for student in self.students:
            gid = student.study_group_id
            self._study_groups.setdefault(gid, []).append(student)

    # ------------------------------------------------------------------
    # Main simulation loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Execute the full semester simulation."""
        if self._ran:
            raise RuntimeError("Model already ran; create a new ClassroomModel to re-run.")

        cfg = self.cfg
        n_weeks = cfg.n_weeks
        delay = self.lecturer.feedback_delay_weeks

        # Identify intervention targets at start (bottom quantile by initial knowledge)
        if cfg.intervention.enabled:
            self._mark_intervention_targets()

        for week_idx in range(n_weeks):  # 0-indexed
            week_num = week_idx + 1      # 1-indexed for display

            is_exam = self._is_exam_week(week_num)
            feedback_this_week = did_receive_feedback(week_idx, delay)
            slump = mid_semester_slump_factor(
                week_num, n_weeks, cfg.environment.mid_semester_slump_strength
            )

            # Active students only for means; track all for counts
            active_students = [s for s in self.students if not s.dropped_out]
            n_active = len(active_students)

            # Feedback quality degrades with class size; class mode reduces effectiveness
            fq = effective_feedback_quality(n_active)
            mode_mods = cfg.environment.class_mode_modifiers
            effective_teach = (
                self.lecturer.current_effectiveness
                * fq
                * mode_mods["teaching_effectiveness_mult"]
            )

            week_stress: List[float] = []
            week_knowledge: List[float] = []
            week_motivation: List[float] = []
            week_fatigue: List[float] = []
            week_satisfaction: List[float] = []
            week_attended: List[bool] = []
            week_submitted: List[int] = []
            week_late: List[int] = []
            week_missed: List[int] = []

            for student in active_students:
                # ---- Attendance ----
                attended = draw_attendance(student, cfg, self.rng)
                student.weeks_attended.append(attended)

                # ---- Assignments ----
                sub, lat, mis = draw_assignment_outcomes(
                    student, self.lecturer.assignment_load, cfg, self.rng
                )
                student.assignments_submitted.append(sub)
                student.assignments_late.append(lat)
                student.assignments_missed.append(mis)

                # ---- Update pending feedback counter ----
                if feedback_this_week:
                    student.pending_feedback_weeks = max(
                        0, student.pending_feedback_weeks - 1
                    )
                else:
                    if self.lecturer.assignment_load > 0:
                        student.pending_feedback_weeks += 1

                # ---- Stress update ----
                new_stress = update_stress(student, attended, feedback_this_week, cfg)
                # SES and grit moderate stress
                new_stress -= ses_stress_adjustment(student.ses_score,
                                                    cfg.dynamics.w_ses_stress_relief)
                new_stress -= grit_recovery(student.grit, new_stress,
                                            cfg.dynamics.w_grit_recovery)
                # Exam week stress spike
                if is_exam:
                    new_stress += cfg.curriculum.exam_stress_delta
                new_stress = max(0.0, min(1.0, new_stress))
                student.stress = new_stress

                # ---- Knowledge update ----
                if is_exam:
                    student.topic_knowledge = consolidate_exam_knowledge(student, cfg)
                else:
                    from .dynamics import get_current_topic
                    topic_idx = get_current_topic(week_num, cfg.curriculum.n_topics,
                                                  n_weeks)
                    student.topic_knowledge = update_topic_knowledge(
                        student, topic_idx, attended, effective_teach, slump, cfg
                    )

                # ---- Peer learning ----
                if cfg.social.enable_peer_learning and student.study_group_id >= 0:
                    group = self._study_groups.get(student.study_group_id, [])
                    peer_rate = cfg.social.peer_learning_rate * mode_mods["peer_learning_mult"]
                    deltas = compute_peer_learning_delta(
                        student, group, peer_rate
                    )
                    student.topic_knowledge = [
                        max(0.0, min(1.0, k + d))
                        for k, d in zip(student.topic_knowledge, deltas)
                    ]

                # ---- Motivation update ----
                new_motivation = update_motivation(student, feedback_this_week, cfg)
                # Apply mid-semester slump to motivation
                new_motivation = max(0.01, new_motivation * slump)
                student.motivation = new_motivation

                # ---- Fatigue update ----
                student.fatigue = update_fatigue(student, attended, cfg)

                # ---- Satisfaction update ----
                student.satisfaction = update_satisfaction(
                    student, attended, feedback_this_week, cfg
                )

                # ---- Intervention ----
                if (cfg.intervention.enabled
                        and student.is_intervention_target
                        and cfg.intervention.start_week <= week_num <= cfg.intervention.end_week):
                    apply_intervention(student, cfg)

                # ---- Snapshot ----
                student.snapshot()

                # Collect for class aggregate
                week_stress.append(student.stress)
                week_knowledge.append(student.knowledge)
                week_motivation.append(student.motivation)
                week_fatigue.append(student.fatigue)
                week_satisfaction.append(student.satisfaction)
                week_attended.append(attended)
                week_submitted.append(sub)
                week_late.append(lat)
                week_missed.append(mis)

            # Inactive (already dropped out) students: append placeholder records
            for student in self.students:
                if student.dropped_out and student.dropout_week != week_num:
                    student.weeks_attended.append(False)
                    student.assignments_submitted.append(0)
                    student.assignments_late.append(0)
                    student.assignments_missed.append(0)
                    student.snapshot()  # freezes last state

            # ---- Adaptive lecturer adjustment ----
            if week_knowledge:
                mean_k = float(np.mean(week_knowledge))
                self._adaptive_lecturer_adjustment(mean_k)

            # ---- Dropout check ----
            for student in active_students:
                check_dropout(student, week_num, cfg)

            # ---- At-risk detection ----
            if week_num == cfg.dynamics.at_risk_detection_week:
                self._detect_at_risk()

            # ---- Class-level weekly aggregate ----
            n_dropped = int(sum(1 for s in self.students if s.dropped_out))
            n_at_risk = int(sum(1 for s in self.students if s.at_risk))
            self._weekly_records.append({
                "week": week_num,
                "mean_stress": float(np.mean(week_stress)) if week_stress else 0.0,
                "std_stress": float(np.std(week_stress)) if week_stress else 0.0,
                "mean_knowledge": float(np.mean(week_knowledge)) if week_knowledge else 0.0,
                "std_knowledge": float(np.std(week_knowledge)) if week_knowledge else 0.0,
                "mean_motivation": float(np.mean(week_motivation)) if week_motivation else 0.0,
                "mean_fatigue": float(np.mean(week_fatigue)) if week_fatigue else 0.0,
                "mean_satisfaction": float(np.mean(week_satisfaction)) if week_satisfaction else 0.0,
                "attendance_rate": float(np.mean(week_attended)) if week_attended else 0.0,
                "assignments_submitted": int(np.sum(week_submitted)),
                "assignments_late": int(np.sum(week_late)),
                "assignments_missed": int(np.sum(week_missed)),
                "dropout_count": n_dropped,
                "at_risk_count": n_at_risk,
                "is_exam_week": is_exam,
            })

        # ---- End of semester: compute GPA ----
        for student in self.students:
            student.gpa_proxy = compute_gpa_proxy(student, cfg)

        self._ran = True

    # ------------------------------------------------------------------
    # Intervention target selection
    # ------------------------------------------------------------------

    def _mark_intervention_targets(self) -> None:
        """Mark bottom-quantile students (by initial knowledge) as targets."""
        quantile = self.cfg.intervention.target_quantile
        knowledges = [s.knowledge for s in self.students]
        threshold = float(np.quantile(knowledges, quantile))
        for s in self.students:
            if s.knowledge <= threshold:
                s.is_intervention_target = True

    # ------------------------------------------------------------------
    # Exam week check
    # ------------------------------------------------------------------

    def _is_exam_week(self, week_num: int) -> bool:
        """Return True if week_num is a scheduled exam/evaluation week."""
        return week_num in self.cfg.curriculum.exam_weeks

    # ------------------------------------------------------------------
    # Adaptive lecturer
    # ------------------------------------------------------------------

    def _adaptive_lecturer_adjustment(self, mean_k: float) -> None:
        """
        If class is struggling (mean knowledge below threshold), boost
        lecturer effectiveness proportional to adaptivity parameter.
        """
        lc = self.cfg.lecturer
        if lc.adaptivity <= 0:
            return
        if mean_k < lc.adaptation_threshold:
            gap = lc.adaptation_threshold - mean_k
            boost = lc.adaptivity * lc.adaptation_boost * gap
            self.lecturer.current_effectiveness = min(
                1.4, self.lecturer.current_effectiveness + boost
            )

    # ------------------------------------------------------------------
    # At-risk detection
    # ------------------------------------------------------------------

    def _detect_at_risk(self) -> None:
        """
        Flag students as at-risk based on knowledge and stress at detection week.

        A student is at-risk if:
            knowledge < at_risk_knowledge_threshold
            OR stress > at_risk_stress_threshold
        """
        dw = self.cfg.dynamics
        for student in self.students:
            if student.dropped_out:
                continue
            if (student.knowledge < dw.at_risk_knowledge_threshold
                    or student.stress > dw.at_risk_stress_threshold):
                student.at_risk = True

    # ------------------------------------------------------------------
    # Output DataFrames
    # ------------------------------------------------------------------

    def student_dataframe(self) -> pd.DataFrame:
        """Return one row per student with end-of-semester metrics."""
        self._assert_ran()
        rows = []
        for s in self.students:
            rows.append({
                "student_id": s.student_id,
                "learning_capacity": round(s.learning_capacity, 4),
                "late_work_prob": round(s.late_work_prob, 4),
                "ses_score": round(s.ses_score, 4),
                "grit": round(s.grit, 4),
                "ses_quartile": int(min(3, int(s.ses_score * 4))),  # 0-3
                "gpa_proxy": round(s.gpa_proxy, 4),
                "final_knowledge": round(s.knowledge, 4),
                "final_stress": round(s.stress, 4),
                "final_motivation": round(s.motivation, 4),
                "final_fatigue": round(s.fatigue, 4),
                "final_satisfaction": round(s.satisfaction, 4),
                "attendance_rate": round(s.attendance_rate, 4),
                "completion_rate": round(s.completion_rate, 4),
                "is_intervention_target": s.is_intervention_target,
                "dropped_out": s.dropped_out,
                "dropout_week": s.dropout_week,
                "at_risk": s.at_risk,
                "study_group_id": s.study_group_id,
            })
        return pd.DataFrame(rows)

    def weekly_dataframe(self) -> pd.DataFrame:
        """Return one row per week with class-level aggregates."""
        self._assert_ran()
        return pd.DataFrame(self._weekly_records)

    def knowledge_matrix(self) -> pd.DataFrame:
        """
        Return a (n_students × n_weeks) DataFrame of mean-knowledge snapshots.
        Backward compatible: uses knowledge_history (= mean topic knowledge).
        """
        self._assert_ran()
        data = {
            s.student_id: s.knowledge_history for s in self.students
        }
        df = pd.DataFrame(data).T
        df.index.name = "student_id"
        df.columns = [f"week_{w+1}" for w in range(self.cfg.n_weeks)]
        return df

    def stress_matrix(self) -> pd.DataFrame:
        """Return a (n_students × n_weeks) DataFrame of stress snapshots."""
        self._assert_ran()
        data = {
            s.student_id: s.stress_history for s in self.students
        }
        df = pd.DataFrame(data).T
        df.index.name = "student_id"
        df.columns = [f"week_{w+1}" for w in range(self.cfg.n_weeks)]
        return df

    def topic_mastery_dataframe(self) -> pd.DataFrame:
        """
        Return a (n_students × n_topics) DataFrame of final topic knowledge.
        Rows = students, columns = topic_0 … topic_N.
        Only includes non-dropped-out students.
        """
        self._assert_ran()
        rows = []
        for s in self.students:
            row = {"student_id": s.student_id, "dropped_out": s.dropped_out}
            for t_idx, k in enumerate(s.topic_knowledge):
                row[f"topic_{t_idx}"] = round(k, 4)
            rows.append(row)
        return pd.DataFrame(rows)

    def equity_dataframe(self) -> pd.DataFrame:
        """
        SES quartile breakdown of outcomes.

        Returns a DataFrame with one row per SES quartile (0=lowest, 3=highest)
        and columns: mean_gpa, failure_rate, mean_knowledge, dropout_rate, mean_satisfaction.
        """
        self._assert_ran()
        df = self.student_dataframe()
        rows = []
        for q in range(4):
            group = df[df["ses_quartile"] == q]
            if len(group) == 0:
                continue
            rows.append({
                "ses_quartile": q,
                "ses_quartile_label": f"Q{q+1} ({'Low' if q==0 else 'Mid-Low' if q==1 else 'Mid-High' if q==2 else 'High'})",
                "n_students": len(group),
                "mean_gpa": round(float(group["gpa_proxy"].mean()), 4),
                "failure_rate": round(float((group["gpa_proxy"] < 2.0).mean()), 4),
                "mean_knowledge": round(float(group["final_knowledge"].mean()), 4),
                "dropout_rate": round(float(group["dropped_out"].mean()), 4),
                "mean_satisfaction": round(float(group["final_satisfaction"].mean()), 4),
                "at_risk_rate": round(float(group["at_risk"].mean()), 4),
            })
        return pd.DataFrame(rows)

    def dropout_timeline(self) -> pd.DataFrame:
        """
        Cumulative dropout count by week.

        Returns DataFrame with columns: week, new_dropouts, cumulative_dropouts.
        """
        self._assert_ran()
        dropout_weeks = [s.dropout_week for s in self.students if s.dropped_out]
        rows = []
        cumulative = 0
        for w in range(1, self.cfg.n_weeks + 1):
            new = sum(1 for dw in dropout_weeks if dw == w)
            cumulative += new
            rows.append({"week": w, "new_dropouts": new, "cumulative_dropouts": cumulative})
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------------

    def summary(self) -> Dict:
        """Return a dict of headline metrics for the run."""
        self._assert_ran()
        df = self.student_dataframe()
        gpas = df["gpa_proxy"].tolist()
        return {
            "n_students": self.cfg.n_students,
            "n_weeks": self.cfg.n_weeks,
            "mean_gpa": round(float(df["gpa_proxy"].mean()), 4),
            "std_gpa": round(float(df["gpa_proxy"].std()), 4),
            "failure_rate": round(float((df["gpa_proxy"] < 2.0).mean()), 4),
            "mean_final_knowledge": round(float(df["final_knowledge"].mean()), 4),
            "mean_final_stress": round(float(df["final_stress"].mean()), 4),
            "mean_attendance_rate": round(float(df["attendance_rate"].mean()), 4),
            "mean_completion_rate": round(float(df["completion_rate"].mean()), 4),
            # --- NEW ---
            "dropout_rate": round(float(df["dropped_out"].mean()), 4),
            "at_risk_rate": round(float(df["at_risk"].mean()), 4),
            "gini_gpa": round(compute_gini(gpas), 4),
            "mean_satisfaction": round(float(df["final_satisfaction"].mean()), 4),
            "mean_final_fatigue": round(float(df["final_fatigue"].mean()), 4),
        }

    # ------------------------------------------------------------------
    # Export helpers
    # ------------------------------------------------------------------

    def save(self, output_dir: Path) -> Path:
        """
        Save all outputs to *output_dir*:
          - config.json
          - students.csv
          - class_weekly.csv
          - summary.json

        Returns the directory path for chaining.
        """
        self._assert_ran()
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        (output_dir / "config.json").write_text(
            self.cfg.model_dump_json(indent=2)
        )
        self.student_dataframe().to_csv(output_dir / "students.csv", index=False)
        self.weekly_dataframe().to_csv(output_dir / "class_weekly.csv", index=False)
        (output_dir / "summary.json").write_text(json.dumps(self.summary(), indent=2))

        return output_dir

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _assert_ran(self) -> None:
        if not self._ran:
            raise RuntimeError("Call model.run() before accessing results.")
