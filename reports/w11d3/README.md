
# W11D3 - Apache Superset BI Dashboard Preparation

## Objective

Prepare a business intelligence dashboard using the Indian Business Sales dataset, with five dashboard components and supporting analytical outputs.

## Dataset

- Source: `data/w8d3/indian_business_sales.csv`
- Source rows: 128,975
- Analytical columns: 22 after removing index-only fields
- Data period: 31 March 2022 to 29 June 2022
- Recorded Amount: INR 78,592,678.30
- Amount coverage: 93.96%
- Missing Amount rows: 7,795
- Distinct order statuses: 13

## Dashboard Components

1. Bar chart - top categories by recorded Amount, with dataset-period context.
2. Line chart - monthly recorded Amount.
3. Horizontal bar chart - distribution across all 13 order statuses.
4. Table - top 10 states by recorded Amount.
5. Metric card - source row count, recorded Amount, and Amount coverage.

## Reproduction

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe .\reports\w11d3\dashboard.py
```

## Generated Deliverables

- `outputs/dashboard.html` - combined interactive dashboard.
- `outputs/dashboard_summary.md` - summary and interpretation limitations.
- `outputs/images/dashboard_preview.png` - static dashboard preview.
- `outputs/charts/category_bar.html` - category bar chart.
- `outputs/charts/monthly_line.html` - monthly trend chart.
- `outputs/charts/order_status_bar.html` - all-status horizontal bar chart.
- `outputs/charts/state_amount_table.html` - state summary table.
- `outputs/category_amount.csv`
- `outputs/monthly_amount.csv`
- `outputs/order_status.csv`
- `outputs/state_amount.csv`

## Validation

- Python compilation completed successfully.
- Dashboard generation completed successfully.
- All 11 expected deliverables were generated and checked for non-empty files.
- The order-status summary contains all 13 distinct statuses.
- The status counts sum to 128,975 source rows.
- Interactive HTML dashboard was previously opened and visually checked.
- PNG preview was opened; some components may be less visible at preview scale.

## Stakeholder Sharing

The hosted stakeholder dashboard is published in the Preset workspace:

**Dashboard:** [W11D3 Stakeholder Dashboard](https://de37bc60.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=XVAbs_qn33MclWhO94eqZw)

The hosted dashboard contains five saved components:
- Category-wise Amount Analysis (bar chart)
- Monthly Amount Trend (line chart)
- Order Status Distribution (pie chart)
- State-wise Amount Summary (table)
- Total Amount KPI Summary (Big Number, displayed as 39.4M)

Stakeholder access depends on Preset workspace permissions and service availability.

The local screenshot `W11D3_dashboard.png` is a Windows Snipping Tool capture, not a native Superset PNG export. The Python-generated interactive HTML and PNG preview remain separate local deliverables.

## Interpretation Limitations

- Recorded Amount is not verified net revenue or profit.
- Missing Amount values are excluded from amount aggregations.
- Cancelled rows represent recorded statuses, not completed sales.
- The source data does not establish why orders were cancelled.
- The `Set` category is retained as a source label; its business meaning is not assumed.
- The dataset covers approximately three months, not a full year.

## Deployment Status

- Python-generated dashboard preparation and local output validation: complete.
- Hosted Preset workspace database uploads and Superset chart creation: complete.
- `W11D3 Stakeholder Dashboard`: published in the hosted Preset workspace.
- Five saved dashboard components: bar, line, pie, table and Big Number KPI.
- Published dashboard link and local screenshot are documented above.
- The screenshot is a Snipping Tool capture; a native Superset PNG export is not claimed.
- Stakeholder access remains subject to Preset workspace permissions and service availability.
