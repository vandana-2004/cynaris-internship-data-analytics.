\# W12D5 — AI Data Analyst Platform Capstone



\## Project

Indian E-Commerce Business EDA with a deployed AI Data Analyst platform.



\## Deliverables

\- `capstone\_demo.ipynb`: reproducible EDA validation.

\- `create\_demo\_sample.py`: reproducible 5,000-row sample generator.

\- `indian\_business\_demo\_sample.csv`: 292,751-byte demonstration sample.

\- `cia\_interactions.md`: API test and CIA interaction evidence.



\## Dataset Scope

The original dataset contains 128,975 rows and 24 columns (approximately 68.9 MB). It is stored locally at `data/w8d3/indian\_business\_sales.csv` and is not included in this W12D5 submission.



The deployed API has a 10 MB upload limit. Therefore, the live demonstration used a separate 5,000-row sample with eight columns.



\## Full-Dataset Findings

\- Duplicate rows: 0.

\- Missing Amount: 7,795; valid observations: 121,180.

\- Mean recorded Amount: ₹648.56.

\- Median recorded Amount: ₹605.00.

\- Skewness: 0.885.

\- IQR upper bound: ₹1,296.50.

\- Potential upper outliers: 3,600.

\- The notebook identifies nine categories, including Dupatta (₹915), omitted from the older eight-category W8D3 summary.



\## Deployed API Demonstration

\- Deployment: https://cynaris-cia-data-analyst.onrender.com

\- Swagger: https://cynaris-cia-data-analyst.onrender.com/docs

\- CSV upload: HTTP 200.

\- AI category query: HTTP 200; eight category totals and a chart returned.

\- Executive summary: HTTP 200; five insights and recommendations returned.

\- PowerPoint export: HTTP 200; downloaded presentation opened successfully.



\## Limitations

\- API results describe the 5,000-row sample, not the full dataset.

\- Category averages were not verified by the query response.

\- Missing values were not claimed to be imputed.

\- Duplicate detection does not prove records are erroneous.

\- Recorded Amount includes all order statuses and is not net realized revenue.

\- Executive summary returned `uploaded.csv` instead of the original upload filename.

\- API sessions are stored in memory and may be lost on restart.



\## Reproduction

Run from the repository root:



```powershell

python reports/w12d5/create\_demo\_sample.py

```



Open `capstone\_demo.ipynb` in VS Code and execute its cells. The original dataset must be available locally.



\## Status

Notebook execution and deployed API demonstration verified. Git submission and PR status are tracked separately.
