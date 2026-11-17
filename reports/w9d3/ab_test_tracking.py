from pathlib import Path

import numpy as np
import pandas as pd
import mlflow
from scipy import stats


# ==================================================
# 1. CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
TRACKING_URI = "sqlite:///" + (ROOT / "mlflow.db").as_posix()
EXPERIMENT_NAME = "W9D3 - Indian Business A/B Testing"

OUTPUT_DIR = Path(__file__).resolve().parent / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. LOAD AND VALIDATE DATA
# ==================================================

print("\n===== LOADING DATASET =====")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

required_columns = [
    "Order ID", "Fulfilment", "Amount", "Qty", "Status"
]

df = pd.read_csv(DATA_PATH, usecols=required_columns)

missing = set(required_columns) - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

print("Loaded required columns:", df.shape)


# ==================================================
# 3. CLEAN DATA AND AGGREGATE TO ORDER LEVEL
# ==================================================

df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")

clean = df[
    df["Order ID"].notna()
    & df["Status"].astype(str).str.startswith("Shipped", na=False)
    & df["Fulfilment"].isin(["Amazon", "Merchant"])
    & (df["Amount"] > 0)
    & (df["Qty"] > 0)
].copy()

orders = (
    clean.groupby(["Order ID", "Fulfilment"], as_index=False)
    .agg(order_amount=("Amount", "sum"))
)

group_a = orders.loc[
    orders["Fulfilment"] == "Amazon", "order_amount"
]

group_b = orders.loc[
    orders["Fulfilment"] == "Merchant", "order_amount"
]

if len(group_a) < 2 or len(group_b) < 2:
    raise ValueError("Insufficient orders in one or both groups.")

if orders["Order ID"].duplicated().any():
    raise ValueError("An Order ID appears in multiple fulfilment groups.")

print("Valid shipped line records:", len(clean))
print("Unique orders:", len(orders))
print("Group A - Amazon orders:", len(group_a))
print("Group B - Merchant orders:", len(group_b))


# ==================================================
# 4. DESCRIPTIVE STATISTICS
# ==================================================

mean_a = float(group_a.mean())
mean_b = float(group_b.mean())

std_a = float(group_a.std(ddof=1))
std_b = float(group_b.std(ddof=1))

n_a = len(group_a)
n_b = len(group_b)

difference = mean_b - mean_a

percentage_difference = (
    difference / mean_a * 100 if mean_a != 0 else 0.0
)

print("\n===== ORDER-LEVEL GROUP COMPARISON =====")
print(f"Amazon average order value: INR {mean_a:.2f}")
print(f"Merchant average order value: INR {mean_b:.2f}")
print(f"Difference (Merchant - Amazon): INR {difference:.2f}")
print(f"Percentage difference: {percentage_difference:.2f}%")


# ==================================================
# 5. WELCH'S INDEPENDENT TWO-SAMPLE T-TEST
# ==================================================

test = stats.ttest_ind(
    group_b,
    group_a,
    equal_var=False,
    alternative="two-sided",
)

t_statistic = float(test.statistic)
p_value = float(test.pvalue)

se_a = std_a**2 / n_a
se_b = std_b**2 / n_b

standard_error = np.sqrt(se_a + se_b)

degrees_freedom = (
    (se_a + se_b) ** 2
    / (
        se_a**2 / (n_a - 1)
        + se_b**2 / (n_b - 1)
    )
)

critical_value = stats.t.ppf(0.975, degrees_freedom)

ci_lower = difference - critical_value * standard_error
ci_upper = difference + critical_value * standard_error


# ==================================================
# 6. EFFECT SIZE: COHEN'S D
# ==================================================

pooled_std = np.sqrt(
    (
        (n_a - 1) * std_a**2
        + (n_b - 1) * std_b**2
    )
    / (n_a + n_b - 2)
)

cohens_d = (
    difference / pooled_std if pooled_std > 0 else 0.0
)

significant = p_value < 0.05

print("\n===== STATISTICAL TEST =====")
print(f"T-statistic: {t_statistic:.4f}")
print(f"P-value: {p_value:.8g}")
print(f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")
print(f"Cohen's d: {cohens_d:.4f}")
print("Statistically significant:", significant)


# ==================================================
# 7. BUILD RESULTS AND REPORT
# ==================================================

summary = pd.DataFrame([
    {
        "group": "A - Amazon",
        "sample_size_orders": n_a,
        "mean_order_amount": mean_a,
        "std_order_amount": std_a,
    },
    {
        "group": "B - Merchant",
        "sample_size_orders": n_b,
        "mean_order_amount": mean_b,
        "std_order_amount": std_b,
    },
])

summary_path = OUTPUT_DIR / "group_summary.csv"
summary.to_csv(summary_path, index=False)

decision = (
    "Statistically significant difference detected."
    if significant
    else "No statistically significant difference detected."
)

report = f"""
# W9D3 - A/B Test Tracking with MLflow

## Experiment design

- Group A: Amazon-fulfilled shipped orders.
- Group B: Merchant-fulfilled shipped orders.
- Observation unit: Unique Order ID.
- Outcome: Total order amount (INR), summed across qualifying lines.
- Statistical test: Welch's independent two-sample t-test.
- Significance level: 0.05.

## Data preparation

Only records with a non-null Order ID, shipped status, Amazon or
Merchant fulfilment, positive Amount, and positive Qty were retained.

Qualifying line amounts were summed by Order ID and Fulfilment.
Each resulting order is one observation.

- Qualifying line records: {len(clean)}
- Unique orders: {len(orders)}
- Amazon orders: {n_a}
- Merchant orders: {n_b}

## Results

| Metric | Result |
|---|---:|
| Amazon average order value | INR {mean_a:.2f} |
| Merchant average order value | INR {mean_b:.2f} |
| Difference (Merchant - Amazon) | INR {difference:.2f} |
| Percentage difference | {percentage_difference:.2f}% |
| T-statistic | {t_statistic:.4f} |
| P-value | {p_value:.8g} |
| 95% CI lower | INR {ci_lower:.2f} |
| 95% CI upper | INR {ci_upper:.2f} |
| Cohen's d | {cohens_d:.4f} |

## Statistical interpretation

{decision}

The p-value is compared with the 0.05 significance level.
The confidence interval describes uncertainty around the estimated
difference in average order value.

## Limitations

This is an observational comparison, not a randomized A/B test.
Fulfilment type was not randomly assigned. Differences may reflect
product mix, order characteristics, customer choices, or other
confounding factors.

Order-level aggregation avoids treating multiple line records from
the same order as independent observations. It does not eliminate
all possible dependence or confounding.

The results do not establish a causal effect of fulfilment type.
"""

report_path = OUTPUT_DIR / "ab_test_report.md"
report_path.write_text(report, encoding="utf-8")


# ==================================================
# 8. TRACK A NEW ORDER-LEVEL RUN WITH MLFLOW
# ==================================================

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(
    run_name="order-level-amazon-vs-merchant"
) as run:

    mlflow.log_params({
        "dataset": DATA_PATH.name,
        "group_a": "Amazon",
        "group_b": "Merchant",
        "outcome": "Total order amount",
        "currency": "INR",
        "observation_unit": "Unique Order ID",
        "aggregation": "Sum Amount by Order ID and Fulfilment",
        "filter": "Shipped records, positive Amount and Qty",
        "statistical_test": "Welch independent t-test",
        "significance_level": 0.05,
        "experiment_type": "Observational comparison",
    })

    mlflow.log_metrics({
        "valid_line_records": len(clean),
        "unique_orders": len(orders),
        "group_a_sample_size_orders": n_a,
        "group_b_sample_size_orders": n_b,
        "group_a_mean_order_amount": mean_a,
        "group_b_mean_order_amount": mean_b,
        "mean_difference": difference,
        "percentage_difference": percentage_difference,
        "t_statistic": t_statistic,
        "p_value": p_value,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "cohens_d": float(cohens_d),
        "statistically_significant": int(significant),
    })

    mlflow.set_tags({
        "project": "Indian Business EDA",
        "lesson": "W9D3",
        "method": "Order-level observational comparison",
        "observation_unit": "Order ID",
        "status": "completed",
    })

    mlflow.log_artifact(str(summary_path))
    mlflow.log_artifact(str(report_path))

    print("\n===== MLFLOW TRACKING =====")
    print("Experiment:", EXPERIMENT_NAME)
    print("Run ID:", run.info.run_id)
    print("Tracking URI:", TRACKING_URI)


# ==================================================
# 9. FINAL OUTPUT
# ==================================================

print("\n===== W9D3 COMPLETED =====")
print("Group summary:", summary_path)
print("Analysis report:", report_path)
print("MLflow experiment:", EXPERIMENT_NAME)

