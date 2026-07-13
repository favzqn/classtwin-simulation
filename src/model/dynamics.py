"""
dynamics.py — Weekly update rules for the Classroom Digital Twin.

All functions here are *pure* (no side effects on agents) so they can be
unit-tested independently.  The ClassroomModel calls them and applies the
returned values back to agent state.

Design decisions (thesis-defensible):
--------------------------------------
1. Attendance is a Bernoulli draw whose probability is modulated by
   current stress and motivation (Credé & Kuncel 2008).

2. Knowledge gain follows a multiplicative model:
       Δk = base_rate × attended × effectiveness × capacity × g(motivation, stress)
            × topic_dependency × difficulty × fatigue_penalty × slump
   where g = motivation × (1 - stress).

3. Stress accumulates from workload and unresolved uncertainty (pending
   feedback) and decays via rest, SES support, and grit recovery, reflecting
   self-determination theory (Ryan & Deci 2000).

4. Topic dependency chains: mastery of topic N gates learning of topic N+1,
   representing prerequisite knowledge structures common in STEM curricula.

5. Exam weeks consolidate existing knowledge without new topic learning,
   producing a transient stress spike followed by cognitive relief.

6. Peer learning within heterogeneous study groups allows the most advanced
   student to transfer knowledge to weaker group members (Vygotsky 1978).

7. Fatigue accumulates from cognitive load and external pressure, reducing
   effective learning rate (Kahneman 1973).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, List

import numpy as np

if TYPE_CHECKING:
    from .agents import StudentAgent
    from ..config import SimulationConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp a float to [lo, hi]."""
    return max(lo, min(hi, value))


def _clamp4(value: float) -> float:
    return max(0.0, min(4.0, value))


# ---------------------------------------------------------------------------
# Thermal discomfort
# ---------------------------------------------------------------------------

def thermal_discomfort(room_temp: float) -> float:
    """
    Discomfort factor from suboptimal classroom temperature.

    Optimal comfort range: 20–24°C (centre 22°C, tolerance ±2°C).
    Discomfort rises linearly beyond this band, capped at 1.0.

    Examples:
        22°C → 0.00 (optimal)
        26°C → 0.25 (mildly warm)
        30°C → 0.75 (uncomfortably hot)
        32°C → 1.00 (maximum discomfort)
        16°C → 0.50 (uncomfortably cold)
    """
    excess = max(0.0, abs(room_temp - 22.0) - 2.0)
    return min(1.0, excess / 8.0)


# ---------------------------------------------------------------------------
# Attendance
# ---------------------------------------------------------------------------

def compute_attendance_prob(
    student: "StudentAgent",
    cfg: "SimulationConfig",
) -> float:
    """
    Effective attendance probability for this week.

    Formula:
        p_eff = base_prob
                - stress_penalty × stress
                + motivation_bonus × motivation
                + schedule_modifier (from EnvironmentConfig)

    Clamped to [0.05, 0.99].
    """
    dw = cfg.dynamics
    schedule_mod = cfg.environment.schedule_motivation_modifier
    mode_mods = cfg.environment.class_mode_modifiers
    discomfort = thermal_discomfort(cfg.environment.room_temp_celsius)
    p = (
        student.attendance_prob
        - dw.stress_attendance_penalty * student.stress
        + dw.motivation_attendance_bonus * student.motivation
        + schedule_mod * 0.5
        + mode_mods["attendance_bonus"]
        - 0.15 * discomfort
    )
    return _clamp(p, lo=0.05, hi=0.99)


def draw_attendance(
    student: "StudentAgent",
    cfg: "SimulationConfig",
    rng: np.random.Generator,
) -> bool:
    """Return True if the student attends this week."""
    p = compute_attendance_prob(student, cfg)
    return bool(rng.random() < p)


# ---------------------------------------------------------------------------
# Assignment completion
# ---------------------------------------------------------------------------

def compute_completion_prob(
    student: "StudentAgent",
    cfg: "SimulationConfig",
) -> float:
    """
    Probability of completing *each* assignment on time.

        p_complete = 0.85 - stress_penalty × stress + motivation_bonus × motivation
    """
    dw = cfg.dynamics
    p = (
        0.85
        - dw.stress_completion_penalty * student.stress
        + dw.motivation_completion_bonus * student.motivation
    )
    return _clamp(p, lo=0.05, hi=0.99)


def draw_assignment_outcomes(
    student: "StudentAgent",
    n_assignments: int,
    cfg: "SimulationConfig",
    rng: np.random.Generator,
) -> tuple[int, int, int]:
    """
    For each assignment this week determine: submitted-on-time, late, missed.

    Returns (submitted, late, missed).
    """
    if n_assignments == 0:
        return 0, 0, 0

    p_on_time = compute_completion_prob(student, cfg)
    p_late_given_not_ontime = _clamp(student.late_work_prob * (1.0 - student.stress * 0.5))

    submitted = 0
    late = 0
    missed = 0
    for _ in range(n_assignments):
        r = rng.random()
        if r < p_on_time:
            submitted += 1
        elif r < p_on_time + (1.0 - p_on_time) * p_late_given_not_ontime:
            late += 1
        else:
            missed += 1
    return submitted, late, missed


# ---------------------------------------------------------------------------
# Stress update
# ---------------------------------------------------------------------------

def update_stress(
    student: "StudentAgent",
    attended: bool,
    received_feedback: bool,
    cfg: "SimulationConfig",
) -> float:
    """
    New stress value after applying this week's events (before SES/grit adjustments).

    Stress drivers:
        + w_load × assignment_load
        + w_pending × pending_feedback_weeks
        + w_absence × (not attended)
        + external_pressure × 0.02

    Stress reducers:
        - w_feedback_relief  (if feedback arrived)
        - w_rest             (baseline weekly recovery)

    Returns the new stress clamped to [0, 1].
    """
    dw = cfg.dynamics
    lect = cfg.lecturer

    delta = (
        dw.w_stress_load * lect.assignment_load
        + dw.w_stress_pending_feedback * student.pending_feedback_weeks
        + dw.w_stress_absence * (0 if attended else 1)
        + cfg.environment.external_pressure * 0.02
        - dw.w_stress_feedback_relief * (1 if received_feedback else 0)
        - dw.w_stress_rest
    )
    return _clamp(student.stress + delta)


def ses_stress_adjustment(ses_score: float, w_ses: float) -> float:
    """
    Weekly stress relief from socioeconomic status.

    High SES students have more academic resources, support, and financial
    security, producing lower chronic stress.

    Returns: relief ∈ [0, w_ses]
    """
    return w_ses * ses_score


def grit_recovery(grit: float, current_stress: float, w_grit: float) -> float:
    """
    Additional weekly stress recovery from grit/resilience.

    Grit moderates the impact of high stress — highly resilient students
    recover faster when stressed (Duckworth et al. 2007).

    Returns: additional relief ∈ [0, w_grit × stress]
    """
    return w_grit * grit * current_stress


# ---------------------------------------------------------------------------
# Knowledge update — topic-aware
# ---------------------------------------------------------------------------

def topic_dependency_modifier(
    topic_idx: int,
    topic_knowledge: List[float],
    strength: float,
) -> float:
    """
    Prerequisite mastery gates learning of topic_idx.

    For topic 0 (no prerequisite): always 1.0.
    For topic N>0: modifier = (1 - strength) + strength × mastery[N-1]

    At strength=0: no gating (modifier = 1.0 always).
    At strength=1: learning rate scales linearly with prereq mastery.

    Returns a float in [1-strength, 1.0].
    """
    if topic_idx == 0 or strength == 0.0:
        return 1.0
    prereq_mastery = topic_knowledge[topic_idx - 1]
    return (1.0 - strength) + strength * prereq_mastery


def get_current_topic(week_num: int, n_topics: int, n_weeks: int) -> int:
    """
    Return the 0-based topic index being taught in a given week.

    Topics are distributed evenly across the semester.
    Week 1 always starts topic 0.
    """
    # Map week_num (1-indexed) to topic index
    progress = (week_num - 1) / max(n_weeks - 1, 1)
    topic_idx = int(progress * (n_topics - 1) + 0.5)
    return min(max(topic_idx, 0), n_topics - 1)


def _difficulty_modifier(topic_idx: int, n_topics: int, curve: str) -> float:
    """
    Difficulty scaling for a given topic based on the curriculum difficulty curve.

    flat      → 1.0 for all topics
    linear    → 1.0 at topic 0, 0.7 at last topic
    steep_end → 1.0 at topic 0, 0.5 at last topic (quadratic)
    """
    if n_topics <= 1 or curve == "flat":
        return 1.0
    progress = topic_idx / (n_topics - 1)
    if curve == "linear":
        return 1.0 - 0.3 * progress
    elif curve == "steep_end":
        return 1.0 - 0.5 * (progress ** 2)
    return 1.0


def update_topic_knowledge(
    student: "StudentAgent",
    topic_idx: int,
    attended: bool,
    teaching_effectiveness: float,
    slump_factor: float,
    cfg: "SimulationConfig",
) -> List[float]:
    """
    Return updated topic_knowledge list after this week's learning.

    Only the current topic gains new knowledge; all topics decay slightly.

    Formula for current topic:
        dep  = topic_dependency_modifier(topic_idx, topic_knowledge, strength)
        diff = _difficulty_modifier(topic_idx, n_topics, curve)
        fat  = 1 - w_fatigue_penalty × fatigue
        g    = motivation × (1 - stress)
        Δk   = base_rate × attended × effectiveness × capacity × g × dep × diff × fat × slump

    All topics: k_new[i] = clamp(k[i] - decay)
    Current topic: k_new[topic_idx] += Δk
    """
    dw = cfg.dynamics
    cur = cfg.curriculum

    dep = topic_dependency_modifier(topic_idx, student.topic_knowledge,
                                    cur.topic_dependency_strength)
    diff = _difficulty_modifier(topic_idx, cur.n_topics, cur.difficulty_curve)
    fatigue_pen = 1.0 - dw.w_fatigue_learning_penalty * student.fatigue
    g = student.motivation * (1.0 - student.stress)

    delta = (
        dw.base_learning_rate
        * (1 if attended else 0)
        * teaching_effectiveness
        * student.learning_capacity
        * g
        * dep
        * diff
        * max(0.0, fatigue_pen)
        * slump_factor
    )

    # Decay all topics, then add gain to current topic
    new_tk = [_clamp(k - dw.knowledge_decay) for k in student.topic_knowledge]
    new_tk[topic_idx] = _clamp(new_tk[topic_idx] + delta)
    return new_tk


def consolidate_exam_knowledge(
    student: "StudentAgent",
    cfg: "SimulationConfig",
) -> List[float]:
    """
    Exam week: proportional knowledge consolidation (no new topic learning).

    Each topic already mastered is boosted by knowledge_consolidation fraction.
    Topics at zero are not boosted.

    Returns updated topic_knowledge list.
    """
    consolidation = cfg.curriculum.knowledge_consolidation
    return [_clamp(k + consolidation * k) for k in student.topic_knowledge]


# ---------------------------------------------------------------------------
# Mid-semester slump
# ---------------------------------------------------------------------------

def mid_semester_slump_factor(
    week_num: int,
    n_weeks: int,
    strength: float,
) -> float:
    """
    Gaussian motivation dip centred on the mid-semester point.

    Returns a multiplier in [1 - strength, 1.0].
    Peak dip (1 - strength) occurs exactly at the semester midpoint.
    """
    midpoint = (n_weeks + 1) / 2.0
    sigma = n_weeks / 6.0
    peak = math.exp(-0.5 * ((week_num - midpoint) / sigma) ** 2)
    return 1.0 - strength * peak


# ---------------------------------------------------------------------------
# Motivation update
# ---------------------------------------------------------------------------

def update_motivation(
    student: "StudentAgent",
    received_feedback: bool,
    cfg: "SimulationConfig",
) -> float:
    """
    New motivation value.

    Motivation decays slightly each week and is boosted by feedback.
    The schedule modifier applies a persistent weekly shift.
    """
    dw = cfg.dynamics
    schedule_mod = cfg.environment.schedule_motivation_modifier
    mode_mods = cfg.environment.class_mode_modifiers
    discomfort = thermal_discomfort(cfg.environment.room_temp_celsius)
    delta = (
        dw.motivation_feedback_boost * (1 if received_feedback else 0)
        - dw.motivation_decay
        - mode_mods["motivation_decay_extra"]
        - 0.015 * discomfort
        + schedule_mod * 0.005
    )
    return _clamp(student.motivation + delta)


# ---------------------------------------------------------------------------
# Fatigue update
# ---------------------------------------------------------------------------

def update_fatigue(
    student: "StudentAgent",
    attended: bool,
    cfg: "SimulationConfig",
) -> float:
    """
    Cognitive fatigue cycle.

    Fatigue accumulates from attending class and external course pressure.
    It recovers partially each week via rest.

    formula:
        if attended: fatigue += w_fatigue_gain + external_pressure × 0.02
        always:      fatigue -= w_fatigue_rest
    """
    dw = cfg.dynamics
    ext = cfg.environment.external_pressure
    mode_mods = cfg.environment.class_mode_modifiers
    delta = -dw.w_fatigue_rest
    if attended:
        delta += (dw.w_fatigue_gain + ext * 0.02) * mode_mods["fatigue_gain_mult"]
    return _clamp(student.fatigue + delta)


# ---------------------------------------------------------------------------
# Satisfaction update
# ---------------------------------------------------------------------------

def update_satisfaction(
    student: "StudentAgent",
    attended: bool,
    received_feedback: bool,
    cfg: "SimulationConfig",
) -> float:
    """
    Academic satisfaction proxy.

    Increases with feedback receipt and attendance; decreases with stress;
    has a small baseline decay representing grade pressure.
    """
    delta = (
        0.03 * (1 if received_feedback else 0)
        + 0.02 * (1 if attended else 0)
        - 0.04 * student.stress
        + 0.01 * student.motivation
        - 0.02  # baseline decay
    )
    return _clamp(student.satisfaction + delta)


# ---------------------------------------------------------------------------
# Feedback tracking
# ---------------------------------------------------------------------------

def did_receive_feedback(week: int, feedback_delay: int) -> bool:
    """
    Return True if feedback from past assignments arrives this week.

    Week is 0-indexed internally.
    """
    return week >= feedback_delay and feedback_delay >= 0


# ---------------------------------------------------------------------------
# Peer learning
# ---------------------------------------------------------------------------

def compute_peer_learning_delta(
    student: "StudentAgent",
    group_members: List["StudentAgent"],
    rate: float,
) -> List[float]:
    """
    Knowledge transfer from the strongest group member to this student.

    For each topic, the best group member's knowledge is used as the source.
    Transfer only happens when the source knows more than the recipient.

    Returns a per-topic delta list (same length as topic_knowledge).
    """
    others = [m for m in group_members
              if m.student_id != student.student_id and not m.dropped_out]
    if not others:
        return [0.0] * len(student.topic_knowledge)

    deltas = []
    for t_idx, k in enumerate(student.topic_knowledge):
        best_k = max(m.topic_knowledge[t_idx] for m in others
                     if len(m.topic_knowledge) > t_idx)
        gap = best_k - k
        deltas.append(rate * max(0.0, gap))
    return deltas


# ---------------------------------------------------------------------------
# Effective feedback quality
# ---------------------------------------------------------------------------

def effective_feedback_quality(n_students: int) -> float:
    """
    Feedback quality degrades as class size increases.

    Based on the principle that individualised feedback quality drops
    when a lecturer has more students to assess.

    Returns 1.0 at n=30, 0.5 at n=60, capped at floor of 0.5.
    """
    return max(0.5, min(1.0, 30.0 / max(n_students, 1)))


# ---------------------------------------------------------------------------
# Dropout check
# ---------------------------------------------------------------------------

def check_dropout(
    student: "StudentAgent",
    week_num: int,
    cfg: "SimulationConfig",
) -> None:
    """
    Flag a student as dropped out if they meet dropout criteria (in-place).

    Criteria:
        consecutive_high_stress_weeks >= dropout_consecutive_weeks
        AND mean knowledge < dropout_knowledge_threshold

    High-stress week is defined as stress >= dropout_stress_threshold.
    """
    if student.dropped_out:
        return

    dw = cfg.dynamics
    if student.stress >= dw.dropout_stress_threshold:
        student.consecutive_high_stress_weeks += 1
    else:
        student.consecutive_high_stress_weeks = 0

    if (student.consecutive_high_stress_weeks >= dw.dropout_consecutive_weeks
            and student.knowledge < dw.dropout_knowledge_threshold):
        student.dropped_out = True
        student.dropout_week = week_num


# ---------------------------------------------------------------------------
# GPA proxy
# ---------------------------------------------------------------------------

def compute_gpa_proxy(
    student: "StudentAgent",
    cfg: "SimulationConfig",
) -> float:
    """
    Semester-end GPA proxy on [0, 4] scale.

    Uses student.knowledge (property = mean topic mastery) — backward compatible.
    """
    total = student.total_assignments_expected
    if total == 0:
        completion_score = 1.0
    else:
        on_time = sum(student.assignments_submitted) / total
        late = sum(student.assignments_late) / total
        effective = on_time + (1.0 - cfg.lecturer.strictness) * late
        completion_score = _clamp(effective)

    raw = (
        student.knowledge * cfg.gpa_knowledge_weight
        + completion_score * cfg.gpa_completion_weight
    )
    return _clamp4(raw * 4.0)


# ---------------------------------------------------------------------------
# Intervention
# ---------------------------------------------------------------------------

def apply_intervention(
    student: "StudentAgent",
    cfg: "SimulationConfig",
) -> None:
    """
    Apply tutoring intervention to a targeted student (in-place mutation).
    """
    iv = cfg.intervention
    student.motivation = _clamp(student.motivation + iv.motivation_boost)
    student.stress = _clamp(student.stress - iv.stress_reduction)


# ---------------------------------------------------------------------------
# Gini coefficient
# ---------------------------------------------------------------------------

def compute_gini(values: List[float]) -> float:
    """
    Gini coefficient for a distribution of values.

    Returns 0 (perfect equality) to 1 (maximum inequality).
    Used to measure GPA distribution inequality across SES groups.
    """
    if len(values) < 2:
        return 0.0
    arr = sorted(values)
    n = len(arr)
    cumsum = 0.0
    for i, v in enumerate(arr):
        cumsum += (2 * (i + 1) - n - 1) * v
    total = sum(arr)
    if total == 0:
        return 0.0
    return cumsum / (n * total)
