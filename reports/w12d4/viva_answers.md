\# W12D4 — Viva Preparation

\## Indian E-Commerce Business Exploratory Data Analysis



\### Question 1: Explain what you built and the key decisions you made.



\*\*Answer:\*\*



I developed an Exploratory Data Analysis (EDA) project using an Indian e-commerce business dataset containing 128,975 records and 24 columns.



The project involved:



\- Dataset inspection and data-quality assessment.

\- Missing-value and duplicate analysis.

\- Statistical analysis of transaction Amount values.

\- Outlier identification using the IQR method.

\- Product category analysis.

\- Order-status and fulfilment analysis.

\- Six visualizations.

\- A nine-slide PowerPoint presentation.

\- Final project documentation and demo preparation.



I used Python, Pandas, NumPy, and Matplotlib.



One important decision was to preserve the original source records rather than automatically remove missing values or potential outliers. Missing Amount observations were excluded from Amount-specific statistical calculations, while potential outliers were flagged for investigation.



I also distinguished recorded transaction amounts from net realized revenue.



\### Question 2: What was the most difficult part? How did you solve it?



\*\*Answer:\*\*



One of the main challenges was interpreting data-quality issues correctly.



The dataset contained 7,795 missing Amount values, along with missing values in other columns. It also contained potential outliers.



I addressed these challenges by:



\- Performing systematic missing-value analysis.

\- Checking duplicate records.

\- Validating date conversions.

\- Applying the IQR method to identify potential outliers.

\- Preserving original source records.

\- Excluding missing Amount observations from Amount-specific statistical calculations.

\- Documenting analytical assumptions and limitations.



This helped prevent incorrect conclusions from being drawn from incomplete or unusual observations.



\### Question 3: What would you improve with more time?



\*\*Answer:\*\*



With additional time, I would extend the project in several ways:



1\. Perform deeper customer-level purchasing analysis.

2\. Investigate cancellation and return patterns.

3\. Calculate validated net realized revenue.

4\. Develop demand forecasting models.

5\. Build an interactive dashboard using Streamlit or Power BI.

6\. Introduce automated data-quality checks.

7\. Improve the analysis with additional business context.



These improvements would help transform the existing descriptive analysis into a more comprehensive business intelligence solution.



\---



\## Additional Technical Viva Questions



\### 4. Why did you use Pandas?



Pandas provides efficient data manipulation, cleaning, aggregation, and analysis capabilities. It was useful for examining the dataset, identifying missing values, and calculating descriptive statistics.



\### 5. What is the IQR method, and why did you use it?



IQR stands for Interquartile Range.



It is calculated as:



IQR = Q3 - Q1



Potential outliers are observations below Q1 - 1.5 × IQR or above Q3 + 1.5 × IQR.



I used IQR because it is based on quartiles and is less influenced by extreme observations than standard-deviation-based methods.



In this project:



\- Q1 = ₹449

\- Q3 = ₹788

\- IQR = ₹339

\- Lower bound = -₹59.50

\- Upper bound = ₹1,296.50

\- Potential outliers = 3,600



These observations were flagged rather than automatically removed.



\### 6. What does positive skewness mean?



Positive skewness indicates a distribution with a longer right tail.



In this project, the Amount distribution had a skewness of 0.885. The mean was ₹648.56, while the median was ₹605. This indicates that higher-value observations influence the distribution.



\### 7. How did you handle missing Amount values?



The dataset contained 128,975 rows, of which 121,180 had valid Amount observations.



Therefore, 7,795 Amount values were missing.



These missing values were excluded from Amount-specific statistical calculations. I did not silently impute them or automatically remove their original source records.



\### 8. Why should outliers not always be removed?



Some unusual observations may represent genuine high-value transactions. Removing them without investigation could distort business findings.



I therefore flagged potential outliers and retained them in the analysis.



\### 9. What is the difference between recorded amount and realized revenue?



Recorded amount represents the amount stored in the transaction data.



Realized revenue requires validation of completed transactions and relevant financial adjustments, including cancellations and returns.



The category-level amounts in this project include all order statuses, so they should not automatically be interpreted as net realized revenue.



\### 10. What is the importance of data visualization?



Data visualization helps communicate patterns, comparisons, distributions, and trends. It makes analytical findings easier for business stakeholders to understand.



\### 11. Why is documentation important?



Documentation explains the dataset, methodology, assumptions, results, and limitations. It makes the project easier to reproduce, review, maintain, and communicate.



\### 12. What is the purpose of a project demo?



A project demo communicates the business problem, dataset, methodology, analytical findings, and potential business value to reviewers and stakeholders.



\---



\## Suggested Demo Narrative



Instead of presenting six charts as unrelated outputs, organize the presentation into three story arcs:



\*\*Story Arc 1 — Understanding the Data\*\*

\- Dataset overview.

\- Data-quality findings.

\- Amount distribution.



\*\*Story Arc 2 — Understanding Business Performance\*\*

\- Product category analysis.

\- Order-status distribution.

\- Fulfilment analysis.



\*\*Story Arc 3 — Business and Operational Insights\*\*

\- Monthly recorded amounts.

\- Geographical distribution.

\- Recommendations and limitations.



Explain why each visualization was selected and what takeaway it provides.



\---



\## Final Viva Reminder



\- Explain the project in your own words.

\- Support numerical statements with actual analysis results.

\- State the denominator when reporting percentages.

\- Distinguish recorded amounts from realized revenue.

\- Explain how missing values and potential outliers were treated.

\- Be honest about limitations and future improvements.

\- Avoid claiming predictive modeling or deployment that was not performed.
