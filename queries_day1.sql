-- SQL Fundamentals - Week 1 Day 1

-- Query 1
SELECT *
FROM orders;

-- Query 2
SELECT order_id, customer_name, product, quantity
FROM orders
WHERE quantity > 10;

-- Query 3: AND
SELECT order_id, customer_name, product, region, quantity
FROM orders
WHERE region = 'North'
  AND quantity > 10;

-- Query 4: OR
SELECT order_id, customer_name, product, region
FROM orders
WHERE region = 'North'
   OR region = 'South';

-- Query 5: NOT
SELECT order_id, customer_name, product, region
FROM orders
WHERE NOT region = 'North';

-- Query 6: LIKE
SELECT order_id, customer_name, product
FROM orders
WHERE customer_name LIKE 'A%';

-- Query 7: IN
SELECT order_id, product, category
FROM orders
WHERE category IN ('Electronics', 'Furniture', 'Clothing');

-- Query 8: BETWEEN
SELECT order_id, product, unit_price
FROM orders
WHERE unit_price BETWEEN 100 AND 500;

-- Query 9: IS NULL
SELECT order_id, customer_name, product, discount
FROM orders
WHERE discount IS NULL;

-- Query 10: Combined filtering
SELECT order_id, product, category, quantity, unit_price
FROM orders
WHERE category IN ('Electronics', 'Furniture')
  AND unit_price BETWEEN 100 AND 1000
  AND quantity >= 5;








