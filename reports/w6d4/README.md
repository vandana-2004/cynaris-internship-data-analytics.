# W6D4: Combining Vanna and Superset for Executive Reporting

## Objective
Improve the Vanna SQL analyst API so its health and request-validation
behavior can be tested without initializing the external LLM client.

## Implementation
- Initialize the Vanna agent lazily when a non-empty analyst request arrives.
- Keep SQLite queries read-only using the existing SQLite authorizer.
- Report whether the Groq API key is configured without exposing its value.
- Return HTTP 503 when the Groq key is missing.

## API test evidence
Tested with FastAPI TestClient in the project virtual environment.

| Check | Expected | Observed |
|---|---:|---:|
| GET /health | 200 | 200 |
| POST /cia/sql-analyst with an empty question | 400 | 400 |
| POST /cia/sql-analyst with a valid question and no Groq key | 503 | 503 |
| POST /cia/sql-analyst with Groq configured: 'How many orders are there?' | 200 | 200; total_orders = 10 |

## Existing SQL validation
The existing W6D2 validator reported 10/10 SQL validation tests passed
and found five training examples. These tests validate known SQL queries;
they do not prove that ten live AI-generated queries passed.

## Live AI-generated query validation
Ten distinct live Vanna/Groq questions returned HTTP 200. Each result was
compared with a direct, read-only SQLite query.

| # | Question / result | Verification |
|---:|---|---|
| 1 | Total orders = 10 | Matched SQLite |
| 2 | Orders by category: Clothing 3, Electronics 4, Furniture 3 | Matched SQLite |
| 3 | Orders by region: East 2, North 3, South 3, West 2 | Matched SQLite |
| 4 | Average order quantity = 11.3 | Matched SQLite |
| 5 | Total quantity ordered = 113 | Matched SQLite |
| 6 | Sales by region: East 328000.0, North 485500.0, South 106500.0, West 189000.0 | Matched SQLite |
| 7 | Average unit price by category: Clothing 2900.0, Electronics 31875.0, Furniture 7500.0 | Matched SQLite |
| 8 | Orders by sales representative: Amit 2, Neha 2, Priya 3, Rahul 3 | Matched SQLite |
| 9 | Quantity by category: Clothing 42, Electronics 49, Furniture 22 | Matched SQLite |
| 10 | Highest order value: order #1, 375000.0 | Matched SQLite |

## Limitations and remaining work
- The existing W6D2 validator's 10/10 checks use predefined SQL and are separate
  from these ten live AI-generated query tests.
- Superset installation, connection, and dashboard integration have not been verified.
- The combined Vanna and Superset workflow is not yet complete.
- Both CIA review interactions are complete and documented.
- PR #41 remains open pending final review and merge.

## Safety
The SQLite runner retains its read-only URI and SQL authorizer restrictions.
