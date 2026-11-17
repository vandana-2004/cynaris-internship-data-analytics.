from pathlib import Path
import hashlib

import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn

from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_DIR = ROOT / "reports" / "w9d4"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRACKING_URI = "sqlite:///" + (ROOT / "mlflow.db").as_posix()
EXPERIMENT_NAME = "W9D4 - Model Version Comparison"
MODEL_NAME = "IndianBusinessOrderAmountRegressor"

BASELINE_RUN_ID = "86e4765896664473b206016adc2d8f57"
EXPECTED_DATASET_SHA256 = (
    "ac9a366da5f3af418831fa53da9eebfc3b3838803e3774eec97dbcb291441beb"
)

FEATURES = [
    "Qty",
    "Category",
    "Fulfilment",
    "Sales Channel ",
    "ship-service-level",
    "B2B",
]
TARGET = "Amount"

CANDIDATE_PARAMS = {
    "n_estimators": 250,
    "max_depth": 16,
    "min_samples_leaf": 2,
    "random_state": 42,
}


def main():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_registry_uri(TRACKING_URI)
    client = MlflowClient()

    # Verify the existing baseline.
    baseline_version = client.get_model_version(MODEL_NAME, "1")
    baseline_run = client.get_run(BASELINE_RUN_ID)

    if baseline_version.run_id != BASELINE_RUN_ID:
        raise RuntimeError("Baseline version 1 does not match expected run.")

    existing_versions = client.search_model_versions(
        f"name='{MODEL_NAME}'"
    )
    if len(existing_versions) != 1:
        raise RuntimeError(
            "Expected exactly one registered version before W9D4. "
            "Inspect the registry before proceeding."
        )

    baseline_metrics = {
        metric: baseline_run.data.metrics[metric]
        for metric in ("mae", "rmse", "r2")
    }

    # Verify the exact same dataset as W9D2.
    if not DATA_PATH.exists():
        raise FileNotFoundError(DATA_PATH)

    dataset_hash = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()
    if dataset_hash != EXPECTED_DATASET_SHA256:
        raise ValueError("Dataset fingerprint differs from W9D2.")

    df = pd.read_csv(DATA_PATH, low_memory=False)

    missing = [col for col in FEATURES + [TARGET] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df["Qty"] = pd.to_numeric(
        df["Qty"], errors="coerce"
    ).astype("float64")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=[TARGET]).copy()

    if len(df) != 121180:
        raise ValueError(f"Unexpected valid row count: {len(df)}")

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    if len(X_train) != 96944 or len(X_test) != 24236:
        raise ValueError("Train/test split differs from baseline.")

    # Match W9D2 preprocessing exactly.
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, ["Qty"]),
        (
            "categorical",
            categorical_pipeline,
            [
                "Category",
                "Fulfilment",
                "Sales Channel ",
                "ship-service-level",
                "B2B",
            ],
        ),
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(
                **CANDIDATE_PARAMS,
                n_jobs=-1,
            ),
        ),
    ])

    mlflow.set_experiment(EXPERIMENT_NAME)

    print("Dataset and baseline verified.")
    print("Training rows:", len(X_train))
    print("Testing rows:", len(X_test))
    print("Training candidate model...")

    with mlflow.start_run(run_name="random-forest-v2-comparison") as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        candidate_metrics = {
            "mae": float(mean_absolute_error(y_test, predictions)),
            "rmse": float(root_mean_squared_error(y_test, predictions)),
            "r2": float(r2_score(y_test, predictions)),
        }

        mlflow.log_params({
            "algorithm": "RandomForestRegressor",
            **CANDIDATE_PARAMS,
            "test_size": 0.20,
            "target": TARGET,
            "feature_count": len(FEATURES),
            "baseline_version": 1,
        })
        mlflow.log_metrics(candidate_metrics)

        mlflow.set_tags({
            "project": "Indian Business EDA",
            "task": "Model Version Comparison",
            "dataset": DATA_PATH.name,
            "dataset_sha256": dataset_hash,
            "baseline_run_id": BASELINE_RUN_ID,
            "interpretation": "Recorded order amount, not net revenue",
        })

        input_example = X_train.head(3)
        signature = infer_signature(
            input_example, model.predict(input_example)
        )

        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name=MODEL_NAME,
            signature=signature,
            input_example=input_example,
            skops_trusted_types=[
                "numpy.dtype",
                "sklearn.tree._tree.Tree",
            ],
        )

        versions = client.search_model_versions(
            f"name='{MODEL_NAME}'"
        )
        candidate = next(
            (item for item in versions if item.run_id == run.info.run_id),
            None,
        )
        if candidate is None:
            raise RuntimeError("Candidate registration was not verified.")

        comparison = pd.DataFrame([
            {"version": 1, "model": "Baseline", **baseline_metrics},
            {
                "version": int(candidate.version),
                "model": "Candidate",
                **candidate_metrics,
            },
        ])

        csv_path = OUTPUT_DIR / "model_comparison.csv"
        md_path = OUTPUT_DIR / "model_comparison.md"
        comparison.to_csv(csv_path, index=False)

        report = f"""# W9D4 - MLflow Model Version Comparison

## Dataset and evaluation setup

- Dataset: `{DATA_PATH.name}`
- SHA256: `{dataset_hash}`
- Valid records: {len(df)}
- Training records: {len(X_train)}
- Testing records: {len(X_test)}
- Features: {", ".join(FEATURES)}
- Target: `{TARGET}` (recorded amount, not net revenue)
- Split: 80/20, random_state=42

## Model configurations

| Parameter | Version 1 | Version 2 |
|---|---:|---:|
| Algorithm | RandomForestRegressor | RandomForestRegressor |
| n_estimators | 150 | 250 |
| max_depth | 12 | 16 |
| min_samples_leaf | 2 | 2 |
| random_state | 42 | 42 |

## Evaluation results

| Version | Model | MAE | RMSE | R2 |
|---:|---|---:|---:|---:|
{chr(10).join(
    f"| {int(row.version)} | {row.model} | {row.mae:.4f} | {row.rmse:.4f} | {row.r2:.4f} |"
    for row in comparison.itertuples()
)}

Lower MAE and RMSE are better. Higher R2 is better.

## MLflow registry

- Registered model: `{MODEL_NAME}`
- Baseline version: 1
- Candidate version: {candidate.version}
- Candidate run ID: `{run.info.run_id}`
- Model URI: `{model_info.model_uri}`
- Champion alias: intentionally unchanged.
"""
        md_path.write_text(report, encoding="utf-8")

        mlflow.log_artifact(str(csv_path))
        mlflow.log_artifact(str(md_path))

        champion = client.get_model_version_by_alias(
            MODEL_NAME, "champion"
        )
        if str(champion.version) != "1":
            raise RuntimeError("Champion alias changed unexpectedly.")

        print("\nW9D4 comparison completed.")
        print("Candidate version:", candidate.version)
        print("Candidate run ID:", run.info.run_id)
        print(comparison.to_string(index=False))
        print("Champion remains version:", champion.version)
        print("CSV:", csv_path)
        print("Report:", md_path)


if __name__ == "__main__":
    main()

