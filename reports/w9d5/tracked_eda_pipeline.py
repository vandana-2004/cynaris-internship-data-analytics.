
import hashlib
from pathlib import Path

import pandas as pd
import mlflow
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUTPUT_DIR = ROOT / "reports" / "w9d5" / "outputs"
TRACKING_DB = ROOT / "mlflow.db"
EXPERIMENT_NAME = "W9D5 - Tracked DA Experiment Pipeline"


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH, low_memory=False)
    df.columns = df.columns.str.strip()

    # --------------------------------------------------
    # 1. RAW DATA QUALITY CHECKS
    # --------------------------------------------------

    original_rows, original_columns = df.shape

    duplicate_rows = int(df.duplicated().sum())

    raw_missing_cells = int(df.isna().sum().sum())

    # Identify and exclude unnamed export/index columns.
    unnamed_columns = [
        column
        for column in df.columns
        if column.lower().startswith("unnamed")
    ]

    analysis = df.drop(columns=unnamed_columns).copy()

    analytical_missing_cells = int(
        analysis.isna().sum().sum()
    )

    if "Amount" not in analysis.columns:
        raise ValueError("Required column 'Amount' is missing.")

    if "Category" not in analysis.columns:
        raise ValueError("Required column 'Category' is missing.")

    # --------------------------------------------------
    # 2. AMOUNT VALIDATION
    # --------------------------------------------------

    raw_amount = analysis["Amount"].copy()

    # Count values that were already missing in the dataset.
    amount_missing_count = int(raw_amount.isna().sum())

    # Convert Amount to numeric values.
    parsed_amount = pd.to_numeric(
        raw_amount,
        errors="coerce"
    )

    # Count non-missing values that failed numeric conversion.
    amount_parse_errors = int(
        (raw_amount.notna() & parsed_amount.isna()).sum()
    )

    analysis["Amount"] = parsed_amount

    # Missing and invalid values are excluded, not imputed.
    amount = parsed_amount.dropna()

    amount_excluded_total = (
        amount_missing_count + amount_parse_errors
    )

    if amount.empty:
        raise ValueError("No valid Amount values are available.")

    # --------------------------------------------------
    # 3. IQR OUTLIER ANALYSIS
    # --------------------------------------------------

    q1, q3 = amount.quantile([0.25, 0.75])

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outlier_count = int(
        ((amount < lower_bound) | (amount > upper_bound)).sum()
    )

    # --------------------------------------------------
    # 4. CATEGORY SUMMARY
    # --------------------------------------------------

    category_amounts = (
        analysis.groupby("Category", dropna=False)["Amount"]
        .agg(
            order_line_count="count",
            recorded_amount_sum="sum"
        )
        .sort_values(
            "recorded_amount_sum",
            ascending=False
        )
    )

    category_amounts.to_csv(
        OUTPUT_DIR / "category_summary.csv"
    )

    # --------------------------------------------------
    # 5. ORDER STATUS SUMMARY
    # --------------------------------------------------

    if "Status" in analysis.columns:
        status_counts = (
            analysis["Status"]
            .fillna("Missing")
            .value_counts()
            .rename_axis("status")
            .reset_index(name="row_count")
        )

        status_counts.to_csv(
            OUTPUT_DIR / "status_summary.csv",
            index=False
        )

    # --------------------------------------------------
    # 6. DATE COVERAGE
    # --------------------------------------------------

    date_min = None
    date_max = None

    if "Date" in analysis.columns:
        dates = pd.to_datetime(
            analysis["Date"],
            errors="coerce",
            format="mixed"
        ).dropna()

        if not dates.empty:
            date_min = dates.min().strftime("%Y-%m-%d")
            date_max = dates.max().strftime("%Y-%m-%d")

    # --------------------------------------------------
    # 7. EDA SUMMARY REPORT
    # --------------------------------------------------

    dataset_hash = sha256_file(DATA_PATH)

    amount_skewness = float(amount.skew())

    summary = f"""# W9D5 — Tracked EDA Experiment Results

## Dataset

- File: `{DATA_PATH.name}`
- SHA-256: `{dataset_hash}`
- Original rows: {original_rows:,}
- Original columns: {original_columns}
- Analytical columns: {len(analysis.columns)}
- Excluded unnamed columns: {len(unnamed_columns)}
- Duplicate rows: {duplicate_rows:,}

## Missing Data

- Missing cells in original dataset: {raw_missing_cells:,}
- Missing cells in analytical dataset before Amount parsing: {analytical_missing_cells:,}
- Originally missing Amount values: {amount_missing_count:,}
- Amount parsing errors: {amount_parse_errors:,}
- Total Amount values excluded from statistics: {amount_excluded_total:,}
- Amount handling: Missing and non-numeric values were excluded; no imputation was performed.

## Recorded Amount Analysis

- Valid Amount values: {len(amount):,}
- Mean: INR {amount.mean():,.2f}
- Median: INR {amount.median():,.2f}
- Standard deviation: INR {amount.std():,.2f}
- Minimum: INR {amount.min():,.2f}
- Maximum: INR {amount.max():,.2f}
- Skewness: {amount_skewness:.4f}
- IQR outliers (1.5 × IQR): {outlier_count:,}
- Lower IQR bound: INR {lower_bound:,.2f}
- Upper IQR bound: INR {upper_bound:,.2f}

## Date Coverage

- Earliest date: {date_min or "Unavailable"}
- Latest date: {date_max or "Unavailable"}

## Interpretation

Amount represents recorded order amounts, not net revenue.

The distribution is positively skewed (skewness approximately {amount_skewness:.2f}).
The mean exceeds the median, indicating a right-skewed distribution.

IQR outliers are statistical flags, not automatic errors.
Business justification is required before excluding them from further analysis.

Missing and non-numeric Amount values were excluded from Amount statistics.
If missingness is not random, this may introduce bias.

The analysis is descriptive and does not establish causation.
"""

    (OUTPUT_DIR / "eda_summary.md").write_text(
        summary,
        encoding="utf-8"
    )

    # --------------------------------------------------
    # 8. VISUALIZATIONS
    # --------------------------------------------------

    plt.figure(figsize=(9, 5))

    plt.hist(amount, bins=40)

    plt.title("Recorded Order Amount Distribution")
    plt.xlabel("Amount (INR)")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "amount_distribution.png",
        dpi=120
    )

    plt.close()

    top_categories = category_amounts.head(10)[
        "recorded_amount_sum"
    ]

    plt.figure(figsize=(9, 5))

    top_categories.sort_values().plot(kind="barh")

    plt.title("Top 10 Categories by Recorded Amount")
    plt.xlabel("Recorded Amount (INR)")
    plt.ylabel("Category")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "top_categories.png",
        dpi=120
    )

    plt.close()

    # --------------------------------------------------
    # 9. MLFLOW EXPERIMENT TRACKING
    # --------------------------------------------------

    mlflow.set_tracking_uri(
        "sqlite:///" + TRACKING_DB.as_posix()
    )

    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run(
        run_name="indian-business-tracked-eda"
    ) as run:

        # Experiment parameters.
        mlflow.log_params({
            "dataset": DATA_PATH.name,
            "dataset_sha256": dataset_hash,
            "analysis_type": "descriptive_eda",
            "outlier_method": "1.5x_IQR",
            "histogram_bins": 40,
            "top_categories": 10,
            "unnamed_columns_excluded": len(unnamed_columns),
            "missingness_scope": "raw_and_analytical",
            "amount_handling": "missing_and_parse_errors_excluded",
        })

        # Experiment metrics.
        mlflow.log_metrics({
            "rows": original_rows,
            "original_columns": original_columns,
            "analytical_columns": len(analysis.columns),
            "duplicate_rows": duplicate_rows,

            "raw_missing_cells": raw_missing_cells,
            "analytical_missing_cells": analytical_missing_cells,

            "amount_missing_count": amount_missing_count,
            "amount_parse_errors": amount_parse_errors,
            "amount_excluded_total": amount_excluded_total,
            "valid_amounts": len(amount),

            "amount_mean": float(amount.mean()),
            "amount_median": float(amount.median()),
            "amount_std": float(amount.std()),
            "amount_min": float(amount.min()),
            "amount_max": float(amount.max()),
            "amount_skewness": amount_skewness,

            "iqr_outliers": outlier_count,
        })

        # Experiment tags.
        mlflow.set_tags({
            "dataset_domain": "Indian business sales",
            "target_interpretation": "Recorded amount, not net revenue",
            "pipeline_stage": "EDA",
            "reproducibility": "Dataset SHA-256 logged",
            "missingness_interpretation": (
                "Raw and analytical missing cells tracked separately"
            ),
            "amount_missing_handling": (
                "Excluded from Amount statistics; no imputation"
            ),
            "outlier_interpretation": (
                "Statistical flags requiring business review"
            ),
        })

        # Log all generated reports and charts.
        mlflow.log_artifacts(
            str(OUTPUT_DIR),
            artifact_path="eda_outputs"
        )

        print("\nSUCCESS — W9D5 EDA experiment tracked")
        print("Experiment:", EXPERIMENT_NAME)
        print("Run ID:", run.info.run_id)
        print("Rows:", original_rows)
        print("Raw missing cells:", raw_missing_cells)
        print("Analytical missing cells:", analytical_missing_cells)
        print("Originally missing Amount:", amount_missing_count)
        print("Amount parsing errors:", amount_parse_errors)
        print("Valid Amount values:", len(amount))
        print("IQR outliers:", outlier_count)
        print("Artifacts:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
