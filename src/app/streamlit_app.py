"""
streamlit_app.py — Interactive dashboard for the Classroom Digital Twin.

Run with:
    streamlit run src/app/streamlit_app.py

Three tabs:
  1. Simulator   — interactive run with full parameter controls
  2. Campus Board — executive dashboard, policy ROI, equity analysis
  3. Deep Dive    — topic mastery heatmap, at-risk list, dropout timeline
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root on sys.path when run directly
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
import streamlit as st

from src.config import (
    CurriculumConfig,
    EnvironmentConfig,
    InterventionConfig,
    LecturerDefaults,
    SimulationConfig,
    SocialConfig,
    StudentDefaults,
)
from src.experiments.runner import MultiSeedRunner, ScenarioRunner
from src.experiments.scenarios import SCENARIO_LABELS, SCENARIOS, get_scenario
from src.experiments.sensitivity import SensitivityAnalyzer
from src.insights import CampusBoardInsights
from src.model.classroom_model import ClassroomModel
from src.viz.plots import (
    plot_at_risk_comparison,
    plot_attendance_over_time,
    plot_convergence,
    plot_dropout_timeline,
    plot_executive_dashboard,
    plot_gpa_distribution,
    plot_knowledge_over_time,
    plot_multi_seed_comparison,
    plot_ses_equity,
    plot_ses_scatter,
    plot_stress_over_time,
    plot_topic_mastery_heatmap,
    plot_tornado_chart,
    save_all_plots,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Classroom Digital Twin",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎓 Classroom Ecosystem Digital Twin")
st.caption(
    "Agent-based simulation of a 14-week university classroom. "
    "Adjust parameters, run scenarios, and compare outcomes."
)

# ---------------------------------------------------------------------------
# Sidebar — parameter controls
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("⚙️ Configuration")

    # ---- Scenario presets ----
    preset_options = ["Custom"] + list(SCENARIO_LABELS.keys())
    preset_labels = ["Custom (manual settings)"] + list(SCENARIO_LABELS.values())
    preset_idx = st.selectbox(
        "Scenario Preset",
        options=range(len(preset_options)),
        format_func=lambda i: preset_labels[i],
        index=1,  # default: baseline
    )
    selected_preset = preset_options[preset_idx]

    if selected_preset != "Custom":
        _preset_cfg = get_scenario(selected_preset)
    else:
        _preset_cfg = SimulationConfig()

    st.divider()
    st.subheader("Class Setup")

    n_students = st.slider(
        "Number of Students", min_value=5, max_value=120, step=5,
        value=_preset_cfg.n_students,
    )

    st.divider()
    st.subheader("Teaching Quality")

    teaching_effectiveness = st.slider(
        "Lecturer Effectiveness", min_value=0.6, max_value=1.4, step=0.05,
        value=float(_preset_cfg.lecturer.teaching_effectiveness),
        help="How clearly the lecturer explains material. 1.0 = average, 1.4 = excellent.",
    )
    feedback_delay = st.select_slider(
        "Assignment Return Speed",
        options=[0, 1, 2, 3, 4],
        format_func=lambda x: {
            0: "Same week (immediate)",
            1: "1 week",
            2: "2 weeks",
            3: "3 weeks",
            4: "4 weeks (very slow)",
        }[x],
        value=_preset_cfg.lecturer.feedback_delay_weeks,
        help="How quickly the lecturer returns graded assignments.",
    )
    assignment_load = st.select_slider(
        "Weekly Task Load",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "No assignments",
            1: "Light (1 per week)",
            2: "Standard (2 per week)",
            3: "Heavy (3 per week)",
        }[x],
        value=_preset_cfg.lecturer.assignment_load,
        help="Number of assignments or quizzes due per week.",
    )

    st.divider()
    st.subheader("Environment")

    room_temp = st.slider(
        "Room Temperature (°C)", min_value=16, max_value=34, step=1,
        value=int(_preset_cfg.environment.room_temp_celsius),
        help="Optimal: 20–24°C. Discomfort outside this range reduces motivation and attendance.",
    )
    class_mode = st.selectbox(
        "Delivery Mode",
        options=["in_person", "hybrid", "online"],
        format_func=lambda x: {"in_person": "In-Person", "hybrid": "Hybrid", "online": "Online"}[x],
        index=["in_person", "hybrid", "online"].index(_preset_cfg.environment.class_mode),
    )

    st.divider()
    st.subheader("Student Background")
    st.caption("SES = Socioeconomic Status — reflects family income, access to resources, and prior education quality.")

    ses_mean = st.slider(
        "Average Family Support Level", 0.0, 1.0,
        value=float(_preset_cfg.students.ses_score_mean), step=0.05,
        help="0 = very limited resources, 1 = very well-supported. Affects stress and attendance.",
    )
    ses_std = st.slider(
        "Diversity of Student Backgrounds", 0.0, 0.5,
        value=float(_preset_cfg.students.ses_score_std), step=0.05,
        help="Higher value = greater inequality between students. Use 0.35+ to simulate mixed-SES cohorts.",
    )

    st.divider()
    st.subheader("Support Program")

    enable_intervention = st.checkbox(
        "Enable Tutoring Support",
        value=_preset_cfg.intervention.enabled,
        help="Activates weekly tutoring for the bottom 25% of students in weeks 7–10.",
    )
    iv_start, iv_end, iv_mot, iv_str = 7, 10, 0.10, 0.10

    st.divider()
    run_btn = st.button("▶ Run Simulation", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Build config from sidebar inputs
# ---------------------------------------------------------------------------

cfg = SimulationConfig(
    n_students=n_students,
    n_weeks=_preset_cfg.n_weeks,
    seed=_preset_cfg.seed,
    lecturer=LecturerDefaults(
        teaching_effectiveness=teaching_effectiveness,
        feedback_delay_weeks=feedback_delay,
        assignment_load=assignment_load,
        strictness=_preset_cfg.lecturer.strictness,
        adaptivity=_preset_cfg.lecturer.adaptivity,
    ),
    students=StudentDefaults(
        ses_score_mean=ses_mean,
        ses_score_std=ses_std,
    ),
    social=SocialConfig(
        enable_peer_learning=_preset_cfg.social.enable_peer_learning,
    ),
    environment=EnvironmentConfig(
        class_schedule=_preset_cfg.environment.class_schedule,
        external_pressure=_preset_cfg.environment.external_pressure,
        room_temp_celsius=float(room_temp),
        class_mode=class_mode,
    ),
    intervention=InterventionConfig(
        enabled=enable_intervention,
        start_week=iv_start if enable_intervention else 7,
        end_week=iv_end if enable_intervention else 10,
        motivation_boost=iv_mot,
        stress_reduction=iv_str,
    ),
)

# ---------------------------------------------------------------------------
# Session state: cache last result
# ---------------------------------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if run_btn:
    with st.spinner("Running simulation…"):
        model = ClassroomModel(cfg)
        model.run()
        st.session_state.result = {
            "model": model,
            "name": selected_preset if selected_preset != "Custom" else "custom",
            "label": SCENARIO_LABELS.get(selected_preset, "Custom Run"),
            "summary": model.summary(),
            "student_df": model.student_dataframe(),
            "weekly_df": model.weekly_dataframe(),
            "cfg": cfg,
        }

# ---------------------------------------------------------------------------
# Tab layout
# ---------------------------------------------------------------------------

result = st.session_state.result

if result is None:
    st.info("Configure parameters in the sidebar and click **▶ Run Simulation** to begin.")
    st.stop()

tab_sim, tab_board, tab_deep, tab_analysis = st.tabs(
    ["📊 Simulator", "🏛️ Campus Board", "🔬 Deep Dive", "🔍 Analysis"]
)


# ===========================================================================
# TAB 1: SIMULATOR
# ===========================================================================

with tab_sim:
    summ = result["summary"]
    student_df: pd.DataFrame = result["student_df"]
    weekly_df: pd.DataFrame = result["weekly_df"]

    # ---- Headline metrics ----
    st.subheader("Key Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Mean GPA (0–4)", f"{summ['mean_gpa']:.2f}")
    col2.metric("GPA Std Dev", f"{summ['std_gpa']:.2f}")
    col3.metric("Failure Rate", f"{summ['failure_rate']:.1%}")
    col4.metric("Mean Attendance", f"{summ['mean_attendance_rate']:.1%}")
    col5.metric("Final Stress", f"{summ['mean_final_stress']:.2f}")
    col6.metric("Dropout Rate", f"{summ.get('dropout_rate', 0):.1%}")

    if summ.get("at_risk_rate", 0) > 0:
        st.warning(
            f"⚠️ At-risk detection (week {cfg.dynamics.at_risk_detection_week}): "
            f"**{summ['at_risk_rate']:.0%}** of students flagged at-risk."
        )
    if summ.get("dropout_rate", 0) > 0:
        st.error(
            f"⛔ {summ.get('dropout_rate', 0):.0%} of students dropped out "
            f"(Gini GPA: {summ.get('gini_gpa', 0):.3f})"
        )

    st.divider()

    # ---- Plots ----
    left_col, right_col = st.columns(2)
    _weekly = {"This run": weekly_df}
    _students = {"This run": student_df}

    with left_col:
        st.subheader("Stress Over Time")
        fig_stress = plot_stress_over_time(_weekly)
        st.pyplot(fig_stress, use_container_width=True)

        st.subheader("Attendance Rate Over Time")
        fig_att = plot_attendance_over_time(_weekly)
        st.pyplot(fig_att, use_container_width=True)

    with right_col:
        st.subheader("Knowledge Over Time")
        _iv_band = (
            (cfg.intervention.start_week, cfg.intervention.end_week)
            if cfg.intervention.enabled else None
        )
        fig_know = plot_knowledge_over_time(_weekly, intervention_weeks=_iv_band)
        st.pyplot(fig_know, use_container_width=True)

        st.subheader("GPA Distribution")
        fig_gpa = plot_gpa_distribution(_students)
        st.pyplot(fig_gpa, use_container_width=True)

    # ---- Multi-scenario comparison ----
    st.divider()
    st.subheader("🔬 Multi-Scenario Comparison")

    compare_scenarios = st.multiselect(
        "Add named scenarios to compare against current run:",
        options=list(SCENARIO_LABELS.keys()),
        default=[],
    )

    if compare_scenarios:
        with st.spinner("Running comparison scenarios…"):
            compare_weekly = {"Current run": weekly_df}
            compare_students = {"Current run": student_df}
            compare_rows = [summ | {"label": "Current run"}]

            for sc_name in compare_scenarios:
                sc_cfg = get_scenario(sc_name)
                sc_model = ClassroomModel(sc_cfg)
                sc_model.run()
                sc_label = SCENARIO_LABELS[sc_name]
                compare_weekly[sc_label] = sc_model.weekly_dataframe()
                compare_students[sc_label] = sc_model.student_dataframe()
                sc_summ = sc_model.summary()
                compare_rows.append(sc_summ | {"label": sc_label})

        comp_df = pd.DataFrame(compare_rows)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Stress Comparison")
            fig_cs = plot_stress_over_time(compare_weekly)
            st.pyplot(fig_cs, use_container_width=True)
        with c2:
            st.subheader("Knowledge Comparison")
            fig_ck = plot_knowledge_over_time(compare_weekly)
            st.pyplot(fig_ck, use_container_width=True)

        st.subheader("GPA Distribution Comparison")
        fig_cg = plot_gpa_distribution(compare_students)
        st.pyplot(fig_cg, use_container_width=True)

        st.subheader("Summary Table")
        _raw_cols = ["label", "mean_gpa", "std_gpa", "failure_rate",
                     "mean_final_stress", "mean_attendance_rate",
                     "mean_completion_rate", "dropout_rate", "at_risk_rate"]
        _raw_cols = [c for c in _raw_cols if c in comp_df.columns]
        _col_rename = {
            "mean_gpa": "Mean GPA",
            "std_gpa": "GPA Spread",
            "failure_rate": "Fail Rate",
            "mean_final_stress": "Avg Stress",
            "mean_attendance_rate": "Attendance",
            "mean_completion_rate": "Task Completion",
            "dropout_rate": "Dropout Rate",
            "at_risk_rate": "At-Risk Rate",
        }
        st.dataframe(
            comp_df[_raw_cols].rename(columns=_col_rename).set_index("label"),
            use_container_width=True,
        )

    # ---- Data tables ----
    st.divider()
    st.subheader("📋 Student Data")
    with st.expander("Show / hide student table", expanded=False):
        st.dataframe(student_df, use_container_width=True)
        csv = student_df.to_csv(index=False).encode()
        st.download_button("⬇ Download students.csv", data=csv,
                           file_name="students.csv", mime="text/csv")

    with st.expander("Show / hide weekly class data", expanded=False):
        st.dataframe(weekly_df, use_container_width=True)
        csv2 = weekly_df.to_csv(index=False).encode()
        st.download_button("⬇ Download class_weekly.csv", data=csv2,
                           file_name="class_weekly.csv", mime="text/csv")


# ===========================================================================
# TAB 2: CAMPUS BOARD
# ===========================================================================

with tab_board:
    st.subheader("🏛️ Campus Board Executive Dashboard")
    st.caption(
        "Run multiple scenarios to generate policy comparison. "
        "Select scenarios below or use the pre-defined policy set."
    )

    # ---- Thesis export (top, always visible) ----
    _THESIS_SCENARIOS = [
        "baseline", "small_class", "large_class",
        "fast_feedback", "slow_feedback",
        "low_load", "high_load", "stress_test",
        "intervention", "ses_diverse", "combined_intervention",
        "hot_classroom", "cold_classroom", "online_class", "hybrid_class",
    ]

    with st.expander("📄 Generate Thesis Report", expanded=False):
        st.caption(
            "Runs all 15 key scenarios, saves figures and CSV reports to `data/thesis_report/`. "
            "Use these files directly in your skripsi."
        )
        if st.button("📄 Generate Thesis Report", type="secondary", key="thesis_export"):
            report_dir = Path("data/thesis_report")
            with st.spinner(f"Running {len(_THESIS_SCENARIOS)} scenarios and saving all outputs…"):
                runner = ScenarioRunner(output_root="data")
                thesis_results = runner.run_all(_THESIS_SCENARIOS, tag="thesis")
                save_all_plots(
                    thesis_results,
                    plots_dir=report_dir / "figures",
                    comparison_df=pd.DataFrame([r["summary"] for r in thesis_results]),
                )
                cb_thesis = CampusBoardInsights(thesis_results)
                cb_thesis.generate_report(report_dir)
            st.success(f"Report saved to `{report_dir.resolve()}/`")
            st.markdown(
                "**Files generated:**\n"
                "- `figures/` — all thesis plots as PNG\n"
                "- `executive_summary.txt` — copy-paste for Chapter 4\n"
                "- `policy_roi.csv` — Table 3 data\n"
                "- `equity_analysis.csv` — SES quartile breakdown\n"
                "- `recommendations.txt` — ranked policy recommendations\n"
            )

    st.divider()

    board_scenarios = st.multiselect(
        "Select scenarios for board analysis:",
        options=list(SCENARIO_LABELS.keys()),
        default=["baseline", "fast_feedback", "low_load",
                 "intervention", "combined_intervention"],
        key="board_scenarios",
    )

    run_board = st.button("▶ Run Board Analysis", type="primary", key="board_run")

    if "board_results" not in st.session_state:
        st.session_state.board_results = None

    if run_board and board_scenarios:
        with st.spinner(f"Running {len(board_scenarios)} scenarios…"):
            board_results = []
            for sc_name in board_scenarios:
                sc_cfg = get_scenario(sc_name)
                sc_model = ClassroomModel(sc_cfg)
                sc_model.run()
                board_results.append({
                    "name": sc_name,
                    "label": SCENARIO_LABELS.get(sc_name, sc_name),
                    "summary": sc_model.summary(),
                    "student_df": sc_model.student_dataframe(),
                    "weekly_df": sc_model.weekly_dataframe(),
                    "model": sc_model,
                    "config": sc_cfg,
                })
            st.session_state.board_results = board_results

    board_results = st.session_state.board_results

    if board_results:
        cb = CampusBoardInsights(board_results)

        # Executive summary
        st.subheader("Executive Summary")
        st.text(cb.executive_summary())

        st.divider()

        # Executive dashboard plot
        st.subheader("Policy Impact Overview")
        fig_dash = plot_executive_dashboard(board_results)
        st.pyplot(fig_dash, use_container_width=True)

        st.divider()

        # Policy ROI table
        st.subheader("Policy Impact Table")
        roi_df = cb.policy_roi_table()
        _roi_raw_cols = [
            "policy_name", "mean_gpa", "gpa_delta", "failure_rate",
            "failure_rate_delta", "dropout_rate", "at_risk_rate",
            "gini_gpa", "ease", "cost_level",
        ]
        _roi_raw_cols = [c for c in _roi_raw_cols if c in roi_df.columns]
        display_roi = roi_df[_roi_raw_cols].rename(columns={
            "policy_name": "Policy",
            "mean_gpa": "Mean GPA",
            "gpa_delta": "GPA Δ vs Baseline",
            "failure_rate": "Fail Rate",
            "failure_rate_delta": "Fail Rate Δ",
            "dropout_rate": "Dropout Rate",
            "at_risk_rate": "At-Risk Rate",
            "gini_gpa": "GPA Inequality",
            "ease": "Ease of Implementation",
            "cost_level": "Estimated Cost",
        }).copy()
        # Colour GPA delta: green if positive, fail rate delta: green if negative
        st.dataframe(
            display_roi.style
                .background_gradient(subset=["GPA Δ vs Baseline"], cmap="RdYlGn")
                .background_gradient(subset=["Fail Rate Δ"], cmap="RdYlGn_r"),
            use_container_width=True,
        )

        st.divider()

        # Equity analysis
        st.subheader("SES Equity Analysis")
        fig_ses = plot_ses_equity(board_results)
        st.pyplot(fig_ses, use_container_width=True)

        eq_df = cb.equity_analysis()
        if not eq_df.empty:
            pivot = eq_df.pivot_table(
                index="label", columns="ses_quartile_label",
                values="mean_gpa", aggfunc="first"
            )
            st.caption("Mean GPA by SES Quartile and Scenario")
            st.dataframe(pivot, use_container_width=True)

        st.divider()

        # Ranked recommendations
        st.subheader("Ranked Policy Recommendations")
        recs = cb.ranked_recommendations()
        if recs:
            for rec in recs:
                st.markdown(f"- {rec}")
        else:
            st.info("No actionable scenarios in the current selection.")

        # Download
        st.divider()
        roi_csv = roi_df.to_csv(index=False).encode()
        st.download_button("⬇ Download Policy ROI CSV", data=roi_csv,
                           file_name="policy_roi.csv", mime="text/csv")
    else:
        st.info("Select scenarios and click **▶ Run Board Analysis** to generate insights.")



# ===========================================================================
# TAB 3: DEEP DIVE
# ===========================================================================

with tab_deep:
    st.subheader("🔬 Deep Dive Analysis")
    model = result["model"]

    # ---- Topic mastery heatmap ----
    st.subheader("Topic Mastery Heatmap")
    st.caption("Each row is a student (sorted by mean knowledge). "
               "Columns are curriculum topics. Green = high mastery.")
    fig_heat = plot_topic_mastery_heatmap(model)
    st.pyplot(fig_heat, use_container_width=True)

    # Per-topic breakdown table
    topic_df = model.topic_mastery_dataframe()
    topic_cols = [c for c in topic_df.columns if c.startswith("topic_")]
    if topic_cols:
        st.caption("Mean final mastery per topic:")
        topic_means = topic_df[topic_cols].mean().rename(
            lambda c: c.replace("topic_", "Topic ")
        )
        st.bar_chart(topic_means)

    st.divider()

    # ---- At-risk student list ----
    st.subheader("At-Risk Student List")
    at_risk_df = result["student_df"][result["student_df"]["at_risk"]].copy()
    if len(at_risk_df) > 0:
        st.warning(f"⚠️ {len(at_risk_df)} students flagged at-risk at week "
                   f"{cfg.dynamics.at_risk_detection_week}")
        display_at_risk = at_risk_df[[
            "student_id", "ses_score", "grit", "final_knowledge",
            "final_stress", "final_satisfaction", "gpa_proxy", "dropped_out"
        ]].rename(columns={
            "student_id": "Student ID",
            "ses_score": "SES Score",
            "grit": "Grit",
            "final_knowledge": "Knowledge",
            "final_stress": "Stress",
            "final_satisfaction": "Satisfaction",
            "gpa_proxy": "GPA",
            "dropped_out": "Dropped Out",
        }).sort_values("Knowledge")
        st.dataframe(display_at_risk, use_container_width=True)
    else:
        st.success("No students flagged at-risk in this run.")

    st.divider()

    # ---- Dropout timeline (this run) ----
    st.subheader("Dropout Timeline")
    dropout_df = model.dropout_timeline()
    if dropout_df["cumulative_dropouts"].max() > 0:
        st.error(f"⛔ Total dropouts: {int(dropout_df['cumulative_dropouts'].max())}")
        st.line_chart(dropout_df.set_index("week")["cumulative_dropouts"])
    else:
        st.success("No dropouts in this run.")

    st.divider()

    # ---- SES vs GPA scatter ----
    st.subheader("Family Support Level vs Final GPA")
    st.caption(
        "Each dot is one student. Blue = passed, red × = failed. "
        "The trend line reveals whether higher family support correlates with better outcomes."
    )
    fig_scatter = plot_ses_scatter(result["student_df"])
    st.pyplot(fig_scatter, use_container_width=True)

    # GPA gap callout
    eq_df = model.equity_dataframe()
    if not eq_df.empty and len(eq_df) >= 2:
        q1_row = eq_df[eq_df["ses_quartile"] == 0]
        q4_row = eq_df[eq_df["ses_quartile"] == 3]
        if len(q1_row) and len(q4_row):
            gap = float(q4_row["mean_gpa"].iloc[0]) - float(q1_row["mean_gpa"].iloc[0])
            if gap > 0.2:
                st.warning(
                    f"Equity gap detected: top-SES students score **{gap:.2f} GPA points** "
                    f"above bottom-SES students. Consider targeted support for low-SES cohorts."
                )

# ===========================================================================
# TAB 4: ANALYSIS
# ===========================================================================

with tab_analysis:
    st.subheader("🔍 Robustness, Sensitivity & Convergence")
    st.caption(
        "Academic validation tools for thesis. "
        "Run these to confirm findings are not seed-dependent and to identify "
        "which parameters drive outcomes."
    )

    # -----------------------------------------------------------------------
    # Section 1: Multi-seed robustness
    # -----------------------------------------------------------------------
    st.subheader("1. Multi-Seed Robustness")
    st.caption(
        "Runs each scenario N times with different random seeds. "
        "Reports mean ± 95% CI — use these numbers in your thesis tables."
    )

    robust_scenarios = st.multiselect(
        "Scenarios to test:",
        options=list(SCENARIO_LABELS.keys()),
        default=["baseline", "fast_feedback", "slow_feedback",
                 "high_load", "intervention", "online_class"],
        key="robust_scenarios",
    )
    n_runs = st.slider("Number of seeds (runs per scenario)",
                       min_value=5, max_value=30, value=10, step=5)
    run_robust = st.button("▶ Run Robustness Analysis", type="primary", key="robust_run")

    if "robust_results" not in st.session_state:
        st.session_state.robust_results = None

    if run_robust and robust_scenarios:
        with st.spinner(f"Running {len(robust_scenarios)} scenarios × {n_runs} seeds…"):
            msr = MultiSeedRunner(n_runs=n_runs)
            st.session_state.robust_results = [
                msr.run_scenario(name) for name in robust_scenarios
            ]

    if st.session_state.robust_results:
        rr = st.session_state.robust_results

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            fig_r_gpa = plot_multi_seed_comparison(rr, "mean_gpa", "Mean GPA")
            st.pyplot(fig_r_gpa, use_container_width=True)
        with col_r2:
            fig_r_fail = plot_multi_seed_comparison(
                rr, "failure_rate", "Failure Rate"
            )
            st.pyplot(fig_r_fail, use_container_width=True)

        st.caption("Full results table (copy Mean ± CI95 values into thesis Table 3):")
        rr_df = pd.DataFrame(rr)
        _rr_cols = ["label", "n_runs"] + [
            c for c in rr_df.columns
            if c.endswith("_mean") or c.endswith("_ci95")
        ]
        _rr_cols = [c for c in _rr_cols if c in rr_df.columns]
        _rr_rename = {
            "n_runs": "Seeds",
            "mean_gpa_mean": "Mean GPA",
            "mean_gpa_ci95": "GPA ±CI95",
            "failure_rate_mean": "Fail Rate",
            "failure_rate_ci95": "Fail Rate ±CI95",
            "mean_final_stress_mean": "Avg Stress",
            "mean_final_stress_ci95": "Stress ±CI95",
            "mean_attendance_rate_mean": "Attendance",
            "mean_attendance_rate_ci95": "Attendance ±CI95",
            "dropout_rate_mean": "Dropout Rate",
            "dropout_rate_ci95": "Dropout ±CI95",
            "at_risk_rate_mean": "At-Risk Rate",
            "at_risk_rate_ci95": "At-Risk ±CI95",
        }
        st.dataframe(
            rr_df[_rr_cols].rename(columns=_rr_rename).set_index("label"),
            use_container_width=True,
        )

    st.divider()

    # -----------------------------------------------------------------------
    # Section 2: Sensitivity analysis (tornado chart)
    # -----------------------------------------------------------------------
    st.subheader("2. Sensitivity Analysis (Tornado Chart)")
    st.caption(
        "One-at-a-time (OAT) analysis: each parameter swept from low to high "
        "while others stay at baseline. Shows which levers matter most."
    )

    sens_metric = st.selectbox(
        "Target metric:",
        options=["mean_gpa", "failure_rate", "mean_final_stress", "dropout_rate"],
        format_func=lambda x: {
            "mean_gpa": "Mean GPA",
            "failure_rate": "Failure Rate",
            "mean_final_stress": "Final Stress",
            "dropout_rate": "Dropout Rate",
        }[x],
        key="sens_metric",
    )
    sens_runs = st.slider(
        "Runs per parameter (more = smoother)", 1, 5, 1, key="sens_runs",
        help="Each parameter is tested at 2 levels × this many seeds",
    )
    run_sens = st.button("▶ Run Sensitivity Analysis", type="primary", key="sens_run")

    if "sens_results" not in st.session_state:
        st.session_state.sens_results = None

    if run_sens:
        with st.spinner("Running OAT sweep (8 parameters × 2 levels)…"):
            sa = SensitivityAnalyzer(metric=sens_metric, n_runs=sens_runs)
            st.session_state.sens_results = {
                "df": sa.analyze(), "metric": sens_metric,
            }

    if st.session_state.sens_results:
        sd = st.session_state.sens_results
        mlabel = {
            "mean_gpa": "Mean GPA", "failure_rate": "Failure Rate",
            "mean_final_stress": "Final Stress", "dropout_rate": "Dropout Rate",
        }.get(sd["metric"], sd["metric"])

        fig_tornado = plot_tornado_chart(sd["df"], metric_label=mlabel)
        st.pyplot(fig_tornado, use_container_width=True)

        with st.expander("Full sensitivity table"):
            st.dataframe(
                sd["df"].rename(columns={
                    "label": "Parameter",
                    "low_value": "Low Value",
                    "high_value": "High Value",
                    "metric_baseline": "Baseline",
                    "metric_at_low": "Value at Low",
                    "metric_at_high": "Value at High",
                    "delta_low": "Δ at Low",
                    "delta_high": "Δ at High",
                    "max_abs_delta": "Max Impact |Δ|",
                }).set_index("Parameter"),
                use_container_width=True,
            )

    st.divider()

    # -----------------------------------------------------------------------
    # Section 3: Convergence test
    # -----------------------------------------------------------------------
    st.subheader("3. Convergence Test")
    st.caption(
        "Validates that the simulation produces stable estimates with sufficient N. "
        "Results should converge (narrow CI) as class size increases. "
        "Include this figure in thesis Section 5.2 (Model Validation)."
    )

    conv_seeds = st.slider("Seeds per N", min_value=5, max_value=20, value=10,
                           key="conv_seeds")
    run_conv = st.button("▶ Run Convergence Test", type="primary", key="conv_run")

    if "conv_results" not in st.session_state:
        st.session_state.conv_results = None

    if run_conv:
        with st.spinner("Testing N = 10, 15, 20, 30, 45, 60, 90, 120 students…"):
            sa_conv = SensitivityAnalyzer(metric="mean_gpa")
            st.session_state.conv_results = sa_conv.convergence_test(
                n_seeds=conv_seeds
            )

    if st.session_state.conv_results is not None:
        fig_conv = plot_convergence(
            st.session_state.conv_results, metric_label="Mean GPA"
        )
        st.pyplot(fig_conv, use_container_width=True)
        st.dataframe(
            st.session_state.conv_results.rename(columns={
                "n_students": "Class Size (N)",
                "mean": "Mean GPA",
                "std": "Std Dev",
                "ci95": "95% CI",
            }),
            use_container_width=True,
        )


# ---- Footer ----
st.divider()
st.caption(
    "Classroom Ecosystem Digital Twin · Agent-Based Simulation · "
    "Built with Python, pandas, NumPy, Matplotlib, Streamlit."
)
