"""
scenarios.py — Named scenario configurations for policy comparison experiments.

Each scenario is a SimulationConfig variant.  Scenarios are designed so
that the Streamlit app and the batch runner can enumerate them by name.

Original scenarios:
    baseline           — 30 students, 1-week delay, 2 assignments/week
    large_class        — 60 students, else baseline
    small_class        — 15 students, else baseline
    fast_feedback      — feedback delay = 0
    slow_feedback      — feedback delay = 4
    low_load           — 1 assignment/week
    high_load          — 3 assignments/week
    stress_test        — 60 students + 3 assignments + 4-week delay (worst case)
    intervention       — baseline + tutoring weeks 7–10 for bottom 25%

New scenarios (Tier 3/4):
    ses_diverse        — high SES variance; reveals equity gaps
    morning_class      — early schedule penalty on attendance/motivation
    evening_class      — evening schedule; fatigue compound effect
    adaptive_lecturer  — lecturer adapts effectiveness to class performance
    no_peer_learning   — disable study groups; tests peer learning value
    combined_intervention — fast feedback + low load + tutoring (best case)
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict

from ..config import (
    CurriculumConfig,
    EnvironmentConfig,
    InterventionConfig,
    LecturerDefaults,
    SimulationConfig,
    SocialConfig,
    StudentDefaults,
)


def _base() -> SimulationConfig:
    """Fresh baseline config (same seed so comparisons are fair)."""
    return SimulationConfig(seed=42)


# ---------------------------------------------------------------------------
# Original scenarios (preserved, backward compatible)
# ---------------------------------------------------------------------------

def _scenario_baseline() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer.feedback_delay_weeks = 1
    cfg.lecturer.assignment_load = 2
    return cfg


def _scenario_large_class() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 60
    cfg.lecturer.feedback_delay_weeks = 1
    cfg.lecturer.assignment_load = 2
    return cfg


def _scenario_small_class() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 15
    cfg.lecturer.feedback_delay_weeks = 1
    cfg.lecturer.assignment_load = 2
    return cfg


def _scenario_fast_feedback() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer.feedback_delay_weeks = 0
    cfg.lecturer.assignment_load = 2
    return cfg


def _scenario_slow_feedback() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer.feedback_delay_weeks = 4
    cfg.lecturer.assignment_load = 2
    return cfg


def _scenario_low_load() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer.feedback_delay_weeks = 1
    cfg.lecturer.assignment_load = 1
    return cfg


def _scenario_high_load() -> SimulationConfig:
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer.feedback_delay_weeks = 1
    cfg.lecturer.assignment_load = 3
    return cfg


def _scenario_stress_test() -> SimulationConfig:
    """Worst-case combined: 60 students, 3 assignments, 4-week delay."""
    cfg = _base()
    cfg.n_students = 60
    cfg.lecturer.feedback_delay_weeks = 4
    cfg.lecturer.assignment_load = 3
    return cfg


def _scenario_tutoring_high_stress() -> SimulationConfig:
    """Worst-case stress + tutoring intervention for bottom 25%."""
    cfg = _base()
    cfg.n_students = 60
    cfg.lecturer.feedback_delay_weeks = 4
    cfg.lecturer.assignment_load = 3
    cfg.intervention = InterventionConfig(
        enabled=True,
        start_week=7,
        end_week=10,
        motivation_boost=0.10,
        stress_reduction=0.10,
        target_quantile=0.25,
    )
    return cfg


def _scenario_intervention() -> SimulationConfig:
    """Baseline + tutoring weeks 7–10 for bottom 25% students."""
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer.feedback_delay_weeks = 1
    cfg.lecturer.assignment_load = 2
    cfg.intervention = InterventionConfig(
        enabled=True,
        start_week=7,
        end_week=10,
        motivation_boost=0.10,
        stress_reduction=0.10,
        target_quantile=0.25,
    )
    return cfg


# ---------------------------------------------------------------------------
# New scenarios
# ---------------------------------------------------------------------------

def _scenario_ses_diverse() -> SimulationConfig:
    """
    High SES variance (std=0.40) — reveals equity gaps.

    Expected finding: Gini coefficient of GPA increases; low-SES students
    are disproportionately represented in failures and dropouts.
    """
    cfg = _base()
    cfg.n_students = 30
    cfg.students = StudentDefaults(
        ses_score_mean=0.5,
        ses_score_std=0.40,   # high variance (matches Bab 3 Table 3.5)
    )
    return cfg


def _scenario_morning_class() -> SimulationConfig:
    """
    Morning schedule — slight attendance and motivation penalty.

    Expected finding: marginally lower attendance rate and mean GPA
    compared to afternoon baseline.
    """
    cfg = _base()
    cfg.n_students = 30
    cfg.environment = EnvironmentConfig(
        class_schedule="morning",
        external_pressure=0.3,
        mid_semester_slump_strength=0.12,
    )
    return cfg


def _scenario_evening_class() -> SimulationConfig:
    """
    Evening schedule — stronger motivation penalty and fatigue compounding.

    Expected finding: lower mean GPA than morning; higher fatigue;
    worse performance for high-external-pressure students.
    """
    cfg = _base()
    cfg.n_students = 30
    cfg.environment = EnvironmentConfig(
        class_schedule="evening",
        external_pressure=0.4,   # evening students often have other obligations
        mid_semester_slump_strength=0.15,
    )
    return cfg


def _scenario_adaptive_lecturer() -> SimulationConfig:
    """
    Lecturer with high adaptivity (0.8) — responds to class knowledge gaps.

    Expected finding: partially buffers against struggling students;
    smaller long-tail of failures; slightly lower overall GPA variance.
    """
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer = LecturerDefaults(
        teaching_effectiveness=1.0,
        feedback_delay_weeks=1,
        assignment_load=2,
        strictness=0.5,
        adaptivity=0.8,
        adaptation_threshold=0.40,
        adaptation_boost=0.15,
    )
    return cfg


def _scenario_no_peer_learning() -> SimulationConfig:
    """
    Peer learning disabled — tests the value of study groups.

    Expected finding: lower mean knowledge; higher variance in outcomes;
    weaker students benefit less without knowledge transfer from peers.
    """
    cfg = _base()
    cfg.n_students = 30
    cfg.social = SocialConfig(
        enable_peer_learning=False,
    )
    return cfg


def _scenario_hot_classroom() -> SimulationConfig:
    """Hot classroom (32°C) — no AC or broken HVAC. Relevant for tropical campuses."""
    cfg = _base()
    cfg.n_students = 30
    cfg.environment = EnvironmentConfig(
        class_schedule="afternoon",
        external_pressure=0.3,
        mid_semester_slump_strength=0.12,
        room_temp_celsius=32.0,
        class_mode="in_person",
    )
    return cfg


def _scenario_cold_classroom() -> SimulationConfig:
    """Cold classroom (16°C) — over-airconditioned room."""
    cfg = _base()
    cfg.n_students = 30
    cfg.environment = EnvironmentConfig(
        class_schedule="afternoon",
        external_pressure=0.3,
        mid_semester_slump_strength=0.12,
        room_temp_celsius=16.0,
        class_mode="in_person",
    )
    return cfg


def _scenario_online_class() -> SimulationConfig:
    """Fully online delivery — reduced teaching effectiveness and peer interaction."""
    cfg = _base()
    cfg.n_students = 30
    cfg.environment = EnvironmentConfig(
        class_schedule="afternoon",
        external_pressure=0.3,
        mid_semester_slump_strength=0.15,
        room_temp_celsius=22.0,
        class_mode="online",
    )
    return cfg


def _scenario_hybrid_class() -> SimulationConfig:
    """Hybrid delivery — mix of in-person and online sessions."""
    cfg = _base()
    cfg.n_students = 30
    cfg.environment = EnvironmentConfig(
        class_schedule="afternoon",
        external_pressure=0.3,
        mid_semester_slump_strength=0.13,
        room_temp_celsius=22.0,
        class_mode="hybrid",
    )
    return cfg


def _scenario_combined_intervention() -> SimulationConfig:
    """
    Combined best-case intervention: fast feedback + low load + tutoring.

    Expected finding: highest mean GPA; lowest failure rate; lowest
    dropout; best satisfaction. Represents the ceiling scenario for
    policy evaluation.
    """
    cfg = _base()
    cfg.n_students = 30
    cfg.lecturer = LecturerDefaults(
        teaching_effectiveness=1.2,
        feedback_delay_weeks=0,   # immediate feedback
        assignment_load=1,         # low load
        strictness=0.3,
        adaptivity=0.5,
        adaptation_threshold=0.40,
        adaptation_boost=0.15,
    )
    cfg.intervention = InterventionConfig(
        enabled=True,
        start_week=5,
        end_week=12,
        motivation_boost=0.12,
        stress_reduction=0.12,
        target_quantile=0.30,
    )
    return cfg


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

SCENARIOS: Dict[str, SimulationConfig] = {
    "baseline":               _scenario_baseline(),
    "large_class":            _scenario_large_class(),
    "small_class":            _scenario_small_class(),
    "fast_feedback":          _scenario_fast_feedback(),
    "slow_feedback":          _scenario_slow_feedback(),
    "low_load":               _scenario_low_load(),
    "high_load":              _scenario_high_load(),
    "stress_test":            _scenario_stress_test(),
    "intervention":           _scenario_intervention(),
    "tutoring_high_stress":   _scenario_tutoring_high_stress(),
    # --- new ---
    "ses_diverse":            _scenario_ses_diverse(),
    "morning_class":          _scenario_morning_class(),
    "evening_class":          _scenario_evening_class(),
    "adaptive_lecturer":      _scenario_adaptive_lecturer(),
    "no_peer_learning":       _scenario_no_peer_learning(),
    "combined_intervention":  _scenario_combined_intervention(),
    # --- environment ---
    "hot_classroom":          _scenario_hot_classroom(),
    "cold_classroom":         _scenario_cold_classroom(),
    "online_class":           _scenario_online_class(),
    "hybrid_class":           _scenario_hybrid_class(),
}

# Human-readable labels for UI
SCENARIO_LABELS: Dict[str, str] = {
    "baseline":               "Standard Class",
    "large_class":            "Large Class (60 students)",
    "small_class":            "Small Class (15 students)",
    "fast_feedback":          "Immediate Feedback (same-week return)",
    "slow_feedback":          "Delayed Feedback (4-week return)",
    "low_load":               "Light Workload (1 task/week)",
    "high_load":              "Heavy Workload (3 tasks/week)",
    "stress_test":            "Worst-Case Scenario (large class + overload + slow feedback)",
    "intervention":           "Tutoring Support Program (weeks 7–10)",
    "tutoring_high_stress":   "Tutoring Under Worst-Case Conditions",
    # --- new ---
    "ses_diverse":            "High Socioeconomic Diversity",
    "morning_class":          "Morning Schedule",
    "evening_class":          "Evening Schedule",
    "adaptive_lecturer":      "Adaptive Teaching Style",
    "no_peer_learning":       "No Study Groups",
    "combined_intervention":  "Best-Practice Bundle",
    # --- environment ---
    "hot_classroom":          "Hot Classroom (32°C, no AC)",
    "cold_classroom":         "Cold Classroom (16°C, over-AC)",
    "online_class":           "Fully Online Delivery",
    "hybrid_class":           "Hybrid Delivery (in-person + online)",
}


def get_scenario(name: str) -> SimulationConfig:
    """Return a *deep copy* of the named scenario config."""
    if name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        raise KeyError(f"Unknown scenario '{name}'. Available: {available}")
    return deepcopy(SCENARIOS[name])
