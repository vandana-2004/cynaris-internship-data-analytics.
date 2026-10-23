
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "archive" / "creditcard.csv"
OUT = Path(__file__).resolve().parent
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

# Analyze the complete dataset in chunks to limit memory use.
total_rows = 0
fraud_rows = 0
fraud_amount_sum = 0.0
legit_amount_sum = 0.0
fraud_count = 0
legit_count = 0

for chunk in pd.read_csv(
    DATA, usecols=["Amount", "Class"], chunksize=50000
):
    total_rows += len(chunk)
    fraud = chunk[chunk["Class"] == 1]
    legit = chunk[chunk["Class"] == 0]

    fraud_rows += len(fraud)
    fraud_count += len(fraud)
    legit_count += len(legit)
    fraud_amount_sum += fraud["Amount"].sum()
    legit_amount_sum += legit["Amount"].sum()

# Read only two columns for a lightweight sample.
sample = pd.read_csv(
    DATA, usecols=["Amount", "Class"], nrows=10000
)

# Chart 1: class counts
counts = sample["Class"].value_counts().reindex([0, 1], fill_value=0)
plt.figure(figsize=(6, 4))
plt.bar(["Legitimate", "Fraud"], counts.values)
plt.title("Transaction Class Counts (first 10,000 rows)")
plt.ylabel("Transactions")
plt.tight_layout()
plt.savefig(CHARTS / "class_counts.png", dpi=100)
plt.close()

# Chart 2: transaction amount distribution
plt.figure(figsize=(6, 4))
sample["Amount"].clip(
    upper=sample["Amount"].quantile(0.99)
).hist(bins=30)
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount (capped at sample 99th percentile)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(CHARTS / "amount_distribution.png", dpi=100)
plt.close()

# Chart 3: amounts by class
plt.figure(figsize=(6, 4))
sample.boxplot(column="Amount", by="Class")
plt.title("Transaction Amount by Class")
plt.suptitle("")
plt.xlabel("Class (0 = legitimate, 1 = fraud)")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig(CHARTS / "amount_by_class.png", dpi=100)
plt.close()

fraud_rate = fraud_rows / total_rows * 100
fraud_mean = fraud_amount_sum / fraud_count if fraud_count else 0
legit_mean = legit_amount_sum / legit_count if legit_count else 0

insights = f"""# W5D2 — Automated EDA Findings

## Dataset
- Source: Credit Card Fraud Detection
- Total rows analyzed: {total_rows:,}
- Fraud transactions: {fraud_rows:,}
- Legitimate transactions: {legit_count:,}
- Fraud prevalence: {fraud_rate:.4f}%

## Three insights
1. Fraud represents {fraud_rate:.4f}% of the dataset, showing severe class imbalance.
2. Mean fraud transaction amount is {fraud_mean:.2f}; mean legitimate amount is {legit_mean:.2f}. Means alone cannot identify fraud.
3. The three charts explore class counts and transaction amounts. They use the first 10,000 rows, while the summary statistics use the complete dataset.

## Method limitation
AutoViz and SweetViz were removed because report generation was resource-intensive in this environment. Pandas and Matplotlib were used instead; these charts are not AutoViz or SweetViz reports.
"""
(OUT / "insights.md").write_text(insights, encoding="utf-8")

comparison = """# AutoViz vs SweetViz — Business Recommendation

AutoViz supports flexible automated chart exploration and is useful for analysts examining patterns across many variables. SweetViz creates a structured HTML report with feature summaries and target comparisons, making results convenient to share. Both tools can accelerate initial exploratory data analysis, but their findings still require validation and business interpretation. For business stakeholders, I would generally recommend SweetViz because its organized report is easier to review. AutoViz is useful for analysts who want broader visual exploration. For fraud detection, both approaches should make class imbalance clear. Due to resource constraints, this exercise uses lightweight Pandas and Matplotlib charts instead of running either automated-reporting tool.
"""
(OUT / "comparison.md").write_text(comparison, encoding="utf-8")

print(f"Rows analyzed: {total_rows:,}")
print(f"Fraud transactions: {fraud_rows:,}")
print(f"Fraud prevalence: {fraud_rate:.4f}%")
print(f"Mean fraud amount: {fraud_mean:.2f}")
print(f"Mean legitimate amount: {legit_mean:.2f}")
print(f"Charts saved to: {CHARTS}")
print("Documentation saved: insights.md, comparison.md")
