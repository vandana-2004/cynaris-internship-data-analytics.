# W10D4 - CIA Mentor Reviews

Date: 12 November 2026

## Interaction 1 - Forecasting Methodology Review

CIA provided a methodology-based review using the implementation details and reported metrics.

### Feedback received
- Holt-Winters additive trend and additive weekly seasonality is an appropriate starting approach, subject to checking the seasonal pattern.
- The chronological 14-day holdout is structurally correct and avoids shuffled time-series validation.
- The 77-day training period provides 11 weekly cycles for model initialization.
- MAE and RMSE suggest some larger errors may be present in the holdout period.
- MAPE requires careful interpretation around zero or near-zero actual values.
- Multiplicative seasonality was suggested as an alternative to investigate if seasonal fluctuations increase with the series level.

### Implementation verification
- The implementation excludes zero actual values from MAPE.
- All 14 holdout observations were included in the saved MAPE calculation.
- The holdout validation and future forecast dates were independently checked.
- No change to the forecasting model was made solely on the basis of this advisory feedback.

### Review limitation
The CIA response ended partway through its WAPE discussion. No missing feedback has been inferred or added.

## Interaction 2 - Dashboard Architecture Review

CIA provided a logical and architectural review framework, not a line-by-line code review.

### Feedback received
- Accurate Recorded Order Amount terminology is important.
- Historical date filtering and forecast horizon controls should work as expected.
- Missing values and short history should be clearly explained.
- Prediction intervals or uncertainty bands were suggested as a possible enhancement.
- Observed and forecast values should be clearly distinguished.

### Implementation verification
- The dashboard labels the target as recorded order amount, not verified net revenue.
- The historical date filter and 7-30 day forecast horizon slider were tested.
- Validation metrics, forecast tables, charts and CSV downloads were tested successfully.
- The dashboard explains missing Amount values and the limitations of the 91-day dataset.

### Review limitation
The CIA did not inspect the uploaded source code line by line. Its feedback was based on the stated requirements and implementation details.

## Overall outcome

Both CIA interactions were completed and documented. The implementation passed the performed functional and data validation checks. Prediction intervals and further seasonality diagnostics remain potential improvements.
