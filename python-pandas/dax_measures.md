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

**Explanation:** `CALCULATE()` evaluates the measure under a modified filter context, here restricting the calculation to the South region.

## 3. Year-to-Date Sales

```dax
YTD Sales =
CALCULATE(
    [Total Sales],
    DATESYTD('Date'[Date])
)
```

**Explanation:** Calculates sales from the beginning of the year through the current date in the applicable date context. This requires a proper Date table related to the sales table.

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

**Explanation:** Calculates cumulative sales up to the current row's order ID. `EARLIER()` refers to an earlier row context. This example assumes order IDs define the intended sequence; a date-based running total would require a suitable date column.

## 5. Profit Margin Calculated Column

```dax
Profit Margin % =
DIVIDE(
    sales_data[profit],
    sales_data[sales],
    0
) * 100
```

**Explanation:** Calculates profit as a percentage of sales and returns zero when sales is zero. This requires a `profit` column in the data; the current dataset does not contain one, so this expression cannot be evaluated until profit data is available.

## Row Context, Filter Context and Context Transition

- **Row context:** Evaluates an expression for the current row, as in a calculated column.
- **Filter context:** The rows included in a calculation after report filters, slicers and DAX filters are applied.
- **Context transition:** `CALCULATE()` can convert an existing row context into filter context, allowing an expression to be evaluated for the current row's values.

## Data Limitations

The current sales dataset has no date or profit column. The YTD measure requires a proper date table and relationship. The profit margin column requires actual profit data. These fields must be added from a valid source before those calculations can be used in the report.
