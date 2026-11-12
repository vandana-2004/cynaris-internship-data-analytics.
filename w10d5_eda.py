from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
REPORT_DIR = ROOT / "reports" / "w10d5"


def load_data(data_path=DATA_PATH):
    columns = [
        "Order ID", "Date", "Status", "Fulfilment",
        "Category", "Qty", "Amount", "ship-state",
    ]
    raw = pd.read_csv(data_path, low_memory=False)
    duplicate_rows = int(raw.duplicated().sum())
    df = raw.loc[:, columns].copy()
    del raw

    df["Date"] = pd.to_datetime(
        df["Date"], format="%m-%d-%y", errors="coerce"
    )
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")

    for col in ["Category", "Fulfilment", "Status"]:
        df[col] = df[col].astype("string").str.strip()

    df["Category"] = df["Category"].str.title().fillna("Unknown")
    df["Fulfilment"] = df["Fulfilment"].fillna("Unknown")
    df["Status"] = df["Status"].fillna("Unknown")
    df["ship-state"] = (
        df["ship-state"].astype("string").str.strip().str.upper()
        .replace("", pd.NA).fillna("UNKNOWN")
    )
    return df, duplicate_rows


def grouped_summary(df, group_col):
    result = (
        df.groupby(group_col, dropna=False)
        .agg(
            order_rows=("Order ID", "size"),
            recorded_amount=("Amount", "sum"),
            quantity=("Qty", "sum"),
            rows_with_amount=("Amount", "count"),
            average_recorded_amount_per_valid_row=("Amount", "mean"),
        )
        .reset_index()
        .sort_values("recorded_amount", ascending=False)
    )
    return result


def run_eda(data_path=DATA_PATH, output_dir=REPORT_DIR):
    df, duplicate_rows = load_data(data_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    valid_dates = df["Date"].dropna()
    if valid_dates.empty:
        raise ValueError("The dataset contains no valid dates.")

    daily = (
        df.dropna(subset=["Date"])
        .groupby("Date")
        .agg(
            order_rows=("Order ID", "size"),
            recorded_amount=("Amount", "sum"),
            quantity=("Qty", "sum"),
            rows_with_amount=("Amount", "count"),
            average_recorded_amount_per_valid_row=("Amount", "mean"),
        )
        .sort_index()
    )

    monthly = (
        df.dropna(subset=["Date"])
        .assign(month=lambda x: x["Date"].dt.to_period("M").astype(str))
        .groupby("month")
        .agg(
            order_rows=("Order ID", "size"),
            recorded_amount=("Amount", "sum"),
            quantity=("Qty", "sum"),
            rows_with_amount=("Amount", "count"),
            average_recorded_amount_per_valid_row=("Amount", "mean"),
        )
        .reset_index()
    )

    category = grouped_summary(df, "Category")
    state = grouped_summary(df, "ship-state")
    fulfilment = grouped_summary(df, "Fulfilment")
    status = grouped_summary(df, "Status")

    missing_by_status = (
        df.groupby("Status", dropna=False)
        .agg(
            order_rows=("Order ID", "size"),
            missing_amounts=("Amount", lambda values: int(values.isna().sum())),
        )
        .reset_index()
    )
    missing_by_status["missing_amount_percent"] = (
        missing_by_status["missing_amounts"]
        .div(missing_by_status["order_rows"])
        .mul(100)
        .round(2)
    )

    missing_by_fulfilment = (
        df.groupby("Fulfilment", dropna=False)
        .agg(
            order_rows=("Order ID", "size"),
            missing_amounts=("Amount", lambda values: int(values.isna().sum())),
        )
        .reset_index()
    )
    missing_by_fulfilment["missing_amount_percent"] = (
        missing_by_fulfilment["missing_amounts"]
        .div(missing_by_fulfilment["order_rows"])
        .mul(100)
        .round(2)
    )

    daily.to_csv(output_dir / "daily_business_summary.csv", index_label="date")
    monthly.to_csv(output_dir / "monthly_business_summary.csv", index=False)
    category.to_csv(output_dir / "category_performance.csv", index=False)
    state.to_csv(output_dir / "state_performance.csv", index=False)
    fulfilment.to_csv(output_dir / "fulfilment_summary.csv", index=False)
    status.to_csv(output_dir / "status_summary.csv", index=False)
    missing_by_status.to_csv(
        output_dir / "missing_amount_by_status.csv", index=False
    )
    missing_by_fulfilment.to_csv(
        output_dir / "missing_amount_by_fulfilment.csv", index=False
    )

    amount = df["Amount"]
    quality = {
        "source_rows": int(len(df)),
        "source_columns_used": int(len(df.columns)),
        "duplicate_rows": duplicate_rows,
        "invalid_dates": int(df["Date"].isna().sum()),
        "missing_amounts": int(amount.isna().sum()),
        "rows_with_valid_amount": int(amount.notna().sum()),
        "missing_states_after_normalization": int(
            (df["ship-state"] == "UNKNOWN").sum()
        ),
        "date_start": str(valid_dates.min().date()),
        "date_end": str(valid_dates.max().date()),
        "daily_observations": int(len(daily)),
        "category_count": int(df["Category"].nunique()),
        "normalized_state_count": int(df["ship-state"].nunique()),
        "recorded_amount_total": float(amount.sum()),
        "recorded_amount_average": float(amount.mean()),
        "recorded_amount_median": float(amount.median()),
        "quantity_total": float(df["Qty"].sum()),
    }

    quality["amount_coverage_percent"] = round(
        amount.notna().mean() * 100, 2
    )
    quality["cancelled_rows"] = int(
        df["Status"].str.contains("cancel", case=False, na=False).sum()
    )
    quality["cancelled_row_percent"] = round(
        quality["cancelled_rows"] / len(df) * 100, 2
    )

    (output_dir / "data_quality.json").write_text(
        json.dumps(quality, indent=2), encoding="utf-8"
    )

    top_category = category.iloc[0]
    top_state = state[state["ship-state"] != "UNKNOWN"].iloc[0]
    top_fulfilment = fulfilment.iloc[0]

    summary = f"""# W10D5 - Indian Business Sales EDA

## Dataset overview
- Source: `data/w8d3/indian_business_sales.csv`
- Rows analyzed: {len(df):,}
- Date range: {quality['date_start']} to {quality['date_end']}
- Daily observations: {len(daily)}
- Exact duplicate rows: {quality['duplicate_rows']:,}

## Recorded amount and quantity
- Total recorded Amount: {amount.sum():,.2f}
- Average recorded Amount per row with an amount: {amount.mean():,.2f}
- Median recorded Amount per row with an amount: {amount.median():,.2f}
- Total quantity: {df['Qty'].sum():,.0f}
- Rows with valid Amount: {quality['rows_with_valid_amount']:,}
- Rows with missing Amount: {quality['missing_amounts']:,}
- Amount coverage: {quality['amount_coverage_percent']:.2f}%
- Financial aggregations exclude missing Amount values; record counts retain all rows.
- Average recorded Amount is calculated per row with a valid Amount, not per unique order.

## Category performance
- Highest recorded amount category: {top_category['Category']}
- Category recorded amount: {top_category['recorded_amount']:,.2f}
- Category order rows: {top_category['order_rows']:,}

## State performance
- Highest recorded amount state: {top_state['ship-state']}
- State recorded amount: {top_state['recorded_amount']:,.2f}
- State order rows: {top_state['order_rows']:,}
- State names were trimmed and normalized to uppercase before grouping.

## Fulfilment and order status
- Largest fulfilment group by recorded amount: {top_fulfilment['Fulfilment']}
- Rows with a cancelled status: {quality['cancelled_rows']:,}
- Cancelled-status row share: {quality['cancelled_row_percent']:.2f}%

## Data quality
- Invalid dates: {quality['invalid_dates']:,}
- Missing state values after normalization: {quality['missing_states_after_normalization']:,}
- Duplicate rows: {quality['duplicate_rows']:,}

## Business interpretation and limitations
- `Amount` is recorded order amount, not verified net revenue.
- Missing Amount values are excluded from amount totals and averages.
- Status counts describe recorded order rows; they are not a confirmed
  measure of delivered revenue or final customer outcomes.
- The source contains order-item rows. Row counts should not automatically
  be interpreted as unique orders.
- State names are normalized for consistent grouping.
- The dataset covers a limited historical period from 2022. Findings are
  descriptive and should not be treated as current market conditions.
- Forecast performance is reported separately using the W10D4
  chronological holdout results.

## Generated evidence
- `daily_business_summary.csv`
- `monthly_business_summary.csv`
- `category_performance.csv`
- `state_performance.csv`
- `fulfilment_summary.csv`
- `status_summary.csv`
- `missing_amount_by_status.csv`
- `missing_amount_by_fulfilment.csv`
- `data_quality.json`
"""
    (output_dir / "eda_summary.md").write_text(summary, encoding="utf-8")

    return {
        "data": df,
        "daily": daily,
        "monthly": monthly,
        "category": category,
        "state": state,
        "fulfilment": fulfilment,
        "status": status,
        "missing_by_status": missing_by_status,
        "missing_by_fulfilment": missing_by_fulfilment,
        "quality": quality,
    }


if __name__ == "__main__":
    result = run_eda()
    print("W10D5 EDA completed.")
    print(json.dumps(result["quality"], indent=2))
    print("Reports:", REPORT_DIR)
