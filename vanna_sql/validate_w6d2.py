import csv
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sales.db"
EXAMPLES_PATH = BASE_DIR / "vanna_sql" / "w6d2_training_examples.json"
REPORT_PATH = BASE_DIR / "reports" / "w6d2" / "sql_validation_results.csv"

QUERIES = [
    ("Q01", "How many orders are there?",
     "SELECT COUNT(*) AS total_orders FROM orders"),
    ("Q02", "What are total discounted sales by region?",
     "SELECT region, SUM(quantity * unit_price * (1 - COALESCE(discount, 0) / 100.0)) AS total_sales FROM orders GROUP BY region ORDER BY total_sales DESC"),
    ("Q03", "Which products have the highest quantity sold?",
     "SELECT product, SUM(quantity) AS total_quantity FROM orders GROUP BY product ORDER BY total_quantity DESC"),
    ("Q04", "What is the average order quantity?",
     "SELECT AVG(quantity) AS average_quantity FROM orders"),
    ("Q05", "How many orders are in each category?",
     "SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category ORDER BY order_count DESC"),
    ("Q06", "How many orders are in each region?",
     "SELECT region, COUNT(*) AS order_count FROM orders GROUP BY region ORDER BY order_count DESC"),
    ("Q07", "What is the total quantity sold by product?",
     "SELECT product, SUM(quantity) AS total_quantity FROM orders GROUP BY product ORDER BY total_quantity DESC"),
    ("Q08", "What is the order count by sales representative?",
     "SELECT sales_rep, COUNT(*) AS order_count FROM orders GROUP BY sales_rep ORDER BY order_count DESC"),
    ("Q09", "How many orders have no discount recorded?",
     "SELECT COUNT(*) AS missing_discount_orders FROM orders WHERE discount IS NULL"),
    ("Q10", "What is the net sales value of each order?",
     "SELECT order_id, quantity * unit_price * (1 - COALESCE(discount, 0) / 100.0) AS net_sales FROM orders ORDER BY order_id"),
]


def main():
    examples = json.loads(EXAMPLES_PATH.read_text(encoding="utf-8-sig"))
    assert len(examples) == 5, "Expected exactly five training examples."

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results = []

    with sqlite3.connect(DB_PATH.resolve().as_uri() + "?mode=ro", uri=True) as conn:
        def authorize(action, arg1, arg2, database, trigger):
            allowed = {
                sqlite3.SQLITE_SELECT,
                sqlite3.SQLITE_READ,
                sqlite3.SQLITE_FUNCTION,
                sqlite3.SQLITE_RECURSIVE,
            }
            return sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY

        conn.set_authorizer(authorize)

        for query_id, question, sql in QUERIES:
            try:
                if not sql.lstrip().upper().startswith("SELECT"):
                    raise ValueError("Only SELECT queries are allowed.")

                cursor = conn.execute(sql)
                rows = cursor.fetchall()
                columns = [item[0] for item in cursor.description or []]

                if not columns:
                    raise AssertionError("No result columns returned.")
                if not rows:
                    raise AssertionError("Query returned no rows.")
                if query_id == "Q01" and rows[0][0] != 10:
                    raise AssertionError(f"Expected 10 orders, got {rows[0][0]}.")

                results.append({
                    "query_id": query_id,
                    "question": question,
                    "status": "PASS",
                    "columns": ", ".join(columns),
                    "rows_returned": len(rows),
                    "error": "",
                })
            except Exception as exc:
                results.append({
                    "query_id": query_id,
                    "question": question,
                    "status": "FAIL",
                    "columns": "",
                    "rows_returned": 0,
                    "error": str(exc),
                })

    with REPORT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "query_id", "question", "status",
                "columns", "rows_returned", "error"
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    for result in results:
        print(
            f"{result['query_id']} {result['status']}: "
            f"{result['question']} "
            f"(rows={result['rows_returned']})"
        )

    passed = sum(result["status"] == "PASS" for result in results)
    print(f"\nTraining examples: {len(examples)}")
    print(f"SQL validation: {passed}/{len(results)} passed")
    print(f"Evidence: {REPORT_PATH.relative_to(BASE_DIR)}")

    if passed != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
