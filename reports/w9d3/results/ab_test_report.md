
# W9D3 - A/B Test Tracking with MLflow

## Experiment design

- Group A: Amazon-fulfilled shipped orders.
- Group B: Merchant-fulfilled shipped orders.
- Observation unit: Unique Order ID.
- Outcome: Total order amount (INR), summed across qualifying lines.
- Statistical test: Welch's independent two-sample t-test.
- Significance level: 0.05.

## Data preparation

Only records with a non-null Order ID, shipped status, Amazon or
Merchant fulfilment, positive Amount, and positive Qty were retained.

Qualifying line amounts were summed by Order ID and Fulfilment.
Each resulting order is one observation.

- Qualifying line records: 107160
- Unique orders: 99907
- Amazon orders: 71193
- Merchant orders: 28714

## Results

| Metric | Result |
|---|---:|
| Amazon average order value | INR 706.87 |
| Merchant average order value | INR 721.83 |
| Difference (Merchant - Amazon) | INR 14.96 |
| Percentage difference | 2.12% |
| T-statistic | 5.9126 |
| P-value | 3.3876344e-09 |
| 95% CI lower | INR 10.00 |
| 95% CI upper | INR 19.92 |
| Cohen's d | 0.0419 |

## Statistical interpretation

Statistically significant difference detected.

The p-value is compared with the 0.05 significance level.
The confidence interval describes uncertainty around the estimated
difference in average order value.

## Limitations

This is an observational comparison, not a randomized A/B test.
Fulfilment type was not randomly assigned. Differences may reflect
product mix, order characteristics, customer choices, or other
confounding factors.

Order-level aggregation avoids treating multiple line records from
the same order as independent observations. It does not eliminate
all possible dependence or confounding.

The results do not establish a causal effect of fulfilment type.
