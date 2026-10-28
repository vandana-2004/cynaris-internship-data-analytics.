# W7D1 — CIA Data Analyst Mode: CSV + PandasAI

## Objective

Perform natural-language analysis on an Indian e-commerce sales sample using PandasAI and compare selected AI-generated results against deterministic Pandas calculations.

## Dataset

- **File:** `python-pandas/amazon_india_sales_sample.csv`
- **Sample size:** 1,000 rows selected from a public Amazon Sale Report dataset.
- **Source dataset size:** 128,975 rows.
- **Sampling:** Random sample using `random_state=42`.
- **Selected columns:** `Order ID`, `Date`, `Status`, `Fulfilment`, `Category`, `Qty`, `currency`, `Amount`, `ship-state`, `ship-country`, `B2B`.
- **Currency filter:** Retained records where `currency` is `INR`.
- **Cleaning:** Excluded cancelled orders, converted `Amount` and `Qty` to numeric values, and removed records missing either value.
- **Original sample:** `python-pandas/sales_data.csv` was preserved unchanged.

The sample is derived from a publicly available third-party dataset. It should not be interpreted as verified internal Amazon company data. The analysis represents only the sampled records that remain after cleaning, not all Amazon sales.

## Implementation

- **Script:** `scripts/w7d1_analysis.py`
- **AI provider:** Groq through LiteLLM.
- **Model:** `groq/openai/gpt-oss-120b`.
- **Input:** `python-pandas/amazon_india_sales_sample.csv`.
- **Query results:** `reports/w7d1/query_results.csv`.
- **Manual comparison:** `reports/w7d1/manual_comparison.csv`.
- **Error log:** `reports/w7d1/pandasai_errors.log`.

The script loads and cleans the sample, submits ten natural-language questions to PandasAI, records query outcomes, and compares three numeric results with independent Pandas calculations. Existing successful query results are preserved when failed queries are retried.

## Results

All 10 natural-language queries succeeded in the final recorded run.

1. Total sales amount: `557229.0`
2. Total quantity: `871`
3. Unique order IDs: `869`
4. Average amount per row: approximately `641.23`
5. Sales by shipping state.
6. Sales by product category.
7. Category with the highest total amount: `Set`, reported as `286345.00`.
8. Order with the highest amount: `407-9758387-6970707`.
9. Shipping state with the highest total amount: `MAHARASHTRA`, reported as `98320.0`.
10. Total amount for category `kurta`: `149367.0`.

The results describe the cleaned sample only. The grouping and ranking outputs are AI-generated and should be checked independently before being used for business decisions.

## Manual Validation

Three AI-generated numeric results were compared with independent Pandas calculations:

| Metric             | Manual Pandas result | Validation |
| ------------------ | -------------------: | ---------- |
| Total sales amount |             557229.0 | Passed     |
| Total quantity     |                871.0 | Passed     |
| Unique order IDs   |                  869 | Passed     |

**Validation outcome:** 3 of 3 comparisons passed.

The numeric comparison checks do not independently verify every grouping, ranking, or natural-language explanation.

## Error Handling and Limitations

- Each AI query is wrapped in exception handling.
- Failed queries are recorded in the results CSV and logged.
- The final recorded run contains 10 successful queries.
- Groq rate limiting affected three queries during the initial run. Only those failed queries were retried; the seven successful results were preserved.
- LiteLLM displayed an SSL warning while attempting to retrieve its remote model cost map. It fell back to its local copy, and the analysis completed.
- PandasAI displayed a deprecation warning for the `Agent` configuration parameter. This did not prevent the run from succeeding.
- The analysis uses a 1,000-row sample rather than the full source dataset.
- AI-generated results may be incorrect or inconsistent and should be independently validated.
- The script requires a valid `GROQ_API_KEY` environment variable and network access to the configured provider.

## Viva Preparation

**1. How does PandasAI translate natural language into Pandas analysis?**

PandasAI uses a configured language model to interpret a question and generate an analysis operation based on the supplied dataframe. Results depend on the model, question, available data, and execution environment.

**2. What are the risks of AI-generated analysis in production?**

Potential risks include incorrect calculations, misunderstood questions, privacy exposure, unsafe generated code, provider changes, latency, and cost. Validation, access controls, logging, and human review help manage these risks.

**3. When is manual Pandas preferable?**

Manual Pandas is preferable for deterministic calculations, repeatable data pipelines, strict testing, performance-sensitive operations, and work requiring auditability.

## CIA and Git Workflow

- CIA interactions: Two general review and guidance interactions were previously recorded.
- Review topics included correctness, error handling, numeric validation, API-key protection, logging, and Git hygiene.
- Evidence: Terminal output and generated CSV reports.
- Role Mentor review and final PR status: To be verified.
- Portal completion status: To be verified.
