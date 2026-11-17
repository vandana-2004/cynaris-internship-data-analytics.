-- category_amount.csv
SELECT category AS Category,
               COUNT(*) AS Order_Count,
               ROUND(SUM(amount), 2) AS Recorded_Amount
        FROM orders
        WHERE amount IS NOT NULL
        GROUP BY category
        ORDER BY Recorded_Amount DESC;

-- monthly_amount.csv
SELECT substr(order_date, 1, 7) AS Month,
               COUNT(*) AS Order_Count,
               ROUND(SUM(amount), 2) AS Recorded_Amount
        FROM orders
        WHERE amount IS NOT NULL
        GROUP BY substr(order_date, 1, 7)
        ORDER BY Month;

-- order_status.csv
SELECT status AS Status,
               COUNT(*) AS Order_Count
        FROM orders
        GROUP BY status
        ORDER BY Order_Count DESC;

-- state_amount.csv
SELECT state AS State,
               COUNT(*) AS Order_Count,
               ROUND(SUM(amount), 2) AS Recorded_Amount
        FROM orders
        WHERE amount IS NOT NULL
        GROUP BY state
        ORDER BY Recorded_Amount DESC;

-- kpi_metrics.csv
SELECT
            COUNT(*) AS Total_Orders,
            ROUND(SUM(amount), 2) AS Recorded_Amount_Total,
            ROUND(100.0 * COUNT(amount) / COUNT(*), 2)
                AS Amount_Coverage_Pct,
            SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)
                AS Missing_Amount_Rows,
            SUM(CASE WHEN lower(status) LIKE '%cancel%' THEN 1 ELSE 0 END)
                AS Cancelled_Status_Rows
        FROM orders;
