
"""Generate Plotly charts and ECharts-compatible options for Superstore data."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
from plotly.offline import plot


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "raw" / "archive" / "Sample - Superstore.csv"
OUT = Path(__file__).resolve().parent

REQUIRED_COLUMNS = {
    "Category",
    "Region",
    "Sales",
    "Profit",
    "Quantity",
    "Order Date",
}

NUMERIC_COLUMNS = ["Sales", "Profit", "Quantity"]


def load_data():
    """Load the Superstore dataset and convert numeric columns."""
    df = pd.read_csv(DATA, encoding="cp1252")

    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_cols)}"
        )

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    invalid_counts = df[NUMERIC_COLUMNS].isna().sum()
    invalid_counts = invalid_counts[invalid_counts > 0]

    if not invalid_counts.empty:
        raise ValueError(
            "Non-numeric or missing values found: "
            f"{invalid_counts.to_dict()}"
        )

    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


def build_echarts_options(df):
    """Build ECharts-compatible options for category sales and regional profit."""

    category_sales = (
        df.groupby("Category", dropna=False)["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    region_profit = (
        df.groupby("Region", dropna=False)["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "sales_by_category": {
            "title": {"text": "Sales by Category"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "data": [str(value) for value in category_sales.index],
            },
            "yAxis": {"type": "value", "name": "Sales"},
            "series": [
                {
                    "name": "Sales",
                    "type": "bar",
                    "data": [
                        round(float(value), 2)
                        for value in category_sales
                    ],
                }
            ],
        },
        "profit_by_region": {
            "title": {"text": "Profit by Region"},
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "data": [str(value) for value in region_profit.index],
            },
            "yAxis": {"type": "value", "name": "Profit"},
            "series": [
                {
                    "name": "Profit",
                    "type": "bar",
                    "data": [
                        round(float(value), 2)
                        for value in region_profit
                    ],
                }
            ],
        },
    }


def main():
    """Generate Plotly dashboard HTML and ECharts JSON options."""

    if not DATA.is_file():
        raise FileNotFoundError(f"Dataset not found: {DATA}")

    OUT.mkdir(parents=True, exist_ok=True)

    df = load_data()

    # Aggregate sales by category and profit by region.
    category_sales = (
        df.groupby("Category", dropna=False)["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    region_profit = (
        df.groupby("Region", dropna=False)["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Convert order dates and report invalid values.
    dates = pd.to_datetime(df["Order Date"], errors="coerce")
    invalid_dates = int(dates.isna().sum())

    if invalid_dates:
        print(f"Warning: {invalid_dates} rows have invalid dates.")

    # Calculate total sales for each month.
    monthly_sales = (
        df.assign(Month=dates.dt.to_period("M").astype("string"))
        .dropna(subset=["Month"])
        .groupby("Month")["Sales"]
        .sum()
        .sort_index()
    )

    if monthly_sales.empty:
        raise ValueError("No valid order dates available for the monthly chart.")

    # Create the three Plotly charts.
    figures = {
        "sales_by_category": px.bar(
            category_sales.reset_index(),
            x="Category",
            y="Sales",
            title="Sales by Category",
            labels={"Sales": "Total Sales"},
        ),
        "profit_by_region": px.bar(
            region_profit.reset_index(),
            x="Region",
            y="Profit",
            title="Profit by Region",
            labels={"Profit": "Total Profit"},
        ),
        "monthly_sales": px.line(
            x=monthly_sales.index.astype(str),
            y=monthly_sales.values,
            markers=True,
            title="Monthly Sales Trend",
            labels={"x": "Month", "y": "Total Sales"},
        ),
    }

    # Assemble the standalone HTML dashboard.
    html_parts = [
        "<!doctype html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>W7D3 Superstore Charts</title>",
        (
            "<style>"
            "body{font-family:Arial,sans-serif;max-width:1100px;"
            "margin:24px auto;padding:0 16px}"
            "section{margin:24px 0}"
            "</style>"
        ),
        "</head>",
        "<body>",
        "<h1>Superstore Interactive Charts</h1>",
        "<p>Generated from the existing Superstore dataset.</p>",
    ]

    # Load Plotly JavaScript only once for all three charts.
    for index, (name, figure) in enumerate(figures.items()):
        html_parts.append(
            f"<section><h2>{name.replace('_', ' ').title()}</h2>"
        )

        html_parts.append(
            plot(
                figure,
                output_type="div",
                include_plotlyjs="cdn" if index == 0 else False,
            )
        )

        html_parts.append("</section>")

    html_parts.extend(["</body>", "</html>"])

    # Save the Plotly dashboard.
    dashboard_path = OUT / "plotly_dashboard.html"
    dashboard_path.write_text("\n".join(html_parts), encoding="utf-8")

    # Save the ECharts-compatible JSON options.
    echarts_path = OUT / "echarts_options.json"
    echarts_path.write_text(
        json.dumps(
            build_echarts_options(df),
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    print(f"Rows analyzed: {len(df)}")
    print(f"Invalid dates: {invalid_dates}")
    print(f"Plotly charts generated: {len(figures)}")
    print(f"Created: {dashboard_path}")
    print(f"Created: {echarts_path}")


if __name__ == "__main__":
    main()
