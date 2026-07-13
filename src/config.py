"""
config.py — Simulation configuration via Pydantic.

All parameters live here so experiments are fully reproducible
by serialising/deserialising this object to/from JSON.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StudentDefaults(BaseModel):
    """Initial distribution parameters for student agents."""

    learning_capacity_min: float = Field(0.6, ge=0.0, le=2.0,
                                         description="Min individual learning capacity")
    learning_capacity_max: float = Field(1.4, ge=0.0, le=2.0,
                                         description="Max individual learning capacity")
    motivation_mean: float = Field(0.65, ge=0.0, le=1.0,
                                   description="Initial motivation mean")
    motivation_std: float = Field(0.15, ge=0.0, le=0.5,
                                  description="Initial motivation std")
    stress_mean: float = Field(0.25, ge=0.0, le=1.0,
                               description="Initial stress mean")
    stress_std: float = Field(0.1, ge=0.0, le=0.5,
                              description="Initial stress std")
    knowledge_mean: float = Field(0.2, ge=0.0, le=1.0,
                                  description="Initial knowledge mean (prior knowledge)")
    knowledge_std: float = Field(0.1, ge=0.0, le=0.5,
                                 description="Initial knowledge std")
    base_attendance_prob: float = Field(0.85, ge=0.0, le=1.0,
                                        description="Base attendance probability")
    base_late_work_prob: float = Field(0.15, ge=0.0, le=1.0,
                                       description="Base probability of submitting work late")

    # --- NEW: SES and Grit ---
    ses_score_mean: float = Field(0.5, ge=0.0, le=1.0,
                                  description="Mean socioeconomic status score [0,1]")
    ses_score_std: float = Field(0.20, ge=0.0, le=0.5,
                                 description="SES score standard deviation")
    grit_mean: float = Field(0.5, ge=0.0, le=1.0,
                             description="Mean grit/resilience score [0,1]")
    grit_std: float = Field(0.15, ge=0.0, le=0.5,
                            description="Grit standard deviation")


class LecturerDefaults(BaseModel):
    """Parameters for the lecturer agent."""

    teaching_effectiveness: float = Field(1.0, ge=0.6, le=1.4,
                                          description="Multiplier on knowledge transmission")
    feedback_delay_weeks: int = Field(1, ge=0, le=4,
                                      description="Weeks before feedback reaches students")
    assignment_load: int = Field(2, ge=0, le=3,
                                 description="Number of assignments issued per week")
    strictness: float = Field(0.5, ge=0.0, le=1.0,
                              description="Grade penalty weight for late submissions")

    # --- NEW: Adaptive lecturer ---
    adaptivity: float = Field(0.0, ge=0.0, le=1.0,
                              description="How strongly lecturer adapts to class performance (0=none, 1=full)")
    adaptation_threshold: float = Field(0.40, ge=0.0, le=1.0,
                                        description="Mean class knowledge below this triggers adaptation")
    adaptation_boost: float = Field(0.15, ge=0.0, le=0.5,
                                    description="Max effectiveness boost per step from adaptation")


class DynamicsWeights(BaseModel):
    """
    Coefficients governing weekly update rules.
    All weights are positive and documented for thesis defensibility.
    """

    # --- Stress drivers (increase stress) ---
    w_stress_load: float = Field(0.04, ge=0.0, description="Stress per assignment per week")
    w_stress_pending_feedback: float = Field(0.03, ge=0.0,
                                             description="Stress per week of pending feedback")
    w_stress_absence: float = Field(0.05, ge=0.0,
                                    description="Stress increment when student is absent")

    # --- Stress relief (decrease stress) ---
    w_stress_feedback_relief: float = Field(0.08, ge=0.0,
                                            description="Stress reduction when feedback arrives")
    w_stress_rest: float = Field(0.03, ge=0.0,
                                 description="Baseline weekly stress recovery")

    # --- Knowledge ---
    base_learning_rate: float = Field(0.42, ge=0.0, le=1.0,
                                      description="Max knowledge gain per week when all factors are 1")
    knowledge_decay: float = Field(0.003, ge=0.0, le=0.1,
                                   description="Weekly forgetting rate")

    # --- Motivation ---
    motivation_feedback_boost: float = Field(0.05, ge=0.0,
                                             description="Motivation gain on feedback receipt")
    motivation_decay: float = Field(0.01, ge=0.0,
                                    description="Weekly motivation decay")

    # --- Attendance probability adjustment ---
    stress_attendance_penalty: float = Field(0.3, ge=0.0, le=1.0,
                                             description="How much high stress reduces attendance")
    motivation_attendance_bonus: float = Field(0.2, ge=0.0, le=1.0,
                                               description="How much motivation boosts attendance")

    # --- Assignment completion ---
    stress_completion_penalty: float = Field(0.4, ge=0.0, le=1.0,
                                             description="How much stress reduces completion prob")
    motivation_completion_bonus: float = Field(0.3, ge=0.0, le=1.0,
                                               description="How much motivation boosts completion")

    # --- NEW: SES and Grit ---
    w_ses_stress_relief: float = Field(0.10, ge=0.0,
                                       description="Weekly stress relief per unit SES (high SES = less stress)")
    w_grit_recovery: float = Field(0.05, ge=0.0,
                                   description="Additional weekly stress recovery from grit")

    # --- NEW: Fatigue ---
    w_fatigue_learning_penalty: float = Field(0.20, ge=0.0, le=1.0,
                                              description="Fatigue multiplier reducing effective learning rate")
    w_fatigue_gain: float = Field(0.04, ge=0.0,
                                  description="Fatigue gained per week when attending class")
    w_fatigue_rest: float = Field(0.06, ge=0.0,
                                  description="Fatigue recovered per week (rest component)")

    # --- NEW: Dropout thresholds ---
    dropout_stress_threshold: float = Field(0.92, ge=0.0, le=1.0,
                                            description="Stress level that counts as a 'high stress week' for dropout")
    dropout_knowledge_threshold: float = Field(0.25, ge=0.0, le=1.0,
                                               description="Knowledge below this (combined with high stress) triggers dropout")
    dropout_consecutive_weeks: int = Field(3, ge=1,
                                           description="Consecutive high-stress weeks required to trigger dropout")

    # --- NEW: At-risk detection ---
    at_risk_knowledge_threshold: float = Field(0.20, ge=0.0, le=1.0,
                                               description="Knowledge below this at detection week flags at-risk")
    at_risk_stress_threshold: float = Field(0.65, ge=0.0, le=1.0,
                                            description="Stress above this at detection week flags at-risk")
    at_risk_detection_week: int = Field(5, ge=1,
                                        description="Week number when at-risk detection runs (1-indexed)")


class CurriculumConfig(BaseModel):
    """Curriculum structure including topic sequence and exam schedule."""

    n_topics: int = Field(5, ge=1, le=10,
                          description="Number of sequential curriculum topics")
    exam_weeks: List[int] = Field(default_factory=lambda: [7, 14],
                                  description="Weeks with exams/evaluations (1-indexed)")
    topic_dependency_strength: float = Field(0.4, ge=0.0, le=1.0,
                                             description="How strongly prereq mastery gates next topic (0=none, 1=full gate)")
    difficulty_curve: str = Field("linear",
                                  description="Topic difficulty progression: flat | linear | steep_end")
    exam_stress_delta: float = Field(0.25, ge=0.0, le=1.0,
                                     description="Stress spike magnitude on exam weeks")
    knowledge_consolidation: float = Field(0.05, ge=0.0, le=0.5,
                                           description="Proportional knowledge boost during exam consolidation")


class SocialConfig(BaseModel):
    """Peer learning and study group configuration."""

    enable_peer_learning: bool = Field(True,
                                       description="Enable peer knowledge transfer via study groups")
    study_group_size: int = Field(4, ge=2, le=10,
                                  description="Target number of students per study group")
    peer_learning_rate: float = Field(0.025, ge=0.0, le=0.5,
                                      description="Fraction of knowledge gap transferred per week")
    formation: str = Field("mixed",
                            description="Group formation strategy: random | mixed (heterogeneous) | homogeneous")


class EnvironmentConfig(BaseModel):
    """External environment, scheduling, and systemic pressure parameters."""

    class_schedule: str = Field("afternoon",
                                 description="Class schedule slot: morning | afternoon | evening")
    external_pressure: float = Field(0.3, ge=0.0, le=1.0,
                                     description="Background stress from other courses [0,1]")
    mid_semester_slump_strength: float = Field(0.12, ge=0.0, le=1.0,
                                               description="Peak magnitude of mid-semester motivation dip (Gaussian)")
    room_temp_celsius: float = Field(22.0, ge=10.0, le=40.0,
                                      description="Classroom temperature in °C. Optimal range: 20–24°C.")
    class_mode: str = Field("in_person",
                             description="Class delivery mode: in_person | hybrid | online")

    @property
    def schedule_motivation_modifier(self) -> float:
        """Attendance and motivation adjustment based on class schedule slot."""
        return {"morning": -0.05, "afternoon": 0.0, "evening": -0.10}.get(
            self.class_schedule, 0.0
        )

    @property
    def class_mode_modifiers(self) -> dict:
        """Multipliers and deltas applied to dynamics based on class delivery mode."""
        if self.class_mode == "online":
            return {
                "attendance_bonus": 0.05,            # easier to log in than commute
                "teaching_effectiveness_mult": 0.80, # less effective remote delivery
                "peer_learning_mult": 0.35,          # much less peer interaction
                "motivation_decay_extra": 0.01,      # harder to stay engaged
                "fatigue_gain_mult": 0.50,           # no commute fatigue
            }
        elif self.class_mode == "hybrid":
            return {
                "attendance_bonus": 0.03,
                "teaching_effectiveness_mult": 0.92,
                "peer_learning_mult": 0.65,
                "motivation_decay_extra": 0.005,
                "fatigue_gain_mult": 0.75,
            }
        else:  # in_person
            return {
                "attendance_bonus": 0.0,
                "teaching_effectiveness_mult": 1.0,
                "peer_learning_mult": 1.0,
                "motivation_decay_extra": 0.0,
                "fatigue_gain_mult": 1.0,
            }


class InterventionConfig(BaseModel):
    """Optional tutoring/intervention applied to the bottom-quartile students."""

    enabled: bool = False
    start_week: int = Field(7, ge=1, description="First week of intervention (1-indexed)")
    end_week: int = Field(10, ge=1, description="Last week of intervention (inclusive)")
    motivation_boost: float = Field(0.1, ge=0.0, le=1.0,
                                    description="Weekly motivation addition for targeted students")
    stress_reduction: float = Field(0.1, ge=0.0, le=1.0,
                                    description="Weekly stress reduction for targeted students")
    target_quantile: float = Field(0.25, ge=0.0, le=1.0,
                                   description="Bottom fraction of students (by knowledge) targeted")

    @model_validator(mode="after")
    def end_after_start(self) -> "InterventionConfig":
        if self.end_week < self.start_week:
            raise ValueError("end_week must be >= start_week")
        return self


class SimulationConfig(BaseModel):
    """
    Top-level configuration.  Serialise to JSON to reproduce any run exactly.

    Example usage::

        cfg = SimulationConfig(n_students=30, seed=42)
        cfg.model_dump_json()  # → reproducible JSON
    """

    # ---- Core ----
    n_students: int = Field(30, ge=5, le=500, description="Number of student agents")
    n_weeks: int = Field(14, ge=4, le=52, description="Semester length in weeks")
    seed: int = Field(42, description="Global random seed for reproducibility")

    # ---- Sub-configs ----
    students: StudentDefaults = Field(default_factory=StudentDefaults)
    lecturer: LecturerDefaults = Field(default_factory=LecturerDefaults)
    dynamics: DynamicsWeights = Field(default_factory=DynamicsWeights)
    intervention: InterventionConfig = Field(default_factory=InterventionConfig)

    # ---- NEW sub-configs ----
    curriculum: CurriculumConfig = Field(default_factory=CurriculumConfig)
    social: SocialConfig = Field(default_factory=SocialConfig)
    environment: EnvironmentConfig = Field(default_factory=EnvironmentConfig)

    # ---- GPA computation ----
    gpa_knowledge_weight: float = Field(0.7, ge=0.0, le=1.0,
                                        description="Weight of knowledge in GPA proxy")
    gpa_completion_weight: float = Field(0.3, ge=0.0, le=1.0,
                                         description="Weight of assignment completion in GPA proxy")

    @field_validator("n_students")
    @classmethod
    def reasonable_class_size(cls, v: int) -> int:
        if v < 5:
            raise ValueError("Need at least 5 students for meaningful simulation")
        return v

    model_config = ConfigDict(frozen=False)


# ---------------------------------------------------------------------------
# Convenience factory functions for named scenarios
# ---------------------------------------------------------------------------

def baseline_config(**overrides) -> SimulationConfig:
    """Standard 30-student semester, 1-week feedback delay, 2 assignments/week."""
    cfg = SimulationConfig(n_students=30, seed=42)
    for k, v in overrides.items():
        setattr(cfg, k, v)
    return cfg


def large_class_config(**overrides) -> SimulationConfig:
    cfg = SimulationConfig(n_students=60, seed=42)
    for k, v in overrides.items():
        setattr(cfg, k, v)
    return cfg
