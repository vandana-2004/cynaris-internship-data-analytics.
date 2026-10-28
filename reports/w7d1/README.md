# W7D1 — CIA Data Analyst Mode: CSV + PandasAI

## Objective
Run natural-language analysis on an existing sales CSV using PandasAI
and compare selected results with deterministic Pandas calculations.

## Dataset
- File: `python-pandas/sales_data.csv`
- Rows: 10
- Columns: `order_id`, `customer`, `region`, `category`, `sales`, `quantity`
- Missing values: 0
- Duplicate rows: 0
- Total sales: 217,500 (currency not specified in the source file)
- Total quantity: 21

This is a small sample dataset. Its Indian-style names and regions do not
establish that it is a verified real-world Indian dataset.

## Implementation
- Script: `scripts/w7d1_analysis.py`
- AI provider: Groq through LiteLLM
- Model: `openai/gpt-oss-120b`
- Results: `reports/w7d1/query_results.csv`
- Manual comparison: `reports/w7d1/manual_comparison.csv`
- Error log: `reports/w7d1/pandasai_errors.log` (created if errors are logged)

## Results
All 10 natural-language queries succeeded in the recorded run:
1. Total sales: 217,500
2. Total quantity: 21
3. Order count: 10
4. Average sales per order: 21,750
5. Sales by region: North 51,000; South 91,500; West 75,000
6. Sales by category: Clothing 38,000; Electronics 120,000; Furniture 59,500
7. Highest-sales category: Electronics
8. Highest-sales order: 1010
9. Highest-sales region: South
10. Electronics sales: 120,000

The three recorded manual-Pandas comparisons passed:
- Total sales: 217,500
- Total quantity: 21
- Order count: 10

## Error handling
Each query is wrapped in exception handling. Failed queries are marked
as failed in the results CSV and written to the error log. The initial
test with an unavailable Groq model was rejected; switching to the
account-listed `openai/gpt-oss-120b` model resolved the test query.

## Limitations and production risks
- Only 10 rows were analyzed; results do not demonstrate large-data performance.
- AI-generated analysis may be incorrect or inconsistent.
- Numeric comparison checks support simple numeric answers; they do not
  prove that every generated grouping or explanation is correct.
- Validate important outputs independently with Pandas or SQL.
- The source CSV does not specify a currency, so the report does not
  assert INR.
- The script requires a valid `GROQ_API_KEY` environment variable and
  network access to the configured provider.

## Viva preparation
**1. How does PandasAI translate natural language into Pandas code?**
It sends the question and dataframe context to a configured language
model, which generates an analysis operation. The result depends on the
model, prompt, available data and execution environment. Errors should
be caught and logged, and outputs should be validated.

**2. What are the risks of AI-generated analysis in production?**
Incorrect calculations, misunderstood questions, privacy exposure,
unsafe generated code, model/provider changes, latency and cost.
Use access controls, validation, logging and human review.

**3. When is manual Pandas preferable?**
For repeatable production pipelines, exact calculations, deterministic
transformations, performance-sensitive tasks and cases needing strict
testing and auditability.

## CIA and Git workflow
- CIA interaction 1: completed; received a general security, error-handling, correctness, and Git-hygiene checklist. This was not a line-by-line review.
- CIA interaction 2: completed; received guidance on numeric validation, AI-failure reporting, API-key protection, logging, and when to prefer manual Pandas.
- Evidence: terminal output and generated CSV reports.
- PR progress note: pending.
