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

- **Status:** Practical work completed; original PR #18 merged. CIA activities partially blocked by service availability.
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
- **Research activity:** Pending.
- **Career activity:** Pending; required roles and skills have not been verified.
- **Review activity:** Pending; workbook feedback has not been obtained.
- **Follow-up:** Retry the required CIA activities when the service becomes available. No AI-generated findings were recorded because no response was received.

### Deliverables

- `analysis_workbook.xlsx`
- `work_log.md`

### Git Submission

- **Original Pull Request:** #18 — merged.
- **Work-log follow-up:** PR #19 pending.

## Week 3 Day 5 — KPI Design

- **Practical work:** Created `kpi_framework.md` with 10 KPIs and their formulas, owners, review frequencies, targets, and leading/lagging classifications.
- **Dashboard:** Created `KPI Dashboard.pbix` with Total Sales, Total Orders, Average Order Value, Sales by Region, and Sales by Category.
- **Interactivity:** Tested Region and Category slicers.
- **Screenshot:** Saved as `kpi_dashboard.png`.
- **Narrative:** Created `kpi_narrative.md` describing the dashboard, key indicators, recommendations, and data limitations.
- **CIA query:** Pending — record the actual response to “What is the difference between a KPI, a metric, and a measure?” when available.
- **CIA Career search:** Pending — search for “KPI Design” when available.
- **Status:** Practical deliverables completed. CIA activities remain pending.

## Week 3 Day 5 — CIA and Career Search Update

- **CIA query:** Attempted the question, "What is the difference between a KPI, a metric, and a measure?"
- **Result:** CIA was unavailable, so no response was received.
- **Career search:** Attempted to access the Career tab and search for "KPI Design".
- **Result:** Unable to complete the search because CIA was not working.
- **Next action:** Retry both activities when CIA becomes available.

## Week 3 — Day 4: Looker Studio

- **Hours Worked:** 1.0
- **Topics Covered:** Looker Studio dashboards, Google Sheets integration, chart creation, interactive filters, and dashboard sharing.
- **Work Completed:** Connected Google Sheets and created a sales dashboard with a scorecard, bar chart, line chart, pie chart, and table. Added Region and Category filters and applied the Edge theme.
- **Tools Used:** Google Sheets, Google Looker Studio, Git, GitHub.
- **Deliverables:** `looker_studio_dashboard.png`; dashboard link added to `README.md`.
- **Git:** Commit `ef9c94d`; PR #22 merged.
- **Challenges:** - **Challenges:** The scorecard metric required troubleshooting. CIA was unavailable because the required Groq, OpenRouter, and Gemini API keys were not configured. CIA session and Career tab activities remain pending.

# Week 4 — Day 1: Statistics

**Date:** 20 October 2026

**Hours Worked:** 1.5

**Topics Covered:** Descriptive statistics, mean, median, mode, variance, standard deviation, percentiles, quartiles, frequency distributions, outliers, and box plots.

## What I Worked On

Created `statistics_analysis.ipynb` to apply descriptive statistics to a sample business sales dataset containing Online and Store sales groups.

Completed the following practical tasks:

- Calculated mean, median, mode, variance, and standard deviation using Pandas and NumPy.
- Calculated the 25th, 50th, 75th, and 90th percentiles.
- Generated a five-number summary and descriptive statistics.
- Created a histogram to visualize the sales frequency distribution.
- Created side-by-side box plots to compare Online and Store sales.
- Examined how an unusually high sales value affects the mean and distribution.
- Added interpretation notes explaining central tendency, variability, outliers, and distribution shape.

## Tools / Technologies Used

Python, Pandas, NumPy, Matplotlib, Jupyter Notebook, VS Code, Git, GitHub, and Cynaris Intelligent Assistant (CIA).

## Deliverable

- `statistics_analysis.ipynb` — descriptive statistics calculations and visualizations.

## Git Tasks

- Created branch: `feature/week-4-day-1`
- Commit: `1f519fd`
- Commit message: `feat: descriptive-statistics week-4-day-1 complete`
- Pushed the branch to GitHub.
- Created Pull Request #24.
- Merged PR #24 into `main` successfully.
- Pulled the latest changes into the local `main` branch.

## CIA Activities and Insights

### 1. Chat — Mean vs. Median

**Query:** When should I use median instead of mean to describe a dataset?

**Insight:** The mean is useful for roughly symmetric distributions without highly influential outliers. The median is more resistant to extreme values and is often more representative of skewed datasets, such as salaries and house prices.

### 2. Search — Statistics Interview Topics

**Search topic:** Key statistical concepts tested in data analyst interviews.

**Key findings:**

- Mean, median, and mode describe central tendency.
- Variance and standard deviation measure data dispersion.
- Percentiles describe the relative position of values in a dataset.
- Normal, binomial, and Poisson distributions describe different patterns of data or random outcomes.
- Outliers should be investigated to determine whether they indicate data errors or meaningful unusual observations.

### 3. Career Advice — Statistics for Data Analysts

**Activity:** Reviewed CIA career guidance on statistical skills for Junior Data Analyst roles.

**Key insights:**

- Apply descriptive statistics and exploratory data analysis to understand datasets.
- Identify outliers and investigate missing values and data quality.
- Understand probability distributions and inferential statistics.
- Learn hypothesis testing, p-values, confidence intervals

### Week 4 Day 1 — Statistics Improvements

- Identified the sales distribution as right-skewed (skewness: 4.13).
- Calculated Q1 (133.75), Q3 (160.0), and IQR (26.25).
- Applied the 1.5 × IQR rule and identified 500 as an outlier.
- Explained why the median and IQR are more robust than the mean and standard deviation when data is skewed or contains outliers.
- Received CIA Chat feedback confirming that the notebook meets the baseline requirements.
- Updated `statistics_analysis.ipynb` and merged PR #25 into `main`.
- Commit: `05c6586`
- PR: #25 — `feat: improve descriptive statistics interpretation`

# Week 4 — Day 2: Probability

**Date:** 20 October 2026  
**Hours Worked:** 1.5 hours (adjust to your actual time)  
**Status:** Practical tasks completed; original Pull Request merged.

## Learning Objective

Understand probability concepts and key distributions used in data analysis and business forecasting.

## Topics Covered

- Basic, joint, and conditional probability
- Normal distribution and the 68–95–99.7 rule
- Binomial distribution and simulation
- Central Limit Theorem (CLT)
- Applications of probability in data analytics and business forecasting

## Practical Tasks Completed

### 1. Probability Calculations

- Created a contingency table using Pandas.
- Calculated basic probability, joint probability, and conditional probability.
- Practised interpreting probability results in a business context.

### 2. Normal Distribution

- Generated random observations from a normal distribution using NumPy.
- Plotted the distribution using Matplotlib.
- Calculated the proportions of observations within one, two, and three standard deviations to examine the 68–95–99.7 rule.

### 3. Binomial Distribution

- Simulated binomial outcomes using NumPy.
- Plotted the simulated distribution.
- Compared the simulated mean with the theoretical mean.

### 4. Central Limit Theorem

- Generated data from an exponential population.
- Repeatedly sampled observations and calculated sample means.
- Plotted the distribution of sample means to demonstrate the CLT.

**Verification:** Executed the notebook and confirmed that the outputs and plots were generated successfully.

## Tools and Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Jupyter Notebook
- Visual Studio Code
- Git and GitHub
- Cynaris Intelligent Assistant (CIA)

## CIA Activities

### 1. Research — Probability in Real Data Analyst Work

**Status:** Completed

**Query:** Where does probability theory show up in real data analyst work?

**Key Insights:**

- Business forecasting uses probability and statistical models to estimate demand and account for uncertainty.
- Customer analytics uses statistical reasoning to investigate customer behavior, churn, conversions, and A/B testing.
- Risk analysis uses probability-based methods to assess uncertainty and potential losses.
- Business decision-making can use simulations to compare possible outcomes.
- Probability is a foundation for statistical analysis and predictive modeling.

### 2. Learning — Central Limit Theorem

**Status:** Completed

**Query:** Explain the Central Limit Theorem with a business forecasting example.

**Key Insights:**

- The distribution of sample means approaches a normal distribution when sufficiently large random samples are repeatedly drawn from a population with a finite mean and variance.
- The original population does not need to be normally distributed.
- The CLT supports statistical inference, including confidence intervals and hypothesis testing when the required assumptions are satisfied.
- Business example: repeatedly sampling customer spending and calculating sample averages to understand their distribution and estimate the population average.

### 3. Career Advice — Probability

**Status:** Completed

**Query:** Probability

**Key Insights:**

- Probability helps analysts generalize from samples to populations and quantify uncertainty.
- Core concepts include events, sample spaces, addition and complement rules, independence, conditional probability, and Bayes' theorem.
- Probability supports predictive modeling techniques, including Naive Bayes.
- Conditional probability can help investigate whether customer engagement is associated with churn.

**Career Relevance:** Probability, statistical reasoning, and Python-based data analysis are useful foundations for data analytics and predictive modeling.

**Note:** CIA provided career-oriented learning guidance, not verified job vacancies or employer-specific requirements.

### 4. Review — Probability Notebook

**Status:** Conceptual feedback received; direct notebook review unavailable.

**Deliverable:** `probability_notebook.ipynb`

**Review Method:** Shared a summary of the practical tasks with CIA because the Chat interface did not support file uploads.

**Feedback Received:**

- Verify the conditional probability formula and the denominator used.
- Check contingency-table totals and explain the results in context.
- Verify the normal-distribution intervals using the mean and standard deviation.
- Compare the simulated binomial mean with the theoretical mean.
- Explain the distribution of sample means in the CLT simulation.

**Limitation:** CIA could not inspect the actual notebook code or independently verify its calculations. The feedback was a conceptual checklist, not a formal code review.

## Git and GitHub

- **Branch:** `feature/week-4-day-2`
- **Initial commit:** `3e2027b` — `feat: probability-distributions week-4-day-2 complete`
- **Correction commit:** `50ce66a` — `fix: save probability analysis notebook`
- **Pull Request:** #26
- **Original Pull Request status:** Merged into `main`
- **Merge commit:** `18f5ee4`
- **Practical deliverable:** `probability_notebook.ipynb`

**Work Log Note:** The work-log changes made after PR #26 was merged were pushed to the feature branch separately. Their inclusion in `main` must be confirmed.

## Challenges and Resolutions

The notebook was initially committed before its contents were saved correctly. The notebook was subsequently saved, corrected, and committed in a follow-up commit. The changes were pushed to GitHub, and PR #26 was merged into `main`. The notebook outputs were verified.

The CIA Chat interface did not support uploading the notebook for direct review. A text-based conceptual checklist was obtained instead.

## Learning Outcomes

- Applied basic, joint, and conditional probability calculations.
- Visualized a normal distribution and examined the empirical rule.
- Simulated a binomial distribution using NumPy.
- Demonstrated the CLT using repeated sampling.
- Connected probability concepts with forecasting, customer analytics, and risk analysis.
- Identified checks for reviewing statistical calculations and simulations.

## Final Checklist

- [x] Practical notebook created and saved.
- [x] Notebook cells executed and outputs verified.
- [x] Probability quiz completed with 100%.
- [x] CIA research completed and documented.
- [x] CIA CLT explanation completed and documented.
- [x] CIA Career Advice query completed and documented.
- [x] CIA conceptual review guidance received and documented.
- [x] Notebook changes committed and pushed.
- [x] Original Pull Request #26 merged into `main`.
- [ ] Latest work-log changes confirmed in `main`.
- [ ] Notebook code checked against the CIA feedback checklist, if not already reviewed.

**Final Status:** The practical tasks, CIA learning activities, and original GitHub pull request are completed. The direct CIA file review was unavailable, and the final work-log merge status and any remaining self-review checks are not yet confirmed.

## Week 4 — Day 3: Regression Analysis

**Status:** Practical notebook committed and pushed; CIA learning interactions completed.

### Practical Work

- Created `regression_analysis.ipynb` for regression analysis using Python.
- Prepared analysis covering correlation, linear regression, model evaluation, and regression diagnostics.
- Used Python data analysis and machine learning libraries, including Pandas, NumPy, Matplotlib, Seaborn, and Scikit-learn.

### CIA Activities

- **Research:** Reviewed linear, multiple linear, logistic, regularized, tree-based, polynomial, and time-series regression techniques and their business applications.
- **Chat:** Learned the difference between correlation and causation. Reviewed rainy weather as a confounding factor affecting umbrella sales and customer complaints.
- **Regression overview:** Reviewed regression assumptions, multicollinearity, residual diagnostics, regularization, and model evaluation practices.

### Key Learnings

- Regression can estimate continuous business metrics and identify relationships between predictors and outcomes.
- Correlation alone does not establish causation.
- Residual plots and appropriate evaluation metrics help assess model performance.
- Multicollinearity should be investigated when using multiple predictors.

### Deliverables

- `regression_analysis.ipynb`

### Git Submission

- Branch: `feature/week-4-day-3`
- Commit: `23bb72a` — `feat: correlation-regression week-4-day-3 complete`
- Notebook branch pushed to GitHub.
- Pull request: verify the PR status and link before recording it here.

### Challenges / Blockers

- The CIA response for the regression overview did not clearly identify which tab generated it.
- Notebook execution results and diagnostic plots should be verified before claiming that all analyses ran successfully.
