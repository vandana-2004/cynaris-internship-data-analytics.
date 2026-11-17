# W8D5 — AI Data Platform: Final Demo and Documentation



## Project Overview



The Cynaris CIA Data Analyst is a FastAPI-based application for CSV uploads, AI-assisted data analysis, executive summaries, and PowerPoint exports.



\*\*Production URL:\*\* https://cynaris-cia-data-analyst.onrender.com



\*\*API documentation:\*\*

\- \[Swagger](https://cynaris-cia-data-analyst.onrender.com/docs)

\- \[ReDoc](https://cynaris-cia-data-analyst.onrender.com/redoc)



## Technology Stack



\- Python 3.10

\- FastAPI and Uvicorn

\- Pandas

\- PandasAI and LiteLLM

\- Groq API

\- Plotly and Chart.js

\- python-pptx

\- Render



## Application Features



1\. CSV upload and preview (10 MB limit).

2\. AI-assisted questions about uploaded datasets.

3\. Chart generation from supported analysis results.

4\. Executive summary with insights and recommendations.

5\. PowerPoint export.

6\. Session deletion.

7\. Health monitoring and interactive API documentation.



## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| GET | `/health` | Application health |

| GET | `/` | Web interface |

| POST | `/cia/upload` | Upload and preview CSV |

| POST | `/cia/query` | AI-assisted analysis |

| POST | `/cia/executive-summary` | Generate executive summary |

| GET | `/cia/executive-summary/ppt/{session\_id}` | Download PowerPoint |

| DELETE | `/cia/session/{session\_id}` | Delete session |



## Indian Business Dataset — EDA Findings



The existing W8D3/W8D4 analysis was reused.



\- Dataset: 128,975 rows and 24 columns.

\- Date range: 31 March 2022 to 29 June 2022.

\- Duplicate rows: 0.

\- Unique order IDs: 120,378.

\- Valid Amount records: 121,180.

\- Missing Amount records: 7,795.

\- Missing shipping city values: 33.

\- Potential IQR outliers: 3,600.

\- Cancelled records: 14.21%.

\- Set has the highest recorded category amount.

\- Maharashtra has the highest record count.



### Business Recommendations



1\. Investigate cancellation drivers.

2\. Validate missing Amount values before financial reporting.

3\. Examine the Set category's recorded amount and sales drivers.

4\. Investigate Maharashtra's high record volume using appropriate KPIs.

5\. Review potential outliers before drawing conclusions.



### Analysis Limitations



\- Recorded amounts include all order statuses and are not net realized revenue.

\- State counts represent records, not unique customers.

\- Potential outliers are not automatically errors.

\- Missing values were not silently imputed.

\- Original source records were preserved.



## Local Setup



Run in PowerShell from the repository root:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt

uvicorn cia\_analyst.app:app --reload

```



Open `http://127.0.0.1:8000/docs` for local API documentation.



## Production Deployment



The application is deployed on Render using `render.yaml`.



Required environment variable: `GROQ\_API\_KEY`.



Configure secrets in the hosting provider's environment settings. Never commit API keys.



## W8D5 Production Validation



Validated on 9 November 2026:



| Resource | Result |

|---|---|

| `/docs` | HTTP 200 |

| `/redoc` | HTTP 200 |

| `/` | HTTP 200 |



The health endpoint had also returned HTTP 200 during the preceding deployment validation. Earlier W8D4 testing documented successful CSV upload, AI query, executive summary, and PowerPoint export.



## Known Limitations



\- CSV upload limit: 10 MB.

\- Sessions are stored in memory and lost when the application restarts.

\- One application instance is recommended because sessions are not shared between instances.

\- AI features require a valid Groq API key.

\- Chart.js is loaded from a CDN.

\- AI-generated findings should be reviewed before business decisions.



## Deliverables



\- `cia\_analyst/app.py`

\- Analysis engines and PowerPoint export modules.

\- `requirements.txt`

\- `render.yaml`

\- `reports/w8d3/` — EDA report and charts.

\- `reports/w8d4/` — business analysis and evidence.

\- `reports/w8d5/` — final project documentation and evidence.



## Final Demo



Recording and shareable link: Pending.



## CIA Mentor Review



W8D5 CIA code review and business-analysis interactions: Pending documentation.