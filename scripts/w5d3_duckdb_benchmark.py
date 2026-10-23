
from pathlib import Path
from time import perf_counter

import duckdb
import pandas as pd
import polars as pl

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "w5d3"
CSV = DATA_DIR / "sales_100k.csv"
REPORT = ROOT / "w5d3_benchmark_results.csv"
ROWS = 100_000

# Generate one reusable dataset only if it does not exist.
if not CSV.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({
        "order_id": range(1, ROWS + 1),
        "region": ["North", "South", "East", "West"] * (ROWS // 4),
        "category": ["Electronics", "Clothing", "Food", "Home"] * (ROWS // 4),
        "quantity": [(i % 10) + 1 for i in range(ROWS)],
        "sales": [float(((i * 17) % 9000) + 100) for i in range(ROWS)],
    })
    df.to_csv(CSV, index=False)
    del df

print(f"Dataset: {CSV}")
print(f"Rows: {sum(1 for _ in open(CSV, encoding='utf-8')) - 1:,}")

queries = {
    "1_total_sales": "SELECT SUM(sales) AS result FROM sales",
    "2_average_sales": "SELECT AVG(sales) AS result FROM sales",
    "3_sales_by_region": "SELECT region, SUM(sales) AS total FROM sales GROUP BY region ORDER BY region",
    "4_category_quantity": "SELECT category, SUM(quantity) AS total FROM sales GROUP BY category ORDER BY category",
    "5_high_value_orders": "SELECT COUNT(*) AS result FROM sales WHERE sales >= 5000",
}

con = duckdb.connect()
con.execute(f"CREATE TABLE sales AS SELECT * FROM read_csv_auto('{CSV.as_posix()}')")

results = []

# DuckDB: execute SQL directly against the CSV.
for name, query in queries.items():
    start = perf_counter()
    output = con.execute(query).fetchall()
    elapsed = perf_counter() - start
    results.append({"operation": name, "tool": "DuckDB", "seconds": elapsed})
    print(f"DuckDB | {name} | {elapsed:.6f}s | {output}")

# Pandas: load the same CSV once, then run equivalent operations.
pdf = pd.read_csv(CSV)
pandas_ops = {
    "1_total_sales": lambda: pdf["sales"].sum(),
    "2_average_sales": lambda: pdf["sales"].mean(),
    "3_sales_by_region": lambda: pdf.groupby("region")["sales"].sum().sort_index(),
    "4_category_quantity": lambda: pdf.groupby("category")["quantity"].sum().sort_index(),
    "5_high_value_orders": lambda: (pdf["sales"] >= 5000).sum(),
}

for name, operation in pandas_ops.items():
    start = perf_counter()
    output = operation()
    elapsed = perf_counter() - start
    results.append({"operation": name, "tool": "Pandas", "seconds": elapsed})
    print(f"Pandas | {name} | {elapsed:.6f}s | {output}")

# Polars: load the same CSV once, then run equivalent operations.
pldf = pl.read_csv(CSV)
polars_ops = {
    "1_total_sales": lambda: pldf.select(pl.col("sales").sum()),
    "2_average_sales": lambda: pldf.select(pl.col("sales").mean()),
    "3_sales_by_region": lambda: pldf.group_by("region").agg(pl.col("sales").sum()).sort("region"),
    "4_category_quantity": lambda: pldf.group_by("category").agg(pl.col("quantity").sum()).sort("category"),
    "5_high_value_orders": lambda: pldf.filter(pl.col("sales") >= 5000).height,
}

for name, operation in polars_ops.items():
    start = perf_counter()
    output = operation()
    elapsed = perf_counter() - start
    results.append({"operation": name, "tool": "Polars", "seconds": elapsed})
    print(f"Polars | {name} | {elapsed:.6f}s | {output}")

pd.DataFrame(results).to_csv(REPORT, index=False)
print(f"\nBenchmark report saved: {REPORT}")
print("\nMean operation time by tool:")
print(pd.DataFrame(results).groupby("tool")["seconds"].mean().sort_values())

con.close()
