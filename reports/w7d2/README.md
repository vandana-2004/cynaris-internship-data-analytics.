# W7D2 — Automated Exploratory Data Analysis

## Dataset
`data/raw/archive/Sample - Superstore.csv` (9,994 rows, 21 columns).

## Deliverables
- `automated_eda.py` — SweetViz report generation and Pandas-based findings.
- `sweetviz_report.html` — SweetViz report generated from a reproducible 5,000-row sample.
- `autoviz/AutoViz/` — HTML visualizations generated separately with AutoViz.
- `insights.md` — Three data-backed findings and limitations.
- `comparison.md` — AutoViz versus SweetViz comparison and recommendation.

## Reproducibility
Run `python reports/w7d2/automated_eda.py` from the project root to regenerate the SweetViz report and Markdown findings. This does not rerun AutoViz.

The large `pair_scatters.html` file is retained locally but excluded from Git to keep the repository smaller.
