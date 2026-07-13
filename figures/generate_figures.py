"""Generate skripsi figures for ClassTwin."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


# ── Figure 1.1 & 2.1: Digital Twin Maturity Spectrum ──────────────────────────
def fig_dt_spectrum(outpath, fig_num):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    levels = [
        ("Digital\nModel", "Tidak ada aliran\ndata otomatis", "#E8F4FD", "#2196F3"),
        ("Digital\nShadow", "Data nyata →\nmodel (satu arah)", "#E8F5E9", "#4CAF50"),
        ("Digital\nTwin", "Dua arah,\nnear real-time", "#FFF3E0", "#FF9800"),
        ("Adaptive\nTwin", "Self-updating,\nprediktif", "#FCE4EC", "#E91E63"),
        ("Federated\nTwin", "Jaringan\ndigital twin", "#F3E5F5", "#9C27B0"),
    ]

    box_w = 1.6
    gap = 0.2
    start_x = 0.4
    y_box = 1.8
    box_h = 2.8

    for i, (title, desc, color, border) in enumerate(levels):
        x = start_x + i * (box_w + gap)
        fancy = FancyBboxPatch((x, y_box), box_w, box_h,
                               boxstyle="round,pad=0.05",
                               facecolor=color, edgecolor=border, linewidth=2)
        ax.add_patch(fancy)
        ax.text(x + box_w / 2, y_box + box_h - 0.35, title,
                ha="center", va="top", fontsize=10, fontweight="bold", color=border)
        ax.text(x + box_w / 2, y_box + 0.5, desc,
                ha="center", va="bottom", fontsize=8.5, color="#444", linespacing=1.4)

        if i < len(levels) - 1:
            ax.annotate("", xy=(x + box_w + gap, y_box + box_h / 2),
                        xytext=(x + box_w, y_box + box_h / 2),
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.5))

    # ClassTwin marker
    ct_x = start_x + box_w / 2
    ax.annotate("ClassTwin\n(penelitian ini)",
                xy=(ct_x, y_box),
                xytext=(ct_x - 0.2, 1.0),
                fontsize=9.5, fontweight="bold", color="#2196F3", ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#2196F3", lw=1.8))

    # Maturity arrow
    ax.annotate("", xy=(9.7, 0.6), xytext=(0.3, 0.6),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=2))
    ax.text(5, 0.25, "Tingkat Kematangan Digital Twin →", ha="center",
            fontsize=10, color="#555")

    # Level numbers
    for i in range(len(levels)):
        x = start_x + i * (box_w + gap)
        ax.text(x + box_w / 2, y_box + box_h + 0.1, f"Tingkat {i+1}",
                ha="center", va="bottom", fontsize=8, color="#777")

    ax.set_title(
        f"Gambar {fig_num}. Spektrum Kematangan Digital Twin dan Posisi ClassTwin",
        fontsize=12, fontweight="bold", pad=10, y=1.0
    )
    ax.text(0.5, -0.02,
            "Sumber: Diadaptasi dari Rasheed, San, & Kvamsdal (2020); Mousavi et al. (2024)",
            ha="center", transform=ax.transAxes, fontsize=8, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 1.2: Research Framework ────────────────────────────────────────────
def fig_kerangka_pikir(outpath):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x, y, w, h, label, sublabel="", color="#E3F2FD", border="#1565C0", fs=10):
        fancy = FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor=border, linewidth=1.8)
        ax.add_patch(fancy)
        ax.text(x + w / 2, y + h / 2 + (0.15 if sublabel else 0),
                label, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=border)
        if sublabel:
            ax.text(x + w / 2, y + h / 2 - 0.28, sublabel,
                    ha="center", va="center", fontsize=8, color="#555")

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.8))

    # Column 1: Problem
    box(0.3, 5.3, 2.8, 1.2, "Masalah Kebijakan", "Keputusan kelas tanpa\ndata dampak", "#FFF3E0", "#E65100")
    box(0.3, 3.8, 2.8, 1.2, "Konteks Indonesia", "9 juta mahasiswa,\n4.600+ PT", "#FFF3E0", "#E65100")
    box(0.3, 2.3, 2.8, 1.2, "Pasca-Pandemi", "Variabel baru:\nmode & interaksi", "#FFF3E0", "#E65100")
    arrow(1.7, 2.3, 1.7, 1.5)
    box(0.3, 0.3, 2.8, 1.2, "Celah Penelitian", "Model ABM pendidikan\ntidak aksesibel", "#FCE4EC", "#C62828")

    # Column 2: Solution (center)
    box(3.8, 2.8, 4.4, 2.4, "ClassTwin", "Model ABM 14 minggu\nNumPy + Pydantic + Streamlit",
        "#E8F5E9", "#2E7D32", fs=12)
    box(3.8, 0.3, 2.0, 2.2, "5 Skenario\nKelompok", "RQ1–RQ5", "#E3F2FD", "#1565C0")
    box(6.1, 0.3, 2.1, 2.2, "Validasi\nModel", "Face validity\nClamp & det.", "#E3F2FD", "#1565C0")

    # Column 3: Output
    box(9.0, 5.0, 2.7, 1.2, "Insight Kebijakan", "Perbandingan\nskenario & OAT", "#F3E5F5", "#6A1B9A")
    box(9.0, 3.5, 2.7, 1.2, "Dashboard\nStreamlit", "Non-teknis\nbisa jalankan", "#F3E5F5", "#6A1B9A")
    box(9.0, 0.3, 2.7, 2.8, "Kontribusi", "Prototipe ABM\nopen-source\nreproducible\ndokumentasi", "#EDE7F6", "#4527A0")

    # Arrows problem → ClassTwin
    arrow(3.1, 0.9, 3.8, 2.8)
    arrow(3.1, 3.4, 3.8, 3.8)
    arrow(3.1, 5.9, 3.8, 4.4)

    # Arrows ClassTwin → output
    arrow(8.2, 3.8, 9.0, 5.6)
    arrow(8.2, 3.4, 9.0, 4.1)
    arrow(8.2, 2.8, 9.0, 1.7)

    # Internal arrows
    arrow(5.0, 2.8, 4.8, 2.5)
    arrow(7.2, 2.8, 7.15, 2.5)

    ax.set_title("Gambar 1.2. Kerangka Pikir Penelitian ClassTwin",
                 fontsize=13, fontweight="bold", pad=8)

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 2.2: Yerkes-Dodson Curve ───────────────────────────────────────────
def fig_yerkes_dodson(outpath):
    fig, ax = plt.subplots(figsize=(8, 5.5))

    x = np.linspace(0, 1, 300)
    y = 4 * x * (1 - x)  # inverted-U on [0,1]

    ax.plot(x, y, color="#E65100", lw=3, label="Kinerja")
    ax.fill_between(x, y, alpha=0.12, color="#E65100")

    # Zones
    ax.axvspan(0, 0.25, alpha=0.08, color="#2196F3", label="Stres rendah\n(kurang motivasi)")
    ax.axvspan(0.35, 0.65, alpha=0.08, color="#4CAF50", label="Zona optimal")
    ax.axvspan(0.75, 1.0, alpha=0.08, color="#F44336", label="Stres tinggi\n(kapasitas kognitif turun)")

    # Peak annotation
    ax.annotate("Kinerja Optimal",
                xy=(0.5, 1.0), xytext=(0.5, 0.7),
                ha="center", fontsize=10, fontweight="bold", color="#2E7D32",
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.5))

    # Zone labels
    ax.text(0.125, 0.15, "Kurang\nTermotivasi", ha="center", fontsize=9, color="#1565C0")
    ax.text(0.50, 0.15, "Zona\nOptimal", ha="center", fontsize=9,
            color="#2E7D32", fontweight="bold")
    ax.text(0.875, 0.15, "Kelebihan\nBeban Kognitif", ha="center", fontsize=9, color="#C62828")

    # Vertical lines
    for xv, ls in [(0.25, "--"), (0.35, ":"), (0.65, ":"), (0.75, "--")]:
        ax.axvline(xv, color="#aaa", lw=1, ls=ls)

    ax.set_xlabel("Tingkat Stres / Gairah (Arousal)", fontsize=11)
    ax.set_ylabel("Kinerja Akademik", fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["Sangat\nRendah", "Rendah", "Sedang", "Tinggi", "Sangat\nTinggi"])
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(["Rendah", "Sedang", "Tinggi"])

    ax.set_title("Gambar 2.2. Kurva Yerkes-Dodson: Hubungan Stres dan Kinerja Akademik",
                 fontsize=12, fontweight="bold", pad=10)
    ax.text(0.5, -0.16, "Sumber: Diadaptasi dari Yerkes & Dodson (1908)",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 2.3: ZPD Diagram ───────────────────────────────────────────────────
def fig_zpd(outpath):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"aspect": "equal"})
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis("off")

    circles = [
        (3.8, "#E8F5E9", "#4CAF50", ""),
        (2.8, "#FFF9C4", "#FBC02D", ""),
        (1.7, "#E3F2FD", "#1976D2", ""),
    ]

    for r, fc, ec, _ in circles:
        c = plt.Circle((0, 0), r, color=fc, ec=ec, lw=2)
        ax.add_patch(c)

    # Labels
    ax.text(0, 0, "Kemampuan\nMandiri\n(Actual\nDevelopment)", ha="center",
            va="center", fontsize=9.5, fontweight="bold", color="#1565C0")

    ax.text(0, 2.25, "Zone of\nProximal\nDevelopment\n(ZPD)", ha="center",
            va="center", fontsize=9.5, fontweight="bold", color="#F57F17")

    ax.text(0, 3.35, "Dengan\nBantuan Teman /\nDosen", ha="center",
            va="center", fontsize=8.5, color="#2E7D32")

    # Arrows ZPD → Mandiri
    for angle in [45, 135, 225, 315]:
        rad = np.deg2rad(angle)
        x1 = 2.8 * np.cos(rad) * 0.7
        y1 = 2.8 * np.sin(rad) * 0.7
        x2 = 1.7 * np.cos(rad) * 0.85
        y2 = 1.7 * np.sin(rad) * 0.85
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#F57F17", lw=1.5))

    # Legend text
    ax.text(-3.8, -3.6, "Lingkaran dalam: Kemampuan mandiri saat ini", fontsize=8.5, color="#1565C0")
    ax.text(-3.8, -3.9, "Lingkaran tengah: ZPD — area yang bisa dicapai dengan bantuan", fontsize=8.5, color="#F57F17")
    ax.text(-3.8, -4.2, "Lingkaran luar: Di luar jangkauan saat ini", fontsize=8.5, color="#4CAF50")

    ax.set_title(
        "Gambar 2.3. Zone of Proximal Development (ZPD) — Vygotsky (1978)",
        fontsize=12, fontweight="bold", pad=8
    )
    ax.text(0.5, 0.01,
            "Sumber: Diadaptasi dari Vygotsky (1978)",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 3.1: Research Flowchart ───────────────────────────────────────────
def fig_alur_penelitian(outpath):
    fig, ax = plt.subplots(figsize=(9, 14))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 14)
    ax.axis("off")

    def rbox(x, y, w, h, text, color="#E3F2FD", border="#1565C0", fs=9.5):
        fancy = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                               facecolor=color, edgecolor=border, linewidth=1.8)
        ax.add_patch(fancy)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=border, multialignment="center")

    def arr(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.8))

    cx = 4.5
    steps = [
        (13.1, "Identifikasi Masalah\n& Studi Literatur", "#FFF3E0", "#E65100"),
        (11.5, "Perancangan Arsitektur\nModel (Agen & Aturan)", "#E8F5E9", "#2E7D32"),
        (9.9,  "Implementasi Model\n(NumPy + Python + Pydantic)", "#E8F5E9", "#2E7D32"),
        (8.3,  "Desain 15 Skenario\nEksperimen (RQ1–RQ5)", "#E3F2FD", "#1565C0"),
        (6.7,  "Eksekusi Eksperimen\n(15 skenario × 20 seed)", "#E3F2FD", "#1565C0"),
        (5.1,  "Analisis Sensitivitas OAT\n& Uji Validasi", "#E3F2FD", "#1565C0"),
        (3.5,  "Pengembangan Dashboard\nStreamlit", "#F3E5F5", "#6A1B9A"),
        (1.9,  "Analisis Hasil &\nPenarikan Kesimpulan", "#FCE4EC", "#C62828"),
        (0.3,  "Penulisan Laporan\nSkripsi", "#FCE4EC", "#C62828"),
    ]

    box_h = 1.0
    box_w = 5.0
    bx = cx - box_w/2

    for y, text, color, border in steps:
        rbox(bx, y, box_w, box_h, text, color, border)

    # Arrows between steps
    for i in range(len(steps) - 1):
        y_top = steps[i][0]
        y_next = steps[i+1][0] + box_h
        arr(cx, y_top, cx, y_next)

    # Phase labels on right
    phases = [
        (12.35, "FASE 1\nPerancangan", "#E65100"),
        (9.15, "FASE 2\nImplementasi", "#2E7D32"),
        (6.05, "FASE 3\nEksperimen", "#1565C0"),
        (2.65, "FASE 4\nAnalisis", "#C62828"),
    ]
    for y, text, color in phases:
        ax.text(8.0, y, text, ha="center", va="center", fontsize=8.5,
                color=color, fontweight="bold", multialignment="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=color, lw=1.2, alpha=0.9))

    ax.set_title("Gambar 3.1. Diagram Alur Penelitian ClassTwin",
                 fontsize=12, fontweight="bold", pad=8)
    ax.text(0.5, 0.0, "Sumber: Desain penelitian ini.",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 3.2: Model Architecture ───────────────────────────────────────────
def fig_arsitektur_model(outpath):
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x, y, w, h, title, lines=None, color="#E3F2FD", border="#1565C0", fs=10):
        fancy = FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.12",
                               facecolor=color, edgecolor=border, linewidth=2)
        ax.add_patch(fancy)
        text_y = y + h - 0.28
        ax.text(x + w / 2, text_y, title,
                ha="center", va="top", fontsize=fs, fontweight="bold", color=border)
        if lines:
            for i, line in enumerate(lines):
                ax.text(x + w / 2, text_y - 0.38 - i * 0.32, line,
                        ha="center", va="top", fontsize=8, color="#333",
                        family="monospace")

    def arrow(x1, y1, x2, y2, label="", color="#555"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.1, my, label, fontsize=8, color=color, va="center")

    # SimulationConfig (top center)
    box(4.5, 5.4, 4.0, 1.3, "SimulationConfig",
        ["StudentDefaults · LecturerDefaults",
         "DynamicsWeights · CurriculumConfig",
         "SocialConfig · EnvironmentConfig · InterventionConfig"],
        "#FFF3E0", "#E65100", fs=11)

    # ClassroomModel (center)
    box(4.5, 3.3, 4.0, 1.6, "ClassroomModel",
        ["schedule.step()  →  14 minggu",
         "run_scenario()   →  20 seed",
         "collect_metrics()"],
        "#E8F5E9", "#2E7D32", fs=11)

    # StudentAgent (left)
    box(0.3, 1.0, 3.6, 3.8, "StudentAgent × N",
        ["knowledge (property)",
         "topic_knowledge[5]",
         "stress · motivation",
         "fatigue · satisfaction",
         "ses_score · grit",
         "learning_capacity",
         "dropped_out · at_risk"],
        "#E3F2FD", "#1565C0", fs=10)

    # LecturerAgent (right)
    box(9.1, 1.8, 3.6, 2.2, "LecturerAgent × 1",
        ["teaching_effectiveness",
         "feedback_delay_weeks",
         "assignment_load",
         "adaptivity"],
        "#F3E5F5", "#6A1B9A", fs=10)

    # Output (bottom center)
    box(3.8, 0.2, 5.4, 1.3, "Output & Analisis",
        ["GPA proxy · stress_history · dropout_week",
         "ScenarioRunner (20 replikasi) → CI 95%",
         "OAT Sensitivity · Streamlit Dashboard"],
        "#FCE4EC", "#C62828", fs=10)

    # Arrows
    arrow(6.5, 5.4, 6.5, 4.9, "", "#E65100")         # config → model
    arrow(4.5, 4.1, 3.9, 3.5, "instansiasi", "#2E7D32")  # model → student
    arrow(8.5, 4.1, 9.1, 3.0, "instansiasi", "#2E7D32")  # model → lecturer
    arrow(6.5, 3.3, 6.5, 1.5, "hasil", "#C62828")        # model → output

    # Framework label
    ax.text(6.5, 6.9, "Custom Agent Loop (NumPy + Pydantic) — Python 3.13",
            ha="center", fontsize=9, color="#777", style="italic")

    ax.set_title("Gambar 3.1. Arsitektur Model ClassTwin",
                 fontsize=13, fontweight="bold", pad=6)
    ax.text(0.5, 0.0, "Sumber: Desain penelitian ini.",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 3.2: Weekly Update Flowchart ──────────────────────────────────────
def fig_flowchart_mingguan(outpath):
    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")

    def rect(x, y, w, h, text, color="#E3F2FD", border="#1565C0", fs=9):
        fancy = FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor=border, linewidth=1.8)
        ax.add_patch(fancy)
        ax.text(x + w / 2, y + h / 2, text,
                ha="center", va="center", fontsize=fs,
                fontweight="bold", color=border, multialignment="center")

    def diamond(cx, cy, hw, hh, text, color="#FFF9C4", border="#F57F17", fs=8.5):
        xs = [cx, cx + hw, cx, cx - hw, cx]
        ys = [cy + hh, cy, cy - hh, cy, cy + hh]
        ax.fill(xs, ys, color=color, edgecolor=border, lw=1.8)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
                fontweight="bold", color=border, multialignment="center")

    def arr(x1, y1, x2, y2, label="", lside=False):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5))
        if label:
            mx = (x1 + x2) / 2 + (-0.15 if lside else 0.15)
            my = (y1 + y2) / 2
            ax.text(mx, my, label, fontsize=7.5, color="#555", va="center")

    cx = 5.0
    # Start
    rect(3.5, 13.1, 3.0, 0.7, "MULAI: t = 1 … 14", "#E8F5E9", "#2E7D32", 10)
    arr(cx, 13.1, cx, 12.5)

    rect(2.8, 11.8, 4.4, 0.65, "Hitung topic_idx(t), slump_factor(t)", "#EDE7F6", "#4527A0")
    arr(cx, 11.8, cx, 11.15)

    rect(2.8, 10.5, 4.4, 0.65, "Untuk setiap StudentAgent aktif:", "#E3F2FD", "#1565C0")
    arr(cx, 10.5, cx, 9.85)

    rect(2.8, 9.2, 4.4, 0.65, "draw_attendance() → Bernoulli", "#E3F2FD", "#1565C0")
    arr(cx, 9.2, cx, 8.55)

    rect(2.8, 7.9, 4.4, 0.65, "draw_assignment_outcomes()\n→ submitted / late / missed", "#E3F2FD", "#1565C0")
    arr(cx, 7.9, cx, 7.25)

    rect(2.8, 6.6, 4.4, 0.65, "update_stress() + SES + grit", "#E3F2FD", "#1565C0")
    arr(cx, 6.6, cx, 5.95)

    rect(2.8, 5.3, 4.4, 0.65, "update_topic_knowledge()\n+ peer_learning_delta", "#E3F2FD", "#1565C0")
    arr(cx, 5.3, cx, 4.65)

    rect(2.8, 4.0, 4.4, 0.65, "update_motivation() / fatigue()\n/ satisfaction()", "#E3F2FD", "#1565C0")
    arr(cx, 4.0, cx, 3.35)

    diamond(cx, 3.0, 1.8, 0.35, "Minggu ujian?", "#FFF9C4", "#F57F17")
    # yes → right
    ax.annotate("", xy=(8.5, 3.0), xytext=(cx + 1.8, 3.0),
                arrowprops=dict(arrowstyle="-|>", color="#F57F17", lw=1.5))
    ax.text(7.3, 3.1, "Ya", fontsize=8, color="#F57F17")
    rect(7.5, 2.65, 2.2, 0.65, "+exam_stress\n+consolidate", "#FFF9C4", "#F57F17", 8)
    ax.annotate("", xy=(8.6, 2.3), xytext=(8.6, 2.65),
                arrowprops=dict(arrowstyle="-|>", color="#F57F17", lw=1.5))
    # no → down
    arr(cx, 2.65, cx, 2.1, "Tidak", True)

    rect(2.8, 1.65, 4.4, 0.65, "check_dropout(i, t)\ni.snapshot()", "#FCE4EC", "#C62828")
    # merge from exam branch
    ax.plot([8.6, 8.6, 5.0], [2.3, 1.97, 1.97], color="#F57F17", lw=1.5)
    ax.annotate("", xy=(5.0, 1.97), xytext=(5.01, 1.97),
                arrowprops=dict(arrowstyle="-|>", color="#F57F17", lw=1.5))

    arr(cx, 1.65, cx, 1.05)
    rect(2.8, 0.35, 4.4, 0.65, "Intervensi / deteksi at-risk\n/ adaptasi dosen (jika aktif)", "#E8F5E9", "#2E7D32")

    ax.set_title("Gambar 3.2. Flowchart Pembaruan Mingguan Model ClassTwin",
                 fontsize=12, fontweight="bold", pad=8)
    ax.text(0.5, 0.0, "Sumber: Desain penelitian ini.",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 3.3: Thermal Discomfort Curve ─────────────────────────────────────
def fig_discomfort_termal(outpath):
    fig, ax = plt.subplots(figsize=(9, 5))

    temps = np.linspace(10, 40, 500)
    discomfort = np.clip((np.abs(temps - 22) - 2) / 8.0, 0, 1)

    ax.plot(temps, discomfort, color="#E65100", lw=3)
    ax.fill_between(temps, discomfort, alpha=0.15, color="#E65100")

    # Comfort zone shading
    ax.axvspan(20, 24, alpha=0.18, color="#4CAF50", label="Zona nyaman ASHRAE 55\n(20–24°C)")

    # Annotations
    for temp, label, offset in [(16, "16°C\ndiscomfort=0.50", (0.5, 0.15)),
                                  (32, "32°C\ndiscomfort=1.00", (-2.5, 0.08))]:
        d = np.clip((abs(temp - 22) - 2) / 8, 0, 1)
        ax.annotate(label, xy=(temp, d), xytext=(temp + offset[0], d + offset[1]),
                    fontsize=9, color="#555",
                    arrowprops=dict(arrowstyle="-|>", color="#aaa", lw=1.2))
        ax.plot(temp, d, "o", color="#E65100", ms=7)

    ax.axvline(22, color="#4CAF50", lw=1.2, ls="--", alpha=0.7)
    ax.text(22.2, 0.85, "Optimal\n22°C", fontsize=9, color="#2E7D32")

    ax.set_xlabel("Suhu Ruangan (°C)", fontsize=11)
    ax.set_ylabel("Faktor Ketidaknyamanan Termal", fontsize=11)
    ax.set_xlim(10, 40)
    ax.set_ylim(-0.05, 1.15)
    ax.legend(loc="upper center", fontsize=9, framealpha=0.8)

    ax.set_title("Gambar 3.3. Kurva Ketidaknyamanan Termal — Formula ASHRAE 55",
                 fontsize=12, fontweight="bold", pad=10)
    ax.text(0.5, -0.14,
            "Sumber: Diadaptasi dari ASHRAE Standard 55 (2020); Wargocki & Wyon (2013).",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 3.4: Mid-Semester Slump ───────────────────────────────────────────
def fig_slump_factor(outpath):
    fig, ax = plt.subplots(figsize=(9, 5))

    weeks = np.arange(1, 15)
    n_weeks = 14
    slump_strength = 0.12
    midpoint = (n_weeks + 1) / 2
    sigma = n_weeks / 6.0
    peak = np.exp(-0.5 * ((weeks - midpoint) / sigma) ** 2)
    slump = 1.0 - slump_strength * peak

    ax.plot(weeks, slump, color="#1565C0", lw=3, marker="o", ms=7, label="slump_factor(t)")
    ax.fill_between(weeks, slump, 1.0, alpha=0.18, color="#1565C0")
    ax.axhline(1.0, color="#aaa", lw=1.2, ls="--", label="Tanpa slump (= 1.0)")

    # Annotate minimum
    min_week = weeks[np.argmin(slump)]
    min_val = slump.min()
    ax.annotate(f"Puncak slump\nMinggu {min_week}\nfaktor = {min_val:.3f}",
                xy=(min_week, min_val), xytext=(min_week + 1.5, min_val - 0.04),
                fontsize=9, color="#1565C0",
                arrowprops=dict(arrowstyle="-|>", color="#1565C0", lw=1.3))

    # Exam weeks
    for ew, label in [(7, "UTS"), (14, "UAS")]:
        ax.axvline(ew, color="#E65100", lw=1.5, ls=":", alpha=0.8)
        ax.text(ew + 0.1, 1.005, label, fontsize=8.5, color="#E65100")

    ax.set_xlabel("Minggu ke-", fontsize=11)
    ax.set_ylabel("slump_factor (pengali perolehan pengetahuan)", fontsize=11)
    ax.set_xticks(weeks)
    ax.set_ylim(0.82, 1.04)
    ax.legend(fontsize=9, loc="lower center")

    ax.set_title("Gambar 3.4. Kurva Mid-Semester Slump (slump_strength = 0.12)",
                 fontsize=12, fontweight="bold", pad=10)
    ax.text(0.5, -0.14,
            "Sumber: Diadaptasi dari Dietz-Uhler & Lanter (2009); implementasi penelitian ini.",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


# ── Figure 3.5: Topic Dependency Chain ───────────────────────────────────────
def fig_topic_dependency(outpath):
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)
    ax.axis("off")

    topics = [
        ("Topik 0\n(Mgg 1–3)", "Dasar\n(tanpa prasyarat)", "#E8F5E9", "#2E7D32"),
        ("Topik 1\n(Mgg 4–6)", "dep dari\nTopik 0", "#E3F2FD", "#1565C0"),
        ("Topik 2\n(Mgg 7–9)", "dep dari\nTopik 1", "#FFF3E0", "#E65100"),
        ("Topik 3\n(Mgg 10–11)", "dep dari\nTopik 2", "#F3E5F5", "#6A1B9A"),
        ("Topik 4\n(Mgg 12–14)", "dep dari\nTopik 3", "#FCE4EC", "#C62828"),
    ]

    box_w = 2.0
    box_h = 2.2
    gap = 0.4
    start_x = 0.4
    y = 2.2

    for i, (title, desc, color, border) in enumerate(topics):
        x = start_x + i * (box_w + gap)
        fancy = FancyBboxPatch((x, y), box_w, box_h,
                               boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor=border, linewidth=2)
        ax.add_patch(fancy)
        ax.text(x + box_w / 2, y + box_h - 0.3, title,
                ha="center", va="top", fontsize=10, fontweight="bold", color=border)
        ax.text(x + box_w / 2, y + 0.45, desc,
                ha="center", va="bottom", fontsize=8.5, color="#444", linespacing=1.4)

        if i < len(topics) - 1:
            x_arr_start = x + box_w
            x_arr_end = x + box_w + gap
            ax.annotate("", xy=(x_arr_end, y + box_h / 2),
                        xytext=(x_arr_start, y + box_h / 2),
                        arrowprops=dict(arrowstyle="-|>", color="#888", lw=2))
            # dep label
            ax.text(x_arr_start + gap / 2, y + box_h / 2 + 0.2,
                    "dep_strength\n= 0.40", ha="center", fontsize=7.5, color="#888")

    # Formula box below
    formula_y = 0.3
    ax.text(6.5, formula_y + 1.4,
            "dep(i, t) = (1 − dep_strength) + dep_strength × topic_knowledge[n−1]",
            ha="center", fontsize=10, family="monospace", color="#333",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F5F5F5", edgecolor="#bbb", lw=1.5))
    ax.text(6.5, formula_y + 0.7,
            "dep_strength = 0.40  →  dep ∈ [0.60, 1.00]",
            ha="center", fontsize=9.5, color="#555")
    ax.text(6.5, formula_y + 0.2,
            "Topik 0 selalu dep = 1.0 (tidak ada prasyarat)",
            ha="center", fontsize=9, color="#777", style="italic")

    ax.set_title("Gambar 3.5. Rantai Ketergantungan Topik Kurikulum (topic_dependency_strength = 0.40)",
                 fontsize=12, fontweight="bold", pad=10)
    ax.text(0.5, 0.0, "Sumber: Diadaptasi dari Vygotsky (1978); desain penelitian ini.",
            ha="center", transform=ax.transAxes, fontsize=8.5, color="#777", style="italic")

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    fig_dt_spectrum(OUT / "gambar_1_1_dt_spectrum.png", "1.1")
    fig_kerangka_pikir(OUT / "gambar_1_2_kerangka_pikir.png")
    fig_dt_spectrum(OUT / "gambar_2_1_dt_spectrum.png", "2.1")
    fig_yerkes_dodson(OUT / "gambar_2_2_yerkes_dodson.png")
    fig_zpd(OUT / "gambar_2_3_zpd.png")
    # Bab 3 figures
    fig_alur_penelitian(OUT / "gambar_3_1_alur_penelitian.png")
    fig_arsitektur_model(OUT / "gambar_3_2_arsitektur_model.png")
    fig_flowchart_mingguan(OUT / "gambar_3_3_flowchart_mingguan.png")
    fig_discomfort_termal(OUT / "gambar_3_4_discomfort_termal.png")
    fig_slump_factor(OUT / "gambar_3_5_slump_factor.png")
    fig_topic_dependency(OUT / "gambar_3_6_topic_dependency.png")
    print("\nDone. All 11 figures generated.")
