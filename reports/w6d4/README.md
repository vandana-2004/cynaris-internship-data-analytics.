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

## Existing SQL validation
The existing W6D2 validator reported 10/10 SQL validation tests passed
and found five training examples. These tests validate known SQL queries;
they do not prove that ten live AI-generated queries passed.

## Limitations and remaining work
- Live LLM-generated SQL has not been tested because GROQ_API_KEY is
  not configured in the current terminal.
- Superset installation and dashboard integration have not been verified.
- The W6D4 combined Vanna and Superset workflow is not yet complete.
- CIA review interactions and the final pull request remain pending.

## Safety
The SQLite runner retains its read-only URI and SQL authorizer restrictions.
