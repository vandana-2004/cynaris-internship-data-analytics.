# W12D1 Production Architecture Review

## Project
Indian Business Sales EDA

## Architecture assessment

| Layer | Current implementation | Production recommendation |
|---|---|---|
| Ingestion | Local CSV with Pandas | Managed ingestion and schema validation |
| Data quality | Column, null and duplicate checks | Automated quality gates |
| Processing | Python and Pandas batch processing | Modular, tested transformation pipeline |
| Storage | Source CSV | Database or analytical warehouse |
| Analytics | EDA and stakeholder analysis | Reusable analytical data models |
| Reporting | CSV, charts and Markdown | Managed BI and scheduled refresh |
| Security | Local project access | Least-privilege access and secret management |
| Monitoring | Execution-time measurements | Centralized logs, alerts and freshness checks |

## Implemented checks

- Required column validation
- Per-column missing-value profiling
- Duplicate record count
- Numeric Amount conversion validation
- Date conversion validation
- Dataset memory measurement
- CSV loading-time measurement
- Runtime environment identification

## Production limitations

- The current workflow reads a local CSV.
- No automated orchestration is implemented.
- No centralized database is implemented in this review.
- No automated alerting or scheduled refresh is implemented.
- Access control and deployment require additional design.

## Architecture recommendation

Use a layered batch architecture:

1. Source ingestion
2. Raw data storage
3. Data validation
4. Transformation and analytical processing
5. Curated storage
6. BI reporting
7. Monitoring and governance

## Interpretation

This is an architecture assessment of the existing EDA project.
Performance measurements are specific to the execution environment
and should not be treated as production service-level guarantees.
