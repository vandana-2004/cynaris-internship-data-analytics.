\# W10D5 — Indian Business Sales Intelligence Dashboard



\## Overview



This project combines exploratory data analysis (EDA), business performance summaries, data-quality checks, and Holt-Winters forecasting in an interactive Streamlit dashboard.



Source dataset: Indian Business Sales, containing 128,975 rows and 24 original columns, covering 31 March 2022 to 29 June 2022.



\## Run the dashboard



From the repository root:



```powershell

.\\.venv-pandasai\\Scripts\\python.exe -m streamlit run .\\w10d5\_dashboard.py

```



\## Dashboard features



\- Business overview KPIs.

\- Date-range, Category, and State filters.

\- Daily and monthly recorded-Amount trends.

\- Category, state, fulfilment, and status summaries.

\- Holt-Winters forecast validation and future estimates.

\- Downloadable CSV and JSON reports.



Forecasting uses the complete historical time series independently of EDA filters. The model uses additive trend and additive weekly seasonality (period 7), with a chronological 14-day holdout.



\## Key findings



| Measure | Result |

|---|---:|

| Source rows | 128,975 |

| Exact duplicate rows | 0 |

| Invalid dates | 0 |

| Daily calendar observations | 91 |

| Rows with valid Amount | 121,180 |

| Rows with missing Amount | 7,795 |

| Amount coverage | 93.96% |

| Total recorded Amount | 78,592,678.30 |

| Average recorded Amount per valid row | 648.56 |

| Total quantity | 116,649 |

| Cancelled-status rows | 18,332 |



\### Missing Amount analysis



\- 7,566 missing Amount values are associated with Cancelled rows.

\- Cancelled rows have a 41.27% missing-Amount rate.

\- Amazon fulfilment has 6,059 missing Amount values.

\- Merchant fulfilment has 1,736 missing Amount values.



These are descriptive associations, not proof of why values are missing.



Missing Amount values are not imputed. They remain included in row counts and are excluded from financial sums and averages. Average recorded Amount is calculated per row with a valid Amount, not per unique order.



\## Forecast validation



| Metric | Result |

|---|---:|

| MAE | 121,237.81 |

| RMSE | 155,727.07 |

| MAPE | 20.11% |

| WAPE | 17.06% |



MAPE uses the 14 non-zero actual validation days. Forecasts are analytical estimates, not guarantees.



The W10D4 forecasting engine is reused. Missing calendar dates are represented as zero in its continuous daily series. This is a modeling assumption, not proof of zero business activity.



\## Evidence files



The `reports/w10d5/` directory contains:



\- `daily\_business\_summary.csv`

\- `monthly\_business\_summary.csv`

\- `category\_performance.csv`

\- `state\_performance.csv`

\- `fulfilment\_summary.csv`

\- `status\_summary.csv`

\- `missing\_amount\_by\_status.csv`

\- `missing\_amount\_by\_fulfilment.csv`

\- `data\_quality.json`

\- `eda\_summary.md`



The dashboard also provides holdout validation and future forecast downloads.



\## Limitations



\- The dataset covers a limited historical period in 2022.

\- Amount is recorded order amount, not verified net revenue.

\- Rows are order-item records, not necessarily unique orders.

\- Status counts describe recorded rows, not confirmed final customer outcomes.

\- Missing Amount values are excluded from financial aggregations and are not imputed.

\- Forecast accuracy on this historical holdout does not guarantee future performance.



\## Validation



Automated checks verified source row counts, duplicates, invalid dates, missing Amount reconciliation, daily and monthly metrics, and evidence-file generation.



Manual dashboard checks covered default filters, combined Category and State filtering, empty-filter handling, and forecast horizon changes.
