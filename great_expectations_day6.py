"""
Great Expectations validation for Week 2 Day 6.
Validates sales data using Great Expectations 1.x.
"""

from pathlib import Path

import great_expectations as gx
import pandas as pd


# Load the dataset
DATA_PATH = Path("python-pandas") / "sales_data.csv"
df = pd.read_csv(DATA_PATH)

# Create a temporary Great Expectations context
context = gx.get_context(mode="ephemeral")

# Register the pandas DataFrame as a data asset
datasource = context.data_sources.add_pandas(
    name="sales_data_source"
)
asset = datasource.add_dataframe_asset(
    name="sales_data"
)
batch_definition = asset.add_batch_definition_whole_dataframe(
    "sales_batch"
)
batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

# Define the data quality expectations
suite = gx.ExpectationSuite(name="sales_data_quality_suite")

required_columns = [
    "order_id",
    "customer",
    "region",
    "category",
    "sales",
    "quantity",
]

for column in required_columns:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column=column
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="order_id"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="sales",
        min_value=0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="quantity",
        min_value=1,
    )
)

# Run the validation
results = batch.validate(suite)

print("\nGREAT EXPECTATIONS — DATA QUALITY REPORT")
print("=" * 45)

for item in results.results:
    expectation_name = item.expectation_config.type
    passed = item.success
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {expectation_name}")

print("=" * 45)
print(f"Overall result: {'PASS' if results.success else 'FAIL'}")
print(f"Rows checked: {len(df)}")
print(f"Columns checked: {len(required_columns)}")

# Save detailed validation results
output_dir = Path("data_governance_output")
output_dir.mkdir(parents=True, exist_ok=True)

validation_rows = []

for item in results.results:
    validation_rows.append(
        {
            "expectation": item.expectation_config.type,
            "success": item.success,
        }
    )

results_df = pd.DataFrame(validation_rows)
results_path = output_dir / "great_expectations_results.csv"
results_df.to_csv(results_path, index=False)

print(f"Validation results saved to: {results_path}")