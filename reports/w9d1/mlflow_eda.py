import tempfile
from pathlib import Path
import pandas as pd
import mlflow
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[2]
data = root / "data" / "w8d3" / "indian_business_sales.csv"
df = pd.read_csv(data, low_memory=False)
amount = pd.to_numeric(df["Amount"], errors="coerce").dropna()
q1, q3 = amount.quantile([0.25, 0.75])
iqr = q3 - q1

mlflow.set_tracking_uri("sqlite:///" + (root / "mlflow.db").as_posix())
mlflow.set_experiment("W9D1 - Indian Business EDA")

with mlflow.start_run(run_name="indian-business-eda") as run:
    mlflow.log_params({"dataset": data.name, "outlier_method": "1.5x IQR"})
    mlflow.log_metrics({
        "rows": len(df), "columns": len(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "missing_amount": int(df["Amount"].isna().sum()),
        "amount_mean": amount.mean(),
        "amount_median": amount.median(),
        "amount_std": amount.std(),
        "amount_skewness": amount.skew(),
        "iqr_outliers": int(((amount < q1-1.5*iqr) | (amount > q3+1.5*iqr)).sum())
    })
    mlflow.set_tag("interpretation", "Recorded amounts, not net revenue")
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "eda_summary.txt").write_text(
            f"Rows: {len(df)}\nColumns: {len(df.columns)}\n"
            f"Valid amounts: {len(amount)}\nMean: {amount.mean():.2f}\n"
            f"Median: {amount.median():.2f}\nIQR outliers: {int(((amount < q1-1.5*iqr) | (amount > q3+1.5*iqr)).sum())}\n",
            encoding="utf-8")
        df.groupby("Category")["Amount"].sum().to_csv(p / "category_amounts.csv")
        plt.figure()
        plt.hist(amount, bins=40)
        plt.title("Recorded Amount Distribution")
        plt.savefig(p / "amount_distribution.png")
        plt.close()
        mlflow.log_artifacts(tmp)
    print("SUCCESS | Run ID:", run.info.run_id)
    print("Rows:", len(df), "| Columns:", len(df.columns))

