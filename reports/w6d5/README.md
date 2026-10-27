# W6D5 — Natural-Language SQL Project

## Objective
Verify natural-language SQL analysis against the local SQLite database.

## Components
- `vanna_sql/w6d1_app.py`: FastAPI endpoint at `POST /cia/sql-analyst`.
- `vanna_sql/w6d2_training_examples.json`: five question-to-SQL examples.
- `vanna_sql/validate_w6d2.py`: predefined SQL validation tests.
- `sales.db`: SQLite database containing the `orders` table.

## Live Query Verification

All 10 API queries returned successful results. Each result was independently checked against SQLite.

| # | Question / Check | Verified result | Status |
|---|---|---|---|
| 1 | How many orders are there? | 10 orders | Passed |
| 2 | How many orders are in each category? | Clothing: 3; Electronics: 4; Furniture: 3 | Passed |
| 3 | What is the total sales amount for all orders? | 1,002,750.0 | Passed |
| 4 | What is the average order quantity? | 11.3 | Passed |
| 5 | Which product has the highest total quantity sold? | Headphones: 25 units | Passed |
| 6 | What is the total sales amount for each region? | East: 286,000; North: 435,500; South: 100,500; West: 180,750 | Passed |
| 7 | How many orders were placed in each region? | East: 2; North: 3; South: 3; West: 2 | Passed |
| 8 | What is the total quantity sold for each product? | Chair: 12; Desk: 6; Headphones: 25; Jacket: 7; Laptop: 5; Monitor: 11; Phone: 8; Shirt: 20; Shoes: 15; Table: 4 | Passed |
| 9 | Which sales representative generated the highest total sales? | Rahul: 435,500.0 | Passed |
| 10 | What is the earliest order date? | 2026-01-05 | Passed |

### Sales Calculation
Sales totals were checked using the discount as a percentage and treating NULL discounts as zero:

`quantity * unit_price * (1 - COALESCE(discount, 0) / 100.0)`

## Verification Summary
- Live natural-language API queries: 10/10 returned successful results.
- Independent SQLite cross-checks: 10/10 matched the API results.
- Earliest order date: API and SQLite both returned `2026-01-05`.
- The 10 live queries are separate from the 10 predefined W6D2 SQL validation tests.
- W6D5 CIA interactions and Role Mentor review: not yet confirmed; record only after they occur.

## Scope and Limitations
The verified database is a sales-orders database. A CRM-specific schema and a completed dashboard have not been established by these checks.

## Safety
Verify generated SQL and results before relying on them. Do not commit API keys or other secrets.
