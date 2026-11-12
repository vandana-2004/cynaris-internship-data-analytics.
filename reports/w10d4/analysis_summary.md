# W10D4 — Forecasting Analysis

## Dataset
- Source: `data/w8d3/indian_business_sales.csv`
- Rows: 128,975
- Daily observations: 91
- Date range: 2022-03-31 to 2022-06-29
- Missing Amount values: 7,795
- Invalid dates: 0

## Forecasting approach
- Target: daily sum of available `Amount` values.
- Model: Holt-Winters additive trend and additive weekly seasonality.
- Seasonal period: 7 days.
- Validation: final 14 days held out from training.
- Future forecast: 14 days, fitted again using all available observations.

## Holdout metrics
- MAE: 121,237.81
- RMSE: 155,727.07
- MAPE: 20.11%
- WAPE: 17.06%

MAPE excludes zero-valued actual observations. WAPE uses total absolute
actual amount as its denominator.

## Interpretation and limitations
`Amount` is treated as recorded order amount, not verified net revenue.
Missing Amount values are excluded from daily sums. Calendar dates without
a recorded non-missing amount are represented as zero. The dataset covers
only 91 days, so this short-history forecast should be treated as an
analytical estimate, not a guarantee of future results.
