from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[2]
W11D3 = ROOT / "reports" / "w11d3"
OUTPUTS = W11D3 / "outputs"
CHARTS = OUTPUTS / "charts"

checks = []

def check(label, condition, detail=""):
    checks.append((label, bool(condition), detail))

def csv_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

# Reused source and dashboard evidence
source = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
screenshot = ROOT / "W11D3_dashboard.png"
preview = OUTPUTS / "images" / "dashboard_preview.png"
dashboard = OUTPUTS / "dashboard.html"

check("Source dataset exists", source.is_file())
check("Published dashboard screenshot exists", screenshot.is_file())
check("Python dashboard preview exists", preview.is_file())
check("Interactive dashboard exists", dashboard.is_file())

# Four local chart outputs
chart_files = [
    "category_bar.html",
    "monthly_line.html",
    "order_status_bar.html",
    "state_amount_table.html",
]
for name in chart_files:
    path = CHARTS / name
    check(f"Chart file: {name}", path.is_file() and path.stat().st_size > 0)

# Four aggregated CSV outputs
csv_files = [
    "category_amount.csv",
    "monthly_amount.csv",
    "order_status.csv",
    "state_amount.csv",
]
for name in csv_files:
    path = OUTPUTS / name
    check(f"Summary CSV: {name}", path.is_file() and path.stat().st_size > 0)

# Validate status aggregation covers the source row count
status_path = OUTPUTS / "order_status.csv"
if status_path.is_file():
    try:
        statuses = csv_rows(status_path)
        count_column = next(
            (column for column in ("Orders", "Count", "count", "Order_Count", "order_count")
             if statuses and column in statuses[0]),
            None,
        )
        total = sum(int(float(row[count_column])) for row in statuses) if count_column else 0
        check(
            "Order-status aggregation totals 128,975 rows",
            total == 128975,
            f"Observed total: {total}; statuses: {len(statuses)}",
        )
        check(
            "All 13 order statuses represented",
            len(statuses) == 13,
            f"Observed statuses: {len(statuses)}",
        )
    except (ValueError, KeyError, OSError) as error:
        check("Order-status CSV validation", False, str(error))
else:
    check("Order-status CSV validation", False, "File missing")

# The fifth component is a metric/KPI card in the dashboard.
if dashboard.is_file():
    html = dashboard.read_text(encoding="utf-8", errors="replace").lower()
    check("Dashboard includes metric/KPI content", "recorded amount" in html or "total amount" in html)
else:
    check("Dashboard includes metric/KPI content", False, "Dashboard HTML missing")

print("\nW11D4 SELF-SERVE BI REUSE AUDIT")
print("=" * 48)
for label, passed, detail in checks:
    print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    if detail:
        print(f"       {detail}")

passed_count = sum(result for _, result, _ in checks)
failed_count = len(checks) - passed_count
print("-" * 48)
print(f"Passed: {passed_count}/{len(checks)}")
print(f"Failed: {failed_count}")

sys.exit(1 if failed_count else 0)
