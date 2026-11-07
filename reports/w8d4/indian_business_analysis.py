from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_FILE = ROOT / "reports" / "w8d4" / "business_insights.txt"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(DATA_FILE)

    try:
        df = pd.read_csv(DATA_FILE, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_FILE, encoding="cp1252", low_memory=False)

    required = [
        "Order ID", "Date", "Status", "Fulfilment",
        "Category", "Qty", "Amount", "ship-state", "B2B"
    ]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], format="%m-%d-%y", errors="coerce")

    valid_amount = df["Amount"].dropna()
    status_counts = df["Status"].value_counts()
    category_amount = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    state_orders = df["ship-state"].value_counts()
    fulfilment_counts = df["Fulfilment"].value_counts()

    cancelled = df["Status"].astype(str).str.contains(
        "cancel", case=False, na=False
    )
    cancellation_rate = cancelled.mean() * 100

    q1 = valid_amount.quantile(0.25)
    q3 = valid_amount.quantile(0.75)
    upper_bound = q3 + 1.5 * (q3 - q1)
    outliers = (valid_amount > upper_bound).sum()

    lines = [
        "W8D4 INDIAN BUSINESS ANALYSIS",
        "=" * 45,
        f"Dataset records: {len(df):,}",
        f"Dataset columns: {len(df.columns)}",
        f"Unique order IDs: {df['Order ID'].nunique():,}",
        f"Valid amount records: {len(valid_amount):,}",
        f"Missing amount records: {df['Amount'].isna().sum():,}",
        f"Missing quantity records: {df['Qty'].isna().sum():,}",
        f"Date range: {df['Date'].min()} to {df['Date'].max()}",
        "",
        "FINANCIAL OVERVIEW",
        "-" * 45,
        f"Recorded amount across all statuses: {valid_amount.sum():,.2f}",
        f"Average recorded amount: {valid_amount.mean():,.2f}",
        f"Median recorded amount: {valid_amount.median():,.2f}",
        f"Total recorded quantity: {df['Qty'].sum():,.0f}",
        "",
        "TOP CATEGORIES BY RECORDED AMOUNT",
        "-" * 45,
    ]

    for category, amount in category_amount.head(5).items():
        lines.append(f"{category}: {amount:,.2f}")

    lines.extend([
        "",
        "ORDER STATUS",
        "-" * 45,
    ])
    for status, count in status_counts.head(8).items():
        lines.append(f"{status}: {count:,} ({count / len(df) * 100:.2f}%)")

    lines.extend([
        "",
        "TOP STATES BY RECORD COUNT",
        "-" * 45,
    ])
    for state, count in state_orders.head(5).items():
        lines.append(f"{state}: {count:,} records")

    lines.extend([
        "",
        "FULFILMENT",
        "-" * 45,
    ])
    for method, count in fulfilment_counts.items():
        lines.append(f"{method}: {count:,} records")

    lines.extend([
        "",
        "OUTLIER ANALYSIS",
        "-" * 45,
        f"Upper IQR boundary: {upper_bound:,.2f}",
        f"Potential high-value outliers: {outliers:,}",
        "",
        "BUSINESS RECOMMENDATIONS",
        "-" * 45,
    ])

    if not category_amount.empty:
        lines.append(
            f"1. Review the {category_amount.index[0]} category, "
            "which has the highest recorded amount."
        )

    if not state_orders.empty:
        lines.append(
            f"2. Examine operations in {state_orders.index[0]}, "
            "which has the highest record count."
        )

    if cancellation_rate > 0:
        lines.append(
            f"3. Investigate cancellation drivers; "
            f"{cancellation_rate:.2f}% of records have cancelled status."
        )

    missing_amount = df["Amount"].isna().sum()
    if missing_amount:
        lines.append(
            f"4. Validate missing Amount values in {missing_amount:,} "
            "records before financial reporting."
        )

    if outliers:
        lines.append(
            "5. Review high-value outliers before drawing conclusions; "
            "do not remove them without business justification."
        )

    lines.extend([
        "",
        "ANALYSIS LIMITATIONS",
        "-" * 45,
        "- Recorded amounts include all order statuses.",
        "- They should not be interpreted as net realized revenue.",
        "- State counts represent records, not unique customers.",
        "- Potential outliers require business validation.",
        "- Missing values were not silently imputed.",
    ])

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nReport saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
