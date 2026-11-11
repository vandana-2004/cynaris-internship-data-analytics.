# W9D2 — MLflow Model Registry for Analyst Models

## Objective

Train, evaluate, register, and retrieve a machine-learning model using MLflow Model Registry.

## Dataset

- Source: `data/w8d3/indian_business_sales.csv`
- Valid records: 121,180
- Target: `Amount` (recorded order amount, not net realised revenue)
- Features: Qty, Category, Fulfilment, Sales Channel, ship-service-level, B2B
- Dataset SHA256: `ac9a366da5f3af418831fa53da9eebfc3b3838803e3774eec97dbcb291441beb`

## Model

- Algorithm: RandomForestRegressor
- Preprocessing: median imputation for Qty; most-frequent imputation and one-hot encoding for categorical features
- Train/test split: 80/20
- Random state: 42
- Training records: 96,944
- Testing records: 24,236

## Evaluation Results

| Metric |   Result |
| ------ | -------: |
| MAE    | 148.9428 |
| RMSE   | 208.4967 |
| R²     |   0.4501 |

This is a baseline model. Its R² indicates that it explains approximately 45% of the variation in test-set Amount values. Further feature engineering and validation are needed before production use.

## MLflow Tracking and Registry

- MLflow version: 3.18.0
- Tracking backend: local SQLite (`mlflow.db`)
- Experiment: `W9D2 - Indian Business Model Registry`
- Successful run ID: `86e4765896664473b206016adc2d8f57`
- Registered model: `IndianBusinessOrderAmountRegressor`
- Model version: `1`
- Registry alias: `champion`

## Verification

- Model training and evaluation completed successfully.
- Model version 1 registered successfully.
- `champion` alias verified against version 1.
- Model loaded using `models:/IndianBusinessOrderAmountRegressor@champion`.
- Predictions generated for three dataset records:
  - 784.3668
  - 450.7331
  - 506.0659
- Model load and prediction test: PASSED.

## Reproduction

From the repository root:

```powershell
& .\.venv-pandasai\Scripts\python.exe .\reports\w9d2\mlflow_model_registry.py
```

Re-running the script may create another MLflow run and registered model version.

## Limitations

- The model uses a limited set of order features.
- Amount is recorded order amount, not confirmed net revenue.
- Model performance is a baseline, not evidence of production readiness.
- MLflow tracking and registry use a local SQLite database.
- The registered model has not been deployed as a prediction service.

## CIA Mentor Review

Status: Pending two W9D2 mentor interactions.
