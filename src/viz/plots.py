"""
plots.py — Matplotlib visualisation functions for the Classroom Digital Twin.

All functions return a matplotlib Figure and optionally save to disk.

Original functions:
    plot_stress_over_time      — mean stress ± 1 SD band over weeks
    plot_knowledge_over_time   — mean knowledge ± 1 SD band over weeks
    plot_motivation_over_time  — mean motivation over weeks
    plot_gpa_distribution      — histogram of final GPA proxy
    plot_scenario_comparison   — bar chart comparing key metrics across scenarios
    plot_attendance_over_time  — attendance rate over weeks
    save_all_plots             — run all plots and save to a directory

New functions (Tier 3/4):
    plot_topic_mastery_heatmap — (n_students × n_topics) heatmap
    plot_ses_equity            — grouped bar: SES Q1 vs Q4 GPA across scenarios
    plot_dropout_timeline      — cumulative dropout count by week
    plot_at_risk_comparison    — at-risk % per scenario at detection week
    plot_executive_dashboard   — 4-panel: GPA + failure + stress + dropout
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from ..model.classroom_model import ClassroomModel

matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 120,
})

_PALETTE = [
    "#2563EB",  # blue
    "#16A34A",  # green
    "#DC2626",  # red
    "#D97706",  # amber
    "#7C3AED",  # violet
    "#0891B2",  # cyan
    "#EA580C",  # orange
    "#BE185D",  # pink
    "#065F46",  # dark green
]

_SES_COLORS = ["#DC2626", "#D97706", "#2563EB", "#16A34A"]  # Q1=red → Q4=green


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _week_ticks(n_weeks: int) -> List[int]:
    """Return sensible x-tick positions for a semester plot."""
    if n_weeks <= 14:
        return list(range(1, n_weeks + 1))
    step = max(1, n_weeks // 7)
    return list(range(1, n_weeks + 1, step))


def _save(fig: plt.Figure, path: Optional[Path]) -> None:
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, bbox_inches="tight")


# ---------------------------------------------------------------------------
# Original plot functions (unchanged API)
# ---------------------------------------------------------------------------

def plot_stress_over_time(
    weekly_dfs: Dict[str, pd.DataFrame],
    title: str = "Mean Student Stress Over Time",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Line + band plot of mean stress ± 1 SD for one or more scenarios."""
    fig, ax = plt.subplots(figsize=(9, 4))
    for idx, (label, df) in enumerate(weekly_dfs.items()):
        color = _PALETTE[idx % len(_PALETTE)]
        weeks = df["week"].tolist()
        mean = df["mean_stress"].tolist()
        std = df["std_stress"].tolist()
        ax.plot(weeks, mean, color=color, linewidth=2, label=label)
        ax.fill_between(
            weeks,
            [m - s for m, s in zip(mean, std)],
            [m + s for m, s in zip(mean, std)],
            color=color, alpha=0.15,
        )
        # Mark exam weeks if column exists
        if "is_exam_week" in df.columns:
            for _, row in df[df["is_exam_week"]].iterrows():
                ax.axvline(x=row["week"], color=color, linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xlabel("Week")
    ax.set_ylabel("Stress (0–1)")
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.set_xticks(_week_ticks(max(len(v) for v in weekly_dfs.values())))
    ax.legend(loc="upper left", fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_knowledge_over_time(
    weekly_dfs: Dict[str, pd.DataFrame],
    title: str = "Mean Student Knowledge Over Time",
    save_path: Optional[Path] = None,
    intervention_weeks: Optional[tuple] = None,
) -> plt.Figure:
    """
    Line + band plot of mean knowledge ± 1 SD.

    Parameters
    ----------
    intervention_weeks : tuple (start_week, end_week), optional
        If provided, draws a shaded band marking the intervention period.
    """
    fig, ax = plt.subplots(figsize=(9, 4))
    for idx, (label, df) in enumerate(weekly_dfs.items()):
        color = _PALETTE[idx % len(_PALETTE)]
        weeks = df["week"].tolist()
        mean = df["mean_knowledge"].tolist()
        std = df["std_knowledge"].tolist()
        ax.plot(weeks, mean, color=color, linewidth=2, label=label)
        ax.fill_between(
            weeks,
            [max(0, m - s) for m, s in zip(mean, std)],
            [min(1, m + s) for m, s in zip(mean, std)],
            color=color, alpha=0.15,
        )

    if intervention_weeks is not None:
        start, end = intervention_weeks
        ax.axvspan(start, end, alpha=0.12, color="#16A34A",
                   label=f"Intervention (wk {start}–{end})")

    ax.set_xlabel("Week")
    ax.set_ylabel("Knowledge (0–1)")
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.set_xticks(_week_ticks(max(len(v) for v in weekly_dfs.values())))
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_motivation_over_time(
    weekly_dfs: Dict[str, pd.DataFrame],
    title: str = "Mean Student Motivation Over Time",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Line plot of mean motivation."""
    fig, ax = plt.subplots(figsize=(9, 4))
    for idx, (label, df) in enumerate(weekly_dfs.items()):
        color = _PALETTE[idx % len(_PALETTE)]
        ax.plot(df["week"], df["mean_motivation"],
                color=color, linewidth=2, label=label)

    ax.set_xlabel("Week")
    ax.set_ylabel("Motivation (0–1)")
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.set_xticks(_week_ticks(max(len(v) for v in weekly_dfs.values())))
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_gpa_distribution(
    student_dfs: Dict[str, pd.DataFrame],
    title: str = "GPA Proxy Distribution",
    bins: int = 20,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Overlapping semi-transparent histograms of GPA proxy."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for idx, (label, df) in enumerate(student_dfs.items()):
        color = _PALETTE[idx % len(_PALETTE)]
        ax.hist(
            df["gpa_proxy"],
            bins=bins,
            range=(0, 4),
            color=color,
            alpha=0.5,
            label=label,
            edgecolor="white",
            linewidth=0.4,
        )

    ax.axvline(x=2.0, color="black", linestyle="--", linewidth=1.2, label="Pass threshold (2.0)")
    ax.set_xlabel("GPA Proxy (0–4)")
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_scenario_comparison(
    comparison_df: pd.DataFrame,
    metrics: Optional[List[str]] = None,
    title: str = "Scenario Comparison",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Grouped bar chart comparing headline metrics across scenarios."""
    if metrics is None:
        metrics = ["mean_gpa", "failure_rate", "mean_final_stress", "mean_attendance_rate"]

    metrics = [m for m in metrics if m in comparison_df.columns]
    label_col = "label" if "label" in comparison_df.columns else "scenario"
    labels = comparison_df[label_col].tolist()

    n_scenarios = len(labels)
    n_metrics = len(metrics)
    x = np.arange(n_scenarios)
    width = 0.8 / n_metrics

    fig, ax = plt.subplots(figsize=(max(8, n_scenarios * 1.4), 5))
    for i, metric in enumerate(metrics):
        vals = comparison_df[metric].tolist()
        offset = (i - n_metrics / 2 + 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=metric,
                      color=_PALETTE[i % len(_PALETTE)], alpha=0.85)
        for bar, val in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.005,
                f"{val:.2f}",
                ha="center", va="bottom", fontsize=7,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8)
    ax.set_title(title)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_attendance_over_time(
    weekly_dfs: Dict[str, pd.DataFrame],
    title: str = "Class Attendance Rate Over Time",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Line plot of weekly attendance rate."""
    fig, ax = plt.subplots(figsize=(9, 4))
    for idx, (label, df) in enumerate(weekly_dfs.items()):
        color = _PALETTE[idx % len(_PALETTE)]
        ax.plot(df["week"], df["attendance_rate"],
                color=color, linewidth=2, label=label)

    ax.set_xlabel("Week")
    ax.set_ylabel("Attendance Rate (0–1)")
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


# ---------------------------------------------------------------------------
# New plot functions
# ---------------------------------------------------------------------------

def plot_topic_mastery_heatmap(
    model: "ClassroomModel",
    title: str = "Final Topic Mastery by Student",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Heatmap of (n_students × n_topics) final topic knowledge.

    Rows = students (sorted by mean knowledge descending).
    Columns = curriculum topics.
    Cell colour = knowledge level [0, 1].
    """
    df = model.topic_mastery_dataframe()
    topic_cols = [c for c in df.columns if c.startswith("topic_")]

    # Sort by mean knowledge
    df = df.copy()
    df["_mean"] = df[topic_cols].mean(axis=1)
    df = df.sort_values("_mean", ascending=False).reset_index(drop=True)

    matrix = df[topic_cols].values
    n_students, n_topics = matrix.shape

    fig_h = max(4, n_students * 0.25)
    fig, ax = plt.subplots(figsize=(max(6, n_topics * 1.2), fig_h))

    im = ax.imshow(matrix, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1,
                   interpolation="nearest")
    plt.colorbar(im, ax=ax, label="Knowledge (0–1)", fraction=0.03, pad=0.02)

    ax.set_xticks(range(n_topics))
    ax.set_xticklabels([f"Topic {i+1}" for i in range(n_topics)], fontsize=9)
    ax.set_ylabel("Student (sorted by mean knowledge)")
    ax.set_yticks([])
    ax.set_title(title)

    # Mark dropped-out students
    if "dropped_out" in df.columns:
        for row_idx, dropped in enumerate(df["dropped_out"]):
            if dropped:
                ax.annotate("✗", xy=(-0.6, row_idx), xycoords="data",
                            fontsize=7, color="#DC2626", va="center")

    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_ses_equity(
    results: List[Dict],
    metric: str = "mean_gpa",
    title: str = "GPA by SES Quartile Across Scenarios",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Grouped bar chart: SES Q1 vs Q4 outcomes for each scenario.

    Parameters
    ----------
    results : list of result dicts with 'label' and 'model' keys
    metric  : column to show from equity_dataframe (default: mean_gpa)
    """
    quartile_labels = {0: "Q1 Low", 1: "Q2 Mid-Low", 2: "Q3 Mid-High", 3: "Q4 High"}
    quartile_colors = {0: "#DC2626", 1: "#D97706", 2: "#2563EB", 3: "#16A34A"}

    scenario_names = [r["label"] for r in results]
    n_scenarios = len(scenario_names)
    quartiles = [0, 3]  # show Q1 and Q4 only for clarity
    width = 0.35
    x = np.arange(n_scenarios)

    fig, ax = plt.subplots(figsize=(max(8, n_scenarios * 1.2), 5))

    for offset_idx, q in enumerate(quartiles):
        vals = []
        for r in results:
            eq_df = r["model"].equity_dataframe()
            row = eq_df[eq_df["ses_quartile"] == q]
            if len(row) == 0:
                vals.append(0.0)
            else:
                vals.append(float(row[metric].iloc[0]))

        offset = (offset_idx - len(quartiles) / 2 + 0.5) * width
        color = quartile_colors[q]
        bars = ax.bar(x + offset, vals, width, label=quartile_labels[q],
                      color=color, alpha=0.85)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.02,
                        f"{val:.2f}",
                        ha="center", va="bottom", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels(scenario_names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.set_title(title)
    ax.legend(fontsize=8, title="SES Quartile")
    if "gpa" in metric:
        ax.set_ylim(0, 4)
        ax.axhline(y=2.0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_dropout_timeline(
    results: List[Dict],
    title: str = "Cumulative Student Dropout by Week",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Line chart of cumulative dropout count over weeks for each scenario.

    Parameters
    ----------
    results : list of result dicts with 'label' and 'model' keys
    """
    fig, ax = plt.subplots(figsize=(9, 4))

    for idx, r in enumerate(results):
        color = _PALETTE[idx % len(_PALETTE)]
        timeline = r["model"].dropout_timeline()
        if timeline["cumulative_dropouts"].max() == 0:
            continue  # skip scenarios with no dropouts
        ax.plot(timeline["week"], timeline["cumulative_dropouts"],
                color=color, linewidth=2, label=r["label"], marker="o", markersize=3)

    ax.set_xlabel("Week")
    ax.set_ylabel("Cumulative Dropouts")
    ax.set_title(title)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_at_risk_comparison(
    results: List[Dict],
    title: str = "At-Risk Student Rate by Scenario (Week 5)",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Horizontal bar chart showing at-risk percentage per scenario.

    Parameters
    ----------
    results : list of result dicts with 'label' and 'summary' keys
    """
    labels = [r["label"] for r in results]
    at_risk_rates = [r["summary"].get("at_risk_rate", 0.0) for r in results]

    # Sort by at_risk_rate descending
    pairs = sorted(zip(at_risk_rates, labels), reverse=True)
    at_risk_rates_sorted = [p[0] for p in pairs]
    labels_sorted = [p[1] for p in pairs]

    colors = [
        "#DC2626" if v > 0.3 else "#D97706" if v > 0.15 else "#16A34A"
        for v in at_risk_rates_sorted
    ]

    fig, ax = plt.subplots(figsize=(9, max(4, len(labels) * 0.45)))
    y = range(len(labels_sorted))
    bars = ax.barh(list(y), at_risk_rates_sorted, color=colors, alpha=0.85)
    for bar, val in zip(bars, at_risk_rates_sorted):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:.1%}", va="center", fontsize=8)

    ax.set_yticks(list(y))
    ax.set_yticklabels(labels_sorted, fontsize=8)
    ax.set_xlabel("At-Risk Rate")
    ax.set_xlim(0, min(1.0, max(at_risk_rates_sorted) * 1.3 + 0.05))
    ax.set_title(title)
    ax.axvline(x=0.2, color="black", linestyle="--", linewidth=0.8,
               alpha=0.5, label="20% threshold")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_executive_dashboard(
    results: List[Dict],
    title: str = "Policy Impact Dashboard",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    4-panel executive dashboard for campus board presentations.

    Panels:
      1. Mean GPA (bar) — higher is better
      2. Failure rate (bar) — lower is better
      3. Mean final stress (bar) — lower is better
      4. Dropout rate (bar) — lower is better
    """
    summaries = [r["summary"] for r in results]
    labels = [r["label"] for r in results]

    metrics = [
        ("mean_gpa",       "Mean GPA (0–4)",     "#2563EB", False),
        ("failure_rate",   "Failure Rate",        "#DC2626", True),
        ("mean_final_stress", "Mean Final Stress", "#D97706", True),
        ("dropout_rate",   "Dropout Rate",        "#7C3AED", True),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    axes = axes.flatten()

    for ax, (metric, ylabel, color, lower_better) in zip(axes, metrics):
        vals = [s.get(metric, 0.0) for s in summaries]
        x = np.arange(len(labels))
        bars = ax.bar(x, vals, color=color, alpha=0.82, edgecolor="white", linewidth=0.5)

        # Highlight best scenario
        best_idx = vals.index(min(vals) if lower_better else max(vals))
        bars[best_idx].set_edgecolor("#111827")
        bars[best_idx].set_linewidth(2.0)

        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(vals) * 0.01,
                    f"{val:.2f}",
                    ha="center", va="bottom", fontsize=7)

        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=7)
        ax.set_ylabel(ylabel, fontsize=9)
        if "gpa" in metric:
            ax.set_ylim(0, 4)
        else:
            ax.set_ylim(0, max(vals) * 1.25 + 0.02)

        arrow = "▼ lower is better" if lower_better else "▲ higher is better"
        ax.set_title(f"{ylabel} ({arrow})", fontsize=9)

    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.01)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_ses_scatter(
    student_df: pd.DataFrame,
    title: str = "Family Support Level vs Final GPA (Individual Students)",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Scatter plot: SES score (x) vs final GPA proxy (y).

    Each dot is one student.  Blue = passed, red cross = failed.
    Includes a linear trend line to show the SES–GPA relationship.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    passed = student_df[student_df["gpa_proxy"] >= 2.0]
    failed = student_df[student_df["gpa_proxy"] < 2.0]

    ax.scatter(
        passed["ses_score"], passed["gpa_proxy"],
        color="#2563EB", alpha=0.65, s=45, label="Passed (GPA ≥ 2.0)", zorder=3,
    )
    ax.scatter(
        failed["ses_score"], failed["gpa_proxy"],
        color="#DC2626", alpha=0.75, s=50, marker="x",
        linewidths=1.5, label="Failed (GPA < 2.0)", zorder=3,
    )

    # Trend line
    if len(student_df) > 2:
        z = np.polyfit(student_df["ses_score"], student_df["gpa_proxy"], 1)
        p = np.poly1d(z)
        xs = np.linspace(float(student_df["ses_score"].min()),
                         float(student_df["ses_score"].max()), 100)
        ax.plot(xs, p(xs), color="#D97706", linewidth=1.8,
                linestyle="--", label="Trend", zorder=2)

    ax.axhline(y=2.0, color="black", linestyle=":", linewidth=1,
               alpha=0.5, label="Pass threshold (2.0)")
    ax.set_xlabel("Family Support Level (SES score: 0 = low, 1 = high)")
    ax.set_ylabel("Final GPA (0–4)")
    ax.set_title(title)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 4)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


# ---------------------------------------------------------------------------
# Analysis plots: tornado, multi-seed, convergence
# ---------------------------------------------------------------------------

def plot_tornado_chart(
    sensitivity_df: pd.DataFrame,
    metric_label: str = "Mean GPA",
    title: str = "Sensitivity Analysis — Parameter Impact (Tornado Chart)",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Horizontal tornado chart showing OAT sensitivity results.

    Each parameter has two bars: left = low-value effect, right = high-value
    effect, both measured as delta from baseline.  Green = improves metric,
    red = worsens metric.

    Parameters
    ----------
    sensitivity_df : DataFrame from SensitivityAnalyzer.analyze()
    metric_label   : human-readable metric name for axis label
    """
    from matplotlib.patches import Patch

    df = sensitivity_df.head(10).copy()
    n = len(df)

    fig, ax = plt.subplots(figsize=(11, max(4, n * 0.65)))
    y_pos = list(range(n))

    for i, row in df.iterrows():
        d_low = row["delta_low"]
        d_high = row["delta_high"]

        # Colour based on direction (for GPA-like metrics: positive = good)
        c_low  = "#16A34A" if d_low  > 0 else "#DC2626"
        c_high = "#16A34A" if d_high > 0 else "#DC2626"

        ax.barh(i, d_low,  color=c_low,  alpha=0.82, height=0.55)
        ax.barh(i, d_high, color=c_high, alpha=0.82, height=0.55)

        # Value labels
        pad = 0.003
        ax.text(
            d_low - pad if d_low < 0 else d_low + pad, i,
            row["low_value"],
            ha="right" if d_low < 0 else "left", va="center", fontsize=7.5,
        )
        ax.text(
            d_high + pad if d_high > 0 else d_high - pad, i,
            row["high_value"],
            ha="left" if d_high > 0 else "right", va="center", fontsize=7.5,
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["label"].tolist(), fontsize=9)
    ax.axvline(x=0, color="#111827", linewidth=1.2)
    ax.set_xlabel(f"Δ {metric_label} from baseline")
    ax.set_title(title, fontsize=11)

    legend_elements = [
        Patch(facecolor="#16A34A", alpha=0.82, label="Improves outcome"),
        Patch(facecolor="#DC2626", alpha=0.82, label="Worsens outcome"),
    ]
    ax.legend(handles=legend_elements, fontsize=8, loc="lower right")
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_multi_seed_comparison(
    aggregated_results: List[Dict],
    metric: str = "mean_gpa",
    metric_label: str = "Mean GPA",
    title: Optional[str] = None,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Bar chart with error bars showing mean ± 95% CI across multiple seeds.

    Parameters
    ----------
    aggregated_results : list of dicts from MultiSeedRunner.run_scenario()
    metric             : base metric key (without _mean / _ci95 suffix)
    """
    if title is None:
        title = f"{metric_label} — Mean ± 95% CI Across Seeds"

    labels = [r.get("label", r.get("name", "?")) for r in aggregated_results]
    means  = [r.get(f"{metric}_mean", 0.0) for r in aggregated_results]
    ci95s  = [r.get(f"{metric}_ci95", 0.0) for r in aggregated_results]
    n_runs = aggregated_results[0].get("n_runs", "?") if aggregated_results else "?"

    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 1.3), 5))
    x = np.arange(len(labels))
    colors = [_PALETTE[i % len(_PALETTE)] for i in range(len(labels))]

    ax.bar(
        x, means, yerr=ci95s, capsize=5,
        color=colors, alpha=0.85,
        error_kw={"elinewidth": 1.8, "ecolor": "#374151"},
    )

    for xi, (mean, ci) in enumerate(zip(means, ci95s)):
        ax.text(xi, mean + ci + max(means) * 0.015,
                f"{mean:.2f}\n±{ci:.2f}",
                ha="center", va="bottom", fontsize=7.5)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel(f"{metric_label}")
    ax.set_title(f"{title} (n={n_runs} seeds per scenario)", fontsize=10)
    if "gpa" in metric:
        ax.set_ylim(0, 4)
    elif "rate" in metric:
        ax.set_ylim(0, min(1.0, max(means) * 1.4 + 0.05))
    fig.tight_layout()
    _save(fig, save_path)
    return fig


def plot_convergence(
    convergence_df: pd.DataFrame,
    metric_label: str = "Mean GPA",
    title: str = "Convergence Test — Result Stability by Class Size",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """
    Line + confidence band showing how the metric stabilises as N increases.

    Parameters
    ----------
    convergence_df : DataFrame from SensitivityAnalyzer.convergence_test()
                     columns: n_students, mean, std, ci95
    """
    fig, ax = plt.subplots(figsize=(9, 4))

    n_vals = convergence_df["n_students"].tolist()
    means  = convergence_df["mean"].tolist()
    ci95s  = convergence_df["ci95"].tolist()

    ax.plot(n_vals, means, color=_PALETTE[0], linewidth=2.2,
            marker="o", markersize=5, label="Mean")
    ax.fill_between(
        n_vals,
        [m - c for m, c in zip(means, ci95s)],
        [m + c for m, c in zip(means, ci95s)],
        color=_PALETTE[0], alpha=0.18, label="95% CI",
    )

    # Stable region (last 3 points)
    stable_mean = float(np.mean(means[-3:]))
    ax.axhline(y=stable_mean, color="gray", linestyle="--",
               linewidth=1, alpha=0.7, label=f"Stable estimate ({stable_mean:.2f})")
    ax.axvline(x=30, color="#D97706", linestyle=":",
               linewidth=1.2, alpha=0.8, label="Baseline N=30")

    ax.set_xlabel("Number of Students (N)")
    ax.set_ylabel(metric_label)
    ax.set_title(title, fontsize=10)
    ax.set_xticks(n_vals)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, save_path)
    return fig


# ---------------------------------------------------------------------------
# Convenience: save all plots for a run
# ---------------------------------------------------------------------------

def save_all_plots(
    results: List[Dict],
    plots_dir: Path,
    comparison_df: Optional[pd.DataFrame] = None,
) -> None:
    """
    Generate and save all standard plots for a batch of scenario results.

    Parameters
    ----------
    results : list of result dicts from ScenarioRunner
    plots_dir : directory to save .png files
    comparison_df : optional pre-built comparison DataFrame
    """
    plots_dir = Path(plots_dir)
    plots_dir.mkdir(parents=True, exist_ok=True)

    weekly_dfs = {r["label"]: r["weekly_df"] for r in results}
    student_dfs = {r["label"]: r["student_df"] for r in results}

    plot_stress_over_time(weekly_dfs,
                          save_path=plots_dir / "stress_over_time.png")
    plot_knowledge_over_time(weekly_dfs,
                             save_path=plots_dir / "knowledge_over_time.png")
    plot_motivation_over_time(weekly_dfs,
                              save_path=plots_dir / "motivation_over_time.png")
    plot_gpa_distribution(student_dfs,
                          save_path=plots_dir / "gpa_distribution.png")
    plot_attendance_over_time(weekly_dfs,
                              save_path=plots_dir / "attendance_over_time.png")

    if comparison_df is not None:
        plot_scenario_comparison(comparison_df,
                                 save_path=plots_dir / "scenario_comparison.png")

    # New plots
    plot_dropout_timeline(results, save_path=plots_dir / "dropout_timeline.png")
    plot_at_risk_comparison(results, save_path=plots_dir / "at_risk_comparison.png")
    plot_executive_dashboard(results, save_path=plots_dir / "executive_dashboard.png")
    plot_ses_equity(results, save_path=plots_dir / "ses_equity.png")

    plt.close("all")
    print(f"Plots saved → {plots_dir}")
