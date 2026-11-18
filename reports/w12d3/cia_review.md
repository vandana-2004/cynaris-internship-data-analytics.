\# W12D3 — CIA Security Audit Review



\## Review 1 — Security Architecture and Privacy



\*\*Review status:\*\* Partial CIA response received.



\### Positive observations

\- Identified four potentially sensitive location columns.

\- Detected 18 phone-pattern matching cells in `ship-city`.

\- Found zero email-pattern matches.

\- Used privacy-conscious reporting without printing raw matched values.



\### Recommendations received

\- Treat the 18 phone-pattern matches as potential data-quality or privacy issues requiring review.

\- Consider masking or generalizing location fields in public-facing reports.

\- Recognize that regex-based PII detection can produce false positives and false negatives.

\- Consider additional PII categories and document detection limitations.



\### Evidence

\- 128,975 dataset rows and 24 columns.

\- 18 phone-pattern matching cells in `ship-city`.

\- Zero email-pattern matches.



\*\*Review limitation:\*\* The CIA response was cut off during the credential-scanning evaluation. No missing verdict or recommendations have been assumed.



\---



\## Review 2 — Production Readiness



\*\*Review status:\*\* Partial CIA response received.



\### Positive observations

\- The audit covers data volume, PII, duplicates, credentials and permissions.

\- Chunk-based processing and avoiding raw-value output demonstrate good security hygiene.



\### Recommendations received

\- Add an analyst-focused risk interpretation instead of reporting scan counts alone.

\- Contextualize the 18 phone-pattern matches and recommend review or regex refinement.

\- Explain the implications of 210,495 missing cells without automatically treating them as a security vulnerability.

\- Expand PII screening to consider IP addresses, dates of birth and India-specific identifiers where relevant.

\- Treat the current regex approach as a basic screen, not production-grade PII detection.



\### Evidence

\- 128,975 rows and 24 columns.

\- Four potentially sensitive location columns.

\- 18 unverified phone-pattern matching cells.

\- Zero email-pattern matches.

\- Zero duplicate rows detected.

\- 210,495 missing cells.

\- 46 source files scanned.

\- Zero potential credential findings.

\- Basic Windows permission screening returned `NO\_BROAD\_WRITE\_GRANT\_DETECTED`.



\*\*Review limitation:\*\* The CIA response ended during its context-aware scanning discussion. No final verdict has been assumed.



\---



\## Consolidated Action Plan



1\. Keep phone-pattern matches classified as unverified potential matches.

2\. Document regex false-positive and false-negative limitations.

3\. Explain missing-value findings in the context of data quality.

4\. Consider additional PII categories for future improvements.

5\. Treat the Windows ACL result as a limited screening result, not proof of complete security.

6\. Document the scope and limitations of credential scanning.

7\. Require human review before treating automated findings as confirmed incidents.



\## Overall Assessment



The implementation provides a useful internship-level technical security screening exercise. The CIA feedback highlights improvements needed in risk interpretation, PII coverage and production-readiness documentation.



\*\*Overall status: PASS WITH IMPROVEMENTS — provisional project assessment, not a final CIA verdict.\*\*
