\# W12D4 — Final EDA Project Demo

\## Indian E-Commerce Business Exploratory Data Analysis



\## 1. Demo Introduction



Hello everyone.



Today I am presenting my Indian E-Commerce Business Exploratory Data Analysis project.



The objective of this project is to analyze e-commerce transaction data, identify business patterns, examine data quality, and communicate meaningful findings through statistical analysis and visualizations.



The project focuses on understanding recorded transaction amounts, product category performance, order statuses, fulfilment patterns, and geographical distribution.



\## 2. Dataset Overview



The dataset contains:



\- 128,975 records

\- 24 columns

\- Transaction dates from 31 March 2022 to 29 June 2022

\- Approximately 65.73 MB of data



The dataset includes order information, product categories, amounts, fulfilment details, order statuses, and shipping information.



\## 3. Technologies Used



The project uses:



\- Python

\- Pandas

\- NumPy

\- Matplotlib

\- Git and GitHub

\- PowerPoint



Python and Pandas were used for data inspection and analysis. NumPy supported numerical operations, while Matplotlib was used to create visualizations.



\## 4. Data Quality Assessment



The initial data-quality assessment identified:



\- Total records: 128,975

\- Duplicate rows: 0

\- Invalid dates: 0

\- Missing Amount values: 7,795

\- Missing shipping city values: 33

\- Missing Courier Status values: 6,872



There were 121,180 valid Amount observations.



The original source records were preserved. Missing Amount values were excluded from Amount-specific statistical calculations rather than silently imputed.



This distinction is important because missing values should be handled transparently to avoid misleading financial conclusions.



\---



\## 5. Visualization Walkthrough — Three Story Arcs



To make the presentation easier to follow, I have grouped the six visualizations into three story arcs.



\### Story Arc 1 — Understanding the Data



\*\*Chart 1: Amount Distribution\*\*



This visualization helps us understand the distribution of recorded transaction amounts.



Key statistics:



\- Mean: ₹648.56

\- Median: ₹605.00

\- Standard deviation: ₹281.21

\- Skewness: 0.885



The positive skewness indicates a right-skewed distribution. The mean being higher than the median suggests that higher-value observations influence the distribution.



\*\*Why this chart matters:\*\* It helps identify the typical range and distribution of recorded transaction amounts.



\*\*Chart 2: Fulfilment Analysis\*\*



This visualization examines the distribution of fulfilment methods.



\*\*Why this chart matters:\*\* Understanding fulfilment patterns can help identify operational characteristics and areas that may need further investigation.



\### Story Arc 2 — Understanding Business Performance



\*\*Chart 3: Category Sales\*\*



This chart compares recorded amounts across product categories.



The Set category recorded the highest aggregate amount at approximately ₹3.92 crore.



Kurta and Western Dress were the next highest categories among the listed results.



\*\*Why this chart matters:\*\* It helps identify categories with higher recorded transaction amounts and supports further product-level investigation.



These amounts include all order statuses and should not be interpreted as net realized revenue.



\*\*Chart 4: Order Status Distribution\*\*



This chart presents the distribution of order statuses.



The analysis identified 18,332 cancelled orders. Other statuses included delivered, returned, pending, and different shipped-status records.



\*\*Why this chart matters:\*\* It helps understand transaction processing outcomes and highlights why cancellations and returns should be considered in business performance analysis.



\### Story Arc 3 — Understanding Trends and Geography



\*\*Chart 5: Monthly Recorded Amount\*\*



This visualization examines recorded amounts across the available months.



\*\*Why this chart matters:\*\* It helps identify monthly patterns and possible changes in recorded transaction activity.



The results should be interpreted as recorded amounts rather than confirmed realized revenue.



\*\*Chart 6: Top States\*\*



This chart highlights geographical distribution across the leading states.



\*\*Why this chart matters:\*\* It helps identify geographical concentration and areas that may deserve additional operational or marketing investigation.



\---



\## 6. Outlier Analysis



The IQR method was used to identify potential outliers.



Key results:



\- Q1: ₹449.00

\- Q3: ₹788.00

\- IQR: ₹339.00

\- Lower boundary: -₹59.50

\- Upper boundary: ₹1,296.50

\- Potential outliers: 3,600



The IQR method uses the middle 50% of the distribution to calculate outlier boundaries.



The potential outliers were retained rather than automatically removed because unusual observations may represent genuine high-value transactions.



The outlier count is approximately 2.97% of the 121,180 valid Amount observations.



\## 7. Key Business Insights



The analysis produced several findings:



1\. The Set category recorded the highest aggregate amount among the listed categories.

2\. The Amount distribution is positively skewed.

3\. Potential outliers require investigation before financial interpretation.

4\. Cancelled and returned orders should be considered when evaluating business performance.

5\. Missing Amount values affect the completeness of financial analysis.

6\. Geographical and fulfilment patterns can support further operational investigation.

7\. Recorded transaction amounts should be distinguished from actual realized revenue.



\## 8. Business Recommendations



Based on the findings, I recommend:



1\. Investigating the high recorded amounts in the Set category.

2\. Studying cancellation and return patterns.

3\. Investigating the causes of missing transaction amounts.

4\. Examining geographical differences in order distribution.

5\. Reviewing fulfilment performance.

6\. Validating potential outliers before using them in financial reporting.



These recommendations are areas for further investigation, not claims that the EDA has established specific causes.



\## 9. Limitations



The project has several limitations:



\- The analysis covers a limited historical period.

\- Missing Amount values reduce the number of available financial observations.

\- Potential outliers require additional business-context validation.

\- Recorded amounts do not necessarily represent net realized revenue.

\- Order status alone cannot establish successful delivery.

\- Exploratory analysis identifies patterns but does not establish causation.



\## 10. Future Improvements



With additional time, the project could be extended through:



\- Customer-level purchasing analysis.

\- Detailed cancellation and return analysis.

\- Validated net realized revenue calculations.

\- Demand forecasting.

\- An interactive Streamlit or Power BI dashboard.

\- Automated data-quality monitoring.



\## 11. Conclusion



This project demonstrates the application of Python-based exploratory data analysis to an Indian e-commerce dataset.



It combines data-quality assessment, descriptive statistics, outlier identification, category-level analysis, order-status analysis, and data visualization.



The findings provide a foundation for further business intelligence and predictive analytics work.



\## 12. Closing Statement



Thank you for your time.



I am ready to explain the methodology, discuss the findings, describe the analytical decisions, and answer questions about the project.
