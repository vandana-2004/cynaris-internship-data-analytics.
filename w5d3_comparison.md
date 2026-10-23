\# W5D3: Pandas vs DuckDB vs Polars



\## Benchmark setup



\- Dataset: 100,000 sales records

\- Data source: `data/w5d3/sales\_100k.csv`

\- Operations: total sales, average sales, sales by region, quantity by category, and high-value order count

\- Tools: Pandas 3.0.5, DuckDB 2.0.0, Polars 2.0.0

\- Timing method: measured each operation after loading the data into each tool



\## Benchmark results



| Tool | Mean operation time | Main approach |

|---|---:|---|

| Pandas | 0.004078 seconds | DataFrame operations |

| DuckDB | 0.003457 seconds | SQL queries on an in-memory table |

| Polars | 0.001878 seconds | Expression-based DataFrame operations |



These are single-run measurements and are environment-dependent, not universal performance rankings.



\## Five-criteria comparison



| Criterion | Pandas | DuckDB | Polars |

|---|---|---|---|

| Query syntax | Python methods | SQL | Python expressions |

| Best suited for | General data manipulation and analysis | Analytical SQL over CSV, Parquet, and tables | Fast DataFrame transformations |

| Execution model | Eager by default | SQL query engine with query optimization | Eager and lazy execution |

| Data handling | In-memory DataFrames | Can query files directly or use database tables | DataFrames and lazy query plans |

| Key strength | Broad Python ecosystem | SQL analytics and direct file querying | Efficient columnar processing |



\## Conclusion



In this benchmark, Polars had the lowest mean operation time, followed by DuckDB and Pandas. DuckDB is useful when SQL-based analysis or querying large files directly is preferred. Pandas remains convenient for general analysis, while Polars is useful for efficient DataFrame workflows.



\## Viva preparation



1\. \*\*What is columnar storage?\*\* Data is organized by columns, which can improve analytical queries that access only selected columns. DuckDB's analytical execution benefits from column-oriented processing.

2\. \*\*DuckDB vs MySQL:\*\* DuckDB is optimized for analytical workloads (OLAP), often embedded within an application. MySQL is commonly used as a persistent server database for transactional workloads (OLTP).

3\. \*\*OLAP vs OLTP:\*\* OLAP focuses on aggregations and analysis over larger datasets; OLTP focuses on many small, reliable transactions such as inserting or updating orders.



