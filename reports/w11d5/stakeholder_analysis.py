
from pathlib import Path
import warnings

import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)

# ============================================================
# W11D5: Stakeholder Report - 5 Business Insights
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = ROOT / "data" / "w8d3" / "indian_business_sales.csv"

OUT = ROOT / "reports" / "w11d5" / "outputs"
CHARTS = OUT / "charts"

OUT.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("W11D5 STAKEHOLDER ANALYSIS")
print("=" * 65)

# ------------------------------------------------------------
# 1. Load and prepare data
# ------------------------------------------------------------

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE, low_memory=False)

# Normalize column names
df.columns = df.columns.str.strip()

required_columns = [
    "Date",
    "Status",
    "Fulfilment",
    "Category",
    "Amount",
    "ship-state",
    "B2B"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Convert numeric values
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# Source dates use MM-DD-YY format, e.g. 04-30-22
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m-%d-%y",
    errors="coerce"
)

# Normalize B2B values
df["B2B"] = (
    df["B2B"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({"true": True, "false": False})
)

# Handle missing grouping values
for column in ["Category", "Status", "Fulfilment", "ship-state"]:
    df[column] = df[column].fillna("Unknown").astype(str).str.strip()

# Overall metrics
total_rows = len(df)

if total_rows == 0:
    raise ValueError("The dataset contains no records.")

valid_amount_rows = int(df["Amount"].notna().sum())
total_amount = float(df["Amount"].sum())

amount_coverage = valid_amount_rows / total_rows * 100

cancelled_rows = int(
    df["Status"].str.lower().eq("cancelled").sum()
)

cancelled_rate = cancelled_rows / total_rows * 100

valid_dates = df["Date"].dropna()

if valid_dates.empty:
    raise ValueError("No valid dates found in the dataset.")

print(f"Dataset rows: {total_rows:,}")
print(f"Valid Amount rows: {valid_amount_rows:,}")
print(f"Recorded Amount: Rs. {total_amount:,.2f}")
print(f"Amount coverage: {amount_coverage:.2f}%")
print(f"Cancelled rows: {cancelled_rows:,} ({cancelled_rate:.2f}%)")
print(f"Date range: {valid_dates.min()} to {valid_dates.max()}")

# ------------------------------------------------------------
# 2. Create stakeholder analysis tables
# ------------------------------------------------------------

# Category analysis
category = (
    df.groupby("Category")
    .agg(
        records=("Category", "size"),
        recorded_amount=("Amount", "sum")
    )
    .sort_values("recorded_amount", ascending=False)
)

category["record_share_pct"] = (
    category["records"] / total_rows * 100
)

category["amount_share_pct"] = (
    category["recorded_amount"] / total_amount * 100
)

# Fulfilment analysis
df["is_cancelled"] = (
    df["Status"].str.lower() == "cancelled"
)

fulfilment = (
    df.groupby("Fulfilment")
    .agg(
        records=("Fulfilment", "size"),
        cancelled_records=("is_cancelled", "sum"),
        recorded_amount=("Amount", "sum")
    )
)

fulfilment["cancellation_rate_pct"] = (
    fulfilment["cancelled_records"]
    / fulfilment["records"] * 100
)

fulfilment["amount_share_pct"] = (
    fulfilment["recorded_amount"] / total_amount * 100
)

# State analysis
state = (
    df.groupby("ship-state")
    .agg(
        records=("ship-state", "size"),
        recorded_amount=("Amount", "sum")
    )
    .sort_values("recorded_amount", ascending=False)
)

state["amount_share_pct"] = (
    state["recorded_amount"] / total_amount * 100
)

# Order status analysis
status = (
    df.groupby("Status")
    .agg(
        records=("Status", "size"),
        recorded_amount=("Amount", "sum")
    )
    .sort_values("records", ascending=False)
)

status["record_share_pct"] = (
    status["records"] / total_rows * 100
)

# B2B analysis
b2b = (
    df.dropna(subset=["B2B"])
    .groupby("B2B")
    .agg(
        records=("B2B", "size"),
        recorded_amount=("Amount", "sum"),
        average_recorded_amount=("Amount", "mean")
    )
)

b2b["record_share_pct"] = (
    b2b["records"] / total_rows * 100
)

if True not in b2b.index or False not in b2b.index:
    raise ValueError("Both B2B and non-B2B groups are required.")

# Monthly analysis
monthly_data = df.dropna(subset=["Date"]).copy()

monthly_data["month"] = (
    monthly_data["Date"].dt.to_period("M").astype(str)
)

monthly = (
    monthly_data.groupby("month")
    .agg(
        records=("month", "size"),
        recorded_amount=("Amount", "sum")
    )
    .reset_index()
)

# ------------------------------------------------------------
# 3. Save supporting CSV files
# ------------------------------------------------------------

category.to_csv(OUT / "category_analysis.csv", encoding="utf-8")
fulfilment.to_csv(OUT / "fulfilment_analysis.csv", encoding="utf-8")
state.to_csv(OUT / "state_analysis.csv", encoding="utf-8")
status.to_csv(OUT / "status_analysis.csv", encoding="utf-8")
b2b.to_csv(OUT / "b2b_analysis.csv", encoding="utf-8")
monthly.to_csv(
    OUT / "monthly_analysis.csv",
    index=False,
    encoding="utf-8"
)

print("\nSix analysis CSV files saved.")

# ------------------------------------------------------------
# 4. Generate charts
# ------------------------------------------------------------

# Chart 1: Category recorded Amount
ax = category.sort_values("recorded_amount").plot.barh(
    y="recorded_amount",
    legend=False,
    figsize=(10, 6)
)

ax.set_title("Recorded Amount by Product Category")
ax.set_xlabel("Recorded Amount (Rs.)")
ax.set_ylabel("Category")

plt.tight_layout()
plt.savefig(CHARTS / "category_amount.png", dpi=150)
plt.close()

# Chart 2: Cancellation rate by fulfilment
ax = fulfilment["cancellation_rate_pct"].plot.bar(
    rot=0,
    figsize=(9, 5)
)

ax.set_title("Cancellation Rate by Fulfilment Method")
ax.set_xlabel("Fulfilment")
ax.set_ylabel("Cancellation Rate (%)")

plt.tight_layout()
plt.savefig(CHARTS / "fulfilment_cancellation.png", dpi=150)
plt.close()

# Chart 3: Top 10 states by recorded Amount
ax = state.head(10).sort_values("recorded_amount").plot.barh(
    y="recorded_amount",
    legend=False,
    figsize=(10, 6)
)

ax.set_title("Top 10 States by Recorded Amount")
ax.set_xlabel("Recorded Amount (Rs.)")
ax.set_ylabel("State")

plt.tight_layout()
plt.savefig(CHARTS / "state_amount.png", dpi=150)
plt.close()

# Chart 4: Top 8 order statuses
ax = status.head(8).sort_values("records").plot.barh(
    y="records",
    legend=False,
    figsize=(10, 6)
)

ax.set_title("Top 8 Order Statuses by Record Count")
ax.set_xlabel("Number of Records")
ax.set_ylabel("Order Status")

plt.tight_layout()
plt.savefig(CHARTS / "order_status.png", dpi=150)
plt.close()

print("Four charts saved.")

# ------------------------------------------------------------
# 5. Calculate the five business insights
# ------------------------------------------------------------

top_two_category_share = (
    category.head(2)["amount_share_pct"].sum()
)

amazon_rate = fulfilment.loc[
    "Amazon", "cancellation_rate_pct"
]

merchant_rate = fulfilment.loc[
    "Merchant", "cancellation_rate_pct"
]

fulfilment_gap = merchant_rate - amazon_rate

top_two_state_share = (
    state.head(2)["amount_share_pct"].sum()
)

b2b_average = b2b.loc[
    True, "average_recorded_amount"
]

non_b2b_average = b2b.loc[
    False, "average_recorded_amount"
]

b2b_difference = (
    b2b_average / non_b2b_average - 1
) * 100

b2b_records = int(b2b.loc[True, "records"])

top_categories = category.head(2)
top_states = state.head(2)

# ------------------------------------------------------------
# 6. Build stakeholder report
# ------------------------------------------------------------

def rupees(value):
    return f"Rs. {value:,.2f}"


monthly_lines = [
    "| Month | Records | Recorded Amount |",
    "|---|---:|---:|"
]

for _, row in monthly.iterrows():
    monthly_lines.append(
        f"| {row['month']} | {int(row['records']):,} "
        f"| {rupees(row['recorded_amount'])} |"
    )

report = f"""# W11D5 Stakeholder Report

## Indian Business Sales Dataset - Five Business Insights

### Executive summary

The dataset contains **{total_rows:,} records** from
**{valid_dates.min():%d %B %Y} to {valid_dates.max():%d %B %Y}**.

Recorded Amount totals **{rupees(total_amount)}**, with valid
Amount values available for **{amount_coverage:.2f}%** of records.

The analysis identifies category concentration, fulfilment
cancellation differences, geographic concentration, cancellation
volume, and an exploratory B2B average-amount difference.

> **Important:** Recorded Amount is a dataset field. It is not
> independently verified net revenue, profit, or cash collected.

---

## Five business insights and recommendations

### 1. Product category concentration

The two largest categories are **{top_categories.index[0]}**
and **{top_categories.index[1]}**. Together they account for
**{top_two_category_share:.2f}%** of recorded Amount.

**Business implication:** A large share of recorded Amount is
concentrated in two categories.

**Recommendation:** Monitor stock availability, demand patterns,
and returns for these categories. Review the remaining categories
for opportunities to diversify demand.

![Category recorded amount](charts/category_amount.png)

### 2. Cancellation rates differ by fulfilment method

Amazon fulfilment has a cancellation rate of **{amazon_rate:.2f}%**,
while Merchant fulfilment has a rate of **{merchant_rate:.2f}%**.

The difference is **{fulfilment_gap:.2f} percentage points**.

**Business implication:** The observed cancellation rates differ
between the two fulfilment groups.

**Recommendation:** Review merchant order processing, dispatch
timelines, and cancellation reasons. Compare similar products and
periods before deciding what operational changes are appropriate.

This is a descriptive comparison and does not establish that
fulfilment method causes cancellations.

![Fulfilment cancellation rates](charts/fulfilment_cancellation.png)

### 3. Recorded Amount is geographically concentrated

The two leading states are **{top_states.index[0]}**
and **{top_states.index[1]}**. Together they represent
**{top_two_state_share:.2f}%** of recorded Amount.

**Business implication:** These two states account for a substantial
share of the dataset's recorded Amount.

**Recommendation:** Monitor service levels and stock availability
in these states while reviewing growth opportunities in other
regions.

![Top states by recorded amount](charts/state_amount.png)

### 4. Cancellations are an operational signal

There are **{cancelled_rows:,} cancelled records**, representing
**{cancelled_rate:.2f}%** of all records.

**Business implication:** Cancellation volume is large enough to
deserve operational investigation.

**Recommendation:** Segment cancellations by date, category,
fulfilment method, and state. Investigate the underlying reasons
before proposing corrective actions.

Cancelled Amount must not automatically be described as lost
revenue. The dataset does not establish the financial outcome
of each cancellation.

![Order status counts](charts/order_status.png)

### 5. B2B records show a higher average recorded Amount

The B2B group has an average recorded Amount of
**{rupees(b2b_average)}**, compared with
**{rupees(non_b2b_average)}** for non-B2B records.

The observed difference is **{b2b_difference:.2f}%**.

However, B2B represents only **{b2b_records:,} records**
({b2b.loc[True, 'record_share_pct']:.2f}% of all records).

**Business implication:** The B2B group has a higher observed
average, but it is a small segment.

**Recommendation:** Treat this as an exploratory finding.
Validate with more data and investigate order size, product mix,
and repeat purchasing before designing a B2B strategy.

---

## Supporting monthly context

{chr(10).join(monthly_lines)}

March and June are partial months in this dataset. Avoid direct
like-for-like comparisons with the full months of April and May.

## Dataset quality and limitations

- Total records: {total_rows:,}
- Valid Amount records: {valid_amount_rows:,}
- Amount coverage: {amount_coverage:.2f}%
- Missing Amount records: {total_rows - valid_amount_rows:,}
- Cancelled records: {cancelled_rows:,} ({cancelled_rate:.2f}%)
- Valid date range: {valid_dates.min():%d %B %Y} to {valid_dates.max():%d %B %Y}
- Missing Amount values are excluded from Amount totals.
- Recorded Amount is not verified profit or net revenue.
- The analysis uses available records and does not establish causation.
- The dataset covers a limited period, not a full year.
- The B2B group is small and should be interpreted cautiously.

## Reproducibility

Run from the repository root:

```powershell
python reports/w11d5/stakeholder_analysis.py
```

### Generated files

- `outputs/category_analysis.csv`
- `outputs/fulfilment_analysis.csv`
- `outputs/state_analysis.csv`
- `outputs/status_analysis.csv`
- `outputs/b2b_analysis.csv`
- `outputs/monthly_analysis.csv`
- `outputs/charts/category_amount.png`
- `outputs/charts/fulfilment_cancellation.png`
- `outputs/charts/state_amount.png`
- `outputs/charts/order_status.png`
- `outputs/stakeholder_report.md`
"""

report_path = OUT / "stakeholder_report.md"

report_path.write_text(
    report,
    encoding="utf-8"
)

print("\nStakeholder report saved:", report_path)

# ------------------------------------------------------------
# 7. Validation checks
# ------------------------------------------------------------

assert total_rows == 128975, (
    f"Unexpected row count: {total_rows}"
)

assert abs(total_amount - 78592678.30) < 1.00, (
    f"Unexpected recorded Amount total: {total_amount}"
)

assert abs(amount_coverage - 93.96) < 0.02, (
    f"Unexpected Amount coverage: {amount_coverage}"
)

assert valid_amount_rows == 121180

assert cancelled_rows == 18332

assert int(status["records"].sum()) == total_rows

assert len(status) == 13

assert len(category) == 9

assert len(monthly) == 4

assert abs(top_two_category_share - 76.98) < 0.02

assert abs(fulfilment_gap - 4.68) < 0.02

assert abs(top_two_state_share - 30.30) < 0.02

assert abs(b2b_difference - 8.20) < 0.02

assert len(list(OUT.glob("*.csv"))) == 6

assert len(list(CHARTS.glob("*.png"))) == 4

assert report_path.exists()

assert report_path.stat().st_size > 0

print("\n" + "=" * 65)
print("VALIDATION: PASS")
print("=" * 65)

print("Rows:", f"{total_rows:,}")
print("Recorded Amount:", rupees(total_amount))
print("Amount coverage:", f"{amount_coverage:.2f}%")
print("Category concentration:", f"{top_two_category_share:.2f}%")
print("Fulfilment cancellation gap:", f"{fulfilment_gap:.2f} pp")
print("Top two state share:", f"{top_two_state_share:.2f}%")
print("B2B average difference:", f"{b2b_difference:.2f}%")

print("\nGenerated files:")
print("CSV files: 6")
print("Chart files: 4")
print("Stakeholder report:", report_path)
print("Charts folder:", CHARTS)

print("\nW11D5 analysis completed successfully.")
