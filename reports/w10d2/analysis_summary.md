# W10D2 - Prophet Forecasting

## Dataset
- Source: Indian Business Sales Dataset, aggregated in W10D1
- Observations: 91
- Date range: 2022-03-31 to 2022-06-29
- Target: Daily recorded order amount (INR)
- Training observations: 77
- Holdout observations: 14
- Holdout period: 2022-06-16 to 2022-06-29

## Prophet configuration
- Prophet version: 1.5.0
- Weekly seasonality: Enabled
- Daily seasonality: Disabled
- Yearly seasonality: Disabled due to the short observation period
- Uncertainty samples: 300
- Holdout: Final 14 observations, chronological split

## Model comparison

                       Model     MAE (INR)   RMSE (INR)
                       Naive  77242.300000 122634.73000
      Seasonal naive (7-day) 166387.240000 189914.24000
              ARIMA(1, 1, 1)  71656.240000 118706.45000
Prophet (weekly seasonality) 122636.499199 157308.05191

- Best model by holdout MAE: ARIMA(1, 1, 1)
- Best holdout MAE: INR 71,656.24

## Final forecast
- Model: Prophet fitted on all 91 observations
- Forecast horizon: 14 days
- Forecast period: 2022-06-30 to 2022-07-13
- Mean predicted daily amount: INR 736,636.79

## Interpretation and limitations
- Amount represents recorded order value, not verified net revenue.
- All order statuses are included in the source aggregation.
- The dataset covers approximately three months only.
- Annual seasonality is not established by this dataset.
- The holdout comparison measures performance on one 14-day period.
- Prediction intervals represent model uncertainty, not guaranteed ranges.
- Forecasts are experimental and are not guaranteed business outcomes.

## Additional validation considerations

- ARIMA achieved lower MAE and RMSE than Prophet on this single 14-day holdout. This does not establish universal business-model superiority.
- Only 91 observations are available, so longer-term seasonal components cannot be reliably established.
- The prediction intervals should be interpreted cautiously; they are model-based uncertainty estimates, not guaranteed ranges.
- Indian holidays were not explicitly modelled.
- Prophet's default changepoint settings were retained; changepoint tuning is future work.
- ARIMA residual diagnostics, including a Ljung-Box test, and further Prophet residual analysis were not performed.
- Future work could evaluate additional chronological holdout windows, holiday effects and residual diagnostics before making a production model recommendation.

## CIA mentor review

- Interaction 1 reviewed chronological splitting, missing dates, scaling, seasonality, changepoints and holiday effects. The mentor supplied an evaluation framework, not a line-by-line code review.
- Interaction 2 reviewed business interpretation, short-series limitations, residual diagnostics and holiday effects. It cautioned against treating one holdout comparison as proof of universal model superiority.
- Both interactions were completed. No formal overall PASS/FAIL verdict was supplied.

## Evidence
- `holdout_predictions.csv`
- `model_comparison.csv`
- `forecast.csv`
- `prophet_holdout.png`
- `prophet_forecast.png`
