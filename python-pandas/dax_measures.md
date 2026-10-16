# Week 3 — Day 2: DAX Basics

## 1. Total Sales Measure

```dax
Total Sales = SUM(sales_data[sales])
```

**Explanation:** Adds the sales values. The result changes according to the filters applied in the report.

## 2. Sales by Region Using CALCULATE()

```dax
South Sales =
CALCULATE(
    [Total Sales],
    sales_data[region] = "South"
)
```

**Explanation:** `CALCULATE()` evaluates a measure under a modified filter context. Here, the calculation is restricted to the South region.

## 3. Year-to-Date Sales

```dax
YTD Sales =
CALCULATE(
    [Total Sales],
    DATESYTD('Date'[Date])
)
```

**Explanation:** Calculates sales from the beginning of the calendar year through the current date in the applicable date context. This requires a proper Date table related to the sales table.

**Practical verification:** Created a separate `TestSales` table and a `DateTable` in Power BI, then established a relationship between `DateTable[Date]` and `TestSales[OrderDate]`. The YTD measure was tested with sample data.

Expected sample results:

| Date             | YTD Sales |
| ---------------- | --------: |
| January 5, 2025  |     1,000 |
| June 15, 2025    |     3,000 |
| January 10, 2026 |     1,500 |
| March 20, 2026   |     4,000 |

The total resets at the beginning of 2026. These are sample results, not actual totals from the original `sales_data` table.

## 4. Running Total Calculated Column

```dax
Running Total =
CALCULATE(
    SUM(sales_data[sales]),
    FILTER(
        sales_data,
        sales_data[order_id] <= EARLIER(sales_data[order_id])
    )
)
```

**Explanation:** Calculates cumulative sales up to the current row's order ID. `EARLIER()` refers to an earlier row context. This example assumes order IDs define the intended sequence. A date-based running total would require a suitable date column.

**Practical verification:** Created a running total calculated column in Power BI using `TestSales[order_id]`. The calculation assumes that order IDs represent the intended sequence.

## 5. Profit Margin Calculated Column

```dax
Profit Margin % =
DIVIDE(
    TestSales[Profit],
    TestSales[Sales],
    0
)
```

**Explanation:** Divides profit by sales and returns zero when sales is zero. The result is formatted as a percentage in Power BI. Do not multiply by 100 when using Percentage formatting.

**Practical verification:** Created the calculated column in the separate `TestSales` table and formatted it as Percentage.

Expected sample results:

| Sales | Profit | Profit Margin |
| ----: | -----: | ------------: |
| 1,000 |    250 |           25% |
| 2,000 |    600 |           30% |
| 1,500 |    300 |           20% |
| 2,500 |    750 |           30% |

These values use sample data, not
