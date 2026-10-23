# W5D4 - Polars: High-Performance DataFrame Operations

## Objective
Compare Pandas, DuckDB, and Polars using the same 100,000-row sales dataset.

## Dataset
`data/w5d3/sales_100k.csv`

Columns: `order_id`, `region`, `category`, `quantity`, `sales`.

## Operations
1. Total sales
2. Sales by region
3. Sales by category
4. Quantity by region
5. Top five orders by sales

## Deliverables
- `benchmark_w5d4.py` - benchmark implementation
- `benchmark_results.csv` - measured execution times
- `comparison.csv` - high-level tool comparison

## Notes
Each run records CSV loading and analytical operation times. Results can vary with system load and execution conditions; single-run timings are not definitive performance rankings.

## CIA Review Status
CIA review attempts failed with a request error. CIA interactions remain incomplete. Local benchmark execution succeeded.
