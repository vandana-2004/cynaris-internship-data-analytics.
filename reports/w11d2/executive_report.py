from pathlib import Path
import warnings

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.express as px
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
BASE = ROOT / "reports" / "w11d2"
OUT = BASE / "outputs"
CHARTS = OUT / "charts"
IMAGES = OUT / "images"

for folder in (OUT, CHARTS, IMAGES):
    folder.mkdir(parents=True, exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError(DATA)

df = pd.read_csv(DATA, low_memory=False)
df.columns = df.columns.astype(str).str.strip()
df = df.loc[:, ~df.columns.str.casefold().str.startswith("unnamed:")].copy()

required = {"Amount", "Category", "Status", "Date", "Qty", "Fulfilment", "ship-state"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

amount_original = df["Amount"]
amount = pd.to_numeric(amount_original, errors="coerce")
valid = amount.dropna()

if valid.empty:
    raise ValueError("No valid Amount values available.")

df["Amount"] = amount
df["Category"] = df["Category"].fillna("Missing").astype(str).str.strip()
df["Status"] = df["Status"].fillna("Missing").astype(str).str.strip()
df["Fulfilment"] = df["Fulfilment"].fillna("Missing").astype(str).str.strip()
df["ship-state"] = df["ship-state"].fillna("Missing").astype(str).str.strip()
df["Date"] = pd.to_datetime(df["Date"], format="%m-%d-%y", errors="coerce")

total_rows = len(df)
total_amount = float(valid.sum())
if total_amount == 0:
    raise ValueError("Recorded Amount total is zero; category shares cannot be calculated.")
mean_amount = float(valid.mean())
median_amount = float(valid.median())
coverage = float(valid.notna().sum() / total_rows * 100)
cancelled = int(df["Status"].str.casefold().eq("cancelled").sum())
duplicate_rows = int(df.duplicated().sum())

category = (
    df.dropna(subset=["Amount"])
    .groupby("Category")
    .agg(recorded_amount=("Amount", "sum"), row_count=("Amount", "count"))
    .sort_values("recorded_amount", ascending=False)
)
category["share_pct"] = category["recorded_amount"] / total_amount * 100
category["cumulative_share_pct"] = category["share_pct"].cumsum()

status = (
    df["Status"].value_counts()
    .rename_axis("Status").reset_index(name="Rows")
)

state = (
    df.dropna(subset=["Amount"])
    .groupby("ship-state")["Amount"].sum()
    .sort_values(ascending=False)
    .head(10)
)

monthly_source = df.dropna(subset=["Date", "Amount"]).copy()
monthly_source["Month"] = monthly_source["Date"].dt.to_period("M").astype(str)
monthly = monthly_source.groupby("Month")["Amount"].sum().sort_index()

fulfilment = df["Fulfilment"].value_counts()

# Save supporting analytical tables.
category.to_csv(OUT / "category_performance.csv", encoding="utf-8")
status.to_csv(OUT / "order_status.csv", index=False, encoding="utf-8")
state.rename("recorded_amount").to_csv(OUT / "state_performance.csv", encoding="utf-8")
monthly.rename("recorded_amount").to_csv(OUT / "monthly_performance.csv", encoding="utf-8")

# Interactive Plotly charts.
figures = {
    "category_performance": px.bar(
        category.head(10).sort_values("recorded_amount"),
        x="recorded_amount", y=category.head(10).sort_values("recorded_amount").index,
        orientation="h", title="Top Categories by Recorded Amount",
        labels={"recorded_amount": "Recorded Amount (INR)", "y": "Category"},
        text_auto=".2s"
    ),
    "order_status": px.bar(
        status, x="Status", y="Rows", title="Order Rows by Status",
        text_auto=True
    ),
    "monthly_performance": px.line(
        x=monthly.index, y=monthly.values, markers=True,
        title="Monthly Recorded Amount",
        labels={"x": "Month", "y": "Recorded Amount (INR)"}
    ),
    "state_performance": px.bar(
        x=state.values, y=state.index, orientation="h",
        title="Top 10 States by Recorded Amount",
        labels={"x": "Recorded Amount (INR)", "y": "State"}
    ),
}

pareto_data = category.reset_index()
pareto_fig = px.bar(
    pareto_data,
    x="Category",
    y="recorded_amount",
    title="Category Pareto Analysis ? Recorded Amount",
    labels={"recorded_amount": "Recorded Amount (INR)"}
)
pareto_fig.add_scatter(
    x=pareto_data["Category"],
    y=pareto_data["cumulative_share_pct"],
    name="Cumulative share (%)",
    mode="lines+markers",
    yaxis="y2"
)
pareto_fig.update_layout(
    yaxis2={
        "title": "Cumulative share (%)",
        "overlaying": "y",
        "side": "right",
        "range": [0, 105]
    },
    xaxis_tickangle=-30
)
figures["category_pareto"] = pareto_fig

for name, fig in figures.items():
    fig.update_layout(template="plotly_white", title_x=0.5)
    fig.write_html(
        CHARTS / f"{name}.html",
        include_plotlyjs="cdn",
        full_html=True
    )

# Matplotlib images for PowerPoint.
fig, ax = plt.subplots(figsize=(10, 5.5))
plot_cat = category.head(10).sort_values("recorded_amount")
ax.barh(plot_cat.index, plot_cat["recorded_amount"])
ax.set_title("Top Categories by Recorded Amount")
ax.set_xlabel("INR")
fig.tight_layout()
fig.savefig(IMAGES / "category_performance.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
pareto_data = category.reset_index()
ax.bar(pareto_data["Category"], pareto_data["recorded_amount"])
ax.set_title("Category Pareto Analysis ? Recorded Amount")
ax.set_ylabel("Recorded Amount (INR)")
ax.tick_params(axis="x", rotation=30)
ax2 = ax.twinx()
ax2.plot(
    pareto_data["Category"],
    pareto_data["cumulative_share_pct"],
    marker="o",
    linewidth=2
)
ax2.set_ylabel("Cumulative share (%)")
ax2.set_ylim(0, 105)
fig.tight_layout()
fig.savefig(IMAGES / "category_pareto.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(status["Status"], status["Rows"])
ax.set_title("Order Rows by Status")
ax.set_ylabel("Rows")
ax.tick_params(axis="x", rotation=35)
fig.tight_layout()
fig.savefig(IMAGES / "order_status.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(monthly.index, monthly.values, marker="o")
ax.set_title("Monthly Recorded Amount")
ax.set_ylabel("INR")
ax.tick_params(axis="x", rotation=35)
fig.tight_layout()
fig.savefig(IMAGES / "monthly_performance.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
plot_state = state.sort_values()
ax.barh(plot_state.index, plot_state.values)
ax.set_title("Top 10 States by Recorded Amount")
ax.set_xlabel("INR")
fig.tight_layout()
fig.savefig(IMAGES / "state_performance.png", dpi=160)
plt.close(fig)

top_category = str(category.index[0])
top_share = float(category.iloc[0]["share_pct"])
top_two_share = float(category.head(2)["recorded_amount"].sum() / total_amount * 100)
missing_amount = int(amount_original.isna().sum())

summary = f"""# W11D2 — Executive Analytics Report

## Executive overview

This report summarizes {total_rows:,} dataset rows from the Indian Business Sales dataset.

| KPI | Result |
|---|---:|
| Dataset rows | {total_rows:,} |
| Recorded Amount total | INR {total_amount:,.2f} |
| Mean recorded Amount per valid row | INR {mean_amount:,.2f} |
| Median recorded Amount per valid row | INR {median_amount:,.2f} |
| Amount completeness | {coverage:.2f}% |
| Cancelled rows | {cancelled:,} ({cancelled / total_rows * 100:.2f}%) |

## Key findings

1. **Category concentration:** {top_category} leads with {top_share:.2f}% of valid recorded Amount. The top two categories account for {top_two_share:.2f}%, indicating concentration worth monitoring. The business meaning of the source label "Set" requires confirmation.
2. **Order status:** {cancelled:,} rows ({cancelled / total_rows * 100:.2f}%) have Cancelled status. This is a descriptive observation, not an explanation of cancellation causes.
3. **Data quality:** {missing_amount:,} Amount values are originally missing. Valid Amount coverage is {coverage:.2f}%.
4. **Typical recorded Amount:** Mean INR {mean_amount:,.2f}; median INR {median_amount:,.2f}.

## Recommendations

- Monitor the top-two-category concentration ({top_two_share:.2f}% of valid recorded Amount) and assess diversification options with additional business context.
- Confirm the official business definition of the "Set" category before assigning it a product or bundle meaning.
- Investigate category-level demand, stock availability and fulfilment patterns.
- Examine cancellations by category, state and date before proposing operational changes.
- Improve Amount field completeness and validation.
- Monitor monthly recorded Amount and state-level distribution.
- Present mean and median together to avoid relying on one summary statistic.

## Limitations

- Recorded Amount is not confirmed net revenue or profit.
- Dataset rows are not necessarily unique orders or customers.
- Amount-based analysis excludes rows with missing Amount.
- Monthly trends reflect the available dataset period only.
- Descriptive analysis does not establish causation.
- State and category comparisons require additional operational context.

## Generated outputs

- Five interactive Plotly HTML charts, including a category Pareto chart.
- Five PowerPoint-ready chart images.
- Four supporting CSV analytical tables.
- Eight-slide executive presentation.
"""

(OUT / "executive_summary.md").write_text(summary, encoding="utf-8")

# Eight-slide executive PowerPoint.
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(31, 55, 80)
BLUE = RGBColor(45, 105, 160)
GREY = RGBColor(85, 95, 105)

def add_title(slide, title, subtitle=None):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(0.3), Inches(12.2), Inches(0.65))
    p = box.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(27)
    p.font.bold = True
    p.font.color.rgb = NAVY
    if subtitle:
        sub = slide.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12), Inches(0.4))
        para = sub.text_frame.paragraphs[0]
        para.text = subtitle
        para.font.size = Pt(11)
        para.font.color.rgb = GREY

def add_bullets(slide, items, top=1.5):
    box = slide.shapes.add_textbox(Inches(0.85), Inches(top), Inches(11.7), Inches(5.3))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(19)
        p.font.color.rgb = NAVY
        p.space_after = Pt(18)

def add_chart_slide(title, image_name, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title, subtitle)
    slide.shapes.add_picture(
        str(IMAGES / image_name),
        Inches(1.1), Inches(1.45), width=Inches(11.1), height=Inches(5.45)
    )
    return slide

# 1. Cover.
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "INDIAN BUSINESS SALES", "Executive Analytics Report | W11D2")
add_bullets(slide, [
    "Executive reporting with Plotly and python-pptx",
    f"Analysis covers {total_rows:,} dataset rows",
    "Focus: category performance, order status, monthly patterns and geography",
    "Prepared as a descriptive business analysis"
], top=2.0)

# 2. Executive KPI overview.
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Executive Overview", "Key metrics from the available dataset")
add_bullets(slide, [
    f"Recorded Amount total: INR {total_amount:,.2f}",
    f"Valid Amount coverage: {coverage:.2f}%",
    f"Mean / median recorded Amount: INR {mean_amount:,.2f} / INR {median_amount:,.2f}",
    f"Cancelled rows: {cancelled:,} ({cancelled / total_rows * 100:.2f}%)",
    f"Duplicate rows: {duplicate_rows:,}"
])
# 3?7. Five visual analysis slides.
add_chart_slide("Category Performance", "category_performance.png",
                f"{top_category} leads with {top_share:.2f}% of valid recorded Amount.")
add_chart_slide("Category Concentration ? Pareto", "category_pareto.png",
                f"Top two categories account for {top_two_share:.2f}% of valid recorded Amount; confirm the meaning of Set.")
add_chart_slide("Order Status", "order_status.png",
                "Status counts describe dataset rows, not unique orders.")
add_chart_slide("Monthly Performance", "monthly_performance.png",
                "Monthly totals include rows with valid dates and recorded Amount.")
add_chart_slide("State Performance", "state_performance.png",
                "Top states ranked by valid recorded Amount.")

# 7. Recommendations and limitations.
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Recommendations & Reporting Caveats")
add_bullets(slide, [
    f"Monitor concentration: the top two categories represent {top_two_share:.2f}% of valid recorded Amount.",
    "Confirm the business definition of the Set category before assigning product meaning.",
    "Investigate category demand, availability and fulfilment together.",
    "Review cancellation patterns by category, state and date.",
    "Improve completeness checks for the Amount field.",
    "Track monthly and state-level recorded Amount over time.",
    "Recorded Amount is not confirmed net revenue or profit; findings are descriptive."
], top=1.45)

ppt_path = OUT / "executive_report.pptx"
prs.save(ppt_path)

# Validation manifest.
expected = [
    *(CHARTS / f"{name}.html" for name in figures),
    *(IMAGES / f"{name}.png" for name in [
        "category_performance", "category_pareto", "order_status",
        "monthly_performance", "state_performance"
    ]),
    OUT / "executive_summary.md",
    ppt_path,
    OUT / "category_performance.csv",
    OUT / "order_status.csv",
    OUT / "state_performance.csv",
    OUT / "monthly_performance.csv",
]

missing_outputs = [str(path) for path in expected if not path.exists() or path.stat().st_size == 0]
if missing_outputs:
    raise RuntimeError(f"Missing or empty outputs: {missing_outputs}")

check = Presentation(ppt_path)
if len(check.slides) != 8:
    raise RuntimeError(f"Expected 8 slides, found {len(check.slides)}")

print("W11D2 EXECUTIVE REPORT COMPLETED")
print(f"Rows: {total_rows:,}")
print(f"Recorded Amount: INR {total_amount:,.2f}")
print(f"Amount coverage: {coverage:.2f}%")
print(f"PowerPoint slides: {len(check.slides)}")
print(f"Validated outputs: {len(expected)}")
for path in expected:
    print(f"{path.relative_to(ROOT)} | {path.stat().st_size:,} bytes")
