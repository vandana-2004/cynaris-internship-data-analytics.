
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# --------------------------------------------------
# 1. Project paths and configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "w8d3" / "indian_business_sales.csv"

OUT = Path(__file__).resolve().parent / "outputs"
CHARTS = OUT / "charts"
IMAGES = OUT / "images"

REQUIRED_COLUMNS = [
    "Date",
    "Amount",
    "Category",
    "Status",
    "ship-state",
]


# --------------------------------------------------
# 2. Directory and data-loading functions
# --------------------------------------------------

def create_directories():
    """Create output directories when they do not exist."""
    for folder in (OUT, CHARTS, IMAGES):
        folder.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load the source dataset and validate its structure."""
    if not DATA.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA}")

    df = pd.read_csv(DATA, low_memory=False)

    if df.empty:
        raise ValueError("The source dataset is empty.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    return df


# --------------------------------------------------
# 3. Data cleaning and validation
# --------------------------------------------------

def prepare_data(df):
    """Clean source-only fields and normalize analytical columns."""
    df = df.copy()

    # Remove non-analytical source fields.
    df = df.drop(
        columns=["index", "Unnamed: 22"],
        errors="ignore",
    )

    # Convert numeric and date fields.
    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce",
    )

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%m-%d-%y",
        errors="coerce",
    )

    # Normalize categorical fields.
    for column in ["Category", "Status", "ship-state"]:
        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )

    if df["Amount"].notna().sum() == 0:
        raise ValueError("No valid Amount values are available.")

    if df["Date"].notna().sum() == 0:
        raise ValueError("No valid dates are available.")

    total_amount = float(df["Amount"].sum())

    if total_amount == 0:
        raise ValueError("Recorded Amount total is zero.")

    return df


# --------------------------------------------------
# 4. Business aggregations
# --------------------------------------------------

def aggregate_data(df):
    """Generate vectorized summaries for dashboard components."""

    category = (
        df.dropna(subset=["Amount"])
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    monthly = (
        df.dropna(subset=["Date", "Amount"])
        .assign(
            Month=lambda x: (
                x["Date"].dt.to_period("M").astype(str)
            )
        )
        .groupby("Month", as_index=False)["Amount"]
        .sum()
        .sort_values("Month")
    )

    # Retain every order status, not just the top eight.
    status = (
        df["Status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Orders")
    )

    states = (
        df.dropna(subset=["Amount"])
        .groupby("ship-state", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
        .head(10)
    )

    return category, monthly, status, states


# --------------------------------------------------
# 5. Export supporting CSV files
# --------------------------------------------------

def export_tables(category, monthly, status, states):
    """Export aggregated dashboard tables as CSV files."""

    category.to_csv(
        OUT / "category_amount.csv",
        index=False,
    )

    monthly.to_csv(
        OUT / "monthly_amount.csv",
        index=False,
    )

    status.to_csv(
        OUT / "order_status.csv",
        index=False,
    )

    states.to_csv(
        OUT / "state_amount.csv",
        index=False,
    )


# --------------------------------------------------
# 6. Interactive chart generation
# --------------------------------------------------

def create_interactive_charts(
    df, category, monthly, status, states
):
    """Create individual Plotly charts and combined dashboard."""

    date_start = df["Date"].min().strftime("%d %b %Y")
    date_end = df["Date"].max().strftime("%d %b %Y")

    date_label = f"{date_start} – {date_end}"

    # Chart 1: Top categories.
    bar = px.bar(
        category.sort_values("Amount"),
        x="Amount",
        y="Category",
        orientation="h",
        title=(
            "Top Categories by Recorded Amount "
            f"({date_label})"
        ),
        labels={
            "Amount": "Recorded Amount (INR)",
            "Category": "Category",
        },
    )

    bar.write_html(
        CHARTS / "category_bar.html",
        include_plotlyjs=True,
    )

    # Chart 2: Monthly trend.
    line = px.line(
        monthly,
        x="Month",
        y="Amount",
        markers=True,
        title="Monthly Recorded Amount",
        labels={
            "Amount": "Recorded Amount (INR)",
            "Month": "Month",
        },
    )

    line.write_html(
        CHARTS / "monthly_line.html",
        include_plotlyjs=True,
    )

    # Chart 3: All order statuses as horizontal bars.
    status_sorted = status.sort_values("Orders")

    status_chart = px.bar(
        status_sorted,
        x="Orders",
        y="Status",
        orientation="h",
        title="Order Status Distribution (All Statuses)",
        labels={
            "Orders": "Number of Rows",
            "Status": "Order Status",
        },
    )

    status_chart.write_html(
        CHARTS / "order_status_bar.html",
        include_plotlyjs=True,
    )

    # Chart 4: Top states table.
    table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[
                        "State",
                        "Recorded Amount (INR)",
                    ]
                ),
                cells=dict(
                    values=[
                        states["ship-state"],
                        states["Amount"].map(
                            lambda x: f"{x:,.2f}"
                        ),
                    ]
                ),
            )
        ]
    )

    table.update_layout(
        title="Top 10 States by Recorded Amount"
    )

    table.write_html(
        CHARTS / "state_amount_table.html",
        include_plotlyjs=True,
    )

    # Metric calculations.
    coverage = df["Amount"].notna().mean() * 100

    cancelled = (
        df["Status"]
        .str.lower()
        .eq("cancelled")
        .mean() * 100
    )

    total_amount = float(df["Amount"].sum())

    # Combined five-component dashboard.
    dashboard = make_subplots(
        rows=3,
        cols=2,
        specs=[
            [{"type": "indicator"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "bar"}],
            [{"type": "table", "colspan": 2}, None],
        ],
        subplot_titles=[
            "Dataset Overview",
            "Top Categories",
            "Monthly Recorded Amount",
            "Order Status",
            "Top States",
        ],
        vertical_spacing=0.13,
        horizontal_spacing=0.10,
        row_heights=[0.25, 0.35, 0.40],
    )

    # Metric card.
    dashboard.add_trace(
        go.Indicator(
            mode="number",
            value=len(df),
            title={
                "text": (
                    "Source Rows"
                    "<br><span style='font-size:13px'>"
                    f"Recorded Amount: INR {total_amount:,.2f}"
                    "<br>"
                    f"Amount Coverage: {coverage:.2f}%"
                    "</span>"
                )
            },
            number={"valueformat": ",.0f"},
        ),
        row=1,
        col=1,
    )

    # Category bar chart.
    dashboard.add_trace(
        go.Bar(
            x=category["Amount"],
            y=category["Category"],
            orientation="h",
            name="Recorded Amount",
        ),
        row=1,
        col=2,
    )

    # Monthly line chart.
    dashboard.add_trace(
        go.Scatter(
            x=monthly["Month"],
            y=monthly["Amount"],
            mode="lines+markers",
            name="Monthly Amount",
        ),
        row=2,
        col=1,
    )

    # All-status horizontal bar chart.
    dashboard.add_trace(
        go.Bar(
            x=status_sorted["Orders"],
            y=status_sorted["Status"],
            orientation="h",
            name="Order Status",
        ),
        row=2,
        col=2,
    )

    # State table.
    dashboard.add_trace(
        go.Table(
            header=dict(
                values=[
                    "State",
                    "Recorded Amount (INR)",
                ]
            ),
            cells=dict(
                values=[
                    states["ship-state"],
                    states["Amount"].map(
                        lambda x: f"{x:,.2f}"
                    ),
                ]
            ),
        ),
        row=3,
        col=1,
    )

    dashboard.update_layout(
        title=(
            "Indian Business Sales — Stakeholder Dashboard"
        ),
        height=1500,
        template="plotly_white",
    )

    dashboard.write_html(
        OUT / "dashboard.html",
        include_plotlyjs=True,
    )

    return coverage, cancelled, total_amount


# --------------------------------------------------
# 7. Static PNG dashboard preview
# --------------------------------------------------

def create_static_preview(
    df, category, monthly, status, states,
    coverage, cancelled, total_amount
):
    """Generate a static dashboard preview using Matplotlib."""

    fig, axes = plt.subplots(
        3, 2,
        figsize=(17, 16),
    )

    fig.suptitle(
        "Indian Business Sales — Dashboard Preview",
        fontsize=18,
        fontweight="bold",
    )

    # Metric card.
    ax = axes[0, 0]
    ax.axis("off")

    ax.text(
        0.05, 0.85,
        f"Source rows: {len(df):,}",
        fontsize=17,
    )

    ax.text(
        0.05, 0.62,
        f"Recorded Amount: INR {total_amount:,.2f}",
        fontsize=12,
    )

    ax.text(
        0.05, 0.42,
        f"Amount coverage: {coverage:.2f}%",
        fontsize=13,
    )

    ax.text(
        0.05, 0.22,
        f"Cancelled rows: {cancelled:.2f}%",
        fontsize=13,
    )

    ax.set_title("Metric Card")

    # Category chart.
    axes[0, 1].barh(
        category["Category"],
        category["Amount"],
    )

    axes[0, 1].set_title(
        "Top Categories by Recorded Amount"
    )

    axes[0, 1].set_xlabel("Recorded Amount (INR)")

    # Monthly trend.
    axes[1, 0].plot(
        monthly["Month"],
        monthly["Amount"],
        marker="o",
    )

    axes[1, 0].set_title(
        "Monthly Recorded Amount"
    )

    axes[1, 0].tick_params(
        axis="x",
        rotation=35,
    )

    axes[1, 0].set_ylabel("Recorded Amount (INR)")

    # All order statuses.
    status_sorted = status.sort_values("Orders")

    axes[1, 1].barh(
        status_sorted["Status"],
        status_sorted["Orders"],
    )

    axes[1, 1].set_title(
        "Order Status Distribution"
    )

    axes[1, 1].set_xlabel("Number of Rows")

    axes[1, 1].tick_params(
        axis="y",
        labelsize=7,
    )

    # State table.
    axes[2, 0].axis("off")
    axes[2, 1].axis("off")

    state_display = states.copy()

    state_display["Amount"] = (
        state_display["Amount"]
        .map(lambda x: f"{x:,.2f}")
    )

    mpl_table = axes[2, 0].table(
        cellText=state_display.values,
        colLabels=[
            "State",
            "Recorded Amount (INR)",
        ],
        loc="center",
        cellLoc="left",
    )

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(8)
    mpl_table.scale(1.1, 1.5)

    axes[2, 0].set_title("Top 10 States")

    # Analytical limitation.
    fig.text(
        0.5,
        0.015,
        (
            "Recorded Amount is not verified net revenue or profit. "
            "Missing Amount values are excluded from amount totals."
        ),
        ha="center",
        fontsize=9,
    )

    fig.tight_layout(
        rect=[0, 0.04, 1, 0.96]
    )

    fig.savefig(
        IMAGES / "dashboard_preview.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)


# --------------------------------------------------
# 8. Summary documentation
# --------------------------------------------------

def write_summary(
    df, coverage, cancelled, total_amount
):
    """Write dashboard metrics and interpretation limitations."""

    date_start = df["Date"].min().strftime("%d %b %Y")
    date_end = df["Date"].max().strftime("%d %b %Y")

    summary = f"""# W11D3 Dashboard Summary

- Source rows: {len(df):,}
- Source columns after removing index-only fields: {len(df.columns)}
- Data period: {date_start} to {date_end}
- Recorded Amount total: INR {total_amount:,.2f}
- Amount coverage: {coverage:.2f}%
- Missing Amount rows: {df["Amount"].isna().sum():,}
- Cancelled rows: {cancelled:.2f}%

## Dashboard components

1. Bar chart: top categories by recorded Amount.
2. Line chart: monthly recorded Amount.
3. Horizontal bar chart: distribution across all order statuses.
4. Table: top 10 states by recorded Amount.
5. Metric card: source rows, recorded Amount, and data-quality indicators.

## Interpretation limitations

- Recorded Amount is not verified net revenue or profit.
- Missing Amount values are excluded from amount aggregations.
- Cancelled rows are shown as recorded statuses, not as completed sales.
- The source data does not establish why orders were cancelled.
- Category rankings represent the complete available dataset period.

## Deployment status

This is a Python-generated dashboard preparation artifact.
Apache Superset has not been installed, configured, or deployed.
"""

    (OUT / "dashboard_summary.md").write_text(
        summary,
        encoding="utf-8",
    )


# --------------------------------------------------
# 9. Output validation
# --------------------------------------------------

def validate_outputs():
    """Verify that every expected deliverable exists and is non-empty."""

    expected = [
        OUT / "dashboard.html",
        OUT / "dashboard_summary.md",
        OUT / "category_amount.csv",
        OUT / "monthly_amount.csv",
        OUT / "order_status.csv",
        OUT / "state_amount.csv",
        IMAGES / "dashboard_preview.png",
        CHARTS / "category_bar.html",
        CHARTS / "monthly_line.html",
        CHARTS / "order_status_bar.html",
        CHARTS / "state_amount_table.html",
    ]

    missing = [
        str(path)
        for path in expected
        if not path.is_file() or path.stat().st_size == 0
    ]

    if missing:
        raise RuntimeError(
            f"Missing or empty outputs: {missing}"
        )

    return expected


# --------------------------------------------------
# 10. Main execution
# --------------------------------------------------

def main():
    """Run the complete W11D3 dashboard preparation workflow."""

    create_directories()

    df = load_data()
    df = prepare_data(df)

    category, monthly, status, states = aggregate_data(df)

    export_tables(
        category,
        monthly,
        status,
        states,
    )

    coverage, cancelled, total_amount = (
        create_interactive_charts(
            df,
            category,
            monthly,
            status,
            states,
        )
    )

    create_static_preview(
        df,
        category,
        monthly,
        status,
        states,
        coverage,
        cancelled,
        total_amount,
    )

    write_summary(
        df,
        coverage,
        cancelled,
        total_amount,
    )

    expected = validate_outputs()

    print("\nW11D3 DASHBOARD PREPARATION COMPLETED")
    print("Rows:", len(df))
    print("Recorded Amount:", f"INR {total_amount:,.2f}")
    print("Amount coverage:", f"{coverage:.2f}%")
    print("Distinct order statuses:", df["Status"].nunique())
    print(
        "Data period:",
        df["Date"].min().date(),
        "to",
        df["Date"].max().date(),
    )
    print("Validated outputs:", len(expected))

    for path in expected:
        print(
            f"{path.relative_to(ROOT)} | "
            f"{path.stat().st_size:,} bytes"
        )


if __name__ == "__main__":
    main()
