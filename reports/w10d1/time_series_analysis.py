
"""
W10D1 - Time Series Analysis: Trends, Seasonality and ARIMA
Project: Indian Business Sales Dataset

Primary series:
All order statuses with a valid Date and non-null Amount.
Amount represents recorded order value, not verified net revenue.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_DIR = ROOT / "reports" / "w10d1"

FORECAST_DAYS = 14
TEST_DAYS = 14
ARIMA_ORDER = (1, 1, 1)
SIGNIFICANCE_LEVEL = 0.05


def load_daily_sales():
    """Load all valid recorded order amounts and aggregate by calendar day."""

    df = pd.read_csv(DATA_PATH, low_memory=False)

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%m-%d-%y",
        errors="coerce",
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce",
    )

    # Include all order statuses.
    # Keep records with valid dates and recorded Amount values.
    # Amount is not verified net revenue.
    df = df[
        df["Date"].notna()
        & df["Amount"].notna()
    ].copy()

    daily = (
        df.groupby("Date")
        .agg(
            recorded_amount_inr=("Amount", "sum"),
            transaction_count=("Amount", "count"),
        )
        .sort_index()
        .asfreq("D")
    )

    if daily.isna().any().any():
        raise ValueError(
            "Missing calendar dates or values detected in the daily series."
        )

    if len(daily) <= TEST_DAYS + 10:
        raise ValueError(
            "Insufficient observations for model evaluation."
        )

    return daily


def calculate_metrics(actual, predicted):
    """Calculate MAE and RMSE."""

    errors = actual.to_numpy() - np.asarray(predicted)

    return {
        "MAE (INR)": float(np.mean(np.abs(errors))),
        "RMSE (INR)": float(np.sqrt(np.mean(errors ** 2))),
    }


def evaluate_models(series):
    """Evaluate forecasting models using a chronological holdout."""

    train = series.iloc[:-TEST_DAYS]
    test = series.iloc[-TEST_DAYS:]

    # Naive baseline: repeat the last training observation.
    naive_predictions = np.repeat(
        train.iloc[-1],
        len(test),
    )

    # Seasonal naive baseline: repeat the previous seven-day pattern.
    last_week = train.iloc[-7:].to_numpy()

    seasonal_predictions = np.tile(
        last_week,
        int(np.ceil(len(test) / 7)),
    )[:len(test)]

    # ARIMA model fitted only on training observations.
    fitted = ARIMA(
        train,
        order=ARIMA_ORDER,
    ).fit()

    arima_predictions = fitted.forecast(
        steps=len(test)
    )

    arima_predictions.index = test.index

    predictions = pd.DataFrame(
        {
            "actual": test,
            "naive": naive_predictions,
            "seasonal_naive": seasonal_predictions,
            "arima": arima_predictions.to_numpy(),
        },
        index=test.index,
    )

    predictions.index.name = "date"

    results = []

    for model_name, prediction in [
        ("Naive", naive_predictions),
        ("Seasonal naive (7-day)", seasonal_predictions),
        (f"ARIMA{ARIMA_ORDER}", arima_predictions.to_numpy()),
    ]:
        results.append(
            {
                "Model": model_name,
                **calculate_metrics(test, prediction),
            }
        )

    comparison = pd.DataFrame(results)

    return train, test, predictions, comparison


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Loading Indian Business Dataset...")

    daily_data = load_daily_sales()

    # Main target series: all-status recorded daily amount.
    daily = daily_data["recorded_amount_inr"]

    daily_data.to_csv(
        OUTPUT_DIR / "daily_sales.csv",
        index_label="date",
    )

    # ---------------------------------------------------------
    # 1. Trend and rolling averages
    # ---------------------------------------------------------

    rolling_7 = daily.rolling(7).mean()
    rolling_14 = daily.rolling(14).mean()

    first_7_day_average = float(
        daily.iloc[:7].mean()
    )

    latest_7_day_average = float(
        rolling_7.iloc[-1]
    )

    trend_change_pct = (
        (latest_7_day_average - first_7_day_average)
        / first_7_day_average
        * 100
    )

    if trend_change_pct > 5:
        trend_direction = "Upward"
    elif trend_change_pct < -5:
        trend_direction = "Downward"
    else:
        trend_direction = "Relatively flat"

    plt.figure(figsize=(12, 6))

    plt.plot(
        daily.index,
        daily.values,
        label="Daily recorded amount",
        alpha=0.7,
    )

    plt.plot(
        rolling_7.index,
        rolling_7,
        label="7-day rolling average",
    )

    plt.plot(
        rolling_14.index,
        rolling_14,
        label="14-day rolling average",
    )

    plt.title("Daily Recorded Order Amount Trend")
    plt.xlabel("Date")
    plt.ylabel("Recorded amount (INR)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "time_series_trend.png",
        dpi=120,
    )

    plt.close()

    # ---------------------------------------------------------
    # 2. Descriptive weekly pattern
    # ---------------------------------------------------------

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    weekly = (
        daily.groupby(daily.index.day_name())
        .agg(
            average_amount="mean",
            total_amount="sum",
            observations="count",
        )
        .reindex(weekday_order)
    )

    weekly.to_csv(
        OUTPUT_DIR / "weekly_seasonality.csv"
    )

    plt.figure(figsize=(10, 5))

    plt.bar(
        weekly.index,
        weekly["average_amount"],
    )

    plt.title("Average Recorded Amount by Day of Week")
    plt.xlabel("Day of week")
    plt.ylabel("Average amount (INR)")
    plt.xticks(rotation=30)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "weekly_seasonality.png",
        dpi=120,
    )

    plt.close()

    # ---------------------------------------------------------
    # 3. Augmented Dickey-Fuller stationarity test
    # ---------------------------------------------------------

    adf_result = adfuller(
        daily,
        autolag="AIC",
        result_object=True,
    )

    adf_stat = float(adf_result.statistic)
    adf_pvalue = float(adf_result.pvalue)

    if adf_pvalue < SIGNIFICANCE_LEVEL:
        adf_interpretation = (
            "Reject the unit-root null at 5%; "
            "evidence against a unit root in this series."
        )
    else:
        adf_interpretation = (
            "Do not reject the unit-root null at 5%; "
            "insufficient evidence against a unit root."
        )

    # ---------------------------------------------------------
    # 4. Chronological model evaluation
    # ---------------------------------------------------------

    train, test, predictions, comparison = evaluate_models(
        daily
    )

    comparison["MAE (INR)"] = (
        comparison["MAE (INR)"].round(2)
    )

    comparison["RMSE (INR)"] = (
        comparison["RMSE (INR)"].round(2)
    )

    comparison.to_csv(
        OUTPUT_DIR / "model_comparison.csv",
        index=False,
    )

    predictions.to_csv(
        OUTPUT_DIR / "holdout_predictions.csv",
        index_label="date",
    )

    best_mae_model = comparison.loc[
        comparison["MAE (INR)"].idxmin(),
        "Model",
    ]

    best_rmse_model = comparison.loc[
        comparison["RMSE (INR)"].idxmin(),
        "Model",
    ]

    # ---------------------------------------------------------
    # 5. Holdout prediction visualization
    # ---------------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.plot(
        test.index,
        predictions["actual"],
        label="Actual",
        marker="o",
    )

    plt.plot(
        test.index,
        predictions["naive"],
        label="Naive",
        marker=".",
    )

    plt.plot(
        test.index,
        predictions["seasonal_naive"],
        label="Seasonal naive",
        marker=".",
    )

    plt.plot(
        test.index,
        predictions["arima"],
        label="ARIMA",
        marker="o",
    )

    plt.title("14-Day Holdout: Actual vs Model Predictions")
    plt.xlabel("Date")
    plt.ylabel("Recorded amount (INR)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "arima_evaluation.png",
        dpi=120,
    )

    plt.close()

    # ---------------------------------------------------------
    # 6. Final ARIMA model and 14-day forecast
    # ---------------------------------------------------------

    final_model = ARIMA(
        daily,
        order=ARIMA_ORDER,
    ).fit()

    forecast_result = final_model.get_forecast(
        steps=FORECAST_DAYS
    )

    prediction_interval = forecast_result.conf_int(
        alpha=0.05
    )

    forecast = pd.DataFrame(
        {
            "forecast_amount_inr": (
                forecast_result.predicted_mean
            ),
            "lower_95": (
                prediction_interval.iloc[:, 0]
            ),
            "upper_95": (
                prediction_interval.iloc[:, 1]
            ),
        }
    )

    # Recorded amounts cannot be negative.
    # Clip interval bounds while ensuring the forecast mean
    # remains inside the displayed interval.
    forecast["lower_95"] = np.minimum(
        forecast["lower_95"].clip(lower=0),
        forecast["forecast_amount_inr"].clip(lower=0),
    )

    forecast["upper_95"] = np.maximum(
        forecast["upper_95"].clip(lower=0),
        forecast["forecast_amount_inr"].clip(lower=0),
    )

    forecast.index.name = "date"

    forecast.to_csv(
        OUTPUT_DIR / "forecast.csv"
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        daily.index,
        daily.values,
        label="Historical recorded amount",
    )

    plt.plot(
        forecast.index,
        forecast["forecast_amount_inr"],
        label="ARIMA 14-day forecast",
        marker="o",
    )

    plt.fill_between(
        forecast.index,
        forecast["lower_95"],
        forecast["upper_95"],
        alpha=0.2,
        label="95% prediction interval",
    )

    plt.title("ARIMA 14-Day Recorded Amount Forecast")
    plt.xlabel("Date")
    plt.ylabel("Recorded amount (INR)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "arima_forecast.png",
        dpi=120,
    )

    plt.close()

    # ---------------------------------------------------------
    # 7. Summary report
    # ---------------------------------------------------------

    summary = f"""# W10D1 - Time Series Analysis

## Dataset and cleaning

- Source: Indian Business Sales Dataset
- Original daily observations: {len(daily)}
- Retained daily observations: {len(daily)}
- Date range: {daily.index.min().date()} to {daily.index.max().date()}
- Excluded dates: None
- Missing calendar dates: {int(daily.isna().sum())}
- Included order statuses: All statuses
- Average daily recorded amount: INR {daily.mean():,.2f}
- Median daily recorded amount: INR {daily.median():,.2f}
- Minimum daily amount: INR {daily.min():,.2f}
- Maximum daily amount: INR {daily.max():,.2f}

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

- First 7-day average: INR {first_7_day_average:,.2f}
- Latest 7-day rolling average: INR {latest_7_day_average:,.2f}
- Latest 14-day rolling average: INR {rolling_14.iloc[-1]:,.2f}
- Change between first and latest 7-day averages: {trend_change_pct:.2f}%
- Descriptive trend direction: {trend_direction}

Trend direction is based on a comparison of the first and latest
7-day averages. The 5% threshold is a descriptive heuristic.
It does not establish causation.

## Weekly pattern

- Highest average day: {weekly["average_amount"].idxmax()}
- Lowest average day: {weekly["average_amount"].idxmin()}

The weekday comparison is descriptive. Approximately three months
of data do not establish a stable recurring seasonal effect.

## Stationarity

- ADF statistic: {adf_stat:.4f}
- ADF p-value: {adf_pvalue:.6f}
- Significance level: 5%
- Result: {adf_interpretation}

The ADF result is evidence from a unit-root test, not proof that
the series has no trend or seasonality.

## Model evaluation

- Training observations: {len(train)}
- Holdout observations: {len(test)}
- Holdout period: {test.index.min().date()} to {test.index.max().date()}
- Split method: Chronological; final {TEST_DAYS} observations held out

| Model | MAE (INR) | RMSE (INR) |
|---|---:|---:|
{chr(10).join(f"| {row['Model']} | {row['MAE (INR)']:,.2f} | {row['RMSE (INR)']:,.2f} |" for _, row in comparison.iterrows())}

- Best model by MAE: {best_mae_model}
- Best model by RMSE: {best_rmse_model}

Naive and seasonal-naive baselines provide reference performance.
ARIMA{ARIMA_ORDER} is included as the required forecasting technique.

The best-performing model on this particular holdout is not
necessarily the best model on other periods.

The ARIMA model is non-seasonal and does not explicitly model
a seven-day seasonal component.

## Forecast

- Model: ARIMA{ARIMA_ORDER}, fitted on all retained observations
- Forecast horizon: {FORECAST_DAYS} days
- Forecast start: {forecast.index.min().date()}
- Forecast end: {forecast.index.max().date()}
- Mean forecast amount: INR {forecast["forecast_amount_inr"].mean():,.2f}
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
"""

    (OUTPUT_DIR / "analysis_summary.md").write_text(
        summary,
        encoding="utf-8",
    )

    # ---------------------------------------------------------
    # 8. Console results
    # ---------------------------------------------------------

    print("\n===== W10D1 RESULTS =====")
    print(summary)

    print("\n===== MODEL COMPARISON =====")
    print(comparison.to_string(index=False))

    print("\n===== FORECAST CHECK =====")
    print(forecast.round(2).to_string())

    print("\n===== GENERATED FILES =====")

    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(
                f"{file.name}: {file.stat().st_size:,} bytes"
            )

    print("\nW10D1 analysis completed successfully.")


if __name__ == "__main__":
    main()
