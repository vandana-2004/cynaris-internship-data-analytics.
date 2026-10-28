# Week 1 Day 1 â€” SQL Fundamentals

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

## Week 1 Day 3 â€” SQL Aggregations

### CIA Research

#### Question

What are the most useful SQL aggregate functions for financial and business reporting?

#### CIA Insights

CIA highlighted the following aggregate functions as useful for financial and business reporting:

- SUM() â€” used for totals such as revenue, sales, and costs.
- AVG() â€” used for averages such as average order value and average salary.
- COUNT() â€” used to count rows or records.
- COUNT(DISTINCT) â€” used to count unique customers or products.
- MIN() â€” used to find the smallest value.

### CIA Career Research

#### Search

SQL Aggregations

#### Key Skills

CIA Career research highlighted these SQL aggregation skills:

- COUNT() â€” counts rows or non-NULL values.
- SUM() â€” calculates the total of a numeric column.
- AVG() â€” calculates the mean of a numeric column.
- MIN() â€” finds the smallest value.
- MAX() â€” finds the largest value.
- GROUP BY â€” groups rows with identical values in selected columns.
- HAVING â€” filters groups after aggregation.
- Conditional aggregation â€” uses CASE inside aggregate functions to calculate values based on conditions.

### CIA Review

#### Deliverable Reviewed

queries_day3.sql

#### CIA Feedback

CIA reviewed the Day 3 SQL aggregation queries and provided the following feedback:

- USE retail_sales; is valid for MySQL/MariaDB but is not supported in PostgreSQL or SQL Server.
- COUNT(\*) is valid and generally fine, but performance should be considered for very large tables.
- SUM(sales_amount) is correct; if sales_amount can contain NULL values, COALESCE(sales_amount, 0) can be considered.

Week 1 Day 4 â€” SQL Subqueries & CTEs

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

### CIA â€” Research

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

### CIA â€” Research: Python Libraries

**Query:** What Python libraries do professional data analysts use beyond Pandas?

**Key Insights:**

- **NumPy** â€” numerical calculations and array operations.
- **Matplotlib** â€” creating charts and visualisations.
- **Seaborn** â€” statistical visualisations and attractive charts.
- **SciPy** â€” scientific and statistical calculations.
- **Scikit-learn** â€” machine learning and predictive analysis.
- **Plotly** â€” interactive charts and dashboards.

**Career Takeaway:** Pandas is commonly used together with these libraries to perform data cleaning, analysis, visualisation, statistics, and machine learning tasks.

### CIA â€” Career

**Query:** Python Pandas

**Key Insights:**

- Pandas is an important skill for Data Analyst roles.
- It is widely used for data cleaning and preprocessing.
- Pandas supports exploratory data analysis and finding patterns in datasets.
- Analysts use Pandas to work with CSV, Excel, SQL, and JSON data.
- Pandas works well with visualisation libraries such as Matplotlib and Seaborn.
- Pandas is built on NumPy.

**Career Takeaway:** Learning Pandas is important for a Data Analyst because it is commonly used to clean, explore, transform, and analyse real-world datasets.

### CIA Review â€” Week 1 Day 5

#### Deliverable Reviewed

analysis_day5.ipynb

#### CIA Feedback

CIA reviewed the Week 1 Day 5 Pandas deliverable and stated:

"Excellent work on your Week 1 Day 5 Pandas deliverable! You've demonstrated a solid understanding."

## CIA Session â€” Data Visualisation

**Question:** What chart type should I use for each type of data relationship?

**Key Insights:**

- Use a **bar chart** to compare values between categories.
- Use a **line chart** to show trends or changes over time.
- Use a **scatter chart** to show relationships between two numerical variables.
- Use a **histogram** to show the distribution of numerical data.
- Use a **box plot** to show data spread and identify potential outliers.

**Application:** I used line, bar, scatter, histogram, and box plot visualisations on the sales dataset in `visualisations.ipynb`.

## CIA Career Search â€” Data Visualisation

**Search:** Data Visualisation

**Key Insights:**

- Data visualisation helps communicate analytical findings clearly to technical and non-technical stakeholders.
- Visualisations help identify patterns, trends, and anomalies in data.
- Clear visualisations support data-driven decision-making.
- Data visualisation projects can strengthen a Data Analyst portfolio.
- Important areas to learn include choosing the appropriate chart type, creating clear visualisations, and communicating insights effectively.

**Application:** I applied these concepts by creating five visualisations using Matplotlib and Seaborn with the sales dataset.

## Week 2 Day 1 â€” Data Visualisation

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

## CIA Session â€” Week 2 Day 2: Pandas Advanced

### CIA Status

CIA AI was unavailable while completing this lesson.

### Planned CIA Questions

- What advanced Pandas operations do senior data analysts use most in production?
- Explain pd.merge() vs pd.concat() with a practical data pipeline example

### CIA Career Search

Search term: Pandas Advanced

CIA AI was unavailable, so the Research/Review activity could not be completed at this time.

## Week 2 â€” Day 3: EDA Workflow

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

Week 2 â€” Day 4: Data Cleaning
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

### Week 2 â€” Day 5: NumPy for Data

- **Status:** Completed
- **Deliverable:** `python-pandas/numpy_analysis.ipynb`
- **Topics:** 1D, 2D, and 3D arrays; vectorised operations; aggregation; boolean masking; fancy indexing; statistics; correlation; broadcasting.
- **Performance benchmark:** Compared Python list comprehension and NumPy vectorisation using 1 million values.
- **Result:** Verified that both methods produced matching results.
- **CIA activity:** To be recorded after completing the CIA session.
- **Git branch:** `feature/week-2-day-5`
- **Pull request:** To be added after creating the PR.

### CIA Activity â€” Week 2 Day 5

- **Topic:** NumPy for Data
- **Attempted query:** Explain NumPy broadcasting with a simple Python example.
- **Status:** Attempted, but CIA returned "Request failed".
- **Learning completed independently:** Studied NumPy broadcasting, vectorised operations, statistical calculations, and performance benchmarking.
- **Follow-up:** Retry CIA when the service is available.

## Week 2 â€” Day 6: Data Governance

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

### CIA Tasks â€” Blocked

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

## Week 3 â€” Day 3: Excel for Analysis

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

- **Original Pull Request:** #18 â€” merged.
- **Work-log follow-up:** PR #19 pending.

## Week 3 Day 5 â€” KPI Design

- **Practical work:** Created `kpi_framework.md` with 10 KPIs and their formulas, owners, review frequencies, targets, and leading/lagging classifications.
- **Dashboard:** Created `KPI Dashboard.pbix` with Total Sales, Total Orders, Average Order Value, Sales by Region, and Sales by Category.
- **Interactivity:** Tested Region and Category slicers.
- **Screenshot:** Saved as `kpi_dashboard.png`.
- **Narrative:** Created `kpi_narrative.md` describing the dashboard, key indicators, recommendations, and data limitations.
- **CIA query:** Pending â€” record the actual response to â€œWhat is the difference between a KPI, a metric, and a measure?â€ when available.
- **CIA Career search:** Pending â€” search for â€œKPI Designâ€ when available.
- **Status:** Practical deliverables completed. CIA activities remain pending.

## Week 3 Day 5 â€” CIA and Career Search Update

- **CIA query:** Attempted the question, "What is the difference between a KPI, a metric, and a measure?"
- **Result:** CIA was unavailable, so no response was received.
- **Career search:** Attempted to access the Career tab and search for "KPI Design".
- **Result:** Unable to complete the search because CIA was not working.
- **Next action:** Retry both activities when CIA becomes available.

## Week 3 â€” Day 4: Looker Studio

- **Hours Worked:** 1.0
- **Topics Covered:** Looker Studio dashboards, Google Sheets integration, chart creation, interactive filters, and dashboard sharing.
- **Work Completed:** Connected Google Sheets and created a sales dashboard with a scorecard, bar chart, line chart, pie chart, and table. Added Region and Category filters and applied the Edge theme.
- **Tools Used:** Google Sheets, Google Looker Studio, Git, GitHub.
- **Deliverables:** `looker_studio_dashboard.png`; dashboard link added to `README.md`.
- **Git:** Commit `ef9c94d`; PR #22 merged.
- **Challenges:** - **Challenges:** The scorecard metric required troubleshooting. CIA was unavailable because the required Groq, OpenRouter, and Gemini API keys were not configured. CIA session and Career tab activities remain pending.

# Week 4 â€” Day 1: Statistics

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

- `statistics_analysis.ipynb` â€” descriptive statistics calculations and visualizations.

## Git Tasks

- Created branch: `feature/week-4-day-1`
- Commit: `1f519fd`
- Commit message: `feat: descriptive-statistics week-4-day-1 complete`
- Pushed the branch to GitHub.
- Created Pull Request #24.
- Merged PR #24 into `main` successfully.
- Pulled the latest changes into the local `main` branch.

## CIA Activities and Insights

### 1. Chat â€” Mean vs. Median

**Query:** When should I use median instead of mean to describe a dataset?

**Insight:** The mean is useful for roughly symmetric distributions without highly influential outliers. The median is more resistant to extreme values and is often more representative of skewed datasets, such as salaries and house prices.

### 2. Search â€” Statistics Interview Topics

**Search topic:** Key statistical concepts tested in data analyst interviews.

**Key findings:**

- Mean, median, and mode describe central tendency.
- Variance and standard deviation measure data dispersion.
- Percentiles describe the relative position of values in a dataset.
- Normal, binomial, and Poisson distributions describe different patterns of data or random outcomes.
- Outliers should be investigated to determine whether they indicate data errors or meaningful unusual observations.

### 3. Career Advice â€” Statistics for Data Analysts

**Activity:** Reviewed CIA career guidance on statistical skills for Junior Data Analyst roles.

**Key insights:**

- Apply descriptive statistics and exploratory data analysis to understand datasets.
- Identify outliers and investigate missing values and data quality.
- Understand probability distributions and inferential statistics.
- Learn hypothesis testing, p-values, confidence intervals

### Week 4 Day 1 â€” Statistics Improvements

- Identified the sales distribution as right-skewed (skewness: 4.13).
- Calculated Q1 (133.75), Q3 (160.0), and IQR (26.25).
- Applied the 1.5 Ã— IQR rule and identified 500 as an outlier.
- Explained why the median and IQR are more robust than the mean and standard deviation when data is skewed or contains outliers.
- Received CIA Chat feedback confirming that the notebook meets the baseline requirements.
- Updated `statistics_analysis.ipynb` and merged PR #25 into `main`.
- Commit: `05c6586`
- PR: #25 â€” `feat: improve descriptive statistics interpretation`

# Week 4 â€” Day 2: Probability

**Date:** 20 October 2026  
**Hours Worked:** 1.5 hours (adjust to your actual time)  
**Status:** Practical tasks completed; original Pull Request merged.

## Learning Objective

Understand probability concepts and key distributions used in data analysis and business forecasting.

## Topics Covered

- Basic, joint, and conditional probability
- Normal distribution and the 68â€“95â€“99.7 rule
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
- Calculated the proportions of observations within one, two, and three standard deviations to examine the 68â€“95â€“99.7 rule.

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

### 1. Research â€” Probability in Real Data Analyst Work

**Status:** Completed

**Query:** Where does probability theory show up in real data analyst work?

**Key Insights:**

- Business forecasting uses probability and statistical models to estimate demand and account for uncertainty.
- Customer analytics uses statistical reasoning to investigate customer behavior, churn, conversions, and A/B testing.
- Risk analysis uses probability-based methods to assess uncertainty and potential losses.
- Business decision-making can use simulations to compare possible outcomes.
- Probability is a foundation for statistical analysis and predictive modeling.

### 2. Learning â€” Central Limit Theorem

**Status:** Completed

**Query:** Explain the Central Limit Theorem with a business forecasting example.

**Key Insights:**

- The distribution of sample means approaches a normal distribution when sufficiently large random samples are repeatedly drawn from a population with a finite mean and variance.
- The original population does not need to be normally distributed.
- The CLT supports statistical inference, including confidence intervals and hypothesis testing when the required assumptions are satisfied.
- Business example: repeatedly sampling customer spending and calculating sample averages to understand their distribution and estimate the population average.

### 3. Career Advice â€” Probability

**Status:** Completed

**Query:** Probability

**Key Insights:**

- Probability helps analysts generalize from samples to populations and quantify uncertainty.
- Core concepts include events, sample spaces, addition and complement rules, independence, conditional probability, and Bayes' theorem.
- Probability supports predictive modeling techniques, including Naive Bayes.
- Conditional probability can help investigate whether customer engagement is associated with churn.

**Career Relevance:** Probability, statistical reasoning, and Python-based data analysis are useful foundations for data analytics and predictive modeling.

**Note:** CIA provided career-oriented learning guidance, not verified job vacancies or employer-specific requirements.

### 4. Review â€” Probability Notebook

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
- **Initial commit:** `3e2027b` â€” `feat: probability-distributions week-4-day-2 complete`
- **Correction commit:** `50ce66a` â€” `fix: save probability analysis notebook`
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

## Week 4 â€” Day 3: Regression Analysis

**Status:** Practical work completed, notebook executed successfully, and pull request #28 opened.

### Practical Work

- Created `regression_analysis.ipynb` for regression analysis using Python.
- Covered correlation analysis, linear regression, model evaluation, and regression diagnostics.
- Used Pandas and NumPy for data preparation and calculations.
- Used Matplotlib and Seaborn for data visualization and diagnostic plots.
- Used Scikit-learn for regression modeling and model evaluation.
- Executed the notebook cells and verified that the regression results and plots appeared successfully.

### CIA Learning Activities

- **Research:** Reviewed linear, multiple linear, logistic, regularized, tree-based, polynomial, and time-series regression techniques and their business applications.
- **Chat:** Learned the difference between correlation and causation. Reviewed the example of rainy weather influencing both umbrella sales and customer complaints.
- **Regression Overview:** Reviewed regression assumptions, multicollinearity, residual diagnostics, regularization, and model evaluation practices.

### Key Learnings

- Regression helps estimate continuous business outcomes and analyze relationships between variables.
- Correlation does not necessarily imply causation.
- Residual plots help identify potential problems with a regression model.
- Multicollinearity can affect the interpretation of multiple regression coefficients.
- Evaluation metrics help assess how well a regression model performs.
- Regularization can help reduce overfitting in suitable regression models.

### Tools and Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Git and GitHub

### Deliverables

- `regression_analysis.ipynb`
- `work_log.md`

### Validation

- Notebook cells executed successfully.
- Regression results and diagnostic plots verified.
- Changes committed and pushed to GitHub.
- Pull request #28 opened for merging into `main`.
- No merge conflicts reported by GitHub.

### Git Submission

- **Branch:** `feature/week-4-day-3`
- **Initial commit:** `23bb72a` â€” `feat: correlation-regression week-4-day-3 complete`
- **Work-log commit:** `2556338` â€” `docs: update week-4-day-3 work log`
- **Notebook correction commit:** `f29f171` â€” `fix: save complete regression analysis notebook`
- **Pull request:** #28 â€” `feat: Week 4 Day 3 Regression Analysis`
- **Pull request status:** Open; merge not yet confirmed.

### Challenges / Blockers

- The CIA regression overview response did not clearly identify which tab generated it.
- The notebook initially contained only a test cell. The complete regression notebook was subsequently saved, committed, pushed, and executed successfully.

### Final Status

Practical work, CIA learning activities, notebook execution, and Git submission are completed. Pull request #28 is awaiting merge confirmation.

# Work Log

## Week 4 â€” Day 4: Hypothesis Testing

**Day:** Thursday  
**Lesson:** Hypothesis Testing  
**Status:** Practical work completed; Git commit and pull request pending.

### Learning Objectives

Learn to formulate null and alternative hypotheses, perform statistical tests, interpret p-values and confidence intervals, and use statistical evidence to support business decisions.

### Topics Covered

- Null hypothesis (Hâ‚€) and alternative hypothesis (Hâ‚)
- One-sample and two-sample t-tests
- P-values and statistical significance
- Confidence intervals
- Type I and Type II errors
- A/B testing
- Business interpretation of statistical results

### Practical Work Completed

- Created `hypothesis_tests.ipynb`.
- Used Python statistical libraries to conduct hypothesis testing.
- Formulated hypotheses for business scenarios.
- Performed a one-sample t-test using `scipy.stats`.
- Performed a two-sample t-test to compare two groups.
- Interpreted p-values and confidence intervals.
- Evaluated statistical significance using a significance level of 0.05.
- Generated a graph to visualize the data.
- Reviewed Type I and Type II errors and their business consequences.
- Executed all notebook cells successfully and reviewed the outputs and graph.

### CIA Research â€” A/B Testing and Hypothesis Testing

- A/B testing compares a control version (A) with a treatment version (B) to evaluate differences in business metrics.
- Random assignment helps reduce selection bias.
- Statistical tests, p-values, confidence intervals, and effect sizes help assess experimental results.
- Adequate sample size is important for statistical power.
- Multiple testing can increase the risk of false-positive results.

### CIA Research â€” P-values and Statistical Significance

- A p-value measures how likely results at least as extreme as the observed results would be if the null hypothesis were true.
- A common significance level is Î± = 0.05.
- When the p-value is below the chosen significance level, the null hypothesis is rejected under the specified testing procedure.
- Statistical significance does not necessarily imply practical or commercial importance.
- Business decisions should consider effect size, confidence intervals, costs, and context.

### CIA Career Research

Used CIA Search to explore career opportunities and skills related to hypothesis testing.

**Relevant career roles:**

- A/B Testing and Experimentation Analyst
- Marketing and Campaign Analyst
- Clinical and Health-Data Analyst
- Financial Risk and Credit Analyst
- Operations and Supply-Chain Analyst
- Business Intelligence Analyst

**Relevant skills:**

- Probability and statistical distributions
- Hypothesis formulation and p-value interpretation
- Experimental design and power analysis
- Python, SciPy, statsmodels, and SQL
- Data cleaning and transformation
- Data visualization and communicating findings

### Tools and Technologies Used

- Python
- Jupyter Notebook
- NumPy
- Pandas
- SciPy
- Matplotlib
- Git and GitHub
- Cynaris Intelligent Assistant (CIA Search)

### Challenges and Blockers

- The CIA Career tab returned information about an unrelated W8D4 lesson.
- Used CIA Search as an alternative and completed the relevant career research.
- No major issues occurred while running the hypothesis-testing notebook.

### Deliverables

- `hypothesis_tests.ipynb`
- `work_log.md`

Git Status

Branch: feature/week-4-day-4

Commit: Completed

Push: Completed

Pull request: Created and merged into main (PR #30)

# Week 4 Day 5 â€” Data Analysis Capstone

## Learning Objective

Apply the complete data analysis workflow to a real-world dataset, from data cleaning and exploratory analysis to statistical testing, dashboard development, and business recommendations.

## Business Question

How can a retail business improve profitability by identifying its strongest products, regions, and discounting patterns?

## Practical Tasks Completed

### 1. Dataset Selection and Loading

- Selected the Kaggle Sample Superstore dataset.
- Dataset file: `data/raw/archive/Sample - Superstore.csv`
- Loaded the dataset into Pandas using Python.
- Confirmed the dataset contains 9,994 rows and 21 columns.

### 2. Data Inspection and Cleaning

- Inspected dataset columns, data types, and sample records.
- Checked for missing values and duplicate rows.
- Confirmed there were no missing values or duplicate rows in the dataset.
- Converted `Order Date` and `Ship Date` into datetime data types.
- Reviewed numerical columns, including Sales, Profit, Quantity, and Discount.
- Retained negative profit values because they represent valid business losses.

### 3. Exploratory Data Analysis (EDA)

Analyzed sales and profitability across regions, product categories, sub-categories, and time periods.

**Key business metrics**

- Total Sales: $2,297,200.86
- Total Profit: $286,397.02
- Total Orders: 5,009
- Units Sold: 37,873

**Regional analysis**

- West: Sales $725,457.82; Profit $108,418.45
- East: Sales $678,781.24; Profit $91,522.78
- Central: Sales $501,239.89; Profit $39,706.36
- South: Sales $391,721.90; Profit $46,749.43

**Category analysis**

- Technology: Sales $836,154.03; Profit $145,454.95
- Furniture: Sales $741,999.80; Profit $18,451.27
- Office Supplies: Sales $719,047.03; Profit $122,490.80

### 4. Data Visualization

Created visualizations in `capstone_analysis.ipynb` to investigate:

- Monthly sales and profit trends.
- Sales and profit by region.
- Profitability by product sub-category.
- The relationship between discount levels and profit.

Used the visualizations to identify strong-performing regions and categories, as well as areas requiring further profitability analysis.

### 5. Statistical Analysis

- Compared record-level profit for discounted and non-discounted transactions.
- Conducted Welch's t-test to assess whether the average profit differed between the two groups.
- Used the notebook's statistical output to evaluate the evidence of a difference.
- Recognized that an observed association between discounts and profit does not, by itself, establish causation.

### 6. Power BI Dashboard

Created `capstone_dashboard.pbix` using Power BI Desktop.

Dashboard components include:

- Total Sales KPI card.
- Total Profit KPI card.
- Total Orders KPI card using distinct order IDs.
- Monthly Sales Trend line chart.
- Profit by Region bar chart.
- Profit by Product Sub-Category bar chart.
- Region slicer.
- Category slicer.
- Order Date slicer.

Tested the interactive slicers and confirmed that dashboard values changed when selections were applied.

**Power BI Service publication**

- Published `capstone_dashboard.pbix` to Power BI Service.
- Selected My workspace as the publication destination.
- **Power BI Dashboard Link:** https://app.powerbi.com/groups/me/reports/48efef76-5e2c-42e9-b18e-7bc96de41ed5/2d6aaac5ed755a3dccf2?experience=power-bi
- Open the published report in your browser and confirm it loads before recording it as verified.

### 7. Executive Summary and Recommendations

Created `executive_summary.md` to communicate the business question, findings, methodology, and recommendations.

**Recommendation 1 â€” Improve Furniture profitability**

Investigate Furniture sub-categories, pricing, costs, and discount levels to identify products that contribute to weak profits. Test targeted improvements and monitor their effects.

**Recommendation 2 â€” Use regional performance to guide decisions**

Study the West region's product mix and sales practices to identify approaches worth testing elsewhere. Investigate the Central region's comparatively low profit relative to sales.

**Recommendation 3 â€” Review discounting practices**

Evaluate how discount levels relate to profitability. Test discount changes carefully and monitor both sales and profit before making broader decisions.

## Tools and Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- SciPy
- Jupyter Notebook
- Power BI Desktop
- Power BI Service
- Git and GitHub
- Markdown

## Deliverables

- `capstone_analysis.ipynb` â€” data inspection, cleaning, EDA, visualizations, and statistical analysis.
- `capstone_dashboard.pbix` â€” interactive Power BI dashboard.
- `executive_summary.md` â€” business findings and three actionable recommendations.
- `data/raw/archive/Sample - Superstore.csv` â€” source dataset.
- `work_log.md` â€” internship work log.
- Power BI Service report URL â€” paste the actual report URL in the Power BI Dashboard section above.

## CIA Activities

### CIA Research

**Question:** What does a strong data analyst portfolio project look like on GitHub?

**Key insights:**

- Clearly explain the business problem and project objectives.
- Organize the repository so the analysis and deliverables are easy to find.
- Make the analysis reproducible and document the workflow.
- Combine technical analysis with visualizations and business storytelling.
- Include a clear README and relevant documentation.

### CIA Career Search

**Search:** Data Analysis Capstone

**Key insights:**

- Define a clear business question and relevant metrics.
- Demonstrate an end-to-end data analysis workflow.
- Explain findings in a way that supports business decisions.
- Present the notebook, dashboard, and recommendations as a coherent portfolio project.

### CIA Review

**Request:** Review my executive summary and suggest improvements for a business audience.

**Outcome:** The request failed. Recorded as a blocker; no review feedback was received.

## Challenges and Blockers

- The CIA Review request failed, preventing automated feedback on the executive summary.
- The Power BI report was published to Power BI Service, but the report URL still needs to be pasted into this work log and verified in a browser.

## Git Status

- Branch: `main`
- Capstone commit: `1108653`
- Commit message: `feat: complete week-4 data analysis capstone`
- Pull request: #31 â€” merged.
- Follow-up work-log update: Save, commit, and push the updated dashboard link after inserting the actual URL.

## Conclusion

Completed the main capstone analysis, exploratory visualizations, statistical comparison, Power BI dashboard, and executive summary. The analysis identified regional and category-level differences in profitability and produced three recommendations for further business investigation. The CIA Review request remains blocked by a failed request. The published dashboard URL must be added to this work log and checked before the documentation is considered fully updated.

## Week 5 â€” Day 1: PandasAI and Automated EDA

### Learning Objective

Use PandasAI to analyze sales data through natural-language queries and compare AI-generated results with manual Pandas calculations.

### Practical Work

- Loaded `python-pandas/sales_data.csv` containing 10 rows and 6 columns.
- Created `python-pandas/w5d1/pandasai_analysis.py`.
- Executed 10 natural-language queries using PandasAI and Groq.
- Saved results in `query_results.json`.
- Compared three AI answers with manual Pandas calculations in `pandas_comparison.md`.
- Recorded errors encountered during troubleshooting in `errors.log`.

### Key Results

- Total sales: 217,500
- Average sales: 21,750
- Highest-sales order: 1010, with sales of 35,000
- Lowest-sales order: 1008, with sales of 11,000
- Highest-sales region: South, with sales of 91,500
- Highest-sales category: Electronics, with sales of 120,000
- Total quantity sold: 21
- Total orders: 10

### Tools and Technologies

Python, Pandas, PandasAI, Groq API, LiteLLM, JSON, Markdown, PowerShell, Git.

### CIA Activities

**Chat â€” Workflow Review:** Received recommendations on separating data loading, validating data types and missing values, improving business-oriented reporting, and comparing AI results with manual calculations.

**Code â€” Code Review:** Received recommendations on path handling, schema validation, secure API-key management, exception handling, logging, dependency management, modular functions, and automated tests. Further improvements remain pending.

**Search â€” Best Practices:** Reviewed recommendations for data quality checks, reproducibility, numeric tolerance checks, unit testing, and documenting prompts and results.

**Outcome:** All three CIA activities completed successfully. Recommendations are documented; additional code improvements have not yet been implemented.

### Challenges and Blockers

Earlier API errors occurred during setup. The final PandasAI run completed all 10 queries successfully. Earlier errors remain recorded in `errors.log`.

### Deliverables

- `python-pandas/w5d1/pandasai_analysis.py`
- `python-pandas/w5d1/query_results.json`
- `python-pandas/w5d1/pandas_comparison.md`
- `python-pandas/w5d1/errors.log`

### Status

Practical analysis, three manual comparisons, and CIA Chat, Code, and Search activities completed. All W5D1 deliverables and the work log have been committed, pushed, and merged into main.

**Hours Worked:** Enter your actual hours.

**Topics Covered:** Automated exploratory data analysis, SweetViz, AutoViz, feature distributions, class imbalance, and business recommendations.

**What did you work on today?**

- Generated `reports/w5d2/sweetviz_report.html` using a reproducible random sample of 5,000 transactions.
- Created three charts using Pandas and Matplotlib.
- Documented three dataset insights and compared AutoViz and SweetViz for business use.

**Tools / Technologies Used:** Python, Pandas, Matplotlib, SweetViz, AutoViz, Git, VS Code.

**Challenges / Blockers:** AutoViz report generation was too resource-intensive to complete. SweetViz successfully generated an HTML report containing 5,000 sampled transactions, including 6 fraud transactions. Sample findings require validation against the full dataset.

**CIA Review:** CIA reviewed W5D2 PR #34 and confirmed that the SweetViz HTML report, three charts, and documentation satisfy the practical intent of the lesson. The AutoViz limitation due to resource and environment constraints was accepted. PR #34 was successfully merged into `main`. The Cynaris lesson page shows Completed, and the quiz was passed with 100%..

## Week 5 Day 3 — DuckDB Benchmark

- Benchmarked DuckDB, Pandas, and Polars on the same 100,000-row sales CSV using five analytical operations.
- Verified that all three tools produced matching aggregate results.
- Saved benchmark timings in `w5d3_benchmark_results.csv` and the comparison in `w5d3_comparison.md`.
- **CIA review:** Attempted multiple times; CIA returned `Request failed` or generic responses and did not review the actual script.
- **Blocker:** Code review remains pending until CIA is available.

## Week 5 Day 4 - Polars: High-Performance DataFrame Operations

### Practical Tasks Completed

- Benchmarked Pandas, DuckDB, and Polars using the same 100,000-row sales CSV.
- Compared total sales, sales by region, sales by category, quantity by region, and the top five orders.
- Recorded execution times and created a high-level tool comparison.
- Re-ran the benchmark successfully.

### Deliverables

- `benchmark_w5d4.py`
- `reports/w5d4/benchmark_results.csv`
- `reports/w5d4/comparison.csv`
- `reports/w5d4/README.md`

### Tools / Technologies Used

Python, Pandas, DuckDB, Polars, CSV, Git.

### Challenges / Blockers

CIA code-review attempts failed with a request error. CIA interactions remain incomplete; local execution succeeded. Benchmark timings varied between runs and are not definitive performance rankings.

## Week 6 Day 1 - Vanna Setup: NL to SQL on Real Database

### Practical Tasks Completed

- Created `vanna_sql/w6d1_app.py` with a FastAPI endpoint at `POST /cia/sql-analyst`.
- Connected the application to the local `sales.db` SQLite database and configured five question-to-SQL examples.
- Configured the OpenAI-compatible Groq API after Gemini model/service errors.
- Verified the database contains 10 orders and tested natural-language queries for order counts, average quantity, category counts, customer counts, dates, regional quantities and sales, and product sales.
- Cross-checked product net sales against SQLite. Laptop ranked first with net sales of 337500.0.
- Corrected the regional sales example to apply discounts as percentages and treat NULL discounts as zero.

### Deliverables

- `vanna_sql/w6d1_app.py`

### Tools / Technologies Used

Python, Vanna 2.0.2, FastAPI, Uvicorn, SQLite, Groq OpenAI-compatible API, Git, PowerShell.

### Challenges / Blockers

- Gemini requests failed because of model availability and temporary service errors; switched to Groq.
- An earlier total-sales query returned an incorrect negative value due to discount-percentage arithmetic. The product-sales query was verified against SQLite, but generated SQL still needs validation.
- CIA review was unavailable after repeated attempts; the blocker was documented.
- Final generated SQL validation remains incomplete and requires further testing.

## W6D2 — Vanna Custom SQL Patterns

### Work Completed

- Created and verified 5 SQL Q&A examples in `vanna_sql/w6d2_training_examples.json`.
- Ran 10 read-only SQL validation tests; all 10 passed.
- Generated validation evidence: `reports/w6d2/sql_validation_results.csv`.
- Confirmed API health; `sales.db` was available.
- Tested `POST /cia/sql-analyst` with “How many orders are there?” The endpoint returned the correct result: 10 orders.
- Completed 2 CIA interactions:
  1. Asked how to calculate discounted sales by region. CIA initially provided a generic example using a different table and column names.
  2. Clarified the actual `orders` schema. CIA returned a query using `COALESCE(discount, 0)` and grouped results by region.

### Validation and Blockers

- Static SQL validation: 10/10 passed.
- API health check: passed.
- SQL analyst endpoint test: passed for the order-count question.
- CIA interactions: 2 completed successfully.
- Note: The 10 SQL validation tests used predefined SQL queries; they do not represent 10 AI-generated query tests.

## W6D5 — Week 6 Project: Natural-Language SQL

### Practical Tasks Completed

- Set up Vanna and connected the application to the local SQLite database, `sales.db`.
- Used five question-to-SQL training examples documented in `vanna_sql/w6d2_training_examples.json`.
- Tested 10 live natural-language questions through `POST /cia/sql-analyst`.
- Independently verified all 10 API results against SQLite.
- Verified order counts, category counts, total and regional sales, average quantity, top product by quantity, regional order counts, product quantities, top sales representative, and earliest order date.
- Verified the sales calculation uses discounts as percentages and treats NULL discounts as zero.
- Tested read-only SQL protection: a SELECT query succeeded, while the tested DELETE statement was rejected.
- Reviewed the CIA feedback shared during the W6D5 review and incorporated the relevant findings into the evidence README.

### Validation Results

- Live API queries: 10/10 successful responses.
- Independent SQLite verification: 10/10 results matched.
- W6D2 predefined SQL validation: 10/10 passed in a separate test set.
- Read-only SQL check: SELECT succeeded; tested DELETE was blocked.
- These checks cover the tested queries and statements; they are not an exhaustive security audit.

### CIA Review and Evaluation

- CIA feedback received and reviewed; relevant documentation and safety recommendations were incorporated.
- The lesson requires at least two CIA interactions and a Full Stack/Role Mentor code review.
- Portal logging and formal Role Mentor review completion have not been independently confirmed. Do not mark these as completed until the portal confirms them.

### Deliverables

- `reports/w6d5/README.md` — query results, independent verification, read-only safety evidence, and limitations.
- `vanna_sql/w6d1_app.py` — FastAPI endpoint and SQL execution protections.
- `vanna_sql/w6d2_training_examples.json` — five training examples.
- `vanna_sql/validate_w6d2.py` — predefined SQL validation tests.
- PR #42 updated with W6D5 evidence.

### Scope and Limitations

- The verified database contains sales-order data.
- A CRM-specific schema and a completed dashboard were not established by these checks.
- The completed practical evidence demonstrates the tested natural-language SQL API workflow and query verification.

### Tools and Technologies

Python, SQLite, FastAPI, Vanna, Swagger UI, PowerShell, Git, GitHub.

### Git and Pull Request Status

- Branch: `feat/w6d5-3m-vandana`.
- Latest pushed commit: `5d00869` — `docs: add W6D5 read-only SQL safety evidence`.
- Local branch was synchronized with its origin branch at the last verification.
- PR #42 remains open as of the last confirmed status.
- Only `origin` is configured; no `upstream` remote is configured.

### Final Actions

1. Save and verify this work-log update.
2. Commit and push the work-log update to the existing W6D5 branch.
3. Check PR #42 for required reviews and status checks.
4. Merge PR #42 when GitHub confirms it is eligible.
5. Verify the PR shows Merged and record the final merge status.
6. Confirm any required CIA interactions and Role Mentor review in the portal.
## W7D1 - CIA Data Analyst Mode: CSV Upload + PandasAI Queries

### Practical Tasks Completed

- Configured PandasAI with the LiteLLM connector and Groq model using the existing `GROQ_API_KEY` environment variable.
- Loaded `python-pandas/sales_data.csv` for natural-language analysis.
- Created `scripts/w7d1_analysis.py` to run 10 natural-language questions, save results, compare selected answers against manual Pandas calculations, and log query failures.
- Executed all 10 questions successfully.
- Compared total sales, total quantity, and order count against manual Pandas results; all three numeric comparisons matched.
- Saved query results, comparison results, and error-log evidence.

### Validation Results

- Natural-language queries: 10/10 successful.
- Manual Pandas comparisons: 3/3 matched.
- Query failures during the recorded run: 0.
- Error log: `reports/w7d1/pandasai_errors.log` (empty for this successful run).
- `git diff --check`: passed at the last check.

### CIA Review and Evaluation

- CIA interaction 1 completed: discussed general security, error handling, correctness, and Git hygiene.
- CIA interaction 2 completed: discussed numeric validation, AI-failure reporting, API-key protection, logging, and when manual Pandas is preferable.
- These interactions provided general guidance; a line-by-line code review and formal Role Mentor approval have not been confirmed.

### Deliverables

- `scripts/w7d1_analysis.py` — PandasAI analysis script.
- `reports/w7d1/query_results.csv` — results for the 10 questions.
- `reports/w7d1/manual_comparison.csv` — manual Pandas comparison evidence.
- `reports/w7d1/pandasai_errors.log` — error log.
- `reports/w7d1/README.md` — results, limitations, production risks, and viva notes.

### Scope and Limitations

- The dataset contains 10 sales records and has no missing or duplicate rows.
- The dataset's status as verified real Indian business data has not been established; its values should not be presented as verified real-world findings.
- Successful test queries do not guarantee that every AI-generated answer will be correct.
- Manual Pandas remains preferable for deterministic calculations and critical reporting.

### Tools and Technologies

Python, Pandas, PandasAI, LiteLLM, Groq, CSV, PowerShell, Git, GitHub.

### Git and Pull Request Status

- Branch: `feat/w7d1-3m-vandana`.
- Implementation and evidence commits: pending.
- Push and pull request status: pending verification.
- Unrelated local files and environments must remain unstaged.

### Final Actions

1. Verify the work-log entry and staged files.
2. Commit the implementation and W7D1 evidence separately.
3. Verify the remote and push the branch after checking Git status.
4. Confirm the pull request and required reviews in GitHub and the internship portal.
