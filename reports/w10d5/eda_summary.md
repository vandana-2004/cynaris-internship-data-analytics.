# W10D5 - Indian Business Sales EDA

## Dataset overview
- Source: `data/w8d3/indian_business_sales.csv`
- Rows analyzed: 128,975
- Date range: 2022-03-31 to 2022-06-29
- Daily observations: 91
- Exact duplicate rows: 0

## Recorded amount and quantity
- Total recorded Amount: 78,592,678.30
- Average recorded Amount per row with an amount: 648.56
- Median recorded Amount per row with an amount: 605.00
- Total quantity: 116,649
- Rows with valid Amount: 121,180
- Rows with missing Amount: 7,795
- Amount coverage: 93.96%
- Financial aggregations exclude missing Amount values; record counts retain all rows.
- Average recorded Amount is calculated per row with a valid Amount, not per unique order.

## Category performance
- Highest recorded amount category: Set
- Category recorded amount: 39,204,124.03
- Category order rows: 50,284

## State performance
- Highest recorded amount state: MAHARASHTRA
- State recorded amount: 13,335,534.14
- State order rows: 22,260
- State names were trimmed and normalized to uppercase before grouping.

## Fulfilment and order status
- Largest fulfilment group by recorded amount: Amazon
- Rows with a cancelled status: 18,332
- Cancelled-status row share: 14.21%

## Data quality
- Invalid dates: 0
- Missing state values after normalization: 33
- Duplicate rows: 0

## Business interpretation and limitations
- `Amount` is recorded order amount, not verified net revenue.
- Missing Amount values are excluded from amount totals and averages.
- Status counts describe recorded order rows; they are not a confirmed
  measure of delivered revenue or final customer outcomes.
- The source contains order-item rows. Row counts should not automatically
  be interpreted as unique orders.
- State names are normalized for consistent grouping.
- The dataset covers a limited historical period from 2022. Findings are
  descriptive and should not be treated as current market conditions.
- Forecast performance is reported separately using the W10D4
  chronological holdout results.

## Generated evidence
- `daily_business_summary.csv`
- `monthly_business_summary.csv`
- `category_performance.csv`
- `state_performance.csv`
- `fulfilment_summary.csv`
- `status_summary.csv`
- `missing_amount_by_status.csv`
- `missing_amount_by_fulfilment.csv`
- `data_quality.json`
