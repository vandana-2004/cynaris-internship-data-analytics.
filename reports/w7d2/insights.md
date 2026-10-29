# W7D2 — Automated EDA Findings

## Dataset
- Source: `data/raw/archive/Sample - Superstore.csv`
- Rows: 9,994
- Columns: 21
- Missing cells: 0
- Duplicate rows: 0
- SweetViz analyzed a reproducible sample of 5,000 rows.
- AutoViz ran successfully on the full 9,994-row DataFrame.

## Three data-backed insights
1. **Sales by category:** Technology has the highest total sales at 836,154.03.
2. **Sales by region:** West has the highest total sales at 725,457.82.
3. **Sub-category profitability:** Tables has the lowest total profit at -17,725.48. Investigate product costs, discounting, and sales mix before deciding on corrective action.

## Generated reports
- SweetViz: `reports/w7d2/sweetviz_report.html`
- AutoViz: `reports/w7d2/autoviz/AutoViz/`
- AutoViz outputs: `cat_var_plots.html`, `distplots_nums.html`, `heatmaps.html`, `pair_scatters.html`, and `violinplots.html`.

## Limitations
AutoViz reported that it could not classify several string columns and detected no date variables. The three findings above were calculated separately with Pandas; they are not attributed to AutoViz.
