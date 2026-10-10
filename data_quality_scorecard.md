# Data Quality Scorecard — Sales Dataset

## Overview

- Dataset: `python-pandas/sales_data.csv`
- Validation method: Python and pandas
- Original dataset checks passed: 8 out of 8
- Intentional error tests detected: 3 out of 3

## Six DAMA Data Quality Dimensions

| Dimension    | Status             | Assessment                                                           |
| ------------ | ------------------ | -------------------------------------------------------------------- |
| Completeness | PASS               | Required values were present according to the implemented checks.    |
| Uniqueness   | PASS               | Every `order_id` was unique in the original dataset.                 |
| Validity     | PASS               | Sales and quantity rules passed; region and category were not blank. |
| Accuracy     | NEEDS VERIFICATION | Compare records with trusted transaction sources.                    |
| Consistency  | PARTIALLY ASSESSED | Basic rules passed; formats and definitions need further review.     |
| Timeliness   | NEEDS VERIFICATION | Confirm the dataset refresh date and reporting schedule.             |

## Intentional Error Testing

Three errors were introduced into a test copy:

- Duplicate `order_id`
- Negative `sales`
- Zero `quantity`

Result: All three errors were detected.

## Recommendations

1. Validate the data whenever new records arrive.
2. Investigate records that fail validation.
3. Compare sales records with trusted transaction sources.
4. Standardize region and category values.
5. Record refresh dates and define freshness requirements.
6. Restrict access to customer information and use pseudonymization when appropriate.

## Conclusion

The original dataset passed all eight implemented checks, and all three intentional errors were detected. Accuracy, consistency, and timeliness require additional verification. The current report was generated with pandas; native Great Expectations validation remains outstanding.
