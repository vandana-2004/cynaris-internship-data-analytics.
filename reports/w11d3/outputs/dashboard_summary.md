# W11D3 Dashboard Summary

- Source rows: 128,975
- Source columns after removing index-only fields: 22
- Data period: 31 Mar 2022 to 29 Jun 2022
- Recorded Amount total: INR 78,592,678.30
- Amount coverage: 93.96%
- Missing Amount rows: 7,795
- Cancelled rows: 14.21%

## Dashboard components

1. Bar chart: top categories by recorded Amount.
2. Line chart: monthly recorded Amount.
3. Horizontal bar chart: distribution across all order statuses.
4. Table: top 10 states by recorded Amount.
5. Metric card: source rows, recorded Amount, and data-quality indicators.

## Interpretation limitations

- Recorded Amount is not verified net revenue or profit.
- Missing Amount values are excluded from amount aggregations.
- Cancelled rows are shown as recorded statuses, not as completed sales.
- The source data does not establish why orders were cancelled.
- Category rankings represent the complete available dataset period.

## Deployment status

This is a Python-generated dashboard preparation artifact.
Apache Superset has not been installed, configured, or deployed.
