"""
agents.py — Agent data structures for the Classroom Digital Twin.

Agents are plain Python dataclasses (no mesa dependency) so the model
stays lightweight and fully serialisable.

StudentAgent:
    Represents one enrolled student with mutable weekly state.
    knowledge is a computed property = mean(topic_knowledge) for
    backward compatibility with all existing code that reads it.

LecturerAgent:
    Represents the instructor; its parameters drive the teaching environment.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------------
# StudentAgent
# ---------------------------------------------------------------------------

@dataclass
class StudentAgent:
    """
    Mutable state for one student across the semester.

    Fixed traits (sampled once at initialisation)
    ---------------------------------------------
    student_id       : unique 0-based index
    learning_capacity: individual learning rate multiplier [0.6, 1.4]
    attendance_prob  : base attendance probability (adjusted each week)
    late_work_prob   : tendency to submit work late (fixed)
    ses_score        : socioeconomic status [0, 1] — reduces stress baseline
    grit             : resilience/persistence [0, 1] — accelerates stress recovery

    Mutable state
    -------------
    motivation       : [0, 1] intrinsic motivation
    stress           : [0, 1] academic stress
    topic_knowledge  : List[float] — mastery per curriculum topic; len = n_topics
    fatigue          : [0, 1] accumulated cognitive fatigue
    satisfaction     : [0, 1] academic satisfaction proxy

    Social
    ------
    study_group_id   : int — group index; -1 if not in a group

    Status
    ------
    dropped_out                 : permanently left the course
    at_risk                     : flagged at detection week
    consecutive_high_stress_weeks: counter for dropout trigger

    Backward-compatible properties
    --------------------------------
    knowledge         → mean(topic_knowledge)  (all read-only accesses still work)
    knowledge_history → list of mean-knowledge snapshots per week
    """

    # --- Identity & fixed traits ---
    student_id: int
    learning_capacity: float
    attendance_prob: float          # base probability, adjusted weekly
    late_work_prob: float           # fixed trait

    # --- NEW fixed traits ---
    ses_score: float = 0.5          # socioeconomic status [0, 1]
    grit: float = 0.5               # resilience [0, 1]

    # --- Mutable state ---
    motivation: float = 0.65
    stress: float = 0.25

    # --- NEW mutable state ---
    fatigue: float = 0.0            # cognitive fatigue [0, 1]
    satisfaction: float = 0.70      # academic satisfaction [0, 1]

    # --- Curriculum: per-topic knowledge vector ---
    topic_knowledge: List[float] = field(default_factory=list)
    # NOTE: scalar `knowledge` is now a @property = mean(topic_knowledge)

    # --- Semester-end metric ---
    gpa_proxy: float = 0.0

    # --- Weekly records ---
    weeks_attended: List[bool] = field(default_factory=list)
    assignments_submitted: List[int] = field(default_factory=list)
    assignments_late: List[int] = field(default_factory=list)
    assignments_missed: List[int] = field(default_factory=list)

    # --- Feedback tracking ---
    pending_feedback_weeks: int = 0

    # --- History snapshots ---
    stress_history: List[float] = field(default_factory=list)
    knowledge_history: List[float] = field(default_factory=list)
    motivation_history: List[float] = field(default_factory=list)
    fatigue_history: List[float] = field(default_factory=list)
    satisfaction_history: List[float] = field(default_factory=list)
    topic_knowledge_history: List[List[float]] = field(default_factory=list)

    # --- Social ---
    study_group_id: int = -1

    # --- Status ---
    dropped_out: bool = False
    at_risk: bool = False
    consecutive_high_stress_weeks: int = 0
    dropout_week: int = -1          # week when dropout occurred (-1 = active)

    # --- Intervention flag (existing) ---
    is_intervention_target: bool = False

    # ------------------------------------------------------------------
    # Backward-compatible knowledge property
    # ------------------------------------------------------------------

    @property
    def knowledge(self) -> float:
        """Mean mastery across all curriculum topics.  Read-only."""
        if not self.topic_knowledge:
            return 0.0
        return statistics.mean(self.topic_knowledge)

    # ------------------------------------------------------------------
    # Derived properties (unchanged from original)
    # ------------------------------------------------------------------

    @property
    def total_assignments_expected(self) -> int:
        return sum(s + l + m for s, l, m in zip(
            self.assignments_submitted,
            self.assignments_late,
            self.assignments_missed,
        ))

    @property
    def completion_rate(self) -> float:
        """Fraction of expected assignments submitted (on time OR late)."""
        total = self.total_assignments_expected
        if total == 0:
            return 1.0
        done = sum(self.assignments_submitted) + sum(self.assignments_late)
        return done / total

    @property
    def attendance_rate(self) -> float:
        if not self.weeks_attended:
            return 0.0
        return sum(self.weeks_attended) / len(self.weeks_attended)

    def snapshot(self) -> None:
        """Record current state into history lists at end of a week."""
        self.stress_history.append(round(self.stress, 4))
        self.knowledge_history.append(round(self.knowledge, 4))
        self.motivation_history.append(round(self.motivation, 4))
        self.fatigue_history.append(round(self.fatigue, 4))
        self.satisfaction_history.append(round(self.satisfaction, 4))
        self.topic_knowledge_history.append([round(k, 4) for k in self.topic_knowledge])


# ---------------------------------------------------------------------------
# LecturerAgent
# ---------------------------------------------------------------------------

@dataclass
class LecturerAgent:
    """
    The instructor.  Parameterises the teaching environment.

    Attributes
    ----------
    teaching_effectiveness : float
        Base multiplier on knowledge transfer [0.6, 1.4].
    current_effectiveness : float
        Mutable effective value — raised by adaptive lecturer logic.
    feedback_delay_weeks : int
        Weeks before feedback returns to students.
    assignment_load : int
        Assignments issued per week (0–3).
    strictness : float
        Grading penalty weight for late submissions [0, 1].
    adaptivity : float
        How strongly the lecturer adapts when class is struggling [0, 1].
    adaptation_threshold : float
        Class mean knowledge below this triggers an effectiveness boost.
    adaptation_boost : float
        Maximum per-step effectiveness increase from adaptation.
    """

    teaching_effectiveness: float = 1.0
    feedback_delay_weeks: int = 1
    assignment_load: int = 2
    strictness: float = 0.5

    # --- NEW: adaptive lecturer ---
    adaptivity: float = 0.0
    adaptation_threshold: float = 0.40
    adaptation_boost: float = 0.15

    # Mutable effective teaching level (starts at base, can be boosted)
    current_effectiveness: float = field(init=False)

    def __post_init__(self) -> None:
        self.current_effectiveness = self.teaching_effectiveness
