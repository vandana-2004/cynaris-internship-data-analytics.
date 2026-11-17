# W9D1 - MLflow Experiment Tracking

Objective: Track EDA using MLflow.

Dataset: data/w8d3/indian_business_sales.csv (128,975 rows, 24 columns).

Run: `& .\.venv-pandasai\Scripts\python.exe .\reports\w9d1\mlflow_eda.py` 

Tracking: Local SQLite database (mlflow.db).

Metrics: dataset dimensions, duplicates, missing amounts, amount statistics, skewness and IQR outliers.

Artifacts: EDA summary, category totals CSV and amount distribution chart.

Interpretation: Amounts are recorded order amounts, not net realized revenue. Outliers are flagged, not automatically removed.
