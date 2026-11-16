# W6D3 - Apache Superset BI Dashboard from SQL Results

## 1. Objective

Create a stakeholder-facing Business Intelligence dashboard using SQL-aggregated Indian business sales data and Apache Superset through the hosted Preset platform.

The dashboard presents key business metrics and trends through five visualizations.

## 2. Dataset Overview

- **Source:** `data/w8d3/indian_business_sales.csv`
- **Rows:** 128,975
- **Columns:** 24
- **Date range:** 31 March 2022 - 29 June 2022
- **Distinct categories:** 9
- **Distinct order statuses:** 13
- **Distinct states:** 70

## 3. SQL Implementation

The SQL workflow is implemented using:

- `reports/w6d3/sql_dashboard.py`
- `reports/w6d3/dashboard_queries.sql`

The Python script executes the SQL aggregation queries, exports dashboard-ready CSV files and validates the results.

### Run the SQL workflow

From the repository root:

```powershell
$root = "$HOME\Desktop\sql-fundamentals"
& "$root\.venv\Scripts\python.exe" "$root\reports\w6d3\sql_dashboard.py"
```

### Generated CSV datasets

The following files are generated in `reports/w6d3/outputs/`:

| File | Purpose |
|---|---|
| `category_amount.csv` | Recorded Amount by category |
| `monthly_amount.csv` | Monthly Recorded Amount trend |
| `order_status.csv` | Order-status distribution |
| `kpi_metrics.csv` | Overall Recorded Amount KPI |
| `state_amount.csv` | State-wise Recorded Amount |

## 4. SQL Validation Results

The SQL workflow completed successfully.

| Validation | Result |
|---|---:|
| Source rows | 128,975 |
| SQL processed rows | 128,975 |
| Recorded Amount total | INR 78,592,678.30 |
| Amount coverage | 93.96% |
| Missing Amount rows | 7,795 |
| Cancelled-status rows | 18,332 |
| Distinct order statuses | 13 |
| Distinct categories | 9 |
| Distinct states | 70 |

### SQL output row counts

| Output dataset | Rows |
|---|---:|
| Category | 9 |
| Monthly | 4 |
| Order status | 13 |
| State | 69 |
| KPI | 1 |

**Validation status:** PASS - all expected dataset checks succeeded.

## 5. Hosted Apache Superset Dashboard

The dashboard was created using the hosted Preset platform and its existing `File Uploads` database with the `main` schema.

**Dashboard name:** W6D3 - Indian Business SQL Dashboard

**Dashboard URL:**

https://de37bc60.us1a.app.preset.io/superset/dashboard/10/?native_filters_key=M9Z7S8s0yYL2WbQctWa07g

### Uploaded datasets

Five separate datasets were uploaded using unique W6D3 prefixes to avoid conflicts with existing W11D3 datasets.

- `w6d3_category_amount`
- `w6d3_monthly_amount`
- `w6d3_order_status`
- `w6d3_kpi_metrics`
- `w6d3_state_amount`

### Dashboard visualizations

| Chart | Visualization | Dataset | Metric |
|---|---|---|---|
| Recorded Amount by Category | Bar chart | `w6d3_category_amount` | SUM(Recorded_Amount) |
| Monthly Recorded Amount Trend | Line chart | `w6d3_monthly_amount` | SUM(Recorded_Amount) |
| Order Status Distribution | Pie chart | `w6d3_order_status` | SUM(Order_Count) |
| Total Recorded Amount KPI | Big Number | `w6d3_kpi_metrics` | MAX(Recorded_Amount_Total) |
| State-wise Recorded Amount | Table | `w6d3_state_amount` | State-level records |

The monthly chart uses ascending month order. The KPI uses MAX because the summary dataset contains one row. The state table displays State, Order_Count and Recorded_Amount.

## 6. Evidence

The following evidence files are maintained in `reports/w6d3/outputs/`:

- `W6D3_Preset_Indian_Business_SQL_Dashboard.png` - hosted Preset dashboard screenshot.
- `looker_studio_dashboard.png` - existing Looker Studio dashboard image.

The Preset screenshot was captured using Windows Snipping Tool.

## 7. Business Interpretation

The dashboard provides an overview of recorded sales amounts across categories, months, order statuses and states.

Key observations:

- The dataset contains 128,975 source records.
- Recorded Amount totals INR 78,592,678.30 for rows with available Amount values.
- Amount coverage is 93.96%.
- There are 7,795 rows with missing Amount values.
- The order-status dataset contains 13 distinct statuses.
- The monthly aggregation covers four months.

## 8. Data Interpretation and Limitations

- Recorded Amount should not be interpreted as verified net revenue or profit.
- Rows with missing Amount values are excluded from amount-based aggregations.
- Order-status counts include all source rows, including cancelled orders.
- The state aggregation contains 69 rows because one state has no non-null Amount available for the amount-based aggregation.
- The KPI represents the total Recorded Amount from the available Amount values.
- Dashboard access depends on Preset workspace permissions and service availability.

## 9. Review and Improvement Status

- CIA mentor review: Pending.
- Peer review: Pending.
- Feedback-based improvement: Pending.

These activities will be documented after they have actually been completed.

## 10. Completion Summary

Completed:

- SQL query implementation.
- Five dashboard-ready CSV exports.
- Source-to-SQL row-count validation.
- Recorded Amount and missing-value validation.
- Five uploaded Preset datasets.
- Five Superset dashboard visualizations.
- Hosted dashboard creation.
- Dashboard screenshot evidence.

**Overall status:** SQL processing, output validation and hosted Preset dashboard creation completed. Review activities remain pending.