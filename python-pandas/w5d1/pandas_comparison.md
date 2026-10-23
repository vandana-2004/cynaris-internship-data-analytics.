# PandasAI vs Manual Pandas Comparison

- Dataset: `sales_data.csv`
- Rows: 10
- Comparison questions: 3

## Results

| Question | Manual Pandas result | PandasAI result | Status |
|---|---|---|---|
| What is the total sales? | `217500.0` | 217500.0 | AI answer received |
| What is the average sales? | `21750.0` | 21750.0 | AI answer received |
| What are total sales by region? | `{"South": 91500.0, "West": 75000.0, "North": 51000.0}` |   region  total_sales
0  South      91500.0
1   West      75000.0
2  North      51000.0 | AI answer received |

## AI Query Summary

- AI status: `completed`
- Successful queries: 10
- Total questions: 10

## Error Handling

Individual query errors are recorded in `errors.log`.
AI results are saved in `query_results.json`.
