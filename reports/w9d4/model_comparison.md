# W9D4 - MLflow Model Version Comparison

## Dataset and evaluation setup

- Dataset: `indian_business_sales.csv`
- SHA256: `ac9a366da5f3af418831fa53da9eebfc3b3838803e3774eec97dbcb291441beb`
- Valid records: 121180
- Training records: 96944
- Testing records: 24236
- Features: Qty, Category, Fulfilment, Sales Channel , ship-service-level, B2B
- Target: `Amount` (recorded amount, not net revenue)
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
| 1 | Baseline | 148.9428 | 208.4967 | 0.4501 |
| 2 | Candidate | 148.9365 | 208.4935 | 0.4501 |

Lower MAE and RMSE are better. Higher R2 is better.

## MLflow registry

- Registered model: `IndianBusinessOrderAmountRegressor`
- Baseline version: 1
- Candidate version: 2
- Candidate run ID: `5f3a536264564010a507a99518e88b0e`
- Model URI: `models:/m-900c7ec48711419e8b7db608781aedc1`
- Champion alias: intentionally unchanged.
