# W5D5 PandasAI Analysis

- Dataset: `data/w5d3/sales_100k.csv`
- Rows loaded: 100,000
- Analysis: AI-generated total sales by region

## PandasAI Result

region total_sales
0 West 114967000.0
1 East 114938000.0
2 South 114918000.0
3 North 114889000.0

## Data Quality Note

A cross-tabulation of all 100,000 rows confirmed that each region contains only one category, with 25,000 rows per pairing:

- East � Food
- North � Electronics
- South � Clothing
- West � Home

All other region-category combinations have zero rows. The reason for this structure has not been confirmed.

## Business Insight

Total sales across the four observed region-category pairings range from 114,889,000 to 114,967,000. West/Home has the highest total, while North/Electronics has the lowest. Since region and category are confounded, the difference cannot be attributed to either factor independently.

## Limitation

The dataset has no cost or profit fields, so profitability and profit margins cannot be calculated. A dataset with multiple categories represented in each region is needed to compare regional and category performance independently.

## Verification Log

Source dataset: `data/w5d3/sales_100k.csv`

Run the following checks using Python to reproduce the analysis:

```python
import pandas as pd

df = pd.read_csv("data/w5d3/sales_100k.csv")

print("Dataset shape:", df.shape)
print(df.groupby("region")["sales"].sum().sort_values(ascending=False))
print(pd.crosstab(df["region"], df["category"]))
```

Expected dataset shape: `(100000, 5)`.

The cross-tabulation shows 25,000 rows each for East/Food, North/Electronics, South/Clothing, and West/Home. All other region-category combinations contain zero rows. Regional sales totals should match the PandasAI results documented above.

Because region and category are confounded, their independent effects cannot be determined. Profitability cannot be assessed without cost or profit fields.
