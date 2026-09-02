CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    unit_price REAL,
    order_date TEXT,
    region TEXT,
    sales_rep TEXT,
    discount REAL
);

INSERT INTO orders
(order_id, customer_name, product, category, quantity, unit_price, order_date, region, sales_rep, discount)
VALUES
(1, 'Ananya', 'Laptop', 'Electronics', 5, 75000, '2026-01-05', 'North', 'Rahul', 10),
(2, 'Arjun', 'Chair', 'Furniture', 12, 2500, '2026-01-07', 'South', 'Priya', 5),
(3, 'Bhavna', 'Shirt', 'Clothing', 20, 1200, '2026-01-10', 'West', 'Amit', NULL),
(4, 'Carlos', 'Phone', 'Electronics', 8, 35000, '2026-01-12', 'East', 'Neha', 15),
(5, 'Deepak', 'Desk', 'Furniture', 6, 8000, '2026-01-15', 'North', 'Rahul', NULL),
(6, 'Aisha', 'Shoes', 'Clothing', 15, 3000, '2026-01-18', 'South', 'Priya', 10),
(7, 'Farhan', 'Monitor', 'Electronics', 11, 15000, '2026-01-20', 'West', 'Amit', 5),
(8, 'Gaurav', 'Table', 'Furniture', 4, 12000, '2026-01-22', 'East', 'Neha', NULL),
(9, 'Anjali', 'Headphones', 'Electronics', 25, 2500, '2026-01-25', 'North', 'Rahul', 20),
(10, 'Harish', 'Jacket', 'Clothing', 7, 4500, '2026-01-28', 'South', 'Priya', NULL);
