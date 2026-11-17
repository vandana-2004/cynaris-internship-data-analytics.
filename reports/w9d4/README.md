\# W9D4: MLflow Dashboard — Compare Model Versions



\## Objective



Compare two registered Random Forest regression model versions using MLflow. Evaluate their performance on the same Indian Business Sales dataset and the same train/test split.



\## Dataset



\- Dataset: `data/w8d3/indian\_business\_sales.csv`

\- Valid records: 121,180

\- Training records: 96,944

\- Testing records: 24,236

\- Split: 80/20

\- Random state: 42

\- Target: `Amount` (recorded order amount, not net revenue)

\- Features: Qty, Category, Fulfilment, Sales Channel, ship-service-level, B2B
## Preprocessing and data leakage prevention

The dataset was split before fitting preprocessing transformations.

- Numeric feature `Qty`: missing values imputed using the median.
- Categorical features: missing values imputed using the most frequent value.
- Categorical encoding: OneHotEncoder with `handle_unknown="ignore"`.
- Preprocessing and Random Forest regression are combined in a scikit-learn Pipeline.
- The pipeline is fitted using training data and evaluated on the held-out test data.
- No feature scaling was applied; it is not required for this Random Forest model.

This approach prevents preprocessing statistics and encoder categories from being learned from the test set.

## CIA Mentor Review

Two CIA Mentor interactions were completed.

1. **Comparison consistency review:** Requested an audit of metric values, dataset split, parameters and validation methodology.
2. **Promotion decision review:** The mentor highlighted negligible metric improvements, the limitations of a single hold-out evaluation, and the increased complexity of Version 2.

**Decision:** Keep Version 1 as champion. Version 2 remains registered as a candidate because its small metric improvements do not justify promotion without further validation.

**Validation limitation:** The comparison uses a single 80/20 hold-out split. Cross-validation and standard-error analysis have not yet been performed.



\## Model configurations



| Parameter | Version 1 | Version 2 |

|---|---:|---:|

| Algorithm | RandomForestRegressor | RandomForestRegressor |

| n\_estimators | 150 | 250 |

| max\_depth | 12 | 16 |

| min\_samples\_leaf | 2 | 2 |

| random\_state | 42 | 42 |



\## Evaluation results



| Metric | Version 1 | Version 2 |

|---|---:|---:|

| MAE | 148.9428 | 148.9365 |

| RMSE | 208.4967 | 208.4935 |

| R2 | 0.450080 | 0.450097 |



Version 2 performed marginally better on all three metrics. However, the improvement is very small and does not represent a substantial performance gain.



\## MLflow registry



\- Registered model: `IndianBusinessOrderAmountRegressor`

\- Baseline version: 1

\- Candidate version: 2

\- Version 1 run ID: `86e4765896664473b206016adc2d8f57`

\- Version 2 run ID: `5f3a536264564010a507a99518e88b0e`

\- Champion alias: Version 1 (unchanged)



Version 2 was registered successfully. Version 1 remains the champion pending further evaluation.



\## Generated deliverables



\- `model\_version\_comparison.py` — model training, registration and comparison

\- `model\_comparison.csv` — metric comparison

\- `model\_comparison.md` — detailed comparison report

\- `README.md` — project documentation



\## Run the script



```powershell

\& .\\.venv-pandasai\\Scripts\\python.exe .\\reports\\w9d4\\model\_version\_comparison.py

```



Note: The script registers a new model version. Do not rerun it just to view existing results.



\## MLflow dashboard



Start MLflow from the repository root:



```powershell

mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000

```



Open `http://127.0.0.1:5000` in your browser to inspect experiments, metrics, parameters and runs.



\## Conclusion



This exercise demonstrates MLflow experiment tracking, model registration, version comparison and evaluation using a consistent dataset and split. The candidate model showed marginal metric improvements, so the existing champion alias was deliberately preserved.

