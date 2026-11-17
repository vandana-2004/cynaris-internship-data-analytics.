



# W11D3 – CIA Mentor Review



## Interaction 1: Technical Review



**Scope:** Python dashboard preparation and data-processing practices.



### Feedback received

- Separate data loading, cleaning, aggregation, and chart generation into modular functions.

- Prefer pandas vectorized operations such as `groupby()` over unnecessary Python loops.

- Explicitly validate date and numeric data types.

- Add checks for empty datasets and missing required columns.

- Review whether the pie chart is suitable for the number of order-status categories.

- Ensure monthly time-series aggregation is clear and readable.

- Add a `if __name__ == "__main__":` entry point.

- Use project-relative paths and add function docstrings.

- Define KPIs clearly and make their calculations reproducible.

- Handle missing values carefully rather than automatically replacing them with zero.



### Review limitations

The mentor provided rubric-based recommendations and did not execute or verify the local script. Its response was incomplete and did not provide a final verdict.



## Interaction 2: Business Stakeholder Review



**Scope:** Business usefulness, chart clarity, and stakeholder communication.



### Feedback received

- The dashboard communicates what happened but needs more context about why the results matter.

- Add time-period context to the top-category chart.

- Provide comparative context or a baseline for state-level results where reliable data is available.

- Reconsider the order-status pie chart if it contains too many categories; a horizontal bar chart may be easier to interpret.

- Keep the term "Recorded Amount" unless the data supports a more specific financial interpretation.

- Improve the wording of data-quality metrics for non-technical stakeholders.



### Review limitations

The mentor reviewed the supplied dashboard description and summary rather than inspecting the local HTML or executing the script. The response ended during the metric-card recommendation, so the remaining feedback and final verdict were not available.



## Overall CIA Review Summary



Two CIA mentor interactions were completed:

1. Technical review.

2. Business stakeholder review.



Both provided improvement recommendations covering maintainability, data validation, chart selection, KPI definitions, and business communication.



## Deliverable Status

- Python-generated dashboard preparation: completed.
- Interactive local HTML dashboard and five local components: generated and validated.
- Two CIA mentor interactions: recorded, with review limitations described above.
- README and supporting analytical outputs: created.
- Hosted Preset workspace: database uploads completed.
- Hosted Superset charts: five charts saved and added to the dashboard.
- `W11D3 Stakeholder Dashboard`: published.
- Published dashboard URL: https://de37bc60.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=XVAbs_qn33MclWhO94eqZw
- Local screenshot: `W11D3_dashboard.png` saved in the repository root using Windows Snipping Tool.
- The hosted dashboard uses an order-status pie chart; the local Python dashboard retains its horizontal bar chart.
- CIA reviews took place before the hosted dashboard was published. CIA did not independently inspect or execute the hosted dashboard.
- The screenshot is not represented as a native Superset export.
