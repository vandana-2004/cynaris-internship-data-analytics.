
from pathlib import Path
import tempfile
import hashlib

import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn

from mlflow.models import infer_signature
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


# ==================================================
# 1. CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT / "data" / "w8d3" / "indian_business_sales.csv"
)

TRACKING_URI = (
    "sqlite:///" + (ROOT / "mlflow.db").as_posix()
)

EXPERIMENT_NAME = "W9D2 - Indian Business Model Registry"

MODEL_NAME = "IndianBusinessOrderAmountRegressor"

FEATURES = [
    "Qty",
    "Category",
    "Fulfilment",
    "Sales Channel ",
    "ship-service-level",
    "B2B",
]

TARGET = "Amount"


# ==================================================
# 2. DATASET VALIDATION
# ==================================================

print("\n===== LOADING DATASET =====")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH, low_memory=False)

required_columns = FEATURES + [TARGET]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# Convert numeric fields safely.
df[TARGET] = pd.to_numeric(
    df[TARGET], errors="coerce"
)

# Float64 supports missing values in the model schema.
df["Qty"] = pd.to_numeric(
    df["Qty"], errors="coerce"
).astype("float64")

# Replace infinite values.
df = df.replace([np.inf, -np.inf], np.nan)

# Remove records without a valid target.
df = df.dropna(subset=[TARGET]).copy()

if len(df) < 20:
    raise ValueError(
        "Insufficient valid records for model training."
    )

X = df[FEATURES].copy()
y = df[TARGET].copy()

print("Dataset:", DATA_PATH.name)
print("Valid records:", len(df))
print("Features:", FEATURES)
print("Target:", TARGET)


# ==================================================
# 3. DATASET FINGERPRINT
# ==================================================

dataset_hash = hashlib.sha256(
    DATA_PATH.read_bytes()
).hexdigest()

print("Dataset SHA256:", dataset_hash)


# ==================================================
# 4. PREPROCESSING PIPELINE
# ==================================================

numeric_features = ["Qty"]

categorical_features = [
    "Category",
    "Fulfilment",
    "Sales Channel ",
    "ship-service-level",
    "B2B",
]

numeric_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median"),
    ),
])

categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="most_frequent"),
    ),
    (
        "encoder",
        OneHotEncoder(handle_unknown="ignore"),
    ),
])

preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_pipeline,
        numeric_features,
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_features,
    ),
])


# ==================================================
# 5. TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

print("\n===== DATA SPLIT =====")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==================================================
# 6. RANDOM FOREST MODEL
# ==================================================

model = Pipeline([
    (
        "preprocessor",
        preprocessor,
    ),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=150,
            max_depth=12,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        ),
    ),
])


# ==================================================
# 7. MLFLOW CONFIGURATION
# ==================================================

mlflow.set_tracking_uri(TRACKING_URI)

mlflow.set_registry_uri(TRACKING_URI)

mlflow.set_experiment(EXPERIMENT_NAME)


# ==================================================
# 8. MODEL TRAINING AND EXPERIMENT TRACKING
# ==================================================

print("\n===== TRAINING MODEL =====")

with mlflow.start_run(
    run_name="order-amount-regression"
) as run:

    # Train model.
    model.fit(X_train, y_train)

    # Generate test predictions.
    predictions = model.predict(X_test)

    # Calculate evaluation metrics.
    mae = mean_absolute_error(
        y_test, predictions
    )

    rmse = root_mean_squared_error(
        y_test, predictions
    )

    r2 = r2_score(
        y_test, predictions
    )

    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "training_rows": len(X_train),
        "testing_rows": len(X_test),
    }

    # Log parameters.
    mlflow.log_params({
        "algorithm": "RandomForestRegressor",
        "n_estimators": 150,
        "max_depth": 12,
        "min_samples_leaf": 2,
        "test_size": 0.20,
        "random_state": 42,
        "target": TARGET,
        "feature_count": len(FEATURES),
    })

    # Log evaluation metrics.
    mlflow.log_metrics(metrics)

    # Log experiment metadata.
    mlflow.set_tags({
        "project": "Indian Business EDA",
        "task": "Order Amount Prediction",
        "model_type": "Regression",
        "dataset": DATA_PATH.name,
        "dataset_sha256": dataset_hash,
        "interpretation": (
            "Predicted recorded order amount, "
            "not net revenue"
        ),
    })

    # Create model signature.
    input_example = X_train.head(3)

    signature = infer_signature(
        input_example,
        model.predict(input_example),
    )

    # Register the model using explicitly reviewed
    # trusted serialization types.
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

    # ==================================================
    # 9. SAVE EVALUATION REPORT
    # ==================================================

    with tempfile.TemporaryDirectory() as temp_dir:

        report_path = (
            Path(temp_dir) / "model_evaluation.txt"
        )

        report_path.write_text(
            "W9D2 - MLflow Model Registry\n"
            "================================\n"
            f"Model: {MODEL_NAME}\n"
            f"Run ID: {run.info.run_id}\n"
            f"Dataset: {DATA_PATH.name}\n"
            f"Dataset SHA256: {dataset_hash}\n"
            f"Valid records: {len(df)}\n"
            f"Training records: {len(X_train)}\n"
            f"Testing records: {len(X_test)}\n"
            f"MAE: {mae:.4f}\n"
            f"RMSE: {rmse:.4f}\n"
            f"R2: {r2:.4f}\n"
            "Target: Recorded Amount (INR)\n"
            "Note: Predictions are not net revenue.\n",
            encoding="utf-8",
        )

        mlflow.log_artifact(
            str(report_path)
        )


    # ==================================================
    # 10. MODEL REGISTRATION VERIFICATION
    # ==================================================

    client = mlflow.MlflowClient()

    registered_versions = client.search_model_versions(
        f"name='{MODEL_NAME}'"
    )

    if not registered_versions:
        raise RuntimeError(
            "Model registration failed."
        )

    latest_version = max(
        registered_versions,
        key=lambda version: int(version.version),
    )

    # Assign champion alias to latest version.
    client.set_registered_model_alias(
        MODEL_NAME,
        "champion",
        latest_version.version,
    )

    print("\n===== W9D2 SUCCESS =====")

    print("Run ID:", run.info.run_id)

    print("Model:", MODEL_NAME)

    print(
        "Model version:",
        latest_version.version,
    )

    print("Alias: champion")

    print(
        "Model URI:",
        model_info.model_uri,
    )

    print("MAE:", round(mae, 4))

    print("RMSE:", round(rmse, 4))

    print("R2:", round(r2, 4))


# ==================================================
# 11. FINAL REGISTRY VERIFICATION
# ==================================================

print("\n===== REGISTRY VERIFICATION =====")

registered_model = client.get_registered_model(
    MODEL_NAME
)

champion = client.get_model_version_by_alias(
    MODEL_NAME,
    "champion",
)

print("Registered model:", registered_model.name)

print("Champion version:", champion.version)

print("Champion run ID:", champion.run_id)

print("\nW9D2 MODEL REGISTRY COMPLETED SUCCESSFULLY")
