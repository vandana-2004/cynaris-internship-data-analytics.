"""
W10D3: Anomaly Detection
Methods: IQR, Z-score, Isolation Forest
Dataset: Indian Business Sales Dataset
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_DIR = ROOT / "reports" / "w10d3"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
CONTAMINATION = 0.02
Z_THRESHOLD = 3.0


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, low_memory=False)

    required = ["Order ID", "Date", "Status", "Category", "Qty", "Amount"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Date"] = pd.to_datetime(
        df["Date"], format="%m-%d-%y", errors="coerce"
    )

    return df


def detect_anomalies(df):
    results = df[
        ["Order ID", "Date", "Status", "Category", "Qty", "Amount"]
    ].copy()

    valid_amount = results["Amount"].dropna()
    positive = results[
        (results["Amount"] > 0) & (results["Qty"] > 0)
    ].copy()

    if len(valid_amount) < 2 or len(positive) < 10:
        raise ValueError("Insufficient valid observations for anomaly detection.")

    # Method 1: Interquartile Range
    q1 = valid_amount.quantile(0.25)
    q3 = valid_amount.quantile(0.75)
    iqr = q3 - q1

    lower_bound = max(0, q1 - 1.5 * iqr)
    upper_bound = q3 + 1.5 * iqr

    results["amount_iqr_anomaly"] = (
        (results["Amount"] < lower_bound)
        | (results["Amount"] > upper_bound)
    ).fillna(False)

    # Method 2: Z-score
    mean_amount = valid_amount.mean()
    std_amount = valid_amount.std()

    if std_amount == 0 or pd.isna(std_amount):
        results["amount_zscore"] = 0.0
    else:
        results["amount_zscore"] = (
            results["Amount"] - mean_amount
        ) / std_amount

    results["amount_zscore_anomaly"] = (
        results["amount_zscore"].abs() > Z_THRESHOLD
    ).fillna(False)

    # Method 3: Isolation Forest
    features = positive[["Amount", "Qty"]].copy()

    model = IsolationForest(
        n_estimators=200,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    predictions = model.fit_predict(features)

    results["isolation_forest_anomaly"] = False
    results.loc[positive.index, "isolation_forest_anomaly"] = (
        predictions == -1
    )

    results["any_anomaly"] = results[
        [
            "amount_iqr_anomaly",
            "amount_zscore_anomaly",
            "isolation_forest_anomaly"
        ]
    ].any(axis=1)

    results["anomaly_methods_count"] = results[
        [
            "amount_iqr_anomaly",
            "amount_zscore_anomaly",
            "isolation_forest_anomaly"
        ]
    ].sum(axis=1)

    return results, {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower": lower_bound,
        "upper": upper_bound,
        "mean": mean_amount,
        "std": std_amount,
        "valid_amount": len(valid_amount),
        "valid_model": len(positive),
        "model": model
    }


def create_outputs(df, results, stats):
    method_columns = [
        "amount_iqr_anomaly",
        "amount_zscore_anomaly",
        "isolation_forest_anomaly"
    ]

    counts = results[method_columns].sum()

    comparison = pd.DataFrame({
        "method": ["IQR", "Z-score", "Isolation Forest"],
        "anomaly_count": counts.values,
        "percentage_of_dataset": (
            counts.values / len(results) * 100
        ).round(3)
    })

    comparison.to_csv(
        OUTPUT_DIR / "method_comparison.csv", index=False
    )

    flagged = results[results["any_anomaly"]].copy()

    flagged.to_csv(
        OUTPUT_DIR / "anomaly_records.csv", index=False
    )

    status_summary = results.groupby(
        "Status", dropna=False
    ).agg(
        total_records=("Order ID", "size"),
        flagged_records=("any_anomaly", "sum"),
        average_amount=("Amount", "mean")
    ).reset_index()

    status_summary["flagged_percentage"] = (
        status_summary["flagged_records"]
        / status_summary["total_records"] * 100
    ).round(2)

    status_summary.to_csv(
        OUTPUT_DIR / "status_anomaly_summary.csv", index=False
    )

    # Visualization 1: Amount distribution
    valid_amount = results["Amount"].dropna()
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        valid_amount.clip(upper=valid_amount.quantile(0.99)),
        bins=50,
        edgecolor="black",
        alpha=0.75
    )

    ax.axvline(
        stats["upper"],
        linestyle="--",
        label="IQR upper bound"
    )

    ax.set_title("Indian Business Sales - Amount Distribution")
    ax.set_xlabel("Amount (INR, capped at 99th percentile)")
    ax.set_ylabel("Transaction Count")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "amount_distribution.png", dpi=150)
    plt.close(fig)

    # Visualization 2: Amount versus quantity
    fig, ax = plt.subplots(figsize=(10, 6))

    normal = results[
        (results["Amount"] > 0)
        & (results["Qty"] > 0)
        & (~results["isolation_forest_anomaly"])
    ]

    anomalies = results[
        results["isolation_forest_anomaly"]
    ]

    ax.scatter(
        normal["Qty"], normal["Amount"],
        alpha=0.18, s=12, label="Normal"
    )

    ax.scatter(
        anomalies["Qty"], anomalies["Amount"],
        alpha=0.65, s=18, label="Isolation Forest flagged"
    )

    ax.set_yscale("log")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Amount (INR, logarithmic scale)")
    ax.set_title("Isolation Forest: Transaction Anomalies")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "anomaly_scatter.png", dpi=150)
    plt.close(fig)

    # Visualization 3: Method comparison
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(comparison["method"], comparison["anomaly_count"])
    ax.set_title("Anomaly Detection Method Comparison")
    ax.set_ylabel("Flagged Records")
    ax.set_xlabel("Detection Method")

    for i, value in enumerate(comparison["anomaly_count"]):
        ax.text(i, value, f"{value:,}", ha="center", va="bottom")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "method_comparison.png", dpi=150)
    plt.close(fig)

    return comparison, flagged, status_summary


def create_summary(df, results, stats, comparison, flagged, status):
    total = len(df)
    valid = stats["valid_model"]

    overlap = int(
        results[[
            "amount_iqr_anomaly",
            "amount_zscore_anomaly",
            "isolation_forest_anomaly"
        ]].all(axis=1).sum()
    )

    missing_amount = int(df["Amount"].isna().sum())
    missing_qty = int(df["Qty"].isna().sum())

    lines = [
        "# W10D3 - Anomaly Detection Analysis",
        "",
        "## 1. Objective",
        "",
        "Identify unusual business transaction observations using "
        "statistical methods and Isolation Forest.",
        "",
        "## 2. Dataset",
        "",
        f"- Dataset: `{DATA_PATH.relative_to(ROOT)}`",
        f"- Total records: {total:,}",
        f"- Missing Amount records: {missing_amount:,}",
        f"- Missing Qty records: {missing_qty:,}",
        f"- Valid positive Amount and Qty model records: {valid:,}",
        f"- Date range: {df['Date'].min()} to {df['Date'].max()}",
        "",
        "## 3. Detection methodology",
        "",
        "### IQR",
        "",
        "- Lower bound: Q1 - 1.5 x IQR, constrained to non-negative values.",
        "- Upper bound: Q3 + 1.5 x IQR.",
        f"- Calculated bounds: INR {stats['lower']:.2f} to "
        f"INR {stats['upper']:.2f}.",
        "",
        "### Z-score",
        "",
        f"- Threshold: absolute Z-score greater than {Z_THRESHOLD}.",
        f"- Mean Amount: INR {stats['mean']:.2f}.",
        f"- Standard deviation: INR {stats['std']:.2f}.",
        "",
        "### Isolation Forest",
        "",
        "- Features: Amount and Qty.",
        f"- Contamination assumption: {CONTAMINATION:.0%}.",
        f"- Estimators: 200.",
        f"- Random state: {RANDOM_STATE}.",
        "- Model fitted only on records with positive Amount and Qty.",
        "",
        "## 4. Results",
        "",
        comparison.to_markdown(index=False),
        "",
        f"- Records flagged by at least one method: {len(flagged):,}.",
        f"- Records flagged by all three methods: {overlap:,}.",
        "",
        "## 5. Status-level interpretation",
        "",
        status.to_markdown(index=False),
        "",
        "## 6. Business interpretation",
        "",
        "IQR identifies observations beyond the central spread of transaction "
        "amounts. Z-score identifies observations far from the overall mean. "
        "Isolation Forest evaluates combinations of Amount and Qty.",
        "",
        "The methods are complementary. A transaction flagged by one method "
        "is a candidate for review, not proof of fraud, data corruption, or "
        "business error. Status, product category, fulfilment and order context "
        "should be checked before taking action.",
        "",
        "The 2% Isolation Forest contamination value is a modelling assumption, "
        "not a measured fraud rate.",
        "",
        "## 7. Limitations and improvements",
        "",
        "- Transaction amounts can be naturally skewed.",
        "- Different product categories may have different normal ranges.",
        "- Seasonal and promotional effects are not modelled.",
        "- Statistical thresholds are global rather than category-specific.",
        "- Future work: category-aware detection, robust transformations, "
        "manual validation and threshold sensitivity analysis.",
        "",
        "## 8. Evidence files",
        "",
        "- `anomaly_records.csv`",
        "- `method_comparison.csv`",
        "- `status_anomaly_summary.csv`",
        "- `amount_distribution.png`",
        "- `anomaly_scatter.png`",
        "- `method_comparison.png`",
        "- `analysis_summary.md`",
        "",
        "## 9. Reproducibility",
        "",
        "Run: `python reports/w10d3/anomaly_detection.py`",
        "",
        "The original dataset is not modified."
    ]

    (OUTPUT_DIR / "analysis_summary.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8"
    )


def main():
    print("Loading Indian Business Sales Dataset...")
    df = load_data()

    print(f"Loaded {len(df):,} records.")
    print("Running IQR, Z-score and Isolation Forest...")

    results, stats = detect_anomalies(df)

    comparison, flagged, status = create_outputs(
        df, results, stats
    )

    create_summary(
        df, results, stats, comparison, flagged, status
    )

    print("\n===== METHOD COMPARISON =====")
    print(comparison.to_string(index=False))

    print("\n===== ANALYSIS SUMMARY =====")
    print(f"Total records: {len(df):,}")
    print(f"Valid model records: {stats['valid_model']:,}")
    print(f"Records flagged: {len(flagged):,}")
    print(f"IQR bounds: {stats['lower']:.2f} - {stats['upper']:.2f}")
    print(f"Output directory: {OUTPUT_DIR}")

    print("\nW10D3 analysis completed successfully.")


if __name__ == "__main__":
    main()
