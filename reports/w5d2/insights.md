# W5D2 — Automated EDA Findings

## Dataset
- Source: Credit Card Fraud Detection
- Total rows analyzed: 284,807
- Fraud transactions: 492
- Legitimate transactions: 284,315
- Fraud prevalence: 0.1727%

## Three insights
1. Fraud represents 0.1727% of the dataset, showing severe class imbalance.
2. Mean fraud transaction amount is 122.21; mean legitimate amount is 88.29. Means alone cannot identify fraud.
3. The three charts explore class counts and transaction amounts. They use the first 10,000 rows, while the summary statistics use the complete dataset.

## Method limitation
AutoViz and SweetViz were removed because report generation was resource-intensive in this environment. Pandas and Matplotlib were used instead; these charts are not AutoViz or SweetViz reports.
