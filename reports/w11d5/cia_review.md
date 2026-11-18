# W11D5 CIA Review Record

## Review 1 — Business and Stakeholder Review

**Question submitted:** Review the five stakeholder insights for business decision usefulness, metric support, actionable recommendations and misleading interpretations.

### CIA feedback received

- Category concentration (Set and kurta: 76.98%) is supported. CIA recommended adding order-volume context to distinguish volume-driven concentration from price-driven concentration.
- CIA questioned the fulfilment cancellation comparison and recommended investigating cancellation reasons.
- CIA advised against interpreting cancellation amounts as confirmed lost revenue.
- The response received ended partway through the second insight's actionability assessment.

### Assessment and decisions

1. Accept the recommendation to include category order counts alongside recorded Amount shares.
2. Retain the Amazon versus Merchant comparison because these are fulfilment-method values within the dataset, not an external-company benchmark.
3. Investigate cancellation reasons in future analysis if reason-level data becomes available. Do not invent reasons or savings estimates.
4. Retain the caveat that cancellation Amount is not confirmed lost revenue.

## Review 2 — Technical Methodology Review

**Question submitted:** Review data cleaning, missing values, date parsing, aggregation, cancellation calculations, charts, reproducibility and validation.

### CIA feedback received

- CIA clarified that it did not access the local filesystem, inspect the raw CSV or execute the Python script.
- CIA identified a potential selection-bias risk if cancellation counts or rates were calculated after filtering out missing Amount records.
- CIA recommended separating full-dataset count metrics from valid-Amount financial metrics.
- CIA suggested timezone handling for date aggregation, although the source dates are date-only strings without timezone information.
- The response received ended partway through the date-aggregation discussion.

### Assessment and decisions

1. Use the full dataset for cancellation counts and cancellation rates.
2. Use valid Amount records for financial totals and Amount-based shares.
3. Parse source dates with the explicit `%m-%d-%y` format. Timezone conversion is unnecessary for these date-only values.
4. Keep partial-month limitations documented when interpreting monthly results.
5. CIA did not independently execute or verify the script. The local script's successful execution and `VALIDATION: PASS` output are separate verification evidence.

## Overall Review Outcome

**Outcome: PASS WITH IMPROVEMENTS**

The business and technical reviews identified useful presentation and methodology considerations. The feedback was assessed rather than accepted automatically.

Both CIA responses were received as partial responses. This record does not claim that CIA inspected or executed local project files.

## Evidence

- Local analysis script: `stakeholder_analysis.py`
- Stakeholder report: `outputs/stakeholder_report.md`
- Local execution: `VALIDATION: PASS`
- Generated outputs: six CSV files and four charts
- Two CIA interactions completed and documented here.