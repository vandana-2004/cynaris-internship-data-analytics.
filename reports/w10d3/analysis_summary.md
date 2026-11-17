# W10D3 - Anomaly Detection Analysis

## 1. Objective

Identify unusual business transaction observations using statistical methods and Isolation Forest.

## 2. Dataset

- Dataset: `data\w8d3\indian_business_sales.csv`
- Total records: 128,975
- Missing Amount records: 7,795
- Missing Qty records: 0
- Valid positive Amount and Qty model records: 113,701
- Date range: 2022-03-31 00:00:00 to 2022-06-29 00:00:00

## 3. Detection methodology

### IQR

- Lower bound: Q1 - 1.5 x IQR, constrained to non-negative values.
- Upper bound: Q3 + 1.5 x IQR.
- Calculated bounds: INR 0.00 to INR 1296.50.

### Z-score

- Threshold: absolute Z-score greater than 3.0.
- Mean Amount: INR 648.56.
- Standard deviation: INR 281.21.

### Isolation Forest

- Features: Amount and Qty.
- Contamination assumption: 2%.
- Estimators: 200.
- Random state: 42.
- Model fitted only on records with positive Amount and Qty.

## 4. Results

| method           |   anomaly_count |   percentage_of_dataset |
|:-----------------|----------------:|------------------------:|
| IQR              |            3600 |                   2.791 |
| Z-score          |             784 |                   0.608 |
| Isolation Forest |            2269 |                   1.759 |

- Records flagged by at least one method: 3,770.
- Records flagged by all three methods: 774.

## 5. Status-level interpretation

| Status                        |   total_records |   flagged_records |   average_amount |   flagged_percentage |
|:------------------------------|----------------:|------------------:|-----------------:|---------------------:|
| Cancelled                     |           18332 |               242 |          642.698 |                 1.32 |
| Pending                       |             658 |                27 |          655.901 |                 4.1  |
| Pending - Waiting for Pick Up |             281 |                 7 |          683.765 |                 2.49 |
| Shipped                       |           77804 |              2471 |          648.542 |                 3.18 |
| Shipped - Damaged             |               1 |                 0 |         1136     |                 0    |
| Shipped - Delivered to Buyer  |           28769 |               905 |          648.476 |                 3.15 |
| Shipped - Lost in Transit     |               5 |                 0 |          399.4   |                 0    |
| Shipped - Out for Delivery    |              35 |                 4 |          770.6   |                11.43 |
| Shipped - Picked Up           |             973 |                38 |          679.601 |                 3.91 |
| Shipped - Rejected by Buyer   |              11 |                 0 |          663.182 |                 0    |
| Shipped - Returned to Seller  |            1953 |                69 |          651.099 |                 3.53 |
| Shipped - Returning to Seller |             145 |                 7 |          742.207 |                 4.83 |
| Shipping                      |               8 |                 0 |          nan     |                 0    |

## 6. Business interpretation

IQR identifies observations beyond the central spread of transaction amounts. Z-score identifies observations far from the overall mean. Isolation Forest evaluates combinations of Amount and Qty.

The methods are complementary. A transaction flagged by one method is a candidate for review, not proof of fraud, data corruption, or business error. Status, product category, fulfilment and order context should be checked before taking action.

The 2% Isolation Forest contamination value is a modelling assumption, not a measured fraud rate.

## 7. Limitations and improvements

- Transaction amounts can be naturally skewed.
- Different product categories may have different normal ranges.
- Seasonal and promotional effects are not modelled.
- Statistical thresholds are global rather than category-specific.
- Future work: category-aware detection, robust transformations, manual validation and threshold sensitivity analysis.

## 8. Evidence files

- `anomaly_records.csv`
- `method_comparison.csv`
- `status_anomaly_summary.csv`
- `amount_distribution.png`
- `anomaly_scatter.png`
- `method_comparison.png`
- `analysis_summary.md`

## 9. Reproducibility

Run: `python reports/w10d3/anomaly_detection.py`

The original dataset is not modified.

## 10. Transaction-level validation

- The analysis operates on transaction-line records, not unique orders.
- The 3,770 flagged rows represent 3,701 distinct Order IDs.
- Repeated Order IDs were checked against the original dataset.
- The flagged orders contained 4,247 source rows.
- No exact duplicate source rows were found among those rows.
- No duplicates were found using the Order ID + SKU + Amount combination.
- Multiple item lines under one Order ID are therefore retained as separate transaction observations.
- The method comparison percentages use the full dataset denominator; Isolation Forest itself was fitted on 113,701 valid positive Amount and Qty records.
- The 2% Isolation Forest contamination setting corresponds to approximately 2,274 observations; 2,269 were flagged (approximately 1.995% of the model population).

## 11. CIA mentor review

### Interaction 1 - Technical assessment

- Requested a technical review of `anomaly_detection.py`.
- CIA stated that it could not inspect the local file because the source code was not supplied in its chat.
- It provided an intermediate assessment based on the reported metrics, rather than a line-by-line code review.
- It initially compared the Isolation Forest count against 2% of all 128,975 dataset rows. This uses the wrong denominator for this implementation.
- The model was fitted on 113,701 valid positive Amount and Qty records; 2,269 flags represent approximately 1.995% of that population.
- CIA also noted that the Z-score count should be interpreted in light of the non-normal, potentially skewed sales distribution.
- No full source-code review or formal overall verdict was provided.

### Interaction 2 - Business and statistical assessment

- Requested interpretation of the differences between IQR, Z-score and Isolation Forest.
- CIA discussed IQR sensitivity to skewness, standard-deviation inflation affecting Z-score thresholds, and Isolation Forest's multivariate detection approach.
- The actual Isolation Forest features are Amount and Qty. CIA's example involving time was illustrative only and time was not used as a model feature.
- The methods use different assumptions and input populations, so their anomaly counts are not directly interchangeable.
- The response was partial and did not provide a formal overall verdict.

**Review outcome:** Two CIA interactions completed. Feedback and limitations documented. The technical assessment was metrics-based, not a direct source-code review. No formal PASS/FAIL verdict was supplied.

**Implementation validation:** CSV consistency checks passed; all 128,975 records were accounted for in the status summary, all 3,770 flagged rows were reconciled, and all three evidence images were present.
