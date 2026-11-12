from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_DIR = ROOT / "reports" / "w11d1" / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, low_memory=False)
df.columns = df.columns.astype(str).str.strip()
unnamed_columns = [c for c in df.columns if c.casefold().startswith("unnamed:")]
if unnamed_columns:
    df = df.drop(columns=unnamed_columns)

required = {"Amount", "Category", "Status"}
missing_columns = required - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

# Preserve the distinction between originally missing and invalid values.
original_amount_missing = df["Amount"].isna()
amount = pd.to_numeric(df["Amount"], errors="coerce")
parse_errors = (~original_amount_missing) & amount.isna()
valid_amount = amount.dropna()

if valid_amount.empty or valid_amount.sum() == 0:
    raise ValueError("No usable Amount values found.")

# Category analysis.
category_source = pd.DataFrame({
    "Category": df["Category"].fillna("Missing").astype(str),
    "Amount": amount
})

category = (
    category_source.groupby("Category", dropna=False)
    .agg(
        order_line_count=("Amount", "count"),
        recorded_amount=("Amount", "sum")
    )
    .sort_values("recorded_amount", ascending=False)
)

category["amount_share_pct"] = (
    category["recorded_amount"] / valid_amount.sum() * 100
)
category.to_csv(OUTPUT_DIR / "category_story.csv", encoding="utf-8")

# Order-status analysis.
status = (
    df["Status"].fillna("Missing").astype(str)
    .value_counts()
    .rename_axis("status")
    .reset_index(name="row_count")
)
status["row_share_pct"] = status["row_count"] / len(df) * 100
status.to_csv(OUTPUT_DIR / "status_story.csv", index=False, encoding="utf-8")

# Core metrics.
top_category = str(category.index[0])
top_two_share = float(category.head(2)["recorded_amount"].sum()
                       / valid_amount.sum() * 100)
top_category_share = float(category.iloc[0]["amount_share_pct"])
cancelled_rows = int((df["Status"].astype("string").str.strip()
                      .str.casefold() == "cancelled").sum())

metrics = {
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "duplicate_rows": int(df.duplicated().sum()),
    "valid_amount_rows": int(amount.notna().sum()),
    "originally_missing_amount_rows": int(original_amount_missing.sum()),
    "amount_parse_errors": int(parse_errors.sum()),
    "amount_coverage_pct": float(amount.notna().mean() * 100),
    "recorded_amount_total": float(valid_amount.sum()),
    "recorded_amount_mean": float(valid_amount.mean()),
    "recorded_amount_median": float(valid_amount.median()),
    "recorded_amount_skewness": float(valid_amount.skew()),
    "top_category": top_category,
    "top_category_share_pct": top_category_share,
    "top_two_category_share_pct": top_two_share,
    "cancelled_rows": cancelled_rows,
    "cancelled_row_share_pct": float(cancelled_rows / len(df) * 100),
}

metrics_df = pd.DataFrame(
    [{"metric": key, "value": value} for key, value in metrics.items()]
)
metrics_df.to_csv(OUTPUT_DIR / "story_metrics.csv", index=False, encoding="utf-8")

# Chart 1: category concentration.
fig, ax = plt.subplots(figsize=(10, 6))
plot_category = category.head(8).sort_values("recorded_amount")
ax.barh(plot_category.index, plot_category["recorded_amount"])
ax.set_title("Recorded Amount Is Concentrated in a Few Categories")
ax.set_xlabel("Recorded Amount (INR)")
ax.set_ylabel("Category")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "01_category_concentration.png", dpi=160)
plt.close(fig)

# Chart 2: order-status distribution.
fig, ax = plt.subplots(figsize=(10, 6))
plot_status = status.head(8).sort_values("row_count")
ax.barh(plot_status["status"], plot_status["row_count"])
ax.set_title("Order Rows by Status")
ax.set_xlabel("Number of Rows")
ax.set_ylabel("Order Status")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "02_order_status.png", dpi=160)
plt.close(fig)

# Chart 3: recorded Amount distribution.
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(valid_amount, bins=40, edgecolor="black")
ax.axvline(valid_amount.median(), linestyle="--",
           label=f"Median: INR {valid_amount.median():,.2f}")
ax.axvline(valid_amount.mean(), linestyle=":",
           label=f"Mean: INR {valid_amount.mean():,.2f}")
ax.set_title("Recorded Amount Distribution Is Right-Skewed")
ax.set_xlabel("Recorded Amount (INR)")
ax.set_ylabel("Number of Rows")
ax.legend()
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "03_amount_distribution.png", dpi=160)
plt.close(fig)

# Business narrative.
report = f"""# W11D1 — Indian Retail Sales: A Data Story

## Executive summary

Recorded Amount is concentrated in a small number of product categories.
Order-status data also identifies a substantial cancelled-row segment.
However, incomplete Amount data means the findings must be interpreted
with care.

## Business question

How can retail management use category performance, order status and
data quality evidence to identify areas that deserve further investigation?

## Finding 1 — Category concentration

The leading category is **{top_category}**, representing
**{top_category_share:.2f}%** of recorded Amount.
The top two categories together represent **{top_two_share:.2f}%**.

**Business implication:** Management could examine category-level
availability, fulfilment and demand patterns before making inventory
or merchandising decisions.

## Finding 2 — Order-status visibility

There are **{cancelled_rows:,}** rows with status Cancelled,
representing **{cancelled_rows / len(df) * 100:.2f}%** of all rows.

**Business implication:** Review cancellation patterns by product,
region and time period to identify where further operational analysis
may be useful. This descriptive result does not explain the cause
of cancellations.

## Finding 3 — Amount data completeness

There are **{int(original_amount_missing.sum()):,}** originally missing
Amount values and **{int(parse_errors.sum()):,}** non-missing values
that could not be converted to numbers.
Valid Amount coverage is **{amount.notna().mean() * 100:.2f}%**.

**Business implication:** Improve data capture and validation before
using Amount-based metrics for operational decisions.

## Finding 4 — Distribution of recorded Amount

The mean recorded Amount is **INR {valid_amount.mean():,.2f}**,
while the median is **INR {valid_amount.median():,.2f}**.
Skewness is **{valid_amount.skew():.4f}**.

**Business implication:** Report both mean and median. The mean alone
may not represent a typical row when the distribution is skewed.

## Recommended next steps

1. Investigate category-level demand and fulfilment together.
2. Break down cancelled rows by category, region and date.
3. Improve completeness checks for Amount before reporting.
4. Track mean and median together in recurring business dashboards.

## Limitations

- Amount is recorded order Amount, not confirmed net revenue or profit.
- Rows are not necessarily unique customers or unique orders.
- Missing Amount values may affect comparisons and totals.
- The analysis is descriptive and does not establish causation.
- Recommendations require validation with additional business context.

## Conclusion

The dataset suggests category concentration, a meaningful cancelled-row
segment and incomplete Amount capture. These findings provide a starting
point for targeted investigation, not proof of the underlying causes.
"""

(OUTPUT_DIR / "story_report.md").write_text(report, encoding="utf-8")

print("W11D1 storytelling analysis completed.")
print(f"Dataset: {DATA_PATH}")
print(f"Rows: {len(df):,}")
print(f"Valid Amount rows: {amount.notna().sum():,}")
print(f"Originally missing Amount: {original_amount_missing.sum():,}")
print(f"Amount parse errors: {parse_errors.sum():,}")
print(f"Amount coverage: {amount.notna().mean() * 100:.2f}%")
print(f"Recorded Amount total: INR {valid_amount.sum():,.2f}")
print(f"Top category: {top_category} ({top_category_share:.2f}%)")
print(f"Top two category share: {top_two_share:.2f}%")
print(f"Cancelled rows: {cancelled_rows:,} ({cancelled_rows / len(df) * 100:.2f}%)")
print(f"Outputs: {OUTPUT_DIR}")
for path in sorted(OUTPUT_DIR.iterdir()):
    if path.is_file():
        print(f" - {path.name}: {path.stat().st_size:,} bytes")
