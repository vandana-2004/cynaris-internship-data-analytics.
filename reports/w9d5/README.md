# W9D5 - Tracked Data Analyst Experiment Pipeline
## Objective

Built a reproducible EDA pipeline for the Indian Business Sales dataset using Python and MLflow.

## Dataset

- File: `data/w8d3/indian_business_sales.csv`
- Rows: 128,975
- Original columns: 24
- Analytical columns: 23
- Excluded unnamed columns: 1
- Duplicate rows: 0

## Data Quality Findings

| Metric | Result |
|---|---:|
| Raw missing cells | 210,495 |
| Analytical missing cells | 161,445 |
| Missing Amount values | 7,795 |
| Amount parsing errors | 0 |
| Valid Amount values | 121,180 |

Missing Amount values were excluded from statistics. No imputation was performed.

## Amount Analysis

| Metric | Result |
|---|---:|
| Mean | INR 648.56 |
| Median | INR 605.00 |
| Standard deviation | INR 281.21 |
| Minimum | INR 0 |
| Maximum | INR 5,584 |
| Skewness | 0.8855 |
| IQR outliers | 3,600 |

Amount represents recorded order amounts, not net revenue.

The distribution is positively skewed, with the mean above the median. IQR outliers are statistical flags, not automatically errors. Business review is required before excluding them.

## Generated Outputs

Location: `reports/w9d5/outputs/`

- `category_summary.csv`
- `status_summary.csv`
- `eda_summary.md`
- `amount_distribution.png`
- `top_categories.png`

## MLflow Tracking

- Experiment: `W9D5 - Tracked DA Experiment Pipeline`
- Original run: `dc9b4abb58cf4d7bab197c312f070ce5`
- Updated run: `20810144df7042e4ab2993b0bd5b8d4f`
- Updated run status: FINISHED

Logged the dataset fingerprint, parameters, data-quality metrics, statistical metrics, tags, and five artifacts.

## CIA Mentor Interactions

**Interaction 1 — Technical Review**

- Recommended distinguishing raw and analytical missing cells.
- Recommended separating missing Amount values from parsing errors.
- Reinforced responsible interpretation of IQR outliers.

**Interaction 2 — Interpretation Review**

- Recommended explaining positive skewness.
- Emphasized that statistical outliers are not automatically errors.
- Recommended documenting missing-value handling and possible bias.
- Reinforced that Amount is not net revenue.

The mentor reviewed supplied project information and metrics. Pipeline execution and MLflow artifacts were verified separately.

## Limitations

- Amount is not net revenue or profit.
- Missing values may introduce bias if missingness is not random.
- Outliers require business investigation.
- Descriptive EDA does not establish causation.

## Reproducibility

Run from the repository root:

```powershell
& .\.venv-pandasai\Scripts\python.exe .\reports\w9d5\tracked_eda_pipeline.py
```

## Status

- [x] EDA pipeline implemented
- [x] MLflow tracking completed
- [x] Artifacts verified
- [x] Two CIA interactions completed
- [ ] Git commits and pull request