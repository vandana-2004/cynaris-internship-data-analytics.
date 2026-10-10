

"""
Great Expectations validation for Week 2 Day 6.
Validates sales data and tests intentional data quality errors.
Compatible with Great Expectations 1.x.
"""

from pathlib import Path

import great_expectations as gx
import pandas as pd


# --------------------------------------------------
# 1. Load dataset and prepare output directory
# --------------------------------------------------

DATA_PATH = Path("python-pandas") / "sales_data.csv"
OUTPUT_DIR = Path("data_governance_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# --------------------------------------------------
# 2. Create one Great Expectations context
# --------------------------------------------------

context = gx.get_context(mode="ephemeral")

datasource = context.data_sources.add_pandas(
    name="sales_data_source"
)


# --------------------------------------------------
# 3. Define nine expectations
# --------------------------------------------------

suite = gx.ExpectationSuite(
    name="sales_data_quality_suite",
    expectations=[],
)
suite = context.suites.add(suite)

required_columns = [
    "order_id",
    "customer",
    "region",
    "category",
    "sales",
    "quantity",
]

# Six columns must not contain null values.
for column in required_columns:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column=column
        )
    )

# Order IDs must be unique.
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="order_id"
    )
)

# Sales must be non-negative.
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="sales",
        min_value=0,
    )
)

# Quantity must be at least one.
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="quantity",
        min_value=1,
    )
)


# --------------------------------------------------
# 4. Validation helper
# --------------------------------------------------

def validate_dataframe(dataframe, asset_suffix):
    """Validate a DataFrame using the shared context and suite."""

    asset = datasource.add_dataframe_asset(
        name=f"sales_asset_{asset_suffix}"
    )

    batch_definition = (
        asset.add_batch_definition_whole_dataframe(
            f"sales_batch_{asset_suffix}"
        )
    )

    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": dataframe}
    )

    return batch.validate(suite)


# --------------------------------------------------
# 5. Validate the original dataset
# --------------------------------------------------

print("\nGREAT EXPECTATIONS - ORIGINAL DATA")
print("=" * 50)

results = validate_dataframe(df, "original")

validation_rows = []

for result in results.results:
    expectation_name = result.expectation_config.type
    column = result.expectation_config.kwargs.get(
        "column", ""
    )
    status = "PASS" if result.success else "FAIL"

    print(f"{status}: {expectation_name} ({column})")

    validation_rows.append(
        {
            "expectation": expectation_name,
            "column": column,
            "success": result.success,
        }
    )

results_path = OUTPUT_DIR / "great_expectations_results.csv"

pd.DataFrame(validation_rows).to_csv(
    results_path,
    index=False,
)

print("=" * 50)
print(
    f"Overall result: {'PASS' if results.success else 'FAIL'}"
)
print(f"Rows checked: {len(df)}")
print(f"Columns checked: {len(required_columns)}")
print(f"Results saved to: {results_path}")


# --------------------------------------------------
# 6. Test three intentional data quality errors
# --------------------------------------------------

print("\nINTENTIONAL ERROR DETECTION TESTS")
print("=" * 50)

test_cases = [
    ("duplicate_order_id", "order_id", "unique"),
    ("negative_sales", "sales", "non_negative"),
    ("zero_quantity", "quantity", "positive"),
]

error_test_rows = []

for test_name, column, rule in test_cases:
    test_df = df.copy()

    # Inject one error into a separate copy of the dataset.
    if rule == "unique":
        test_df.loc[
            test_df.index[-1], column
        ] = test_df.iloc[0][column]

    elif rule == "non_negative":
        test_df.loc[test_df.index[0], column] = -100

    elif rule == "positive":
        test_df.loc[test_df.index[0], column] = 0

    test_results = validate_dataframe(
        test_df,
        test_name,
    )

    # Select the expectation that should catch this error.
    if rule == "unique":
        expected_type = "expect_column_values_to_be_unique"
    else:
        expected_type = "expect_column_values_to_be_between"

    matching_results = [
        result
        for result in test_results.results
        if (
            result.expectation_config.type == expected_type
            and result.expectation_config.kwargs.get("column")
            == column
        )
    ]

    detected = (
        bool(matching_results)
        and not all(
            result.success for result in matching_results
        )
    )

    status = "DETECTED" if detected else "NOT DETECTED"
    print(f"{status}: {test_name}")

    error_test_rows.append(
        {
            "test": test_name,
            "column": column,
            "detected": detected,
        }
    )


# --------------------------------------------------
# 7. Save error test results
# --------------------------------------------------

error_test_path = (
    OUTPUT_DIR / "great_expectations_error_tests.csv"
)

pd.DataFrame(error_test_rows).to_csv(
    error_test_path,
    index=False,
)

all_errors_detected = all(
    row["detected"] for row in error_test_rows
)

print("=" * 50)
print(
    "All three errors detected: "
    f"{'YES' if all_errors_detected else 'NO'}"
)
print(f"Error test results saved to: {error_test_path}")

# --------------------------------------------------
# 8. Generate an HTML validation report
# --------------------------------------------------

html_report_path = (
    OUTPUT_DIR / "great_expectations_validation_report.html"
)

validation_table = pd.DataFrame(validation_rows).to_html(
    index=False,
    escape=True,
    border=0,
    classes="report-table",
)

error_table = pd.DataFrame(error_test_rows).to_html(
    index=False,
    escape=True,
    border=0,
    classes="report-table",
)

overall_status = "PASS" if results.success else "FAIL"

error_status = (
    "PASS" if all_errors_detected else "FAIL"
)

html_report = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Great Expectations Validation Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    max-width: 1000px;
    margin: 30px auto;
    padding: 20px;
    color: #222;
    line-height: 1.6;
}}
h1, h2 {{ color: #243b53; }}
.summary {{
    padding: 15px;
    background: #f2f5f8;
    border-radius: 8px;
    margin-bottom: 20px;
}}
.report-table {{
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0 30px;
}}
.report-table th, .report-table td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}
.report-table th {{ background: #e8edf2; }}
footer {{ margin-top: 30px; color: #555; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>Great Expectations Validation Report</h1>

<div class="summary">
    <p><strong>Dataset:</strong> {DATA_PATH.as_posix()}</p>
    <p><strong>Rows checked:</strong> {len(df)}</p>
    <p><strong>Columns checked:</strong> {len(required_columns)}</p>
    <p><strong>Original validation:</strong> {overall_status}</p>
    <p><strong>Expectations passed:</strong>
       {sum(row["success"] for row in validation_rows)}
       of {len(validation_rows)}</p>
    <p><strong>Intentional error tests:</strong> {error_status}</p>
    <p><strong>Errors detected:</strong>
       {sum(row["detected"] for row in error_test_rows)}
       of {len(error_test_rows)}</p>
</div>

<h2>Original Dataset Checks</h2>
{validation_table}

<h2>Intentional Error Detection Tests</h2>
{error_table}

<h2>Interpretation</h2>
<p>
The original dataset passed its configured Great Expectations checks.
Separate test copies were used to verify detection of a duplicate order ID,
negative sales, and zero quantity. These tests do not modify the source CSV.
</p>

<footer>
Generated by great_expectations_day6.py
</footer>
</body>
</html>
"""

html_report_path.write_text(
    html_report,
    encoding="utf-8",
)

print(f"HTML report saved to: {html_report_path}")
