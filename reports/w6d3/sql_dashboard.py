import csv
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUT = Path(__file__).resolve().parent / "outputs"

QUERIES = {
    "category_amount.csv": """
        SELECT category AS Category,
               COUNT(*) AS Order_Count,
               ROUND(SUM(amount), 2) AS Recorded_Amount
        FROM orders
        WHERE amount IS NOT NULL
        GROUP BY category
        ORDER BY Recorded_Amount DESC
    """,
    "monthly_amount.csv": """
        SELECT substr(order_date, 1, 7) AS Month,
               COUNT(*) AS Order_Count,
               ROUND(SUM(amount), 2) AS Recorded_Amount
        FROM orders
        WHERE amount IS NOT NULL
        GROUP BY substr(order_date, 1, 7)
        ORDER BY Month
    """,
    "order_status.csv": """
        SELECT status AS Status,
               COUNT(*) AS Order_Count
        FROM orders
        GROUP BY status
        ORDER BY Order_Count DESC
    """,
    "state_amount.csv": """
        SELECT state AS State,
               COUNT(*) AS Order_Count,
               ROUND(SUM(amount), 2) AS Recorded_Amount
        FROM orders
        WHERE amount IS NOT NULL
        GROUP BY state
        ORDER BY Recorded_Amount DESC
    """,
    "kpi_metrics.csv": """
        SELECT
            COUNT(*) AS Total_Orders,
            ROUND(SUM(amount), 2) AS Recorded_Amount_Total,
            ROUND(100.0 * COUNT(amount) / COUNT(*), 2)
                AS Amount_Coverage_Pct,
            SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)
                AS Missing_Amount_Rows,
            SUM(CASE WHEN lower(status) LIKE '%cancel%' THEN 1 ELSE 0 END)
                AS Cancelled_Status_Rows
        FROM orders
    """
}

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Dataset not found: {SOURCE}")

    OUT.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(":memory:")

    connection.execute("""
        CREATE TABLE orders (
            order_id TEXT,
            order_date TEXT,
            status TEXT,
            category TEXT,
            amount REAL,
            state TEXT,
            quantity INTEGER
        )
    """)

    insert_sql = """
        INSERT INTO orders
        (order_id, order_date, status, category, amount, state, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    batch = []
    source_rows = 0

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required = {
            "Order ID", "Date", "Status", "Category",
            "Amount", "ship-state", "Qty"
        }
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing expected columns: {sorted(missing)}")

        for row in reader:
            source_rows += 1

            raw_date = (row.get("Date") or "").strip()
            parsed_date = datetime.strptime(raw_date, "%m-%d-%y")
            order_date = parsed_date.strftime("%Y-%m-%d")

            raw_amount = (row.get("Amount") or "").strip()
            amount = float(raw_amount) if raw_amount else None

            raw_qty = (row.get("Qty") or "").strip()
            quantity = int(float(raw_qty)) if raw_qty else None

            batch.append((
                row.get("Order ID", "").strip(),
                order_date,
                row.get("Status", "").strip() or "(blank)",
                row.get("Category", "").strip() or "(blank)",
                amount,
                row.get("ship-state", "").strip() or "(blank)",
                quantity
            ))

            if len(batch) >= 5000:
                connection.executemany(insert_sql, batch)
                batch.clear()

    if batch:
        connection.executemany(insert_sql, batch)

    connection.commit()

    # Export the SQL statements used for the five dashboard datasets.
    sql_file = Path(__file__).resolve().parent / "dashboard_queries.sql"
    with sql_file.open("w", encoding="utf-8") as file:
        for filename, query in QUERIES.items():
            file.write(f"-- {filename}\n{query.strip()};\n\n")

    print("===== SQL QUERY RESULTS =====")
    for filename, query in QUERIES.items():
        cursor = connection.execute(query)
        columns = [item[0] for item in cursor.description]
        records = cursor.fetchall()

        output_file = OUT / filename
        with output_file.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(records)

        print(f"{filename}: {len(records)} result row(s)")

    metrics = connection.execute(QUERIES["kpi_metrics.csv"]).fetchone()
    total_orders, amount_total, coverage, missing_amount, cancelled = metrics

    distinct_statuses = connection.execute(
        "SELECT COUNT(DISTINCT status) FROM orders"
    ).fetchone()[0]

    date_range = connection.execute(
        "SELECT MIN(order_date), MAX(order_date) FROM orders"
    ).fetchone()

    print("\n===== VALIDATION =====")
    print("Source rows:", source_rows)
    print("SQL rows:", total_orders)
    print("Recorded Amount total:", amount_total)
    print("Amount coverage (%):", coverage)
    print("Missing Amount rows:", missing_amount)
    print("Cancelled-status rows:", cancelled)
    print("Distinct statuses:", distinct_statuses)
    print("Date range:", date_range[0], "to", date_range[1])

    assert source_rows == 128975
    assert total_orders == 128975
    assert missing_amount == 7795
    assert distinct_statuses == 13
    assert abs(amount_total - 78592678.30) < 0.01
    assert date_range == ("2022-03-31", "2022-06-29")

    print("\nPASS: All expected dataset checks succeeded.")
    print("SQL file:", sql_file)
    print("Output folder:", OUT)

    connection.close()

if __name__ == "__main__":
    main()
