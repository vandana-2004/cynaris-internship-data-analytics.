
"""
W12D2: Performance Optimisation
DuckDB + Query Caching

Project: EDA on Indian Business Dataset
Benchmark: 100,000-row sales dataset
"""

from pathlib import Path
from functools import lru_cache
from time import perf_counter
from statistics import median

import duckdb
import pandas as pd
from pandas.testing import assert_frame_equal


# --------------------------------------------------
# 1. PATHS AND CONNECTION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent

SALES_CSV = ROOT / "data" / "w5d3" / "sales_100k.csv"
INDIA_CSV = ROOT / "data" / "w8d3" / "indian_business_sales.csv"

con = duckdb.connect(database=":memory:")


# --------------------------------------------------
# 2. LOAD CSV DIRECTLY INTO DUCKDB
# --------------------------------------------------

def load_csv_as_table(csv_path, table_name):
    """Load a CSV directly into a DuckDB table."""

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    # Table names are internal constants supplied by this script.
    allowed_tables = {"sales_100k", "indian_business"}

    if table_name not in allowed_tables:
        raise ValueError("Unsupported table name.")

    path = str(csv_path).replace("\\", "/").replace("'", "''")

    con.execute(
        f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{path}')
        """
    )

    count = con.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(f"{table_name}: {count:,} rows loaded")

    return count


# --------------------------------------------------
# 3. REUSABLE SQL FUNCTION + QUERY CACHE
# --------------------------------------------------

@lru_cache(maxsize=64)
def _cached_query(sql):
    """Execute SQL once and cache its DataFrame result."""

    return con.execute(sql).df()


def query_to_dataframe(sql):
    """
    Accept a SQL string and return a Pandas DataFrame.
    Repeated identical SELECT queries use cached results.
    """

    normalized = sql.strip()
    first_word = normalized.split(maxsplit=1)[0].lower() if normalized else ""

    if first_word not in ("select", "with"):
        raise ValueError("Only SELECT queries are supported.")

    return _cached_query(normalized).copy()


# --------------------------------------------------
# 4. FIVE ANALYTICAL SQL QUERIES: 100K DATASET
# --------------------------------------------------

sales_queries = {

    "overall_kpis": """
        SELECT
            COUNT(*) AS total_orders,
            SUM(sales) AS total_sales,
            AVG(sales) AS average_sales,
            SUM(quantity) AS total_quantity
        FROM sales_100k
    """,

    "regional_sales": """
        SELECT
            region,
            SUM(sales) AS total_sales,
            SUM(quantity) AS total_quantity
        FROM sales_100k
        GROUP BY region
        ORDER BY region
    """,

    "category_sales": """
        SELECT
            category,
            COUNT(*) AS order_count,
            SUM(sales) AS total_sales,
            AVG(sales) AS average_sales
        FROM sales_100k
        GROUP BY category
        ORDER BY total_sales DESC
    """,

    "top_10_orders": """
        SELECT
            order_id,
            region,
            category,
            sales
        FROM sales_100k
        ORDER BY sales DESC
        LIMIT 10
    """,

    "quantity_by_category": """
        SELECT
            category,
            SUM(quantity) AS total_quantity
        FROM sales_100k
        GROUP BY category
        ORDER BY total_quantity DESC
    """
}


# --------------------------------------------------
# 5. PANDAS VS DUCKDB BENCHMARK
# --------------------------------------------------

benchmark_queries = {

    "regional_sales": sales_queries["regional_sales"],

    "category_sales": sales_queries["category_sales"],

    "quantity_by_region": """
        SELECT
            region,
            SUM(quantity) AS total_quantity
        FROM sales_100k
        GROUP BY region
        ORDER BY region
    """
}


def pandas_operations(df):
    """Equivalent Pandas operations for benchmark queries."""

    return {

        "regional_sales": lambda: (
            df.groupby("region", as_index=False)
            .agg(
                total_sales=("sales", "sum"),
                total_quantity=("quantity", "sum")
            )
            .sort_values("region")
            .reset_index(drop=True)
        ),

        "category_sales": lambda: (
            df.groupby("category", as_index=False)
            .agg(
                order_count=("order_id", "count"),
                total_sales=("sales", "sum"),
                average_sales=("sales", "mean")
            )
            .sort_values("total_sales", ascending=False)
            .reset_index(drop=True)
        ),

        "quantity_by_region": lambda: (
            df.groupby("region", as_index=False)
            .agg(
                total_quantity=("quantity", "sum")
            )
            .sort_values("region")
            .reset_index(drop=True)
        )
    }


def benchmark(operation, repeats=5):
    """Measure median execution time across repeated runs."""

    timings = []

    for _ in range(repeats):

        start = perf_counter()

        operation()

        elapsed = perf_counter() - start

        timings.append(elapsed)

    return median(timings)


def run_benchmarks(df):
    """Compare DuckDB and Pandas execution times."""

    results = []

    pandas_funcs = pandas_operations(df)

    for name, sql in benchmark_queries.items():

        # Calculate both results before timing.
        duck_result = con.execute(sql).df()
        pandas_result = pandas_funcs[name]()

        # Verify that both engines return equivalent results.
        assert_frame_equal(
            duck_result,
            pandas_result,
            check_dtype=False,
            check_exact=False,
            rtol=1e-9,
            atol=1e-9
        )

        # Benchmark DuckDB.
        duck_time = benchmark(
            lambda: con.execute(sql).df()
        )

        # Benchmark Pandas.
        pandas_time = benchmark(
            pandas_funcs[name]
        )

        speedup = (
            pandas_time / duck_time
            if duck_time > 0
            else None
        )

        results.append({
            "query": name,
            "duckdb_seconds": duck_time,
            "pandas_seconds": pandas_time,
            "pandas_to_duckdb_ratio": speedup
        })

        print(f"\n{name}")
        print(f"DuckDB: {duck_time:.6f} seconds")
        print(f"Pandas: {pandas_time:.6f} seconds")

        if speedup is not None:
            print(f"DuckDB speedup: {speedup:.2f}x")

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT / "benchmark_results.csv",
        index=False
    )

    return result_df


# --------------------------------------------------
# 6. FIVE INDIAN BUSINESS DATASET QUERIES
# --------------------------------------------------

india_queries = {

    "status_analysis": """
        SELECT
            Status,
            COUNT(*) AS order_count,
            SUM(Amount) AS recorded_amount
        FROM indian_business
        GROUP BY Status
        ORDER BY order_count DESC
    """,

    "category_analysis": """
        SELECT
            Category,
            COUNT(*) AS order_count,
            SUM(Qty) AS total_quantity,
            SUM(Amount) AS recorded_amount
        FROM indian_business
        GROUP BY Category
        ORDER BY recorded_amount DESC
    """,

    "state_analysis": """
        SELECT
            "ship-state" AS state,
            COUNT(*) AS order_count,
            SUM(Amount) AS recorded_amount
        FROM indian_business
        GROUP BY "ship-state"
        ORDER BY recorded_amount DESC
        LIMIT 10
    """,

    "fulfilment_analysis": """
        SELECT
            Fulfilment,
            COUNT(*) AS order_count,
            SUM(Amount) AS recorded_amount
        FROM indian_business
        GROUP BY Fulfilment
        ORDER BY order_count DESC
    """,

    "monthly_analysis": """
        SELECT
            STRFTIME(Date, '%Y-%m') AS order_month,
            COUNT(*) AS order_count,
            SUM(Amount) AS recorded_amount
        FROM indian_business
        WHERE Date IS NOT NULL
        GROUP BY order_month
        ORDER BY order_month
    """
}


# --------------------------------------------------
# 7. MAIN EXECUTION
# --------------------------------------------------

def main():

    print("\n===== W12D2 PERFORMANCE OPTIMISATION =====")

    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Load both CSV files directly into DuckDB.
    load_csv_as_table(
        SALES_CSV,
        "sales_100k"
    )

    load_csv_as_table(
        INDIA_CSV,
        "indian_business"
    )

    # Execute five analytical sales SQL queries.
    print("\n===== FIVE SALES SQL QUERIES =====")

    for name, sql in sales_queries.items():

        result = query_to_dataframe(sql)

        print(f"\n{name}")
        print(result.to_string(index=False))

        result.to_csv(
            OUTPUT / f"sales_{name}.csv",
            index=False
        )

    # Compare Pandas and DuckDB.
    print("\n===== PANDAS VS DUCKDB =====")

    pandas_df = pd.read_csv(SALES_CSV)

    benchmark_results = run_benchmarks(pandas_df)

    print("\n===== BENCHMARK SUMMARY =====")

    print(
        benchmark_results.to_string(index=False)
    )

    # Indian Business Dataset analysis.
    print("\n===== INDIAN BUSINESS ANALYSIS =====")

    for name, sql in india_queries.items():

        result = query_to_dataframe(sql)

        print(f"\n{name}")

        print(
            result.head(10).to_string(index=False)
        )

        result.to_csv(
            OUTPUT / f"india_{name}.csv",
            index=False
        )

    # Demonstrate query cache.
    print("\n===== QUERY CACHE TEST =====")

    cache_sql = sales_queries["regional_sales"]

    query_to_dataframe(cache_sql)
    query_to_dataframe(cache_sql)

    print(
        "Cache statistics:",
        _cached_query.cache_info()
    )

    print("\n===== W12D2 COMPLETED =====")

    print("Results saved in:", OUTPUT)


if __name__ == "__main__":

    try:
        main()

    finally:
        con.close()
