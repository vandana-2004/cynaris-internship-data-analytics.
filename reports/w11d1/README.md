# W11D1 - Data Storytelling: Structure and Narrative

## 1. Objective

Apply data storytelling principles to the Indian Business Sales dataset by combining descriptive analysis, visual evidence, business insights, and actionable recommendations.

## 2. Business Question

How can retail management use category performance, order status, and data quality evidence to identify areas that deserve further investigation?

## 3. Dataset

- Source: data/w8d3/indian_business_sales.csv
- Original dataset: 128,975 rows and 24 columns.
- Analytical dataset: 128,975 rows and 23 columns after excluding the unnamed column.
- Amount represents recorded order Amount, not confirmed net revenue or profit.

## 4. Methodology

1. Load and validate the existing dataset.
2. Exclude unnamed columns.
3. Convert Amount values to numeric and identify missing or invalid values.
4. Analyze category-level recorded Amount.
5. Summarize order-status distribution.
6. Calculate Amount completeness, mean, median, and skewness.
7. Create visualizations and a business narrative.

## 5. Key Findings

| Metric | Result |
|---|---:|
| Total rows | 128,975 |
| Valid Amount rows | 121,180 |
| Missing Amount values | 7,795 |
| Amount parsing errors | 0 |
| Amount coverage | 93.96% |
| Recorded Amount total | INR 78,592,678.30 |
| Leading category | Set |
| Leading category share | 49.88% |
| Top two category share | 76.98% |
| Cancelled rows | 18,332 |
| Cancelled row share | 14.21% |
| Mean recorded Amount | INR 648.56 |
| Median recorded Amount | INR 605.00 |
| Amount skewness | 0.8855 |

## 6. Business Insights

- Recorded Amount is concentrated in the Set and kurta categories.
- Cancelled rows represent 14.21% of all dataset rows.
- Missing Amount values reduce the completeness of Amount-based reporting.
- The mean exceeds the median, indicating a positively skewed distribution.

## 7. Business Recommendations

1. Investigate category-level demand and fulfilment patterns.
2. Examine cancellation patterns by category, region, and date.
3. Improve Amount data capture and validation.
4. Track mean and median together in recurring dashboards.

## 8. Visualizations

All charts are saved in the outputs directory.

- 01_category_concentration.png - Recorded Amount by category.
- 02_order_status.png - Order-status distribution.
- 03_amount_distribution.png - Amount distribution with mean and median.

## 9. Generated Deliverables

- storytelling_analysis.py
- outputs/story_report.md
- outputs/story_metrics.csv
- outputs/category_story.csv
- outputs/status_story.csv
- outputs/01_category_concentration.png
- outputs/02_order_status.png
- outputs/03_amount_distribution.png

## 10. Reproduction

Run from the repository root:

python reports/w11d1/storytelling_analysis.py

Required packages: pandas and matplotlib.

## 11. Limitations

- Amount is not confirmed net revenue or profit.
- Dataset rows are not necessarily unique customers or unique orders.
- Missing Amount values may affect comparisons and totals.
- Descriptive analysis does not establish causation.
- Recommendations require validation with additional business context.

## 12. Review and Submission Evidence

CIA mentor interactions, actual review feedback, work-log updates, and Git submission details will be recorded after completion.