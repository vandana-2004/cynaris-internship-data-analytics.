from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
REPORT_DIR = ROOT / "reports" / "w10d4"
HOLDOUT_DAYS = 14


def load_daily_series(data_path=DATA_PATH):
    """Load daily recorded order amounts from the Indian business dataset."""
    frame = pd.read_csv(data_path, usecols=["Date", "Amount"])

    dates = pd.to_datetime(
        frame["Date"], format="%m-%d-%y", errors="coerce"
    )
    invalid_dates = int(dates.isna().sum())
    if invalid_dates:
        raise ValueError(f"{invalid_dates} dates could not be parsed.")

    amounts = pd.to_numeric(frame["Amount"], errors="coerce")
    missing_amounts = int(amounts.isna().sum())

    valid = pd.DataFrame({"date": dates, "amount": amounts}).dropna(
        subset=["amount"]
    )

    daily = valid.groupby("date")["amount"].sum().sort_index()
    calendar = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(calendar, fill_value=0.0)
    daily.index.name = "date"
    daily.name = "recorded_order_amount"

    diagnostics = {
        "source_rows": int(len(frame)),
        "invalid_dates": invalid_dates,
        "missing_amounts": missing_amounts,
        "daily_observations": int(len(daily)),
        "start_date": str(daily.index.min().date()),
        "end_date": str(daily.index.max().date()),
        "zero_amount_days": int((daily == 0).sum()),
    }
    return daily.astype(float), diagnostics


def fit_hw(series, steps):
    """Fit additive-trend, additive-weekly-seasonality Holt-Winters model."""
    model = ExponentialSmoothing(
        series.astype(float),
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="estimated",
    )
    fitted = model.fit(optimized=True)
    forecast = fitted.forecast(steps)
    return forecast.clip(lower=0)


def calculate_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    errors = actual - predicted

    nonzero = actual != 0
    mape = (
        float(np.mean(np.abs(errors[nonzero] / actual[nonzero])) * 100)
        if nonzero.any()
        else None
    )
    denominator = float(np.sum(np.abs(actual)))
    wape = (
        float(np.sum(np.abs(errors)) / denominator * 100)
        if denominator
        else None
    )

    return {
        "mae": float(mean_absolute_error(actual, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "mape_percent": mape,
        "wape_percent": wape,
        "mape_observations": int(nonzero.sum()),
        "validation_observations": int(len(actual)),
    }


def run_analysis(data_path=DATA_PATH, output_dir=REPORT_DIR, horizon=14):
    daily, diagnostics = load_daily_series(data_path)

    if len(daily) <= HOLDOUT_DAYS + 14:
        raise ValueError("Not enough daily observations for weekly forecasting.")

    train = daily.iloc[:-HOLDOUT_DAYS]
    actual = daily.iloc[-HOLDOUT_DAYS:]

    validation_values = fit_hw(train, HOLDOUT_DAYS)
    validation = pd.DataFrame({
        "actual_amount": actual.to_numpy(),
        "forecast_amount": validation_values.to_numpy(),
    }, index=actual.index)
    validation.index.name = "date"

    metrics = calculate_metrics(
        validation["actual_amount"],
        validation["forecast_amount"],
    )

    future_values = fit_hw(daily, horizon)
    future_index = pd.date_range(
        daily.index[-1] + pd.Timedelta(days=1),
        periods=horizon,
        freq="D",
    )
    future = pd.DataFrame({
        "forecast_amount": future_values.to_numpy(),
    }, index=future_index)
    future.index.name = "date"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    daily.rename("recorded_order_amount").to_csv(
        output_dir / "daily_recorded_amount.csv",
        index_label="date",
    )
    validation.to_csv(output_dir / "validation_forecast.csv")
    future.to_csv(output_dir / "future_forecast.csv")

    results = {
        "model": "Holt-Winters additive trend + additive weekly seasonality",
        "seasonal_periods": 7,
        "holdout_days": HOLDOUT_DAYS,
        "future_horizon_days": horizon,
        "target": "Daily sum of non-missing Amount values (recorded order amount)",
        "metrics": metrics,
        "data_quality": diagnostics,
    }
    (output_dir / "forecast_metrics.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    def display_metric(value):
        return "N/A" if value is None else f"{value:,.2f}"

    summary = f"""# W10D4 — Forecasting Analysis

## Dataset
- Source: `data/w8d3/indian_business_sales.csv`
- Rows: {diagnostics['source_rows']:,}
- Daily observations: {diagnostics['daily_observations']}
- Date range: {diagnostics['start_date']} to {diagnostics['end_date']}
- Missing Amount values: {diagnostics['missing_amounts']:,}
- Invalid dates: {diagnostics['invalid_dates']}

## Forecasting approach
- Target: daily sum of available `Amount` values.
- Model: Holt-Winters additive trend and additive weekly seasonality.
- Seasonal period: 7 days.
- Validation: final {HOLDOUT_DAYS} days held out from training.
- Future forecast: {horizon} days, fitted again using all available observations.

## Holdout metrics
- MAE: {display_metric(metrics['mae'])}
- RMSE: {display_metric(metrics['rmse'])}
- MAPE: {display_metric(metrics['mape_percent'])}%
- WAPE: {display_metric(metrics['wape_percent'])}%

MAPE excludes zero-valued actual observations. WAPE uses total absolute
actual amount as its denominator.

## Interpretation and limitations
`Amount` is treated as recorded order amount, not verified net revenue.
Missing Amount values are excluded from daily sums. Calendar dates without
a recorded non-missing amount are represented as zero. The dataset covers
only 91 days, so this short-history forecast should be treated as an
analytical estimate, not a guarantee of future results.
"""
    (output_dir / "analysis_summary.md").write_text(
        summary, encoding="utf-8"
    )

    return {
        "daily": daily,
        "validation": validation,
        "future": future,
        "metrics": metrics,
        "diagnostics": diagnostics,
        "results": results,
    }


if __name__ == "__main__":
    result = run_analysis()
    print("W10D4 forecasting analysis completed.")
    print("Metrics:", json.dumps(result["metrics"], indent=2))
    print("Reports:", REPORT_DIR)
