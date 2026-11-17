# W11D2 ? CIA Mentor Review Evidence

## Interaction 1 ? Technical review

**Status:** Completed

### Feedback received
- Retain interactive Plotly HTML charts alongside static presentation images.
- Consider providing access to interactive charts from the presentation or its supporting materials.
- Check KPI calculations, INR and percentage formatting, and consistency with the earlier EDA.
- Apply exception handling where calculations involve possible division by zero.

### Actions and considerations
- Retained five interactive Plotly HTML charts and five static chart images.
- Generated an eight-slide PowerPoint report.
- Validated key totals and Amount coverage against the W11D2 outputs.
- No YoY or conversion-rate KPI was introduced because those metrics were not part of this analysis.

## Interaction 2 ? Business stakeholder review

**Status:** Completed

### Context supplied to CIA
The report overview, chart descriptions, and definitions and limitations of Recorded Amount, net revenue, and profit were supplied for review. CIA did not directly inspect the local repository files or execute the report.

### Feedback received
- Do not equate Recorded Amount with net revenue or profit without the required financial definitions and cost information.
- Clarify the business meaning of the source category label `Set`; do not assume it means a product bundle.
- Treat the 76.98% share of the top two categories as a concentration finding worth monitoring.
- A Pareto chart can make the category concentration easier to communicate.
- Preserve the Amount completeness context, including 93.96% coverage and 7,795 missing values.

### Actions taken
- Added an interactive Pareto chart and a PowerPoint-ready Pareto image.
- Added a dedicated Pareto slide to the presentation.
- Documented the 76.98% top-two-category share.
- Flagged `Set` as an undefined source category requiring business confirmation.
- Retained the caveat that Recorded Amount is not confirmed net revenue or profit.

## Review scope and evidence limitation

Both mentor interactions were completed using implementation details and report information supplied during the conversations. These notes record the feedback and resulting changes; they do not claim that CIA independently accessed or tested the local source files.

## Final report checks
- Python compilation passed.
- Report generation and its 16-output validation passed.
- Five interactive HTML charts and five static chart images were generated.
- Pareto cumulative share reaches 100.00%; top-two share is 76.98%.
- PowerPoint contains eight slides.
