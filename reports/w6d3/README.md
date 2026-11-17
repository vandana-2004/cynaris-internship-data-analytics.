# W6D3 - Apache Superset BI Dashboard from SQL Results

## 1. Objective

Create a stakeholder-facing Business Intelligence dashboard using SQL-aggregated Indian business sales data and Apache Superset through the hosted Preset platform.

The dashboard presents key business metrics and trends through six visualizations.

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
- `reports/w6d3/cancellation_analysis.sql` (supplementary analysis)

The Python script executes the original SQL aggregation queries, exports dashboard-ready CSV files and validates the results. The cancellation analysis was generated separately and does not modify the original Python pipeline.

### Run the SQL workflow

From the repository root:

```powershell
$root = "$HOME\Desktop\sql-fundamentals"
& "$root\.venv\Scripts\python.exe" "$root\reports\w6d3\sql_dashboard.py"
```

### Generated CSV datasets

The original workflow generates:

| File | Purpose |
|---|---|
| `category_amount.csv` | Recorded Amount by category |
| `monthly_amount.csv` | Monthly Recorded Amount trend |
| `order_status.csv` | Order-status distribution |
| `kpi_metrics.csv` | Overall Recorded Amount KPI |
| `state_amount.csv` | State-wise Recorded Amount |

Supplementary output:

- `cancellation_analysis.csv` - Cancelled vs non-cancelled recorded amounts and missing Amount values.

## 4. SQL Validation Results

The original SQL workflow completed successfully.

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

**Original workflow validation:** PASS.

### Supplementary cancellation analysis

| Order group | Rows | Recorded Amount (INR) | Missing Amount rows |
|---|---:|---:|---:|
| Cancelled | 18,332 | 6,919,284.30 | 7,566 |
| Non-Cancelled | 110,643 | 71,673,394.00 | 229 |

These figures group the source records by cancellation status. Non-cancelled Recorded Amount is not verified revenue.

## 5. Hosted Apache Superset Dashboard

The dashboard was created using the hosted Preset platform and its existing `File Uploads` database with the `main` schema.

**Dashboard name:** W6D3 - Indian Business SQL Dashboard

**Dashboard URL:**

https://de37bc60.us1a.app.preset.io/superset/dashboard/10/?native_filters_key=M9Z7S8s0yYL2WbQctWa07g

### Uploaded datasets

Six datasets were uploaded using unique W6D3 prefixes:

- `w6d3_category_amount`
- `w6d3_monthly_amount`
- `w6d3_order_status`
- `w6d3_kpi_metrics`
- `w6d3_state_amount`
- `w6d3_cancellation_analysis`

### Dashboard visualizations

| Chart | Visualization | Dataset | Metric |
|---|---|---|---|
| Recorded Amount by Category | Bar chart | `w6d3_category_amount` | SUM(Recorded_Amount) |
| Monthly Recorded Amount Trend | Line chart | `w6d3_monthly_amount` | SUM(Recorded_Amount) |
| Order Status Distribution | Pie chart | `w6d3_order_status` | SUM(Order_Count) |
| Total Recorded Amount KPI | Big Number | `w6d3_kpi_metrics` | MAX(Recorded_Amount_Total) |
| State-wise Recorded Amount | Table | `w6d3_state_amount` | State-level records |
| Recorded Amount by Cancellation Status | Bar chart | `w6d3_cancellation_analysis` | SUM(Recorded_Amount) |

The monthly chart uses ascending month order. The KPI uses MAX because the summary dataset contains one row.

## 6. Evidence

The following evidence files are maintained in `reports/w6d3/outputs/`:

- `W6D3_Preset_Indian_Business_SQL_Dashboard.png` - updated hosted Preset dashboard screenshot showing six charts.
- `looker_studio_dashboard.png` - existing Looker Studio dashboard image.
- `cancellation_analysis.csv` - supplementary cancellation analysis output.

Additional SQL evidence:

- `reports/w6d3/cancellation_analysis.sql`

The Preset screenshot was captured using Windows Snipping Tool.

## 7. Business Interpretation

- The dataset contains 128,975 source records.
- Total Recorded Amount is INR 78,592,678.30 for rows with available Amount values.
- Amount coverage is 93.96%.
- There are 7,795 rows with missing Amount values.
- The dataset contains 13 distinct order statuses.
- The monthly aggregation covers four months.
- The supplementary analysis separates recorded amounts associated with cancelled and non-cancelled statuses.

## 8. Data Interpretation and Limitations

- Recorded Amount must not be interpreted as verified net revenue or profit.
- The overall KPI includes amounts from cancelled-status rows.
- Rows with missing Amount values are excluded from amount-based aggregations.
- Order-status counts include all source rows, including cancelled orders.
- Non-cancelled Recorded Amount is not proof of completed or realized revenue.
- The state aggregation contains 69 rows because one state has no non-null Amount available for the amount-based aggregation.
- Dashboard access depends on Preset workspace permissions and service availability.

## 9. Review and Improvement Status

- CIA mentor review: Completed once, based on supplied summaries and metadata.
- The CIA review did not visually inspect or interact with the hosted Preset dashboard.
- No explicit PASS, PASS WITH IMPROVEMENTS or FAIL verdict was provided.
- Feedback highlighted the need to distinguish total Recorded Amount from non-cancelled Recorded Amount.
- Supplementary cancellation analysis was added and a sixth chart was added to the existing W6D3 dashboard.
- Human peer review: Pending; no peer approval is claimed.

## 10. Completion Summary

Completed:

- SQL query implementation and validation.
- Five original dashboard-ready CSV exports.
- Supplementary cancellation SQL and CSV analysis.
- Source-to-SQL row-count validation.
- Recorded Amount and missing-value validation.
- Six uploaded Preset datasets.
- Six Superset dashboard visualizations.
- Hosted dashboard creation and screenshot evidence.
- One CIA mentor review and feedback-based improvement.

**Overall status:** SQL processing, output validation, supplementary cancellation analysis and hosted Preset dashboard completed. Human peer review remains pending.