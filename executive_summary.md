# Retail Sales & Profitability Analysis — Executive Summary

## Business Question

How can a retail business improve profitability by identifying its strongest products, regions, and discounting patterns?

## Key Findings

- **Overall performance:** The dataset contains 9,994 records and 5,009 unique orders, generating total sales of $2,297,200.86 and total profit of $286,397.02.
- **Regional performance:** The West region generated the highest sales ($725,457.82) and profit ($108,418.45). The Central region generated $501,239.89 in sales and $39,706.36 in profit.
- **Category performance:** Technology generated the highest sales ($836,154.03) and profit ($145,454.95). Furniture generated $741,999.80 in sales but only $18,451.27 in profit.

## Three Actionable Recommendations

1. **Review Furniture profitability:** Analyze Furniture sub-categories, pricing, costs, and discount levels to identify opportunities to improve margins.
2. **Learn from high-performing regions:** Investigate the West region's product mix and sales performance, then test suitable strategies in lower-profit regions, especially Central.
3. **Evaluate discounting carefully:** Use the discount and profit analysis to identify discount levels associated with weaker profits. Test changes and monitor both sales and profit before making broad pricing decisions.

## Dashboard

The Power BI dashboard is saved as `capstone_dashboard.pbix`. It includes KPI cards, monthly sales trends, regional and sub-category profit charts, and Region, Category, and Order Date slicers.

## Method

The analysis used the Sample Superstore dataset, with 9,994 records. Data quality checks found no missing values or duplicate rows. Date fields were converted to datetime format, followed by exploratory analysis, visualisation, and a Welch's t-test comparing profit for discounted and non-discounted records.

## Conclusion

The analysis indicates that improving Furniture profitability and reviewing discounting practices are useful priorities, while the West region and Technology category provide strong performance benchmarks. Further investigation should account for product mix, costs, and regional differences before implementing changes.
