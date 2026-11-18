# W11D5: Stakeholder Report — Five Business Insights

## Project Overview

This project analyzes the Indian Business Sales dataset and presents five actionable business insights for stakeholders.

The analysis uses Python, Pandas and Matplotlib to generate summary tables, visualizations and a stakeholder report.

## Dataset

- Source: `data/w8d3/indian_business_sales.csv`
- Total records: 128,975
- Date range: 31 March 2022 – 29 June 2022
- Recorded Amount: ₹78,592,678.30
- Valid Amount coverage: 93.96%

## Five Business Insights

1. **Category concentration:** Set and kurta together contribute 76.98% of recorded Amount.
2. **Fulfilment cancellation difference:** Merchant cancellation rate is 17.47%, compared with 12.79% for Amazon, a difference of 4.68 percentage points.
3. **Geographic concentration:** Maharashtra and Karnataka together contribute 30.30% of recorded Amount.
4. **Cancellation volume:** 18,332 records (14.21%) have Cancelled status.
5. **B2B comparison:** Average recorded Amount is ₹701.33 for B2B records versus ₹648.19 for non-B2B records, an observed difference of 8.20%.

## Business Recommendations

- Monitor inventory, demand and returns in the two largest product categories.
- Investigate merchant fulfilment processes and cancellation reasons.
- Monitor service levels and stock availability in Maharashtra and Karnataka.
- Segment cancellations by date, category, fulfilment and state.
- Validate the B2B average difference with additional data before designing a business strategy.

## Generated Deliverables

### Analysis script

`stakeholder_analysis.py`

### Stakeholder report

`outputs/stakeholder_report.md`

### Supporting CSV files

- `outputs/category_analysis.csv`
- `outputs/fulfilment_analysis.csv`
- `outputs/state_analysis.csv`
- `outputs/status_analysis.csv`
- `outputs/b2b_analysis.csv`
- `outputs/monthly_analysis.csv`

### Charts

- `outputs/charts/category_amount.png`
- `outputs/charts/fulfilment_cancellation.png`
- `outputs/charts/state_amount.png`
- `outputs/charts/order_status.png`

## Reproduction

Run from the repository root:

```powershell
& ".venv\Scripts\python.exe" "reports\w11d5\stakeholder_analysis.py"
```

## Validation

The script completed successfully with `VALIDATION: PASS`.

Verified:

- 128,975 dataset records
- ₹78,592,678.30 recorded Amount
- 93.96% Amount coverage
- 18,332 cancelled records
- Six CSV outputs
- Four chart outputs

## Limitations

- Recorded Amount is not independently verified net revenue or profit.
- Missing Amount values are excluded from Amount totals.
- Cancellation records do not establish confirmed lost revenue.
- The fulfilment comparison is descriptive and does not establish causation.
- March and June are partial months.
- B2B contains only 871 records and requires further validation.

## CIA Review

Two CIA interactions were completed. The questions, feedback, decisions and conclusions are documented in `cia_review.md`. The review outcome is **PASS WITH IMPROVEMENTS**.

## Git

Feature branch: `feat/w11d5-vandana`

Two meaningful commits will be recorded for this deliverable.