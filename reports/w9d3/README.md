\# W9D3: A/B Test Tracking with MLflow



\## Objective

Compare order amounts between Amazon and Merchant fulfilment groups using statistical testing and MLflow tracking.



\## Dataset

\- Source: `data/w8d3/indian\_business\_sales.csv`

\- Original dataset: 128,975 rows and 24 columns.

\- Columns used: Order ID, Fulfilment, Amount, Qty, Status.



\## Data preparation

\- Filtered shipped-status records.

\- Selected Amazon and Merchant fulfilment.

\- Excluded invalid amounts and quantities.

\- Aggregated line amounts by Order ID.

\- Used unique orders as independent observations.



\## Sample sizes

\- Amazon: 71,193 orders

\- Merchant: 28,714 orders

\- Total: 99,907 orders



\## Statistical method

\- Welch's independent two-sample t-test

\- Significance level: 0.05

\- 95% confidence interval

\- Cohen's d effect size



\## Results



| Metric | Result |

|---|---:|

| Amazon average order amount | INR 706.87 |

| Merchant average order amount | INR 721.83 |

| Difference | INR 14.96 |

| Percentage difference | 2.12% |

| T-statistic | 5.9126 |

| P-value | 3.3876344e-09 |

| 95% confidence interval | INR 10.00 to INR 19.92 |

| Cohen's d | 0.0419 |



The difference is statistically significant, but the effect size is small.



\## MLflow

\- Experiment: `W9D3 - Indian Business A/B Testing`

\- Run: `order-level-amazon-vs-merchant`

\- Run ID: `f58016f8861242718a327c8b61eddc48`

\- Tracking database: `mlflow.db`



Artifacts:

\- `ab\_test\_report.md`

\- `group\_summary.csv`



\## Run command



```powershell

\& .\\.venv-pandasai\\Scripts\\python.exe .\\reports\\w9d3\\ab\_test\_tracking.py

```



\## Limitations

This is an observational comparison, not a randomized experiment. It does not establish causation. Product mix, customer characteristics, and other factors may influence order amounts. Order-level aggregation avoids treating multiple lines from one order as independent observations, but does not eliminate all confounding.

