# W11D2 — Executive Analytics Report

## Executive overview

This report summarizes 128,975 dataset rows from the Indian Business Sales dataset.

| KPI | Result |
|---|---:|
| Dataset rows | 128,975 |
| Recorded Amount total | INR 78,592,678.30 |
| Mean recorded Amount per valid row | INR 648.56 |
| Median recorded Amount per valid row | INR 605.00 |
| Amount completeness | 93.96% |
| Cancelled rows | 18,332 (14.21%) |

## Key findings

1. **Category concentration:** Set leads with 49.88% of valid recorded Amount. The top two categories account for 76.98%, indicating concentration worth monitoring. The business meaning of the source label "Set" requires confirmation.
2. **Order status:** 18,332 rows (14.21%) have Cancelled status. This is a descriptive observation, not an explanation of cancellation causes.
3. **Data quality:** 7,795 Amount values are originally missing. Valid Amount coverage is 93.96%.
4. **Typical recorded Amount:** Mean INR 648.56; median INR 605.00.

## Recommendations

- Monitor the top-two-category concentration (76.98% of valid recorded Amount) and assess diversification options with additional business context.
- Confirm the official business definition of the "Set" category before assigning it a product or bundle meaning.
- Investigate category-level demand, stock availability and fulfilment patterns.
- Examine cancellations by category, state and date before proposing operational changes.
- Improve Amount field completeness and validation.
- Monitor monthly recorded Amount and state-level distribution.
- Present mean and median together to avoid relying on one summary statistic.

## Limitations

- Recorded Amount is not confirmed net revenue or profit.
- Dataset rows are not necessarily unique orders or customers.
- Amount-based analysis excludes rows with missing Amount.
- Monthly trends reflect the available dataset period only.
- Descriptive analysis does not establish causation.
- State and category comparisons require additional operational context.

## Generated outputs

- Five interactive Plotly HTML charts, including a category Pareto chart.
- Five PowerPoint-ready chart images.
- Four supporting CSV analytical tables.
- Eight-slide executive presentation.
