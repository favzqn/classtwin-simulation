import sys
sys.path.insert(0, ".")
from src.experiments.sensitivity import SensitivityAnalyzer
import pandas as pd

print("Running OAT sensitivity with n_runs=20 ...")
sa = SensitivityAnalyzer(metric="mean_gpa", n_runs=20)
df = sa.analyze()
print("\n=== OAT Results (n_runs=20) ===")
print(df.to_string(index=False))
print("\n=== Summary for skripsi ===")
for _, row in df.iterrows():
    delta = row.get("max_abs_delta", abs(row.get("high_val", 0) - row.get("low_val", 0)))
    print(f"  {row['parameter']}: delta = {delta:.2f}")
