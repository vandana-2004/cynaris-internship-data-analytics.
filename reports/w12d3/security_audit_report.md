# W12D3 - Security Audit Report

## 1. Audit Overview

- Dataset: `indian_business_sales.csv`
- Dataset size: 65.73 MB
- Dataset size in bytes: 68,923,428
- Rows inspected: 128,975
- Columns inspected: 24
- Audit mode: Read-only
- Customer values printed: No

## 2. Potentially Sensitive Columns

- `ship-city` - Potential location information
- `ship-country` - Potential location information
- `ship-postal-code` - Potential location information
- `ship-state` - Potential location information

## 3. Privacy Pattern Detection

- Email pattern matches: 0
- Phone pattern matches: 18
- Email match columns: []
- Phone match columns: ['ship-city']
- Pattern audit status: REVIEW_REQUIRED
- Matching values are intentionally excluded.
- Pattern matches require manual verification.

## 4. Data Integrity

- Total rows: 128,975
- Exact duplicate rows: 0
- Total missing cells: 210,495
- Completely empty columns: []
- Duplicate detection uses SHA-256 row fingerprints.

### Missing Values by Column

| Column | Missing values |
|---|---:|
| ASIN | 0 |
| Amount | 7,795 |
| B2B | 0 |
| Category | 0 |
| Courier Status | 6,872 |
| Date | 0 |
| Fulfilment | 0 |
| Order ID | 0 |
| Qty | 0 |
| SKU | 0 |
| Sales Channel  | 0 |
| Size | 0 |
| Status | 0 |
| Style | 0 |
| Unnamed: 22 | 49,050 |
| currency | 7,795 |
| fulfilled-by | 89,698 |
| index | 0 |
| promotion-ids | 49,153 |
| ship-city | 33 |
| ship-country | 33 |
| ship-postal-code | 33 |
| ship-service-level | 0 |
| ship-state | 33 |

## 5. Credential Exposure Audit

- Source files scanned: 46
- Potential findings: 0
- Status: NO_MATCHES_DETECTED
- Both tracked and non-ignored untracked source files are included.
- Virtual environments, datasets and generated artifacts are excluded.
- Secret values are never recorded.

| File | Line | Finding type |
|---|---:|---|

## 6. Windows File Permission Audit

- Status: NO_BROAD_WRITE_GRANT_DETECTED
- Assessment: Basic ACL screening did not detect broad write permissions.
- Scope: Dataset file ACL screening.
- This is not a complete review of effective permissions.

## 7. Security Recommendations

1. Restrict access to potentially sensitive location information.
2. Avoid exposing customer identifiers in logs and reports.
3. Store API keys in environment variables or a secret manager.
4. Never commit credentials to Git.
5. Review Windows file and directory permissions.
6. Validate incoming datasets before processing.
7. Apply data minimisation and retention policies.
8. Investigate phone and email pattern matches.
9. Review credential scanner findings manually.
10. Introduce automated security checks into CI/CD.

## 8. Audit Limitations

- Pattern matching may produce false positives and false negatives.
- No pattern match does not prove that a dataset contains no PII.
- Credential scanning covers configured source extensions only.
- Credential scanning is not a replacement for a dedicated secret scanner.
- ACL screening checks selected broad principals and permissions only.
- SHA-256 fingerprints provide highly reliable duplicate detection, but are not a mathematical proof of row equality.
- This audit does not establish legal or regulatory compliance.

## 9. Conclusion

The automated security audit completed its configured checks. Potential findings require human verification. A clean automated scan should not be interpreted as proof that the platform is completely secure.
