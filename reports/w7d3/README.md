# W7D3 - CIA Chart Generation: Plotly + ECharts

## Objective

Generate interactive Plotly charts and ECharts-compatible options from the Superstore dataset.

## Dataset

- Source: `data/raw/archive/Sample - Superstore.csv`
- Rows analyzed: 9,994

## Deliverables

- `chart_generation.py`
- `plotly_dashboard.html`
- `echarts_options.json`

## Charts

1. Sales by Category (Plotly)
2. Profit by Region (Plotly)
3. Monthly Sales Trend (Plotly)

## ECharts Configurations

1. Sales by Category
2. Profit by Region

## Run

```powershell
python reports/w7d3/chart_generation.py
```

## Validation

- Python compilation passed.
- Chart generation completed successfully.
- 9,994 rows analyzed.
- Zero invalid dates.
- Three Plotly charts generated.
- ECharts JSON parsed successfully.
- Both ECharts configurations contain valid series.

## CIA Review

Two CIA interactions completed:

1. **Python code review:** Reviewed code quality, data handling, chart generation, validation, and maintainability.
2. **ECharts configuration review:** Received PASS for ECharts option structure, label/data alignment, and JSON serialization.

Both reviews completed. The ECharts configurations are ready for frontend consumption.

Note: Live CIA frontend integration has not been established.

## Limitation

This is a standalone chart-generation workflow. ECharts-compatible JSON is generated for frontend integration, but live CIA frontend integration has not yet been established.
