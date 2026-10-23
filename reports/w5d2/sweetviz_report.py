
from pathlib import Path
import pandas as pd
import sweetviz as sv

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "archive" / "creditcard.csv"
OUT = Path(__file__).resolve().parent

print("Loading dataset...")
df = pd.read_csv(DATA)

sample = df.sample(n=min(5000, len(df)), random_state=42)
print(f"Generating SweetViz report for {len(sample):,} sampled rows...")

report = sv.analyze(sample, target_feat="Class")
report_path = OUT / "sweetviz_report.html"
report.show_html(str(report_path), open_browser=False)

print(f"SweetViz report saved: {report_path}")
print(f"Sample fraud transactions: {(sample['Class'] == 1).sum()}")
