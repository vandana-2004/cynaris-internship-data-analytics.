# Week 3 — Day 5: KPI Design

## 1. Business Domain

**Domain:** Retail Sales Analytics

**Objective:** Monitor sales performance, customer activity, product demand, profitability, and business growth to support better decisions.

## 2. KPI Framework

| No. | KPI                         | Formula                                                      | Owner              | Frequency | Target          | Type    |
| --- | --------------------------- | ------------------------------------------------------------ | ------------------ | --------- | --------------- | ------- |
| 1   | Total Sales                 | Sum of sales revenue                                         | Sales Manager      | Daily     | ₹2,50,000/month | Lagging |
| 2   | Sales Growth (%)            | (Current Sales - Previous Sales) / Previous Sales × 100      | Sales Manager      | Monthly   | ≥ 10%           | Lagging |
| 3   | Total Orders                | Count of unique order IDs                                    | Operations Manager | Daily     | ≥ 100/month     | Lagging |
| 4   | Average Order Value         | Total Sales / Total Orders                                   | Sales Manager      | Monthly   | ≥ ₹2,500        | Lagging |
| 5   | Profit Margin (%)           | Profit / Sales × 100                                         | Finance Manager    | Monthly   | ≥ 20%           | Lagging |
| 6   | Customer Retention (%)      | Returning Customers / Eligible Previous Customers × 100      | CRM Manager        | Monthly   | ≥ 80%           | Lagging |
| 7   | Customer Acquisition        | Number of new customers acquired                             | Marketing Manager  | Monthly   | ≥ 50            | Lagging |
| 8   | Website Conversion Rate (%) | Completed Purchases / Website Visitors × 100                 | Marketing Manager  | Weekly    | ≥ 3%            | Lagging |
| 9   | Inventory Availability (%)  | Available Product Units / Total Required Product Units × 100 | Inventory Manager  | Daily     | ≥ 95%           | Leading |
| 10  | Sales Leads Generated       | Number of qualified sales leads generated                    | Marketing Manager  | Weekly    | ≥ 25            | Leading |

**Note:** Targets are illustrative business goals, not actual company results. Some KPIs require additional customer, profit, website, or inventory data that is not present in the basic sales dataset.

## 3. Leading vs Lagging Indicators

### Leading Indicators

Leading indicators help predict future performance.

- Inventory Availability: Low availability may reduce future sales.
- Sales Leads Generated: More qualified leads may increase future orders.

### Lagging Indicators

Lagging indicators measure results that have already occurred.

- Total Sales
- Sales Growth
- Total Orders
- Average Order Value
- Profit Margin
- Customer Retention
- Customer Acquisition
- Website Conversion Rate

## 4. Dashboard Design

Create a single-page Power BI dashboard titled **Retail Sales KPI Dashboard**.

Include these visuals:

1. Total Sales — KPI card
2. Total Orders — KPI card
3. Average Order Value — KPI card
4. Sales Growth — KPI card, if historical sales data is available
5. Sales by Region — bar chart
6. Sales by Category — column chart
7. Sales Trend by Date — line chart, if date data is available
8. Region, Category, and Date slicers where the corresponding fields exist

Use a clear layout, descriptive titles, consistent formatting, and appropriate currency and percentage formats.

## 5. KPI Narrative

The dashboard should help managers understand overall sales, order volume, average order value, regional performance, and category contribution.

Compare sales across regions and categories to identify strong and weak performers. Investigate unusual changes by checking the selected date range, product mix, order volume, and data quality.

Do not claim that sales increased or decreased without comparing actual results across time periods. Sales growth, retention, profit margin, and conversion rate should only be reported when the required source data is available.

## 6. SMART KPI Principles

A good KPI should be:

- **Specific:** Clearly identify what is measured.
- **Measurable:** Have a defined formula and reliable data.
- **Achievable:** Use a realistic target based on historical performance.
- **Relevant:** Support a business objective.
- **Time-bound:** Specify when performance is reviewed.

## 7. KPI, Metric, and Measure

- **Metric:** A quantitative value used to monitor business activity, such as order count.
- **KPI:** A metric selected to track progress toward an important business goal, such as monthly sales growth.
- **Measure:** A calculated value, often in Power BI, such as Total Sales = SUM(Sales).

## 8. Limitations and Assumptions

The targets in this document are illustrative and should be validated against company objectives and historical data. The existing sales dataset may not contain all fields required to calculate every KPI.

For unavailable data, document the limitation instead of inventing results.

## 9. Conclusion

A well-designed KPI framework connects business goals to measurable outcomes. Combining clear definitions, accountable owners, review frequencies, realistic targets, and an interactive dashboard helps managers make informed decisions.
