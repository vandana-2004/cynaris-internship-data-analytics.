
from pathlib import Path

import pandas as pd
import sweetviz as sv

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "archive" / "Sample - Superstore.csv"
OUT = Path(__file__).resolve().parent

df = pd.read_csv(DATA, encoding="cp1252")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

for col in ["Sales", "Profit", "Quantity", "Discount"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Dataset shape:", df.shape)
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))

# Generate SweetViz using a reproducible sample to keep analysis manageable.
sample = df.sample(n=min(5000, len(df)), random_state=42)
report = sv.analyze(sample)
report.show_html(
    filepath=str(OUT / "sweetviz_report.html"),
    open_browser=False,
)
print("SweetViz report generated.")

# Calculate business findings independently using Pandas.
category = df.groupby("Category")["Sales"].sum().sort_values(
    ascending=False
)
region = df.groupby("Region")["Sales"].sum().sort_values(
    ascending=False
)
subprofit = df.groupby("Sub-Category")["Profit"].sum().sort_values()

insights = f"""# W7D2 — Automated EDA Findings

## Dataset
- Source: `data/raw/archive/Sample - Superstore.csv`
- Rows: {len(df):,}
- Columns: {len(df.columns)}
- Missing cells: {int(df.isna().sum().sum()):,}
- Duplicate rows: {int(df.duplicated().sum()):,}
- SweetViz analyzed a reproducible sample of {len(sample):,} rows.
- AutoViz was run separately on the full dataset.

## Three data-backed insights
1. **Sales by category:** {category.index[0]} has the highest total sales at {category.iloc[0]:,.2f}.
2. **Sales by region:** {region.index[0]} has the highest total sales at {region.iloc[0]:,.2f}.
3. **Sub-category profitability:** {subprofit.index[0]} has the lowest total profit at {subprofit.iloc[0]:,.2f}. Investigate product costs, discounting, and sales mix before deciding on corrective action.

## Generated reports
- SweetViz: `reports/w7d2/sweetviz_report.html`
- AutoViz outputs: `reports/w7d2/autoviz/AutoViz/`
- AutoViz visualizations include categorical plots, numeric distributions, heatmaps, pair scatter plots, and violin plots.

## Limitations
AutoViz reported that it could not classify several string columns and detected no date variables. The three findings above were calculated separately with Pandas; they are not attributed to either tool's report.
"""

(OUT / "insights.md").write_text(insights, encoding="utf-8")

comparison = """# AutoViz vs SweetViz — Business Recommendation

Both tools automate exploratory data analysis, but their generated outputs differ.

AutoViz produced five HTML visualizations for the 9,994-row Superstore dataset: categorical plots, numeric distributions, heatmaps, pair scatter plots, and violin plots. It completed successfully, although its logs reported classification limitations for several string columns and no detected date variables.

SweetViz generated a structured HTML report using a reproducible sample of 5,000 rows. Its report is a convenient single artifact for sharing variable summaries and visualizations with stakeholders.

**Recommendation:** Use SweetViz as the primary stakeholder-facing report because it offers a consolidated report that is straightforward to share. Keep AutoViz as a complementary tool for exploring visual patterns. Validate automated outputs and add business context before making decisions.
"""

(OUT / "comparison.md").write_text(comparison, encoding="utf-8")

print("\nThree findings saved to reports/w7d2/insights.md")
print("Comparison saved to reports/w7d2/comparison.md")
print("\nTop sales categories:\n", category.to_string())
print("\nSales by region:\n", region.to_string())
print("\nLowest-profit sub-categories:\n", subprofit.head(5).to_string())
