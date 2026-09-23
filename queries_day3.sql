USE retail_sales;
-- SQL Aggregations — GROUP BY & HAVING
-- Week 1 | Day 3


-- 1. Count total number of sales
SELECT COUNT(*) AS total_sales
FROM sales;


-- 2. Calculate total revenue
SELECT SUM(sales_amount) AS total_revenue
FROM sales;


-- 3. Calculate average sale amount
SELECT AVG(sales_amount) AS average_sale
FROM sales;


-- 4. Find the highest sale
SELECT MAX(sales_amount) AS highest_sale
FROM sales;


-- 5. Find the lowest sale
SELECT MIN(sales_amount) AS lowest_sale
FROM sales;


-- 6. Group sales by region
SELECT
    region,
    COUNT(*) AS total_orders,
    SUM(sales_amount) AS total_revenue,
    AVG(sales_amount) AS average_sale
FROM sales
GROUP BY region;


-- 7. Group sales by category
SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(sales_amount) AS total_revenue
FROM sales
GROUP BY category;


-- 8. Filter groups using HAVING
SELECT
    region,
    SUM(sales_amount) AS total_revenue
FROM sales
GROUP BY region
HAVING SUM(sales_amount) > 100000;


-- 9. Window function: running total by region
SELECT
    sale_id,
    sale_date,
    region,
    sales_amount,
    SUM(sales_amount) OVER (
        PARTITION BY region
        ORDER BY sale_date
    ) AS running_total
FROM sales;


-- 10. Group sales by month
SELECT
    YEAR(sale_date) AS sale_year,
    MONTH(sale_date) AS sale_month,
    SUM(sales_amount) AS monthly_revenue,
    COUNT(*) AS total_orders
FROM sales
GROUP BY YEAR(sale_date), MONTH(sale_date)
ORDER BY sale_year, sale_month;