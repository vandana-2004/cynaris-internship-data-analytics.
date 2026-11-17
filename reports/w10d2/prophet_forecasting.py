"""W10D2 - Prophet Forecasting on Indian Business Sales Data."""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from prophet import Prophet


ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "reports" / "w10d1"
OUTPUT_DIR = ROOT / "reports" / "w10d2"

TEST_DAYS = 14
FORECAST_DAYS = 14


def calculate_metrics(actual, predicted):
    errors = np.asarray(actual) - np.asarray(predicted)
    return {
        "MAE (INR)": float(np.mean(np.abs(errors))),
        "RMSE (INR)": float(np.sqrt(np.mean(errors ** 2))),
    }


def markdown_table(df):
    columns = list(df.columns)
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in df.itertuples(index=False, name=None)
    ]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    return "\\n".join([header, separator, *rows])


def load_daily_sales():
    path = INPUT_DIR / "daily_sales.csv"
    daily = pd.read_csv(path, parse_dates=["date"])

    required = {"date", "recorded_amount_inr"}
    if not required.issubset(daily.columns):
        raise ValueError(f"Missing required columns: {required}")

    if daily.empty or daily.isna().any().any():
        raise ValueError("Daily sales data is empty or contains missing values.")

    if daily["date"].duplicated().any():
        raise ValueError("Duplicate dates found.")

    daily = daily.sort_values("date").reset_index(drop=True)

    if len(daily) != 91:
        raise ValueError(f"Expected 91 daily observations; found {len(daily)}.")

    return daily


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    daily = load_daily_sales()

    prophet_data = daily.rename(
        columns={
            "date": "ds",
            "recorded_amount_inr": "y",
        }
    )[["ds", "y"]]

    train = prophet_data.iloc[:-TEST_DAYS].copy()
    test = prophet_data.iloc[-TEST_DAYS:].copy()

    # Evaluate Prophet using the same chronological holdout as W10D1.
    evaluation_model = Prophet(
        weekly_seasonality=True,
        daily_seasonality=False,
        yearly_seasonality=False,
        uncertainty_samples=300,
    )

    evaluation_model.fit(train)

    holdout_dates = pd.DataFrame({"ds": test["ds"]})
    holdout_forecast = evaluation_model.predict(holdout_dates)

    prophet_predictions = holdout_forecast["yhat"].to_numpy()

    # Reuse W10D1 predictions and metrics for a fair comparison.
    predictions = pd.read_csv(INPUT_DIR / "holdout_predictions.csv")
    predictions["date"] = pd.to_datetime(predictions["date"])

    if not predictions["date"].equals(test["ds"].reset_index(drop=True)):
        raise ValueError("W10D1 holdout dates do not match the Prophet test dates.")

    predictions["prophet"] = prophet_predictions
    predictions.to_csv(
        OUTPUT_DIR / "holdout_predictions.csv",
        index=False,
    )

    comparison = pd.read_csv(INPUT_DIR / "model_comparison.csv")

    comparison = pd.concat(
        [
            comparison,
            pd.DataFrame(
                [
                    {
                        "Model": "Prophet (weekly seasonality)",
                        **calculate_metrics(test["y"], prophet_predictions),
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    comparison.to_csv(
        OUTPUT_DIR / "model_comparison.csv",
        index=False,
    )

    # Refit on all observations for the final 14-day forecast.
    final_model = Prophet(
        weekly_seasonality=True,
        daily_seasonality=False,
        yearly_seasonality=False,
        uncertainty_samples=300,
    )

    final_model.fit(prophet_data)

    future = final_model.make_future_dataframe(
        periods=FORECAST_DAYS,
        freq="D",
    )

    forecast = final_model.predict(future)

    future_forecast = forecast.tail(FORECAST_DAYS)[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].copy()

    future_forecast.to_csv(
        OUTPUT_DIR / "forecast.csv",
        index=False,
    )

    # Holdout comparison chart.
    plt.figure(figsize=(11, 5))
    plt.plot(test["ds"], test["y"], label="Actual", marker="o")
    plt.plot(
        test["ds"],
        prophet_predictions,
        label="Prophet",
        marker="o",
    )
    plt.title("W10D2 - Prophet Holdout Evaluation")
    plt.xlabel("Date")
    plt.ylabel("Recorded Amount (INR)")
    plt.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "prophet_holdout.png", dpi=150)
    plt.close()

    # Historical series and future forecast.
    plt.figure(figsize=(11, 5))
    plt.plot(
        prophet_data["ds"],
        prophet_data["y"],
        label="Historical recorded amount",
    )
    plt.plot(
        future_forecast["ds"],
        future_forecast["yhat"],
        label="Prophet forecast",
        marker="o",
    )
    plt.fill_between(
        future_forecast["ds"],
        future_forecast["yhat_lower"],
        future_forecast["yhat_upper"],
        alpha=0.2,
        label="Uncertainty interval",
    )
    plt.title("W10D2 - 14-Day Prophet Forecast")
    plt.xlabel("Date")
    plt.ylabel("Recorded Amount (INR)")
    plt.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "prophet_forecast.png", dpi=150)
    plt.close()

    best = comparison.loc[comparison["MAE (INR)"].idxmin()]

    summary = f"""# W10D2 - Prophet Forecasting

## Dataset
- Source: Indian Business Sales Dataset, aggregated in W10D1
- Observations: {len(prophet_data)}
- Date range: {prophet_data['ds'].min().date()} to {prophet_data['ds'].max().date()}
- Target: Daily recorded order amount (INR)
- Training observations: {len(train)}
- Holdout observations: {len(test)}
- Holdout period: {test['ds'].min().date()} to {test['ds'].max().date()}

## Prophet configuration
- Prophet version: 1.5.0
- Weekly seasonality: Enabled
- Daily seasonality: Disabled
- Yearly seasonality: Disabled due to the short observation period
- Uncertainty samples: 300
- Holdout: Final 14 observations, chronological split

## Model comparison

{comparison.to_string(index=False)}

- Best model by holdout MAE: {best['Model']}
- Best holdout MAE: INR {best['MAE (INR)']:,.2f}

## Final forecast
- Model: Prophet fitted on all {len(prophet_data)} observations
- Forecast horizon: {FORECAST_DAYS} days
- Forecast period: {future_forecast['ds'].min().date()} to {future_forecast['ds'].max().date()}
- Mean predicted daily amount: INR {future_forecast['yhat'].mean():,.2f}

## Interpretation and limitations
- Amount represents recorded order value, not verified net revenue.
- All order statuses are included in the source aggregation.
- The dataset covers approximately three months only.
- Annual seasonality is not established by this dataset.
- The holdout comparison measures performance on one 14-day period.
- Prediction intervals represent model uncertainty, not guaranteed ranges.
- Forecasts are experimental and are not guaranteed business outcomes.

## Evidence
- `holdout_predictions.csv`
- `model_comparison.csv`
- `forecast.csv`
- `prophet_holdout.png`
- `prophet_forecast.png`
"""

    (OUTPUT_DIR / "analysis_summary.md").write_text(
        summary,
        encoding="utf-8",
    )

    print("\n===== W10D2 PROPHET RESULTS =====")
    print(comparison.to_string(index=False))
    print("\n===== FUTURE FORECAST =====")
    print(future_forecast.to_string(index=False))
    print("\n===== OUTPUT FILES =====")

    for path in sorted(OUTPUT_DIR.iterdir()):
        if path.is_file():
            print(f"{path.name}: {path.stat().st_size:,} bytes")

    print("\nW10D2 Prophet pipeline completed successfully.")


if __name__ == "__main__":
    main()
