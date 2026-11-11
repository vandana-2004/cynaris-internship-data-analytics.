# W9D5 — Tracked EDA Experiment Results

## Dataset

- File: `indian_business_sales.csv`
- SHA-256: `ac9a366da5f3af418831fa53da9eebfc3b3838803e3774eec97dbcb291441beb`
- Original rows: 128,975
- Original columns: 24
- Analytical columns: 23
- Excluded unnamed columns: 1
- Duplicate rows: 0

## Missing Data

- Missing cells in original dataset: 210,495
- Missing cells in analytical dataset before Amount parsing: 161,445
- Originally missing Amount values: 7,795
- Amount parsing errors: 0
- Total Amount values excluded from statistics: 7,795
- Amount handling: Missing and non-numeric values were excluded; no imputation was performed.

## Recorded Amount Analysis

- Valid Amount values: 121,180
- Mean: INR 648.56
- Median: INR 605.00
- Standard deviation: INR 281.21
- Minimum: INR 0.00
- Maximum: INR 5,584.00
- Skewness: 0.8855
- IQR outliers (1.5 × IQR): 3,600
- Lower IQR bound: INR -59.50
- Upper IQR bound: INR 1,296.50

## Date Coverage

- Earliest date: 2022-03-31
- Latest date: 2022-06-29

## Interpretation

Amount represents recorded order amounts, not net revenue.

The distribution is positively skewed (skewness approximately 0.89).
The mean exceeds the median, indicating a right-skewed distribution.

IQR outliers are statistical flags, not automatic errors.
Business justification is required before excluding them from further analysis.

Missing and non-numeric Amount values were excluded from Amount statistics.
If missingness is not random, this may introduce bias.

The analysis is descriptive and does not establish causation.
