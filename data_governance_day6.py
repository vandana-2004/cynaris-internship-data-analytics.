
from pathlib import Path
import html
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "python-pandas" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "data_governance_output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Use the actual columns in the CSV.
required_columns = {
    "order_id", "customer", "region",
    "category", "sales", "quantity"
}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing expected columns: {sorted(missing_columns)}")

checks = []

def add_check(name, passed, details):
    checks.append({
        "check": name,
        "passed": bool(passed),
        "details": str(details),
    })

# Eight quality checks
add_check(
    "1. Required values complete",
    df[["order_id", "customer", "region", "category",
        "sales", "quantity"]].notna().all().all(),
    "Required fields should not contain missing values.",
)

add_check(
    "2. Order IDs unique",
    df["order_id"].is_unique,
    "Each order_id should occur only once.",
)

add_check(
    "3. Sales non-negative",
    pd.to_numeric(df["sales"], errors="coerce").ge(0).all(),
    "Sales must be numeric and at least zero.",
)

add_check(
    "4. Quantity positive",
    pd.to_numeric(df["quantity"], errors="coerce").gt(0).all(),
    "Quantity must be numeric and greater than zero.",
)

add_check(
    "5. Sales numeric",
    pd.to_numeric(df["sales"], errors="coerce").notna().all(),
    "Every sales value must be numeric.",
)

add_check(
    "6. Quantity numeric",
    pd.to_numeric(df["quantity"], errors="coerce").notna().all(),
    "Every quantity value must be numeric.",
)

add_check(
    "7. Region values valid",
    df["region"].astype("string").str.strip().ne("").all(),
    "Region must not be blank.",
)

add_check(
    "8. Category values valid",
    df["category"].astype("string").str.strip().ne("").all(),
    "Category must not be blank.",
)

results = pd.DataFrame(checks)
results.to_csv(OUTPUT_DIR / "validation_results.csv", index=False)

# Create a separate copy with three deliberate errors.
bad_df = df.copy()

bad_df.loc[bad_df.index[0], "order_id"] = bad_df.loc[
    bad_df.index[1], "order_id"
]
bad_df.loc[bad_df.index[0], "sales"] = -100
bad_df.loc[bad_df.index[0], "quantity"] = 0

# Verify that our checks catch all three injected errors.
injected_errors_caught = {
    "duplicate order_id": not bad_df["order_id"].is_unique,
    "negative sales": not pd.to_numeric(
        bad_df["sales"], errors="coerce"
    ).ge(0).all(),
    "zero quantity": not pd.to_numeric(
        bad_df["quantity"], errors="coerce"
    ).gt(0).all(),
}

pd.DataFrame([
    {"injected_error": name, "caught": caught}
    for name, caught in injected_errors_caught.items()
]).to_csv(OUTPUT_DIR / "injected_error_tests.csv", index=False)

# Produce a readable HTML report.
rows = []
for result in checks:
    status = "PASS" if result["passed"] else "FAIL"
    rows.append(
        "<tr>"
        f"<td>{html.escape(result['check'])}</td>"
        f"<td>{status}</td>"
        f"<td>{html.escape(result['details'])}</td>"
        "</tr>"
    )

report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Day 6 Data Quality Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 30px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
th {{ background: #eee; }}
</style>
</head>
<body>
<h1>Data Governance — Quality Report</h1>
<p>Dataset: python-pandas/sales_data.csv</p>
<p>Rows checked: {len(df)}</p>
<p>Passing checks: {int(results['passed'].sum())} of {len(results)}</p>
<table>
<tr><th>Check</th><th>Status</th><th>Details</th></tr>
{''.join(rows)}
</table>
<h2>Intentional Error Tests</h2>
<p>Errors caught: {sum(injected_errors_caught.values())} of 3</p>
</body>
</html>
"""

(OUTPUT_DIR / "data_quality_report.html").write_text(
    report, encoding="utf-8"
)

print(results.to_string(index=False))
print("\nIntentional error tests:", injected_errors_caught)
print(f"\nReports saved to: {OUTPUT_DIR}")
