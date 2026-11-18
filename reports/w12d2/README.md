# W12D2: Performance Optimisation — DuckDB + Query Caching

## Overview

This project demonstrates in-process analytical SQL using DuckDB, compares DuckDB query performance with Pandas, and implements query-result caching.

The analysis uses:

- A 100,000-row sales dataset for performance benchmarking.
- A 128,975-row Indian Business dataset for practical EDA.

## Technologies

- Python
- DuckDB
- Pandas
- Python `functools.lru_cache`
- `time.perf_counter`
- PowerShell

## Project Structure

```text
reports/w12d2/
├── duckdb_analytics.py
├── performance_comparison.md
├── README.md
├── benchmark_results.csv
├── sales_overall_kpis.csv
├── sales_regional_sales.csv
├── sales_category_sales.csv
├── sales_top_10_orders.csv
├── sales_quantity_by_category.csv
├── india_status_analysis.csv
├── india_category_analysis.csv
├── india_state_analysis.csv
├── india_fulfilment_analysis.csv
└── india_monthly_analysis.csv
```

## Execution

From the repository root, run:

```powershell
& ".\.venv\Scripts\python.exe" ".\reports\w12d2\duckdb_analytics.py"
```

## Required Datasets

- `data/w5d3/sales_100k.csv`
- `data/w8d3/indian_business_sales.csv`

## Analytical SQL Queries

### Sales Dataset

1. Overall sales KPIs
2. Regional sales
3. Category sales
4. Top 10 orders
5. Quantity by category

### Indian Business Dataset

1. Order status analysis
2. Product category analysis
3. State-wise analysis
4. Fulfilment analysis
5. Monthly analysis

## Performance Results

| Query | DuckDB | Pandas | Speedup |
|---|---:|---:|---:|
| Regional sales | 0.004785 s | 0.010812 s | 2.26x |
| Category sales | 0.005841 s | 0.010904 s | 1.87x |
| Quantity by region | 0.004563 s | 0.009000 s | 1.97x |

Average measured speedup: approximately 2.03x.

See `performance_comparison.md` for the methodology and interpretation.

## Query Caching

The `query_to_dataframe(sql)` function accepts a SQL query and returns a Pandas DataFrame.

The internal `_cached_query()` function uses `lru_cache(maxsize=64)` to cache results for repeated identical SQL strings.

The cache is in-memory and lasts only for the current Python process.

## Key Implementation Notes

- DuckDB loads the CSV datasets directly into in-memory tables.
- Pandas and DuckDB benchmark results are checked for equivalence.
- Median execution time across five repetitions is recorded.
- CSV loading time is excluded from query timings.
- Monthly analysis uses the dataset's native DATE column.
- The `Amount` field is described as recorded amount, not net revenue.

## Outputs

The generated CSV files contain analytical results and benchmark timings.

The script prints query results and cache statistics to the terminal.

## Conclusion

DuckDB successfully executed analytical SQL queries on both datasets and outperformed Pandas in the three measured benchmark operations.

The implementation demonstrates SQL analytics, DataFrame integration, performance measurement, and query-result caching.
