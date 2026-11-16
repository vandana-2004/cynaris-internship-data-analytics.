-- W6D3 supplementary cancellation analysis
-- Recorded Amount is not verified revenue.

SELECT
    CASE
        WHEN lower(status) LIKE '%cancel%' THEN 'Cancelled'
        ELSE 'Non-Cancelled'
    END AS Order_Group,
    COUNT(*) AS Order_Count,
    ROUND(SUM(amount), 2) AS Recorded_Amount,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)
        AS Missing_Amount_Rows
FROM orders
GROUP BY
    CASE
        WHEN lower(status) LIKE '%cancel%' THEN 'Cancelled'
        ELSE 'Non-Cancelled'
    END
ORDER BY Order_Group;
