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

## CIA Session — Data Visualisation

**Question:** What chart type should I use for each type of data relationship?

**Key Insights:**

- Use a **bar chart** to compare values between categories.
- Use a **line chart** to show trends or changes over time.
- Use a **scatter chart** to show relationships between two numerical variables.
- Use a **histogram** to show the distribution of numerical data.
- Use a **box plot** to show data spread and identify potential outliers.

**Application:** I used line, bar, scatter, histogram, and box plot visualisations on the sales dataset in `visualisations.ipynb`.

## CIA Career Search — Data Visualisation

**Search:** Data Visualisation

**Key Insights:**

- Data visualisation helps communicate analytical findings clearly to technical and non-technical stakeholders.
- Visualisations help identify patterns, trends, and anomalies in data.
- Clear visualisations support data-driven decision-making.
- Data visualisation projects can strengthen a Data Analyst portfolio.
- Important areas to learn include choosing the appropriate chart type, creating clear visualisations, and communicating insights effectively.

**Application:** I applied these concepts by creating five visualisations using Matplotlib and Seaborn with the sales dataset.

## Week 2 Day 1 — Data Visualisation

### Deliverable

- visualisations.ipynb
- images/line_chart.png
- images/bar_chart.png
- images/scatter_chart.png
- images/histogram.png
- images/box_plot.png

### Practical Tasks Completed

- Created line, bar, scatter, histogram, and box plot visualisations.
- Applied a Seaborn theme.
- Added chart annotations.
- Saved visualisations as PNG files.
- Embedded the visualisations in `visualisations.ipynb`.

## CIA Session — Week 2 Day 2: Pandas Advanced

### CIA Status

CIA AI was unavailable while completing this lesson.

### Planned CIA Questions

- What advanced Pandas operations do senior data analysts use most in production?
- Explain pd.merge() vs pd.concat() with a practical data pipeline example

### CIA Career Search

Search term: Pandas Advanced

CIA AI was unavailable, so the Research/Review activity could not be completed at this time.

## Week 2 — Day 3: EDA Workflow

### What I Worked On

Completed the Week 2 Day 3 EDA Workflow practical task using the sales dataset.

### Tasks Completed

- Performed dataset overview and structure analysis.
- Checked data types.
- Checked missing values.
- Checked duplicate records.
- Generated descriptive statistics.
- Created numeric distribution plots.
- Created a correlation matrix and heatmap.
- Performed IQR-based outlier detection.
- Analyzed sales by region and category.
- Documented business insights and conclusions.

### Deliverable

- `eda_report.ipynb`

### Tools / Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- VS Code
- Git
- GitHub

### CIA

- Attempted the required CIA EDA checklist query, but CIA AI was unavailable.

Week 2 — Day 4: Data Cleaning
What I Worked On
Performed systematic data cleaning using Pandas.
Checked missing values using isnull().sum().
Confirmed that no missing values were found, so no imputation was required.
Checked for duplicate rows using duplicated().sum().
Confirmed that no duplicate rows were found.
Standardised text columns by removing leading and trailing whitespace.
Detected numerical outliers using the IQR method.
Applied IQR-based capping to numerical columns.
Created a before/after data quality comparison.
Exported the cleaned dataset as cleaned_dataset.csv.
Created cleaning_log.md to document the cleaning decisions.
Tools / Technologies
Python
Pandas
NumPy
VS Code
Git/GitHub
Deliverables
data_cleaning.ipynb
cleaned_dataset.csv
cleaning_log.md
CIA Blocker

CIA was unavailable during the Day 4 session, so I could not complete the required CIA queries, Career search, or Review submission. The practical data-cleaning tasks and Git deliverables were completed successfully.

Key Learning

Data cleaning improves the reliability and consistency of datasets before analysis. Missing values, duplicate records, inconsistent text values, and outliers should be identified and handled using appropriate methods rather than applying the same treatment to every dataset.

### Week 2 — Day 5: NumPy for Data

- **Status:** Completed
- **Deliverable:** `python-pandas/numpy_analysis.ipynb`
- **Topics:** 1D, 2D, and 3D arrays; vectorised operations; aggregation; boolean masking; fancy indexing; statistics; correlation; broadcasting.
- **Performance benchmark:** Compared Python list comprehension and NumPy vectorisation using 1 million values.
- **Result:** Verified that both methods produced matching results.
- **CIA activity:** To be recorded after completing the CIA session.
- **Git branch:** `feature/week-2-day-5`
- **Pull request:** To be added after creating the PR.

### CIA Activity — Week 2 Day 5

- **Topic:** NumPy for Data
- **Attempted query:** Explain NumPy broadcasting with a simple Python example.
- **Status:** Attempted, but CIA returned "Request failed".
- **Learning completed independently:** Studied NumPy broadcasting, vectorised operations, statistical calculations, and performance benchmarking.
- **Follow-up:** Retry CIA when the service is available.

## Week 2 — Day 6: Data Governance

### What I Worked On

Implemented data quality validation and data governance practices using Pandas and Great Expectations.

### Practical Tasks Completed

- Validated required fields and checked for missing values.
- Checked uniqueness of order IDs.
- Validated non-negative sales values and positive quantities.
- Tested validation logic using intentionally injected data errors.
- Created a data contract describing the sales dataset, its columns, and quality rules.
- Created a data quality scorecard covering data quality dimensions.
- Generated Pandas-based validation reports.
- Installed Great Expectations version 1.24.0.
- Implemented Great Expectations validation for the sales dataset.
- Ran the validation successfully and confirmed that all configured expectations passed.
- Exported the Great Expectations validation results to CSV.

### Deliverables

- `data_governance_day6.py`
- `data-contract-sales.yaml`
- `data_quality_scorecard.md`
- `great_expectations_day6.py`
- `data_governance_output/validation_results.csv`
- `data_governance_output/injected_error_tests.csv`
- `data_governance_output/data_quality_report.html`
- `data_governance_output/great_expectations_results.csv`

### Tools and Technologies

- Python
- Pandas
- Great Expectations 1.24.0
- CSV and YAML
- VS Code
- Git and GitHub

### Validation Results

- The existing Pandas validation checks passed on the original sales dataset.
- Intentional error tests confirmed detection of duplicate order IDs, negative sales, and zero quantity.
- Great Expectations validated the 10-row sales dataset.
- All configured Great Expectations checks passed.
- Validation results were saved to `data_governance_output/great_expectations_results.csv`.

### GitHub

- Feature branch: `feature/week-2-day-6`
- Original Day 6 work was merged into `main`.
- Additional Great Expectations branch: `feature/week-2-day-6-great-expectations`
- Additional Great Expectations changes were committed, pushed, and merged into `main`.

### Key Learning

Data governance improves trust in analytical datasets through documented data contracts, validation rules, quality scorecards, and repeatable testing. Pandas and Great Expectations can help identify data quality issues before data is used for reporting or decision-making.

### Outstanding Follow-up

- Verify accuracy, consistency, and timeliness using suitable source data and business rules.
- Retry required CIA activities when the CIA service becomes available, if still outstanding.
- Confirm the learning portal reflects the completed practical work.

### CIA Tasks — Blocked

- **Required query:** "What are the best practices for designing a Power BI dashboard for executives?"
- **Status:** Unable to complete because CIA is currently unavailable.
- **Career tab:** Power BI skills search pending until CIA becomes available.
- **Next action:** Retry the CIA query and Career search when the service is working.

### Outstanding Practical Task

- **Date slicer:** Not added because no suitable date field was available in the imported dataset. Confirm whether the source dataset contains a date column before making further changes.
  @'

## Week 3 - Day 2: DAX Basics

### Learning Objective

Write DAX expressions for calculated columns and measures used in dynamic business reporting.

### Practical Work

- Created `python-pandas/dax_measures.md` with five DAX expressions and explanations.
- Documented `CALCULATE()` for applying filters to measures.
- Documented a Year-to-Date (YTD) sales measure using `DATESYTD()`.
- Documented a running total expression using `EARLIER()`.
- Documented a calculated column for profit margin percentage.
- Explained row context, filter context, and context transition.
- Created a separate `TestSales` table with sample sales, profit, and order dates.
- Created a `DateTable` and established a relationship with `TestSales`.
- Tested the YTD Sales measure and verified the sample totals:
  - January 5, 2025: 1,000
  - June 15, 2025: 3,000
  - January 10, 2026: 1,500
  - March 20, 2026: 4,000
- Created and formatted the Profit Margin % calculated column and verified the sample percentages:
  - January 5, 2025: 25%
  - June 15, 2025: 30%
  - January 10, 2026: 20%
  - March 20, 2026: 30%

### Data Limitations

- The original `sales_data` table does not contain a suitable date column for a working YTD calculation.
- The original `sales_data` table does not contain actual profit data for calculating profit margin.
- YTD Sales and Profit Margin % were tested using separate sample data. These results do not represent actual business results from the original dataset.

### Deliverable

- `python-pandas/dax_measures.md`

### GitHub

- Feature branch: `feature/week-3-day-2`
- Original feature commit: `0218dfe` - `feat: dax-basics week-3-day-2 complete`
- Pull request: #17
- Status: Merged into `main` at merge commit `896adf5`.
- Documentation updates are pending a new commit and push.

### CIA Tasks

- Required query: "Explain the difference between a DAX measure and a calculated column with examples."
- Status: Blocked - CIA displayed "Request failed"; no response was received.
- Career tab search: "DAX Basics" - pending verification.
- Next action: Retry the required query, Career search, and deliverable review when CIA becomes available.

### Outstanding Follow-up

- Confirm the portal checklist, quiz, and work-log requirements are complete.
- Retry the CIA tasks when the service becomes available.
- Commit and push the updated documentation files to the feature branch.

## Week 3 — Day 3: Excel for Analysis

- **Status:** Practical work completed; Git submission merged. CIA activities partially blocked by service availability.
- Created `analysis_workbook.xlsx` with sales data, Profit, Profit Margin, and Quarter columns.
- Created a PivotTable summarising revenue by region, product, and quarter.
- Created a PivotChart with Region and Product slicers and verified interactive filtering.
- Applied conditional formatting to highlight profit-margin thresholds.
- Used Power Query to combine multiple CSV files and refreshed the query successfully, verifying six imported records.
- Created a quarterly revenue summary and calculated quarter-over-quarter growth percentages. Q4 growth displays `N/A` because no Q4 revenue was present in the original sales data.

### CIA Activities

- **Status:** Attempted; CIA returned `Request failed`.
- **Required query:** "What Excel features do professional analysts use beyond basic formulas?"
- **Result:** No response received because the CIA request failed.
- **Research activity:** Pending confirmation; CIA availability prevented completion if the request also failed.
- **Career activity:** Pending; roles and required skills could not be verified.
- **Review activity:** Pending; workbook feedback could not be obtained from CIA.
- **Follow-up:** Retry the required CIA activities when the service becomes available. No AI-generated findings were recorded because no response was received.

### Deliverables

- `analysis_workbook.xlsx`
- `work_log.md`

### Git Submission

- **Pull Request:** #18
- **Status:** Merged, if GitHub confirms the merge.
