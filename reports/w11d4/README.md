\# W11D4 - Metabase Self-Serve BI Setup and Evaluation



\## 1. Objective



Evaluate self-service Business Intelligence (BI) using Metabase and Apache Superset. Reuse the existing Indian Business Sales analysis and stakeholder dashboard to demonstrate dashboard components, data access considerations, and stakeholder sharing.



\## 2. Implementation Approach



The W11D3 Indian Business Sales dashboard and its hosted Preset deployment are reused as the practical BI foundation.



No duplicate dataset, dashboard HTML, or chart files are created for this task.



\*\*Dataset details:\*\*

\- Dataset: `data/w8d3/indian\_business\_sales.csv`

\- Source rows: 128,975

\- Analytical columns: 22

\- Data period: 31 March 2022 to 29 June 2022

\- Recorded Amount: INR 78,592,678.30

\- Amount coverage: 93.96%

\- Missing Amount rows: 7,795

\- Distinct order statuses: 13



\## 3. Metabase vs Apache Superset



| Area | Metabase | Apache Superset |

|---|---|---|

| Primary focus | Accessible self-service analytics | Flexible, extensible BI and visualization |

| Dashboard creation | Query builder and SQL editor | Explore interface and SQL Lab |

| Database connectivity | Supported database connectors | Supported database connectors |

| Visualizations | Common business charts and tables | Broad visualization ecosystem |

| Permissions | Collection, group and data permissions | Roles, datasets and database access controls |

| Typical users | Business users and smaller teams | Analytics teams and organizations needing flexibility |



Both products support self-service BI. The appropriate choice depends on the organization's technical capacity, governance requirements, data environment and user needs.



\## 4. Reused Stakeholder Dashboard



\*\*Hosted platform:\*\* Apache Superset through Preset.



\*\*Dashboard:\*\* \[W11D3 Stakeholder Dashboard](https://de37bc60.us1a.app.preset.io/superset/dashboard/8/?native\_filters\_key=XVAbs\_qn33MclWhO94eqZw)



Five dashboard components:



1\. Category-wise recorded Amount - bar chart.

2\. Monthly recorded Amount - line chart.

3\. Order Status Distribution - pie chart in the hosted dashboard.

4\. State-wise Amount Summary - table.

5\. Total Amount KPI Summary - Big Number chart.



The local Python dashboard uses a horizontal bar chart for order status instead of the hosted dashboard's pie chart.



\## 5. Data Access and Stakeholder Sharing



BI dashboards should follow least-privilege access principles.



Recommended controls:



\- Give users only the database and dataset access required for their work.

\- Separate dashboard viewers from authors and administrators.

\- Restrict sensitive columns and datasets where appropriate.

\- Use organization-managed authentication and account permissions.

\- Review access when roles or responsibilities change.

\- Share published dashboards with approved stakeholders only.

\- Validate that filters and aggregations do not expose restricted information.



In Superset, access can be managed through roles and permissions associated with databases, datasets, dashboards and other resources. Exact controls depend on the deployed version and configuration.



\## 6. Metabase Local Setup Assessment



Metabase was not installed or deployed as part of this task.



The local Docker CLI is present, but the Docker Desktop Linux engine is unavailable. Therefore, a local Metabase deployment was not attempted.



No claim is made that the existing Preset dashboard is a Metabase dashboard.



\## 7. Reuse Audit and Validation



Run from the repository root:



```powershell

.\\.venv\\Scripts\\python.exe .\\reports\\w11d4\\self\_serve\_bi\_audit.py

```



Validation result:



\- 15 checks passed.

\- 0 checks failed.

\- Source dataset and existing dashboard evidence found.

\- Four chart files and four summary CSVs found.

\- All 13 order statuses validated.

\- Order-status aggregation totals 128,975 rows.

\- Dashboard KPI content detected.



\## 8. Existing Evidence References



\- `reports/w11d3/dashboard.py`

\- `reports/w11d3/README.md`

\- `reports/w11d3/cia\_review.md`

\- `reports/w11d3/outputs/dashboard.html`

\- `reports/w11d3/outputs/dashboard\_summary.md`

\- `reports/w11d3/outputs/images/dashboard\_preview.png`

\- `reports/w11d3/outputs/charts/`

\- `reports/w11d3/outputs/\*.csv`

\- `W11D3\_dashboard.png`



The audit script validates the existence and selected structural properties of these outputs. It does not independently verify hosted dashboard permissions, live database connectivity, or Metabase functionality.



\## 9. Interpretation Limitations



\- Recorded Amount is not verified net revenue or profit.

\- Missing Amount values are excluded from amount aggregations.

\- Cancelled orders are not treated as completed sales.

\- The dataset covers approximately three months.

\- The hosted dashboard's Big Number display and local recorded Amount total may use different aggregation definitions; they should not be treated as equivalent without checking the underlying chart query.

\- Stakeholder access depends on Preset workspace permissions and service availability.



\## 10. Completion Status



\- Existing BI assets reused without duplicating the dataset.

\- W11D4 audit script created and executed.

\- 15 of 15 automated checks passed.

\- Metabase and Superset comparison documented.

\- Metabase local deployment limitation disclosed.

\- CIA review evidence to be added after the two W11D4 mentor interactions.
