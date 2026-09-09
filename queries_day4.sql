-- Task 1: Find sales above the average sales amount

SELECT *
FROM sales
WHERE sales_amount > (
    SELECT AVG(sales_amount)
    FROM sales
);

-- Task 2: Find top performer per region

SELECT s1.region, s1.product, s1.sales_amount
FROM sales s1
WHERE s1.sales_amount = (
    SELECT MAX(s2.sales_amount)
    FROM sales s2
    WHERE s2.region = s1.region
);

-- Task 3: CTE using WITH clause

WITH average_sales AS (
    SELECT AVG(sales_amount) AS avg_sales
    FROM sales
)
SELECT *
FROM sales
WHERE sales_amount > (
    SELECT avg_sales
    FROM average_sales
);

-- Task 4: Chain 2 CTEs

WITH regional_sales AS (
    SELECT
        region,
        SUM(sales_amount) AS total_sales
    FROM sales
    GROUP BY region
),
average_region_sales AS (
    SELECT
        AVG(total_sales) AS avg_sales
    FROM regional_sales
)
SELECT
    region,
    total_sales
FROM regional_sales
WHERE total_sales > (
    SELECT avg_sales
    FROM average_region_sales
);