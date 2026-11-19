\# W12D5 — CIA Interaction Evidence



\*\*Deployment:\*\* https://cynaris-cia-data-analyst.onrender.com

\*\*Demo file:\*\* `indian\_business\_demo\_sample.csv`

\*\*Sample size:\*\* 5,000 rows × 8 columns



\## Interaction 1 — AI Category Analysis



\*\*Endpoint:\*\* `POST /cia/query`



\*\*Question submitted:\*\*



For this 5000-row demonstration sample, calculate total recorded Amount and average recorded Amount by Category. Rank categories by total recorded Amount and explain that missing Amount values are excluded. Do not describe these figures as net revenue.



\*\*Verified result:\*\* HTTP 200. The response returned eight category totals and a chart.



\- Set: ₹1,575,744.82

\- kurta: ₹820,640.74

\- Western Dress: ₹445,784.84

\- Top: ₹206,412.10

\- Ethnic Dress: ₹23,890.00

\- Blouse: ₹17,055.57

\- Bottom: ₹5,144.33

\- Saree: ₹3,222.90



\*\*Limitation:\*\* The response did not display category averages or a written explanation of missing-value handling. These are not claimed as verified.



\## Interaction 2 — Executive Summary



\*\*Endpoint:\*\* `POST /cia/executive-summary`



\*\*Verified result:\*\* HTTP 200. The response returned five insights, observations, business implications, and recommendations.



Sample findings:

\- 5,000 rows and 8 columns.

\- 271 missing values, all in Amount.

\- 82 duplicate rows detected.

\- Amount minimum ₹0.00, mean ₹655.08, maximum ₹2,182.00.

\- Most frequent date: 05-04-22 (90 rows).



The recommendations included reviewing missing values and duplicates. No imputation or duplicate removal is claimed.



\## PowerPoint Export Verification



\*\*Endpoint:\*\* `GET /cia/executive-summary/ppt/{session\_id}`



\*\*Result:\*\* HTTP 200. `CIA\_Executive\_Summary.pptx` (37,448 bytes) downloaded and opened successfully.



\## Overall Review



Both required CIA interactions completed successfully at the API level. The category query has a documented limitation because average values were not returned. The executive summary and PowerPoint export succeeded.



No formal CIA approval is claimed.
