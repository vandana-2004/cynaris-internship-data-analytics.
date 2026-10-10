# Data Quality Scorecard — Sales Dataset

## Overview

- Dataset: `python-pandas/sales_data.csv`
- Dataset size: 10 rows and 6 columns
- Pandas validation: 8 checks passed on the original dataset
- Great Expectations validation: 9 configured expectations passed
- Intentional error testing: 3 errors detected by the Pandas validation tests

## Six DAMA Data Quality Dimensions

| Dimension    | Status             | Assessment                                                                       |
| ------------ | ------------------ | -------------------------------------------------------------------------------- |
| Completeness | PASS               | Required fields were populated in the original dataset.                          |
| Uniqueness   | PASS               | All order IDs were unique in the original dataset.                               |
| Validity     | PASS               | Configured checks for sales, quantity, region, and category passed.              |
| Accuracy     | NEEDS VERIFICATION | Compare records with trusted transaction sources.                                |
| Consistency  | PARTIALLY ASSESSED | Basic rules passed; additional business-rule and cross-source checks are needed. |
| Timeliness   | NEEDS VERIFICATION | Confirm the refresh timestamp and agree on a freshness target with the consumer. |

## Intentional Error Testing

Three errors were injected into a test copy of the dataset:

- Duplicate order ID
- Negative sales value
- Zero quantity

Result: All three errors were detected by the Pandas validation checks. Great Expectations detection of these injected errors still needs a separate test.

## Privacy and Data Classification

- `customer`: Potential personal data; confirm the actual values and classification.
- Protection: Restrict access, mask identifiers in reports, and use pseudonymisation or tokenisation when appropriate.
- Avoid exposing customer-identifying information unnecessarily in exported reports.

## Reports and Validation

- Pandas HTML report: `data_governance_output/data_quality_report.html`
- Great Expectations results: `data_governance_output/great_expectations_results.csv`
- Great Expectations HTML summary report: To be generated and verified.

The nine configured Great Expectations checks passed on the original dataset. This does not prove that all possible data quality issues have been tested.

## Recommendations

1. Run validation whenever new data arrives.
2. Investigate failed checks before publishing dashboards.
3. Compare sales records with trusted transaction sources.
4. Standardise region and category values.
5. Record refresh timestamps and agree on freshness requirements.
6. Restrict access to customer data and apply appropriate masking or tokenisation.
7. Test the Great Expectations suite against intentionally invalid records.

## Conclusion

The original dataset passed the implemented Pandas checks and all nine configured Great Expectations expectations. Completeness, uniqueness, and the configured validity rules passed. Accuracy and timeliness need further verification, while consistency has only been partially assessed.
