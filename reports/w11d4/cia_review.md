\# W11D4 - CIA Mentor Review



\## 1. Technical Review



\*\*Topic:\*\* Metabase vs Apache Superset and self-service BI implementation.



\### Project context shared with CIA



\- Reused the W11D3 Indian Business Sales dashboard.

\- Dataset contains 128,975 rows and 22 analytical columns.

\- Five dashboard components and four aggregated CSV files.

\- Python audit script completed 15 validation checks successfully.

\- Existing dashboard is hosted through Apache Superset on Preset.

\- Metabase was not installed because the Docker Desktop Linux engine was unavailable.



\### CIA feedback



\*\*Assessment:\*\* The reuse approach is appropriate for the analytical requirements, with a tooling caveat.



CIA recognized that reusing reliable data preparation and analytical logic is appropriate in a real-world analyst workflow. It highlighted metric definitions, user experience and accessibility as important priorities.



However, the assignment specifically names Metabase. Reusing Superset satisfies the analytical dashboard work but does not fully satisfy the requested Metabase setup requirement.



\### Metabase and Superset comparison



CIA highlighted these differences:



\- Metabase provides a more accessible, guided experience for non-technical users.

\- Superset offers greater visualization flexibility and is more suitable for analytics power users.

\- Both support major database connections.

\- Metabase is generally easier for business users to explore independently.

\- Superset provides more granular visualization and configuration capabilities.



\### Review limitation



The available CIA response ended during the comparison discussion. No additional technical verdict or recommendations are claimed beyond the feedback actually received.



\## 2. Business Stakeholder Review



\*\*Topic:\*\* Usability and business value of the Indian Business Sales dashboard.



\### CIA verdict



\*\*SHIPPABLE WITH MINOR TWEAKS\*\*



\- Confidence: Moderate-High

\- Recommendation: Ship as an internal pilot with clear disclaimers.

\- Do not present as a final revenue report without the stated limitations.



\### Positive feedback



\- Standard chart types are intuitive for business stakeholders.

\- The KPI, trend and breakdown layout is logical.

\- Category-wise Amount analysis is useful for product-mix decisions.

\- Monthly Amount analysis provides useful time-trend context.



\### Improvements recommended



1\. Use a clear dashboard title identifying the March–June 2022 reporting period.

2\. Explain that the metric represents recorded Amount, not verified net revenue.

3\. Display the 93.96% Amount coverage prominently.

4\. Simplify the presentation of 13 order statuses for non-technical stakeholders.

5\. Include a clear reporting-period indicator in the dashboard header.



\### Suggested dashboard title



Sales Performance Dashboard (Mar–Jun 2022) – Recorded Amount



\### Suggested disclaimer



Data includes recorded amounts with 93.96% coverage. Recorded Amount is not verified net revenue or profit. Cancelled orders should not be treated as completed sales.



\### Review limitation



The CIA response ended during its third visualization assessment. No additional visualization findings or recommendations are claimed.



\## 3. Actions and Future Improvements



| Area | Current status | Future improvement |

|---|---|---|

| Existing dashboard | Published through Preset | Improve stakeholder-facing labels |

| KPI definitions | Recorded Amount documented | Add prominent metric definitions |

| Data coverage | 93.96% documented | Display coverage on dashboard |

| Order statuses | All 13 represented | Add business-friendly status grouping |

| Reporting period | Documented in report | Display prominently in dashboard |

| Metabase | Not installed | Complete a Metabase setup when the environment permits |



\## 4. Overall Review Summary



Two W11D4 CIA mentor interactions were completed:



1\. Technical review of the Metabase and Superset self-service BI approach.

2\. Business stakeholder review of the Indian Business Sales dashboard.



The technical review accepted the reuse approach for analytical work while identifying the missing Metabase-specific implementation as a tooling gap.



The stakeholder review recommended an internal pilot with minor improvements and clear financial metric disclaimers.



CIA feedback was based on the project information supplied during the conversations. CIA did not independently execute the audit script, inspect the local dashboard files or verify the hosted dashboard.



\*\*Status:\*\* Two CIA mentor interactions completed and documented. Recommendations recorded for future improvement.
