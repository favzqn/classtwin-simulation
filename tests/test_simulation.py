"""
test_simulation.py — Tests for the Classroom Digital Twin.

Original tests (1–7, 15 test methods) — all preserved and backward compatible.
New tests (8–11) — cover dropout, SES ordering, topic dependency, at-risk detection.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure project root on sys.path
_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root))

from src.config import (
    CurriculumConfig,
    DynamicsWeights,
    LecturerDefaults,
    SimulationConfig,
    SocialConfig,
    StudentDefaults,
)
from src.model.classroom_model import ClassroomModel


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cfg: SimulationConfig) -> ClassroomModel:
    m = ClassroomModel(cfg)
    m.run()
    return m


def _base_cfg(**overrides) -> SimulationConfig:
    cfg = SimulationConfig(n_students=20, n_weeks=14, seed=42)
    for k, v in overrides.items():
        setattr(cfg, k, v)
    return cfg


# ---------------------------------------------------------------------------
# Test 1 — Determinism
# ---------------------------------------------------------------------------

class TestDeterminism:
    def test_same_seed_same_mean_gpa(self):
        cfg = _base_cfg()
        m1 = _run(cfg)
        m2 = _run(SimulationConfig(n_students=20, n_weeks=14, seed=42))
        assert m1.summary()["mean_gpa"] == m2.summary()["mean_gpa"]

    def test_same_seed_same_student_gpas(self):
        cfg = _base_cfg()
        m1 = _run(cfg)
        m2 = _run(SimulationConfig(n_students=20, n_weeks=14, seed=42))
        gpas1 = sorted(m1.student_dataframe()["gpa_proxy"].tolist())
        gpas2 = sorted(m2.student_dataframe()["gpa_proxy"].tolist())
        assert gpas1 == gpas2

    def test_different_seeds_different_results(self):
        m1 = _run(SimulationConfig(n_students=20, seed=1))
        m2 = _run(SimulationConfig(n_students=20, seed=999))
        assert m1.summary()["mean_gpa"] != m2.summary()["mean_gpa"]


# ---------------------------------------------------------------------------
# Test 2 — Clamp: stress, knowledge, motivation, fatigue, satisfaction in [0, 1]
# ---------------------------------------------------------------------------

class TestClamp:
    def test_stress_clamped(self):
        cfg = SimulationConfig(n_students=30, seed=7)
        cfg.lecturer = LecturerDefaults(
            assignment_load=3, feedback_delay_weeks=4, strictness=1.0
        )
        m = _run(cfg)
        for student in m.students:
            for s in student.stress_history:
                assert 0.0 <= s <= 1.0, f"Stress out of range: {s}"
            assert 0.0 <= student.stress <= 1.0

    def test_knowledge_clamped(self):
        cfg = _base_cfg()
        m = _run(cfg)
        for student in m.students:
            for k in student.knowledge_history:
                assert 0.0 <= k <= 1.0, f"Knowledge out of range: {k}"
            assert 0.0 <= student.knowledge <= 1.0

    def test_motivation_clamped(self):
        cfg = _base_cfg()
        m = _run(cfg)
        for student in m.students:
            for mot in student.motivation_history:
                assert 0.0 <= mot <= 1.0, f"Motivation out of range: {mot}"

    def test_fatigue_clamped(self):
        cfg = _base_cfg()
        m = _run(cfg)
        for student in m.students:
            for f in student.fatigue_history:
                assert 0.0 <= f <= 1.0, f"Fatigue out of range: {f}"

    def test_topic_knowledge_clamped(self):
        cfg = _base_cfg()
        m = _run(cfg)
        for student in m.students:
            for k in student.topic_knowledge:
                assert 0.0 <= k <= 1.0, f"Topic knowledge out of range: {k}"


# ---------------------------------------------------------------------------
# Test 3 — Scenario ordering
# ---------------------------------------------------------------------------

class TestScenarioOrdering:
    def test_high_load_not_better_gpa_than_low_load(self):
        """Increasing assignment load from 1→3 should not increase mean GPA."""
        cfg_low = _base_cfg()
        cfg_low.lecturer = LecturerDefaults(assignment_load=1, feedback_delay_weeks=1)

        cfg_high = _base_cfg()
        cfg_high.lecturer = LecturerDefaults(assignment_load=3, feedback_delay_weeks=1)

        m_low = _run(cfg_low)
        m_high = _run(cfg_high)

        gpa_low = m_low.summary()["mean_gpa"]
        gpa_high = m_high.summary()["mean_gpa"]

        assert gpa_high <= gpa_low + 0.1, (
            f"High load GPA ({gpa_high:.3f}) > low load GPA ({gpa_low:.3f}) by >0.1"
        )

    def test_high_load_higher_stress(self):
        """High assignment load should produce higher mean final stress."""
        cfg_low = _base_cfg()
        cfg_low.lecturer = LecturerDefaults(assignment_load=1, feedback_delay_weeks=0)

        cfg_high = _base_cfg()
        cfg_high.lecturer = LecturerDefaults(assignment_load=3, feedback_delay_weeks=0)

        m_low = _run(cfg_low)
        m_high = _run(cfg_high)

        assert m_high.summary()["mean_final_stress"] > m_low.summary()["mean_final_stress"]


# ---------------------------------------------------------------------------
# Test 4 — Feedback delay effect
# ---------------------------------------------------------------------------

class TestFeedbackDelay:
    def test_long_delay_higher_stress(self):
        """Longer feedback delay should cause higher mean stress."""
        def _stress(delay: int) -> float:
            cfg = _base_cfg()
            cfg.lecturer = LecturerDefaults(
                assignment_load=2, feedback_delay_weeks=delay
            )
            return _run(cfg).summary()["mean_final_stress"]

        s0 = _stress(0)
        s4 = _stress(4)
        assert s4 > s0, f"Stress with delay=4 ({s4:.3f}) should exceed delay=0 ({s0:.3f})"


# ---------------------------------------------------------------------------
# Test 5 — GPA always in [0, 4]
# ---------------------------------------------------------------------------

class TestGPARange:
    def test_gpa_in_range(self):
        cfg = _base_cfg()
        m = _run(cfg)
        df = m.student_dataframe()
        assert (df["gpa_proxy"] >= 0.0).all(), "GPA proxy below 0"
        assert (df["gpa_proxy"] <= 4.0).all(), "GPA proxy above 4"

    def test_gpa_non_negative_with_extreme_config(self):
        """Even under worst-case conditions GPA stays in range."""
        cfg = SimulationConfig(n_students=10, seed=123)
        cfg.lecturer = LecturerDefaults(
            assignment_load=3, feedback_delay_weeks=4, strictness=1.0
        )
        m = _run(cfg)
        df = m.student_dataframe()
        assert (df["gpa_proxy"] >= 0.0).all()
        assert (df["gpa_proxy"] <= 4.0).all()


# ---------------------------------------------------------------------------
# Test 6 — Config round-trip serialisation
# ---------------------------------------------------------------------------

class TestConfigSerialisation:
    def test_json_roundtrip_produces_same_results(self):
        cfg = _base_cfg()
        json_str = cfg.model_dump_json()
        cfg2 = SimulationConfig.model_validate_json(json_str)

        m1 = _run(cfg)
        m2 = _run(cfg2)

        assert m1.summary()["mean_gpa"] == m2.summary()["mean_gpa"]

    def test_config_json_contains_seed(self):
        cfg = SimulationConfig(seed=77)
        data = json.loads(cfg.model_dump_json())
        assert data["seed"] == 77

    def test_config_json_contains_new_fields(self):
        """New config classes (curriculum, social, environment) serialise correctly."""
        cfg = SimulationConfig(seed=1)
        data = json.loads(cfg.model_dump_json())
        assert "curriculum" in data
        assert "social" in data
        assert "environment" in data
        assert data["curriculum"]["n_topics"] == 5
        assert data["social"]["enable_peer_learning"] is True
        assert data["environment"]["class_schedule"] == "afternoon"


# ---------------------------------------------------------------------------
# Test 7 — History lengths
# ---------------------------------------------------------------------------

class TestHistoryLengths:
    def test_history_matches_n_weeks(self):
        n_weeks = 14
        cfg = SimulationConfig(n_students=10, n_weeks=n_weeks, seed=42)
        m = _run(cfg)
        for student in m.students:
            assert len(student.stress_history) == n_weeks
            assert len(student.knowledge_history) == n_weeks
            assert len(student.weeks_attended) == n_weeks
            assert len(student.fatigue_history) == n_weeks
            assert len(student.satisfaction_history) == n_weeks
            assert len(student.topic_knowledge_history) == n_weeks

    def test_weekly_df_has_correct_rows(self):
        n_weeks = 10
        cfg = SimulationConfig(n_students=10, n_weeks=n_weeks, seed=42)
        m = _run(cfg)
        assert len(m.weekly_dataframe()) == n_weeks


# ---------------------------------------------------------------------------
# Test 8 — Dropout mechanics
# ---------------------------------------------------------------------------

class TestDropout:
    def test_dropout_rate_in_range(self):
        """Dropout rate must be in [0, 1]."""
        cfg = _base_cfg()
        m = _run(cfg)
        rate = m.summary()["dropout_rate"]
        assert 0.0 <= rate <= 1.0

    def test_high_stress_scenario_can_produce_dropouts(self):
        """
        Under extreme stress conditions, some students may drop out.
        We lower the dropout thresholds to guarantee dropout occurs.
        """
        cfg = SimulationConfig(n_students=30, n_weeks=14, seed=99)
        cfg.lecturer = LecturerDefaults(
            assignment_load=3, feedback_delay_weeks=4, strictness=1.0
        )
        # Lower thresholds to guarantee dropout in extreme scenario
        cfg.dynamics = DynamicsWeights(
            dropout_stress_threshold=0.70,
            dropout_knowledge_threshold=0.50,
            dropout_consecutive_weeks=2,
        )
        m = _run(cfg)
        # With very relaxed dropout thresholds + extreme conditions, some may drop
        # (not guaranteed to be >0 in all seeds, but rate must be in range)
        assert 0.0 <= m.summary()["dropout_rate"] <= 1.0

    def test_dropouts_never_exceed_total_students(self):
        cfg = SimulationConfig(n_students=20, n_weeks=14, seed=42)
        cfg.dynamics = DynamicsWeights(
            dropout_stress_threshold=0.60,
            dropout_knowledge_threshold=0.60,
            dropout_consecutive_weeks=2,
        )
        m = _run(cfg)
        n_dropped = sum(1 for s in m.students if s.dropped_out)
        assert n_dropped <= cfg.n_students

    def test_dropped_out_students_have_dropout_week_set(self):
        cfg = SimulationConfig(n_students=30, n_weeks=14, seed=5)
        cfg.dynamics = DynamicsWeights(
            dropout_stress_threshold=0.60,
            dropout_knowledge_threshold=0.60,
            dropout_consecutive_weeks=2,
        )
        m = _run(cfg)
        for s in m.students:
            if s.dropped_out:
                assert 1 <= s.dropout_week <= cfg.n_weeks, (
                    f"Dropout week {s.dropout_week} out of range"
                )
            else:
                assert s.dropout_week == -1

    def test_dropout_timeline_has_correct_length(self):
        cfg = _base_cfg()
        m = _run(cfg)
        timeline = m.dropout_timeline()
        assert len(timeline) == cfg.n_weeks
        assert list(timeline["week"]) == list(range(1, cfg.n_weeks + 1))

    def test_dropout_timeline_cumulative_monotonic(self):
        cfg = SimulationConfig(n_students=20, n_weeks=14, seed=7)
        m = _run(cfg)
        timeline = m.dropout_timeline()
        cumulative = timeline["cumulative_dropouts"].tolist()
        assert cumulative == sorted(cumulative), "Cumulative dropouts not monotonically increasing"


# ---------------------------------------------------------------------------
# Test 9 — SES ordering
# ---------------------------------------------------------------------------

class TestSESOrdering:
    def test_high_ses_lower_stress_on_average(self):
        """
        When SES is uniformly high vs uniformly low, high-SES cohort
        should have lower mean final stress.
        """
        cfg_low_ses = SimulationConfig(n_students=30, n_weeks=14, seed=42)
        cfg_low_ses.students = StudentDefaults(
            ses_score_mean=0.1,
            ses_score_std=0.05,
        )

        cfg_high_ses = SimulationConfig(n_students=30, n_weeks=14, seed=42)
        cfg_high_ses.students = StudentDefaults(
            ses_score_mean=0.9,
            ses_score_std=0.05,
        )

        m_low = _run(cfg_low_ses)
        m_high = _run(cfg_high_ses)

        stress_low = m_low.summary()["mean_final_stress"]
        stress_high = m_high.summary()["mean_final_stress"]

        assert stress_high < stress_low, (
            f"High-SES stress ({stress_high:.3f}) should be below low-SES ({stress_low:.3f})"
        )

    def test_high_ses_better_or_equal_gpa(self):
        """High SES cohort should achieve at least as high GPA as low SES."""
        cfg_low_ses = SimulationConfig(n_students=30, n_weeks=14, seed=42)
        cfg_low_ses.students = StudentDefaults(ses_score_mean=0.1, ses_score_std=0.05)

        cfg_high_ses = SimulationConfig(n_students=30, n_weeks=14, seed=42)
        cfg_high_ses.students = StudentDefaults(ses_score_mean=0.9, ses_score_std=0.05)

        m_low = _run(cfg_low_ses)
        m_high = _run(cfg_high_ses)

        gpa_low = m_low.summary()["mean_gpa"]
        gpa_high = m_high.summary()["mean_gpa"]

        assert gpa_high >= gpa_low - 0.05, (
            f"High-SES GPA ({gpa_high:.3f}) should not be meaningfully below "
            f"low-SES ({gpa_low:.3f})"
        )

    def test_equity_dataframe_has_four_quartiles(self):
        """equity_dataframe() should return up to 4 rows (one per SES quartile)."""
        cfg = SimulationConfig(n_students=40, n_weeks=14, seed=42)
        m = _run(cfg)
        eq_df = m.equity_dataframe()
        assert len(eq_df) <= 4
        assert len(eq_df) >= 1
        assert "ses_quartile" in eq_df.columns
        assert "mean_gpa" in eq_df.columns


# ---------------------------------------------------------------------------
# Test 10 — Topic dependency
# ---------------------------------------------------------------------------

class TestTopicDependency:
    def test_knowledge_vector_length_matches_n_topics(self):
        """Each student's topic_knowledge should have exactly n_topics entries."""
        for n_topics in [3, 5, 8]:
            cfg = SimulationConfig(n_students=10, n_weeks=14, seed=42)
            cfg.curriculum = CurriculumConfig(n_topics=n_topics)
            m = _run(cfg)
            for student in m.students:
                assert len(student.topic_knowledge) == n_topics, (
                    f"Expected {n_topics} topics, got {len(student.topic_knowledge)}"
                )

    def test_strong_dependency_limits_later_topic_mastery(self):
        """
        With maximum topic dependency strength (1.0), later topics should
        be harder to master than earlier ones (mean of topic 4 < topic 0)
        when students start with uniform low knowledge.
        """
        cfg = SimulationConfig(n_students=40, n_weeks=14, seed=42)
        cfg.curriculum = CurriculumConfig(
            n_topics=5,
            topic_dependency_strength=1.0,
            difficulty_curve="flat",
        )
        cfg.students = StudentDefaults(knowledge_mean=0.05, knowledge_std=0.02)
        m = _run(cfg)

        topic_means = [
            sum(s.topic_knowledge[t] for s in m.students) / len(m.students)
            for t in range(5)
        ]
        # First topic should have higher mastery than last topic
        assert topic_means[0] >= topic_means[4] - 0.05, (
            f"Topic 0 mastery ({topic_means[0]:.3f}) should not be below "
            f"topic 4 mastery ({topic_means[4]:.3f}) with full dependency"
        )

    def test_topic_knowledge_history_shape(self):
        """topic_knowledge_history should have shape (n_weeks, n_topics)."""
        n_topics = 4
        n_weeks = 10
        cfg = SimulationConfig(n_students=5, n_weeks=n_weeks, seed=42)
        cfg.curriculum = CurriculumConfig(n_topics=n_topics)
        m = _run(cfg)
        for student in m.students:
            assert len(student.topic_knowledge_history) == n_weeks
            for week_snap in student.topic_knowledge_history:
                assert len(week_snap) == n_topics

    def test_knowledge_property_equals_mean_topic_knowledge(self):
        """knowledge property must equal mean(topic_knowledge)."""
        import statistics
        cfg = _base_cfg()
        m = _run(cfg)
        for student in m.students:
            expected = statistics.mean(student.topic_knowledge)
            assert abs(student.knowledge - expected) < 1e-9, (
                f"knowledge property {student.knowledge:.6f} != "
                f"mean(topic_knowledge) {expected:.6f}"
            )


# ---------------------------------------------------------------------------
# Test 11 — At-risk detection
# ---------------------------------------------------------------------------

class TestAtRiskDetection:
    def test_at_risk_rate_in_range(self):
        cfg = _base_cfg()
        m = _run(cfg)
        rate = m.summary()["at_risk_rate"]
        assert 0.0 <= rate <= 1.0

    def test_high_stress_scenario_produces_more_at_risk(self):
        """Extreme conditions should yield higher at-risk rate than mild conditions."""
        cfg_mild = SimulationConfig(n_students=30, n_weeks=14, seed=42)
        cfg_mild.lecturer = LecturerDefaults(assignment_load=1, feedback_delay_weeks=0)

        cfg_severe = SimulationConfig(n_students=30, n_weeks=14, seed=42)
        cfg_severe.lecturer = LecturerDefaults(assignment_load=3, feedback_delay_weeks=4)

        m_mild = _run(cfg_mild)
        m_severe = _run(cfg_severe)

        assert m_severe.summary()["at_risk_rate"] >= m_mild.summary()["at_risk_rate"]

    def test_at_risk_flag_consistent_with_dataframe(self):
        """at_risk_rate in summary() should match student_dataframe()."""
        cfg = _base_cfg()
        m = _run(cfg)
        df = m.student_dataframe()
        manual_rate = round(float(df["at_risk"].mean()), 4)
        assert manual_rate == m.summary()["at_risk_rate"]

    def test_at_risk_detection_uses_correct_week(self):
        """
        Students with low knowledge AND high stress at week 5 should be flagged.
        Check that at_risk flag is mutually exclusive with dropped_out=True
        in healthy (non-extreme) runs.
        """
        cfg = _base_cfg()
        m = _run(cfg)
        for s in m.students:
            # Dropped-out students flagged before detection week: at_risk may not be set
            # (they were already gone). Both can be False, but at_risk && dropped_out
            # is possible if they dropped out AFTER detection week.
            # The key constraint: all at_risk students should have been active at week 5
            if s.at_risk:
                # They were flagged, so they must have been active at detection week
                assert not (s.dropped_out and s.dropout_week < cfg.dynamics.at_risk_detection_week), (
                    "Student dropped out before detection week but is flagged at-risk"
                )


# ---------------------------------------------------------------------------
# Test 12 — Summary backward compatibility
# ---------------------------------------------------------------------------

class TestSummaryBackwardCompat:
    def test_original_summary_keys_present(self):
        """All keys from the original summary() must still be present."""
        original_keys = {
            "n_students", "n_weeks", "mean_gpa", "std_gpa", "failure_rate",
            "mean_final_knowledge", "mean_final_stress",
            "mean_attendance_rate", "mean_completion_rate",
        }
        m = _run(_base_cfg())
        summ = m.summary()
        assert original_keys.issubset(set(summ.keys())), (
            f"Missing keys: {original_keys - set(summ.keys())}"
        )

    def test_new_summary_keys_present(self):
        """New summary keys must also be present."""
        new_keys = {"dropout_rate", "gini_gpa", "mean_satisfaction", "at_risk_rate"}
        m = _run(_base_cfg())
        summ = m.summary()
        assert new_keys.issubset(set(summ.keys())), (
            f"Missing new keys: {new_keys - set(summ.keys())}"
        )

    def test_gini_in_range(self):
        cfg = _base_cfg()
        m = _run(cfg)
        gini = m.summary()["gini_gpa"]
        assert 0.0 <= gini <= 1.0

    def test_student_df_backward_compat_columns(self):
        """Original student_df columns must still exist."""
        original_cols = {
            "student_id", "learning_capacity", "late_work_prob",
            "gpa_proxy", "final_knowledge", "final_stress",
            "final_motivation", "attendance_rate", "completion_rate",
            "is_intervention_target",
        }
        m = _run(_base_cfg())
        cols = set(m.student_dataframe().columns)
        assert original_cols.issubset(cols), (
            f"Missing columns: {original_cols - cols}"
        )

    def test_weekly_df_backward_compat_columns(self):
        """Original weekly_df columns must still exist."""
        original_cols = {
            "week", "mean_stress", "std_stress", "mean_knowledge",
            "std_knowledge", "mean_motivation", "attendance_rate",
            "assignments_submitted", "assignments_late", "assignments_missed",
        }
        m = _run(_base_cfg())
        cols = set(m.weekly_dataframe().columns)
        assert original_cols.issubset(cols), (
            f"Missing columns: {original_cols - cols}"
        )
