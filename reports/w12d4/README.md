# W12D4 â€” Final Documentation and Demo Preparation

## Indian E-Commerce Business Exploratory Data Analysis

## 1. Project Overview

This project focuses on exploratory data analysis (EDA) of an Indian e-commerce business dataset. The objective is to understand recorded transaction amounts, product category performance, order statuses, fulfilment methods, and geographical distribution through data analysis and visualizations.

This documentation consolidates the existing EDA work into a structured project suitable for GitHub submission, business presentation, and final viva evaluation.

## 2. Business Objectives

- Understand transaction and recorded amount patterns.
- Identify high-performing product categories.
- Examine order status and fulfilment distributions.
- Investigate missing values, duplicates, and potential outliers.
- Identify geographical patterns in business transactions.
- Communicate findings through visualizations and business insights.

## 3. Dataset Description

| Attribute | Details |
|---|---|
| Dataset | Indian Business Sales |
| Source file | `data/w8d3/indian_business_sales.csv` |
| Total records | 128,975 |
| Total columns | 24 |
| Dataset size | Approximately 65.73 MiB (68.92 MB) |
| Start date | 31 March 2022 |
| End date | 29 June 2022 |

The dataset contains transactional information, including order identifiers, dates, product categories, quantities, amounts, fulfilment information, order statuses, and shipping details.

## 4. Tools and Technologies

- Python 3
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook / Python scripts
- PowerPoint
- Git and GitHub
- Visual Studio Code

## 5. Data Quality Assessment

The existing analysis identified the following data-quality findings.

| Data Quality Check | Result |
|---|---:|
| Total rows | 128,975 |
| Total columns | 24 |
| Duplicate rows | 0 |
| Invalid dates | 0 |
| Missing Amount | 7,795 |
| Missing shipping city | 33 |
| Missing Courier Status | 6,872 |
| Missing promotion IDs | 49,153 |
| Missing fulfilled-by values | 89,698 |

The original source records were preserved. The 7,795 missing Amount values were excluded from Amount-specific statistical calculations, leaving 121,180 valid Amount observations.

Missing Amount values were not silently imputed. The original dataset was not reduced by automatically dropping these records. Other missing values were examined as part of the data-quality assessment.

Potential outliers were flagged for investigation rather than automatically removed.

## 6. Exploratory Data Analysis

### 6.1 Amount Distribution

The analysis of valid Amount observations produced the following results.

| Statistical Measure | Value |
|---|---:|
| Valid observations | 121,180 |
| Mean | â‚¹648.56 |
| Median | â‚¹605.00 |
| Standard deviation | â‚¹281.21 |
| Skewness | 0.885 |
| Minimum | â‚¹0.00 |
| Maximum | â‚¹5,584.00 |

The positive skewness indicates a right-skewed distribution. Some higher-value observations influence the mean, making it greater than the median.

These statistics describe recorded Amount values and should not automatically be interpreted as net realized revenue.

### 6.2 Outlier Analysis

The Interquartile Range (IQR) method was used to identify potential outliers.

- Q1: â‚¹449.00
- Q3: â‚¹788.00
- IQR: â‚¹339.00
- Lower bound: -â‚¹59.50
- Upper bound: â‚¹1,296.50
- Potential outliers: 3,600

The IQR method uses the middle 50% of the distribution to establish outlier boundaries and is less influenced by extreme observations than standard-deviation-based methods.

The 3,600 potential outliers represent approximately 2.97% of the 121,180 valid Amount observations.

These observations were flagged for further investigation and retained in the analysis rather than automatically removed. A potential outlier is not necessarily an incorrect transaction.

### 6.3 Category-Level Analysis

The highest recorded category amounts were:

| Category | Recorded Amount |
|---|---:|
| Set | â‚¹39,204,124.03 |
| kurta | â‚¹21,299,546.70 |
| Western Dress | â‚¹11,216,072.69 |
| Top | â‚¹5,347,792.30 |
| Ethnic Dress | â‚¹791,217.66 |

The Set category recorded the highest aggregate amount among the listed categories.

**Important:** These amounts include all order statuses and should not be interpreted as net realized revenue.

### 6.4 Order Status Analysis

| Order Status | Count |
|---|---:|
| Shipped | 77,804 |
| Shipped - Delivered to Buyer | 28,769 |
| Cancelled | 18,332 |
| Shipped - Returned to Seller | 1,953 |
| Shipped - Picked Up | 973 |
| Pending | 658 |
| Pending - Waiting for Pick Up | 281 |
| Shipped - Returning to Seller | 145 |

The order-status distribution provides insight into transaction processing and fulfilment outcomes.

A shipped status does not necessarily mean that an order was successfully delivered to the customer.

## 7. Visualizations

Six visualizations were generated during the existing EDA work:

1. Amount Distribution
2. Category Sales
3. Fulfilment Analysis
4. Monthly Recorded Amount
5. Order Status Distribution
6. Top States

The six existing chart files are stored in:

`reports/w8d3/charts/`

These visualizations help communicate statistical patterns and business findings.

## 8. Key Business Insights

1. The Set category has the highest recorded aggregate amount among the analyzed categories.
2. The Amount distribution is positively skewed.
3. Potential outliers require investigation before making business decisions.
4. Cancelled and returned orders should be considered when evaluating business performance.
5. Missing values may affect the completeness of certain analytical conclusions.
6. Geographical and fulfilment analysis can support operational planning.
7. Recorded transaction amounts should be distinguished from actual realized revenue.

## 9. Methodology and Assumptions

The existing analysis followed these principles:

- Preserved original source records.
- Checked dataset dimensions and duplicate records.
- Converted date and numeric fields to appropriate data types.
- Represented invalid conversions as missing values.
- Examined missing values by column.
- Used the 1.5 Ã— IQR rule for potential outlier identification.
- Excluded the undocumented `Unnamed: 22` column from analysis.
- Retained potential outliers rather than automatically removing them.
- Excluded missing Amount observations from Amount-specific statistical calculations.
- Included all order statuses in category-level recorded amounts.
- Included statuses beginning with Shipped in shipped-status monthly analysis, including returns.

## 10. Existing Project Deliverables

The original EDA implementation and outputs are maintained separately.

| File or Directory | Description |
|---|---|
| `reports/w8d3/eda_summary.txt` | EDA statistical summary |
| `reports/w8d3/indian_business_eda_ppt.py` | PowerPoint generation script |
| `reports/w8d3/indian_business_eda_report.pptx` | Existing presentation |
| `reports/w8d3/charts/` | Six existing PNG visualization files |
| `data/w8d3/indian_business_sales.csv` | Original dataset |

## 11. Reproducibility

The existing analysis outputs can be reviewed from the repository root.

**Dataset:**

`data/w8d3/indian_business_sales.csv`

**Statistical summary:**

`reports/w8d3/eda_summary.txt`

**Existing chart directory:**

`reports/w8d3/charts/`

**Existing presentation:**

`reports/w8d3/indian_business_eda_report.pptx`

**Existing presentation generation script:**

`reports/w8d3/indian_business_eda_ppt.py`

To regenerate the PowerPoint presentation using the existing script:

```powershell
python reports/w8d3/indian_business_eda_ppt.py
```

This command regenerates the presentation and chart outputs; it does not necessarily reproduce every step of the original EDA workflow.

Before running it, verify the script's dependencies and output paths. The script writes chart files into `reports/w8d3/charts/`, updates `reports/w8d3/eda_summary.txt`, and saves the presentation to `reports/w8d3/indian_business_eda_report.pptx`.

**Important:** Running the script may overwrite existing outputs. Review or preserve existing deliverables before executing it.

The original dataset and generated outputs are maintained in their respective repository paths.

## 12. Limitations

- The dataset represents a limited historical period.
- Missing Amount values reduce the number of available financial observations.
- Potential outliers require business-context validation.
- Recorded amounts do not necessarily represent collected revenue.
- Order status alone cannot establish successful delivery.
- The undocumented `Unnamed: 22` column was excluded from analysis.
- Observational EDA identifies patterns but does not establish causation.

## 13. Future Improvements

- Analyze net realized revenue using validated transaction outcomes.
- Investigate missing values and their causes.
- Perform customer-level purchasing analysis.
- Examine delivery performance and return patterns.
- Develop demand forecasting models.
- Build an interactive business intelligence dashboard.
- Introduce automated data-quality monitoring.

## 14. Conclusion

The Indian E-Commerce Business EDA project demonstrates how Python-based exploratory analysis can transform raw transactional records into meaningful business insights.

The project combines data-quality assessment, descriptive statistics, outlier identification, category-level analysis, order-status analysis, and visualizations.

The final documentation provides a structured explanation of the methodology, results, assumptions, limitations, and future improvements.

These findings can support business discussions and operational analysis when interpreted within the documented limitations.

## 15. W12D4 Final Submission

This folder contains the final documentation and demo-preparation evidence for W12D4.

Additional deliverables include:

- `README.md` â€” Final project documentation
- `demo_script.md` â€” Demo walkthrough
- `viva_answers.md` â€” Viva preparation
- `final_checklist.md` â€” Submission verification
- `cia_review.md` â€” CIA review record

**Project:** Indian E-Commerce Business Exploratory Data Analysis
**Lesson:** W12D4 â€” Final Documentation + Demo Preparation
**Track:** Data Analyst Intern â€” 3-Month Program
