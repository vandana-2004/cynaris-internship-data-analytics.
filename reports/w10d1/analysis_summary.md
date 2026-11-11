# W10D1 - Time Series Analysis

## Dataset and cleaning

- Source: Indian Business Sales Dataset
- Original daily observations: 91
- Retained daily observations: 91
- Date range: 2022-03-31 to 2022-06-29
- Excluded dates: None
- Missing calendar dates: 0
- Included order statuses: All statuses
- Average daily recorded amount: INR 863,655.81
- Median daily recorded amount: INR 882,059.17
- Minimum daily amount: INR 101,683.85
- Maximum daily amount: INR 1,209,364.17

The analysis includes all records with valid dates and non-null
Amount values, regardless of order status.

All available dates are retained. No dates were excluded based
only on low transaction counts.

The daily transaction count represents records with a valid
recorded Amount. Amount represents recorded order value, not
verified net revenue.

Pending, cancelled, shipped, returned, and other statuses may
have different business meanings. Their recorded Amount values
should not be interpreted as completed sales or realized revenue.

## Trend

- First 7-day average: INR 801,659.41
- Latest 7-day rolling average: INR 658,666.33
- Latest 14-day rolling average: INR 710,615.76
- Change between first and latest 7-day averages: -17.84%
- Descriptive trend direction: Downward

Trend direction is based on a comparison of the first and latest
7-day averages. The 5% threshold is a descriptive heuristic.
It does not establish causation.

## Weekly pattern

- Highest average day: Sunday
- Lowest average day: Thursday

The weekday comparison is descriptive. Approximately three months
of data do not establish a stable recurring seasonal effect.

## Stationarity

- ADF statistic: -5.7151
- ADF p-value: 0.000001
- Significance level: 5%
- Result: Reject the unit-root null at 5%; evidence against a unit root in this series.

The ADF result is evidence from a unit-root test, not proof that
the series has no trend or seasonality.

## Model evaluation

- Training observations: 77
- Holdout observations: 14
- Holdout period: 2022-06-16 to 2022-06-29
- Split method: Chronological; final 14 observations held out

| Model | MAE (INR) | RMSE (INR) |
|---|---:|---:|
| Naive | 77,242.30 | 122,634.73 |
| Seasonal naive (7-day) | 166,387.24 | 189,914.24 |
| ARIMA(1, 1, 1) | 71,656.24 | 118,706.45 |

- Best model by MAE: ARIMA(1, 1, 1)
- Best model by RMSE: ARIMA(1, 1, 1)

Naive and seasonal-naive baselines provide reference performance.
ARIMA(1, 1, 1) is included as the required forecasting technique.

The best-performing model on this particular holdout is not
necessarily the best model on other periods.

The ARIMA model is non-seasonal and does not explicitly model
a seven-day seasonal component.

## Forecast

- Model: ARIMA(1, 1, 1), fitted on all retained observations
- Forecast horizon: 14 days
- Forecast start: 2022-06-30
- Forecast end: 2022-07-13
- Mean forecast amount: INR 398,121.53
- Interval: 95% model-based prediction interval

Negative lower interval bounds are clipped at zero because
recorded order amounts cannot be negative.

The forecast is experimental and assumes historical patterns
remain informative beyond the observed period.

## Limitations

- The dataset covers approximately three months only.
- Annual seasonality cannot be established from this time span.
- Weekday averages are descriptive.
- Different order statuses may have different business meanings.
- Recorded Amount is not verified net revenue.
- Including all statuses does not establish completed sales.
- ARIMA(1,1,1) is a baseline specification, not a tuned optimum.
- The holdout period is short; model rankings may change on other periods.
- The final forecast is model-based, not a guaranteed business outcome.
