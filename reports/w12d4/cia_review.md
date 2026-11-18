# W12D4 â€” CIA Review Record

## Purpose

Record the two CIA interactions completed during final documentation and demo preparation. Both interactions were based on project metadata and summaries rather than direct inspection of the documentation files or presentation.

## CIA Interaction 1 â€” Preliminary Documentation Review

**Scope:** Preliminary review of dataset metadata, project scope, and documentation file names.

**CIA limitation:** CIA explicitly stated that it had not received the actual contents of README.md, demo_script.md, viva_answers.md, or final_checklist.md. It therefore could not verify their wording, completeness, clarity, reproducibility, or presentation quality.

**Feedback received:**
- Confirmed the dataset metadata provided for review: 128,975 rows and 121,180 valid Amount observations.
- Highlighted the need to explain how 7,795 missing Amount values were handled.
- Flagged the need to distinguish the valid Amount count from the full dataset row count.
- Identified 3,600 potential IQR outliers and discussed the denominator used for the outlier percentage.
- Noted that a mean greater than the median is consistent with positive skew.

**Calculation clarification:**
3,600 / 121,180 = approximately 2.97% of valid Amount observations.
3,600 / 128,975 = approximately 2.79% of all dataset rows.

**Outcome:** Preliminary feedback received. This was not a full documentation review or a formal CIA approval.

## CIA Interaction 2 â€” Demo and Viva Review

**Scope:** Review of the proposed demo flow, technical explanations, business insights, and viva preparation.

**CIA limitation:** CIA stated that it had not received the actual PowerPoint file, repository, or demo transcript. It could not assess individual slides, code execution, or the actual presentation.

**Feedback received:**
- Identified a potential risk of presenting too many charts without a clear narrative.
- Recommended grouping the six visualizations into three story arcs:
  1. Understanding the data.
  2. Understanding business performance.
  3. Exploring trends and geography.
- Recommended giving each slide one clear takeaway.
- Suggested preparing to explain the IQR method and why potential outliers were retained.
- Asked for clarification of the handling of missing Amount values.

**Response completeness:** The CIA response ended before its full feedback was delivered. The interaction is recorded as partial feedback, not a complete demo or viva assessment.

**Outcome:** Partial review feedback received. No formal CIA pass or approval was claimed.

## Overall Review Summary

Two CIA interactions were completed and recorded.

The feedback informed the documentation structure, demo narrative, statistical explanations, and clarification of missing-value and outlier calculations.

The original `reports/w8d3/eda_summary.txt` was subsequently checked against the documented figures. It confirms the dataset dimensions, missing Amount count, valid Amount count, distribution statistics, IQR results, and analysis assumptions.

**Overall status:** CIA feedback recorded; final documentation evidence independently checked against the original EDA summary. Direct CIA inspection of the final documents and presentation was not performed.
