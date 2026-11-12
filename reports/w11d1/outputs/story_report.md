# W11D1 — Indian Retail Sales: A Data Story

## Executive summary

Recorded Amount is concentrated in a small number of product categories.
Order-status data also identifies a substantial cancelled-row segment.
However, incomplete Amount data means the findings must be interpreted
with care.

## Business question

How can retail management use category performance, order status and
data quality evidence to identify areas that deserve further investigation?

## Finding 1 — Category concentration

The leading category is **Set**, representing
**49.88%** of recorded Amount.
The top two categories together represent **76.98%**.

**Business implication:** Management could examine category-level
availability, fulfilment and demand patterns before making inventory
or merchandising decisions.

## Finding 2 — Order-status visibility

There are **18,332** rows with status Cancelled,
representing **14.21%** of all rows.

**Business implication:** Review cancellation patterns by product,
region and time period to identify where further operational analysis
may be useful. This descriptive result does not explain the cause
of cancellations.

## Finding 3 — Amount data completeness

There are **7,795** originally missing
Amount values and **0** non-missing values
that could not be converted to numbers.
Valid Amount coverage is **93.96%**.

**Business implication:** Improve data capture and validation before
using Amount-based metrics for operational decisions.

## Finding 4 — Distribution of recorded Amount

The mean recorded Amount is **INR 648.56**,
while the median is **INR 605.00**.
Skewness is **0.8855**.

**Business implication:** Report both mean and median. The mean alone
may not represent a typical row when the distribution is skewed.

## Recommended next steps

1. Investigate category-level demand and fulfilment together.
2. Break down cancelled rows by category, region and date.
3. Improve completeness checks for Amount before reporting.
4. Track mean and median together in recurring business dashboards.

## Limitations

- Amount is recorded order Amount, not confirmed net revenue or profit.
- Rows are not necessarily unique customers or unique orders.
- Missing Amount values may affect comparisons and totals.
- The analysis is descriptive and does not establish causation.
- Recommendations require validation with additional business context.

## Conclusion

The dataset suggests category concentration, a meaningful cancelled-row
segment and incomplete Amount capture. These findings provide a starting
point for targeted investigation, not proof of the underlying causes.
