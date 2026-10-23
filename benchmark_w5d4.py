from pathlib import Path
from time import perf_counter


import duckdb
import pandas as pd
import polars as pl

DATA = Path("data/w5d3/sales_100k.csv")
OUT = Path("reports/w5d4")
OUT.mkdir(parents=True, exist_ok=True)

queries = {
    "total_sales": "SELECT SUM(sales) AS total_sales FROM sales",
    "sales_by_region": """
        SELECT region, SUM(sales) AS total_sales
        FROM sales GROUP BY region ORDER BY region
    """,
    "sales_by_category": """
        SELECT category, SUM(sales) AS total_sales
        FROM sales GROUP BY category ORDER BY category
    """,
    "quantity_by_region": """
        SELECT region, SUM(quantity) AS total_quantity
        FROM sales GROUP BY region ORDER BY region
    """,
    "top_5_orders": """
        SELECT order_id, sales FROM sales
        ORDER BY sales DESC, order_id LIMIT 5
    """,
}

results = []

def record(engine, operation, fn):
    start = perf_counter()
    value = fn()
    elapsed = perf_counter() - start
    results.append({
        "engine": engine,
        "operation": operation,
        "seconds": round(elapsed, 6),
    })
    return value

# Pandas: include CSV loading in its benchmark.
pdf = record("Pandas", "load_csv", lambda: pd.read_csv(DATA))


# DuckDB: load the CSV once into a table.
con = duckdb.connect()

record(
    "DuckDB",
    "load_csv",
    lambda: con.execute(
        "CREATE TABLE sales AS SELECT * FROM read_csv_auto(?)",
        [str(DATA)],
    ),
)

# Run all five queries against the loaded table.
for name, sql in queries.items():
    record(
        "DuckDB",
        name,
        lambda sql=sql: con.execute(sql).fetchall(),
    )

# Pandas: run equivalent operations.
pandas_ops = {
    "total_sales": lambda: pdf["sales"].sum(),
    "sales_by_region": lambda: pdf.groupby("region", as_index=False)["sales"].sum().sort_values("region"),
    "sales_by_category": lambda: pdf.groupby("category", as_index=False)["sales"].sum().sort_values("category"),
    "quantity_by_region": lambda: pdf.groupby("region", as_index=False)["quantity"].sum().sort_values("region"),
    "top_5_orders": lambda: pdf.sort_values(
        ["sales", "order_id"], ascending=[False, True]
    )[["order_id", "sales"]].head(5),
}

for name, fn in pandas_ops.items():
    record("Pandas", name, fn)

# Polars: include CSV loading in its benchmark.
pldf = record("Polars", "load_csv", lambda: pl.read_csv(DATA))

polars_ops = {
    "total_sales": lambda: pldf.select(pl.col("sales").sum()),
    "sales_by_region": lambda: pldf.group_by("region").agg(
        pl.col("sales").sum().alias("total_sales")
    ).sort("region"),
    "sales_by_category": lambda: pldf.group_by("category").agg(
        pl.col("sales").sum().alias("total_sales")
    ).sort("category"),
    "quantity_by_region": lambda: pldf.group_by("region").agg(
        pl.col("quantity").sum().alias("total_quantity")
    ).sort("region"),
    "top_5_orders": lambda: pldf.sort(
        ["sales", "order_id"], descending=[True, False]
    ).select(["order_id", "sales"]).head(5),
}

for name, fn in polars_ops.items():
    record("Polars", name, fn)

pd.DataFrame(results).to_csv(OUT / "benchmark_results.csv", index=False)

comparison = pd.DataFrame([
    ["Query style", "DataFrame methods", "SQL", "DataFrame expressions"],
    ["Execution", "Mostly eager", "Query engine", "Eager or lazy"],
    ["Best fit", "General analysis", "SQL analytics", "Fast DataFrame processing"],
    ["Data access", "Loads into memory", "Can query CSV directly", "Loads or scans files"],
    ["Syntax", "Python API", "SQL", "Python expression API"],
], columns=["criterion", "Pandas", "DuckDB", "Polars"])
comparison.to_csv(OUT / "comparison.csv", index=False)

print("Rows:", len(pdf))
print("Results saved to reports/w5d4/")
print(pd.DataFrame(results).to_string(index=False))
print("\nComparison:\n", comparison.to_string(index=False))

con.close()
