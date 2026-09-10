# Week 1 Day 1 — SQL Fundamentals

## Practical Tasks Completed

- Created a sample sales database.
- Created the orders table.
- Wrote 10 SELECT queries.
- Used WHERE with comparison operators.
- Used AND, OR, and NOT.
- Used LIKE, IN, BETWEEN, and IS NULL.
- Exported one result set to CSV.

## Deliverables

- queries_day1.sql
- day1_result.csv

## CIA Session

### Question

What are the most common SQL mistakes junior data analysts make?

### CIA Insights

CIA highlighted these common SQL mistakes:

1. Using SELECT \* in production queries instead of selecting only required columns.
2. Missing or incorrect JOIN conditions, which can cause duplicate rows or incorrect totals.
3. Not using table aliases, which can make queries harder to read and debug.
4. Misusing GROUP BY and HAVING; WHERE should be used for row-level filtering.
5. Not handling NULL values correctly; use IS NULL and appropriate functions such as COALESCE.
6. Using UNION when UNION ALL would be sufficient, causing unnecessary duplicate-removal processing.
7. Writing scalar subqueries that return multiple rows when only one value is expected.

## CIA Research

### Question

What SQL concepts do data analyst job descriptions require most often?

### Key Concepts

CIA identified these SQL concepts as frequently required in data-analyst job postings:

- Core SQL syntax: SELECT, FROM, WHERE, GROUP BY, ORDER BY, HAVING, and JOINs.
- Aggregation and analytics: COUNT(), SUM(), AVG(), MIN(), MAX(), and ranking/percentile functions.
- Window functions: OVER(), PARTITION BY, LAG(), LEAD(), and ROW_NUMBER().
- Subqueries and CTEs: sub-SELECTs and WITH (Common Table Expressions).
- Data transformation: CAST(), CONVERT(), DATE functions, COALESCE(), and CASE WHEN.
- Indexing and performance: CREATE INDEX, ANALYZE, and EXPLAIN PLAN.

## CIA Career Research

### Search

SQL Fundamentals

### Required Skills

CIA Career results identified these important SQL skills:

- Core SQL commands: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, INSERT, UPDATE, DELETE.
- JOINs: INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN.
- Data modeling basics: tables, rows, columns, primary keys, foreign keys, normalization, and indexes.
- Common SQL data types: INT, VARCHAR, DATE, TIMESTAMP, DECIMAL, and BOOLEAN.
- Advanced SQL concepts: subqueries, CTEs, window functions such as ROW_NUMBER() and RANK(), and transaction control using COMMIT and ROLLBACK.

## Viva Preparation

### What is the order of SQL clause execution?

FROM and WHERE are logically processed before SELECT.

### What is the difference between = and LIKE?

= is used for exact matching, while LIKE is used for pattern matching.

### How does IS NULL differ from = NULL?

IS NULL is used to check for NULL values. = NULL does not correctly test for NULL.

## Week 1 Day 2

### CIA Insight

### CIA Research Insight

JOIN order can affect SQL query performance because it changes the size of intermediate results and the cost of the query plan. Modern database systems usually use a cost-based optimizer to choose an efficient join order automatically. Keeping database statistics and indexes up to date helps the optimizer make better decisions.

### Business Reporting Example

For a customer-order report, INNER JOIN shows only customers who placed orders, while LEFT JOIN shows every customer, including customers with no orders. COALESCE can be used to display 0 for customers with no orders.

## Week 1 Day 3 — SQL Aggregations

### CIA Research

#### Question

What are the most useful SQL aggregate functions for financial and business reporting?

#### CIA Insights

CIA highlighted the following aggregate functions as useful for financial and business reporting:

- SUM() — used for totals such as revenue, sales, and costs.
- AVG() — used for averages such as average order value and average salary.
- COUNT() — used to count rows or records.
- COUNT(DISTINCT) — used to count unique customers or products.
- MIN() — used to find the smallest value.

### CIA Career Research

#### Search

SQL Aggregations

#### Key Skills

CIA Career research highlighted these SQL aggregation skills:

- COUNT() — counts rows or non-NULL values.
- SUM() — calculates the total of a numeric column.
- AVG() — calculates the mean of a numeric column.
- MIN() — finds the smallest value.
- MAX() — finds the largest value.
- GROUP BY — groups rows with identical values in selected columns.
- HAVING — filters groups after aggregation.
- Conditional aggregation — uses CASE inside aggregate functions to calculate values based on conditions.

### CIA Review

#### Deliverable Reviewed

queries_day3.sql

#### CIA Feedback

CIA reviewed the Day 3 SQL aggregation queries and provided the following feedback:

- USE retail_sales; is valid for MySQL/MariaDB but is not supported in PostgreSQL or SQL Server.
- COUNT(\*) is valid and generally fine, but performance should be considered for very large tables.
- SUM(sales_amount) is correct; if sales_amount can contain NULL values, COALESCE(sales_amount, 0) can be considered.

Week 1 Day 4 — SQL Subqueries & CTEs

CIA Insight

CIA Research Insight

CTEs (Common Table Expressions) are temporary named result sets created using the WITH clause. They help improve SQL query readability by breaking complex queries into logical steps. Multiple CTEs can be chained together, allowing one CTE to use the result of another.

Business Reporting Example

For a customer sales report, a CTE can first calculate total sales for each customer and then filter customers based on their total sales. This makes multi-step reporting queries easier to read and maintain.

CIA Research

Question

What are recursive CTEs and when are they used in real data pipelines?

CIA Insights

CIA explained that recursive CTEs are CTEs that refer to themselves during query execution. They contain an anchor member that starts the recursion and a recursive member that processes subsequent levels.

Recursive CTEs are useful for hierarchical and tree-structured data such as employee-manager relationships, product categories, bill-of-materials structures, and graph traversal.

CIA Career Research

Search

SQL CTEs

Required Skills

CIA Career results identified these important SQL skills:

- Understanding CTEs and the WITH clause.
- Creating multiple and chained CTEs.
- Using CTEs with aggregation and filtering.
- Understanding recursive CTEs.
- Using CTEs for complex and multi-step SQL analysis.
- Applying recursive CTEs to hierarchical data.

CIA Review

Deliverable Reviewed

queries_day4.sql

CIA Feedback

CIA reviewed the Day 4 SQL subqueries and CTE work and highlighted the importance of using CTEs to make complex queries more readable and organized. It also highlighted recursive CTEs as useful for hierarchical data and multi-level relationships.

CIA Career Activity

Search

SQL CTEs

Key Learning

CIA Career results showed that CTEs are an important SQL skill for data analyst roles, particularly for writing readable multi-step queries, working with aggregations, and handling hierarchical data.

### CIA — Research

**Query:** What are the most useful Pandas methods for exploratory data analysis?

**Key Insights:**

- `head()` and `tail()` are useful for quickly viewing the first and last rows.
- `info()` shows column names, data types, and missing values.
- `describe()` provides statistical summaries such as count, mean, minimum, maximum, and quartiles.
- `value_counts()` helps understand the frequency of values in a column.
- `isnull()` and `dropna()` are useful for identifying and handling missing data.
- Filtering and column selection help focus the analysis on relevant records.
- `groupby()` is useful for summarising data by categories.
- `to_csv()` can be used to export cleaned data for further analysis.

### CIA — Research: Python Libraries

**Query:** What Python libraries do professional data analysts use beyond Pandas?

**Key Insights:**

- **NumPy** — numerical calculations and array operations.
- **Matplotlib** — creating charts and visualisations.
- **Seaborn** — statistical visualisations and attractive charts.
- **SciPy** — scientific and statistical calculations.
- **Scikit-learn** — machine learning and predictive analysis.
- **Plotly** — interactive charts and dashboards.

**Career Takeaway:** Pandas is commonly used together with these libraries to perform data cleaning, analysis, visualisation, statistics, and machine learning tasks.

### CIA — Career

**Query:** Python Pandas

**Key Insights:**

- Pandas is an important skill for Data Analyst roles.
- It is widely used for data cleaning and preprocessing.
- Pandas supports exploratory data analysis and finding patterns in datasets.
- Analysts use Pandas to work with CSV, Excel, SQL, and JSON data.
- Pandas works well with visualisation libraries such as Matplotlib and Seaborn.
- Pandas is built on NumPy.

**Career Takeaway:** Learning Pandas is important for a Data Analyst because it is commonly used to clean, explore, transform, and analyse real-world datasets.

### CIA Review — Week 1 Day 5

#### Deliverable Reviewed

analysis_day5.ipynb

#### CIA Feedback

CIA reviewed the Week 1 Day 5 Pandas deliverable and stated:

"Excellent work on your Week 1 Day 5 Pandas deliverable! You've demonstrated a solid understanding."
