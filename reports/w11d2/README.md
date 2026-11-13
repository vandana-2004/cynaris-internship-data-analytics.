# W11D2 - Building Executive Reports

## 1. Objective

Build an executive analytics report using Plotly and python-pptx, based on the Indian Business Sales dataset.

## 2. Dataset

- Source: `data/w8d3/indian_business_sales.csv`
- Original dimensions: 128,975 rows x 24 columns.
- Analytical dimensions: 128,975 rows x 23 columns.
- Recorded Amount is not confirmed net revenue or profit.

## 3. Technologies

- Python 3.13
- Pandas 3.0.5
- Plotly 7.1.0
- Matplotlib 3.11.1
- python-pptx 1.0.2

## 4. Implementation

The `executive_report.py` script:

1. Loads and validates the source dataset.
2. Cleans column names and excludes unnamed columns.
3. Calculates executive KPIs and business metrics.
4. Analyzes category, status, monthly and state performance, including category concentration.
5. Generates five interactive Plotly HTML charts, including a category Pareto chart.
6. Generates five Matplotlib images for PowerPoint.
7. Creates an executive summary in Markdown.
8. Creates an eight-slide PowerPoint presentation.
9. Validates the generated files and presentation slide count.

## 5. Key Findings

| Metric | Result |
|---|---:|
| Dataset rows | 128,975 |
| Recorded Amount | INR 78,592,678.30 |
| Mean recorded Amount | INR 648.56 |
| Median recorded Amount | INR 605.00 |
| Amount completeness | 93.96% |
| Missing Amount values | 7,795 |
| Leading category | Set |
| Leading category share | 49.88% |
| Top two category share | 76.98% |
| Cancelled rows | 18,332 |
| Cancelled row share | 14.21% |

## 6. Interactive Charts

- `outputs/charts/category_performance.html`
- `outputs/charts/category_pareto.html`
- `outputs/charts/order_status.html`
- `outputs/charts/monthly_performance.html`
- `outputs/charts/state_performance.html`

Open these HTML files in a browser to explore the interactive visualizations.

## 7. PowerPoint Report

`outputs/executive_report.pptx` contains eight slides:

1. Report introduction
2. Executive KPI overview
3. Category performance
4. Category Pareto analysis
5. Order-status analysis
6. Monthly performance
7. State performance
8. Recommendations and limitations

The Pareto analysis shows that the top two categories account for 76.98% of valid recorded Amount. The source label `Set` remains undefined and requires business confirmation.

## 8. Supporting Outputs

- `outputs/executive_summary.md`
- Four analytical CSV files.
- Five chart images, including `category_pareto.png`.
- Five interactive Plotly HTML files, including `category_pareto.html`.
- Eight-slide PowerPoint presentation.

## 9. Reproduction

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe .\reports\w11d2\executive_report.py
```

Required packages: pandas, plotly, matplotlib and python-pptx.

Plotly charts are exported as interactive HTML. Static images for the presentation are generated with Matplotlib, so Kaleido is not required.

## 10. Limitations

- Recorded Amount is not confirmed net revenue or profit.
- Rows are not necessarily unique orders or customers.
- Amount analysis excludes rows with missing values.
- Monthly totals depend on valid dates and Amount values.
- Descriptive analysis does not establish causation.
- Further business context is required before operational decisions.

## 11. CIA Review and Submission

CIA mentor interactions and review feedback are documented in `cia_review.md`. Git submission details will be recorded after submission.
