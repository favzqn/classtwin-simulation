
import sys
sys.path.insert(0, ".")
from src.experiments.sensitivity import SensitivityAnalyzer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sa = SensitivityAnalyzer(metric="mean_gpa", n_runs=10)
cv = sa.convergence_test()
print(cv.to_string())

fig, ax = plt.subplots(figsize=(8, 5))
ax.errorbar(cv["n_students"], cv["mean"], yerr=cv["ci95"],
            marker="o", capsize=5, linewidth=2, markersize=8, color="#2196F3")
ax.set_xlabel("Jumlah Mahasiswa (N)", fontsize=12)
ax.set_ylabel("IPK Rata-rata", fontsize=12)
ax.set_title("Uji Konvergensi: IPK Rata-rata ± CI95% vs Jumlah Mahasiswa", fontsize=13)
ax.grid(True, alpha=0.3)
ax.set_xticks(cv["n_students"])
plt.tight_layout()
plt.savefig("data/thesis_report/figures/convergence_test.png", dpi=150)
print("Saved to data/thesis_report/figures/convergence_test.png")
