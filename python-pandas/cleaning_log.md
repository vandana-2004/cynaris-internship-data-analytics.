# Week 2 — Day 4: Data Cleaning

## Dataset

Sales dataset used for the data cleaning exercise.

## 1. Missing Values

Missing values were checked using `df.isnull().sum()`.

Result:

- No missing values were found.
- Therefore, no mean, median, mode, or forward-fill imputation was required.

## 2. Duplicate Records

Duplicate records were checked using `df.duplicated().sum()`.

Result:

- 0 duplicate rows were found.
- No duplicate rows needed to be removed.

## 3. String Standardisation

Text columns were identified and leading/trailing whitespace was removed using:

`str.strip()`

This helps maintain consistent text values in categorical columns.

## 4. Outlier Detection

Outliers were detected using the Interquartile Range (IQR) method.

The IQR was calculated as:

`IQR = Q3 - Q1`

Potential outliers were identified using:

- Lower bound = Q1 - 1.5 × IQR
- Upper bound = Q3 + 1.5 × IQR

Numeric outliers were treated using IQR capping.

## 5. Before and After Comparison

The dataset was checked before and after cleaning for:

- Number of rows
- Number of columns
- Missing values
- Duplicate rows

The comparison was created in `data_cleaning.ipynb`.

## 6. Output

The cleaned dataset was exported as:

`cleaned_dataset.csv`

## 7. Conclusion

The dataset was checked systematically for missing values, duplicates, inconsistent text formatting, and numerical outliers. The cleaned dataset was then saved for further analysis.
