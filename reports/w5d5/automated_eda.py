from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "w5d3" / "sales_100k.csv"
OUT = ROOT / "reports" / "w5d5"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)
required = {"order_id", "region", "category", "quantity", "sales"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

quality = {
    "rows": int(len(df)),
    "columns": int(len(df.columns)),
    "missing_cells": int(df.isna().sum().sum()),
    "duplicate_rows": int(df.duplicated().sum()),
    "duplicate_order_ids": int(df["order_id"].duplicated().sum()),
    "total_sales": round(float(df["sales"].sum()), 2),
    "average_sales": round(float(df["sales"].mean()), 2),
    "total_quantity": int(df["quantity"].sum()),
    "sales_by_region": {
        str(k): round(float(v), 2)
        for k, v in df.groupby("region")["sales"].sum()
        .sort_values(ascending=False).items()
    },
    "sales_by_category": {
        str(k): round(float(v), 2)
        for k, v in df.groupby("category")["sales"].sum()
        .sort_values(ascending=False).items()
    },
}

(OUT / "eda_summary.json").write_text(
    json.dumps(quality, indent=2), encoding="utf-8"
)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

df.groupby("region")["sales"].sum().sort_values().plot(
    kind="bar", ax=axes[0, 0], title="Total Sales by Region"
)
df.groupby("category")["sales"].sum().sort_values().plot(
    kind="bar", ax=axes[0, 1], title="Total Sales by Category"
)
sns.histplot(df["sales"], bins=30, kde=True, ax=axes[1, 0])
axes[1, 0].set_title("Sales Distribution")
sns.boxplot(data=df, x="region", y="sales", ax=axes[1, 1])
axes[1, 1].set_title("Sales by Region: Distribution")

fig.tight_layout()
fig.savefig(CHARTS / "eda_overview.png", dpi=120)
plt.close(fig)

lines = [
    "# W5D5 — Automated Exploratory Data Analysis",
    "",
    f"- Dataset: `data/w5d3/sales_100k.csv`",
    f"- Rows: {quality['rows']:,}",
    f"- Columns: {quality['columns']}",
    f"- Missing cells: {quality['missing_cells']}",
    f"- Duplicate rows: {quality['duplicate_rows']}",
    f"- Duplicate order IDs: {quality['duplicate_order_ids']}",
    f"- Total sales: {quality['total_sales']:,.2f}",
    f"- Average sales per row: {quality['average_sales']:,.2f}",
    f"- Total quantity: {quality['total_quantity']:,}",
    "",
    "## Sales by region",
]
lines += [f"- {k}: {v:,.2f}" for k, v in quality["sales_by_region"].items()]
lines += ["", "## Sales by category"]
lines += [f"- {k}: {v:,.2f}" for k, v in quality["sales_by_category"].items()]
lines += [
    "",
    "## Chart",
    "See `charts/eda_overview.png` for sales by region, sales by category,",
    "sales distribution, and regional sales distributions.",
    "",
    "## AI analysis status",
    "PandasAI execution is pending because the current Python environment",
    "does not have PandasAI installed. No AI-generated findings are claimed.",
]
(OUT / "eda_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print("W5D5 EDA completed")
print(f"Rows: {quality['rows']:,}")
print(f"Missing cells: {quality['missing_cells']}")
print(f"Duplicate rows: {quality['duplicate_rows']}")
print(f"Total sales: {quality['total_sales']:,.2f}")
print(f"Report: {OUT / 'eda_report.md'}")
print(f"Chart: {CHARTS / 'eda_overview.png'}")
