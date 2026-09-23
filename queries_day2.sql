-- Week 1 Day 2: SQL Joins
-- SQL Joins - Combining Tables

-- Create Departments table
CREATE TABLE Departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT
);

-- Create Employees table
CREATE TABLE Employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT,
    department_id INTEGER,
    manager_id INTEGER
);

-- Insert Departments
INSERT INTO Departments (department_id, department_name) VALUES
(1, 'HR'),
(2, 'IT'),
(3, 'Finance'),
(4, 'Marketing');

-- Insert Employees
INSERT INTO Employees (employee_id, employee_name, department_id, manager_id) VALUES
(101, 'Anita', 1, NULL),
(102, 'Rahul', 2, 105),
(103, 'Priya', 2, 105),
(104, 'Kiran', NULL, 105),
(105, 'Suresh', 2, NULL);

-- 1. INNER JOIN
SELECT
    e.employee_name,
    d.department_name
FROM Employees AS e
INNER JOIN Departments AS d
    ON e.department_id = d.department_id;

-- 2. LEFT JOIN
SELECT
    e.employee_name,
    d.department_name
FROM Employees AS e
LEFT JOIN Departments AS d
    ON e.department_id = d.department_id;

-- 3. RIGHT JOIN
SELECT
    e.employee_name,
    d.department_name
FROM Employees AS e
RIGHT JOIN Departments AS d
    ON e.department_id = d.department_id;

-- 4. FULL OUTER JOIN
SELECT
    e.employee_name,
    d.department_name
FROM Employees AS e
FULL OUTER JOIN Departments AS d
    ON e.department_id = d.department_id;

-- 5. JOIN and duplicate-row concept
SELECT
    e.employee_name,
    d.department_name
FROM Employees AS e
JOIN Departments AS d
    ON e.department_id = d.department_id;

-- 6. SELF JOIN
SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM Employees AS e
LEFT JOIN Employees AS m
    ON e.manager_id = m.employee_id;

-- 7. TABLE ALIASES
SELECT
    e.employee_name,
    d.department_name
FROM Employees AS e
LEFT JOIN Departments AS d
    ON e.department_id = d.department_id;