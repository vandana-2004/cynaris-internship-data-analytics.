

\# W12D2: DuckDB vs Pandas Performance Comparison



\## 1. Objective



Compare DuckDB SQL analytical query performance with equivalent Pandas operations using the 100,000-row sales dataset.



\## 2. Dataset



\- File: `data/w5d3/sales\_100k.csv`

\- Rows: 100,000

\- Columns: order\_id, region, category, quantity, sales

\- Total sales: 459,712,000

\- Average sales: 4,597.12



\## 3. Benchmark Methodology



\- DuckDB loaded the CSV directly into an in-memory table.

\- Pandas loaded the same CSV into a DataFrame.

\- Three equivalent analytical operations were benchmarked.

\- Each operation was executed five times.

\- Median execution time was used to reduce timing variability.

\- Results were checked for equivalence before benchmarking.

\- CSV loading time was excluded from both measurements.



\## 4. Benchmark Results



| Query | DuckDB (seconds) | Pandas (seconds) | Speedup |

|---|---:|---:|---:|

| Regional sales | 0.004785 | 0.010812 | 2.26x |

| Category sales | 0.005841 | 0.010904 | 1.87x |

| Quantity by region | 0.004563 | 0.009000 | 1.97x |



Average speedup: approximately 2.03x.



\## 5. Findings



\- DuckDB was faster in all three benchmarked operations.

\- Regional sales aggregation showed the largest measured speedup.

\- Category aggregation also benefited from DuckDB SQL execution.

\- Results are specific to this dataset, machine, software versions, and benchmark methodology.

\- Performance may differ with larger datasets, different queries, and other hardware.



\## 6. Query Caching



A reusable function accepts SQL strings and returns Pandas DataFrames.



The `lru\_cache` decorator stores results for repeated identical SQL strings.



Observed cache statistics:



\- Hits: 2

\- Misses: 10

\- Maximum cache size: 64

\- Current cached entries: 10



The cache is process-local and is not persistent across application restarts.



\## 7. Indian Business Dataset Application



DuckDB was also used to analyse 128,975 rows from the Indian Business dataset.



Five analytical areas:



1\. Order status analysis

2\. Product category analysis

3\. State-wise analysis

4\. Fulfilment analysis

5\. Monthly analysis



The `Amount` field is reported as recorded amount and should not automatically be interpreted as net revenue.



\## 8. Conclusion



DuckDB provided faster execution than Pandas for all three tested analytical operations.



Its SQL interface, in-process execution, and columnar analytical processing make it useful for analytical workloads.



Pandas remains useful for DataFrame manipulation and integration with Python data-science workflows.
