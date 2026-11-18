
"""
W12D3: Security Audit on Data Platform
Project: EDA on Indian Business Dataset

Security checks:
1. Dataset metadata and schema
2. Potentially sensitive columns
3. Email and Indian phone pattern detection
4. Missing values and exact duplicate rows
5. Tracked and untracked source-code credential scanning
6. Windows dataset file ACL screening
7. UTF-8 security report generation

Privacy:
- No customer values are printed.
- No detected secret values are stored in the report.
- Original dataset is never modified.
- Dataset processing uses chunks.
"""

from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess

import pandas as pd


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parents[2]

DATASET = ROOT / "data" / "w8d3" / "indian_business_sales.csv"

OUTPUT = ROOT / "reports" / "w12d3"

REPORT = OUTPUT / "security_audit_report.md"

CHUNK_SIZE = 20_000
MAX_SOURCE_FILE_SIZE = 2_000_000

OUTPUT.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. SECURITY CLASSIFICATION
# ==================================================

POTENTIAL_PII_COLUMNS = {
    "ship-city",
    "ship-state",
    "ship-postal-code",
    "ship-country",
}

IDENTIFIER_COLUMNS = {
    "order id",
    "sku",
    "asin",
}

EXCLUDED_PHONE_COLUMNS = IDENTIFIER_COLUMNS | {
    "ship-postal-code",
}

EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])"
    r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"
    r"(?![\w.-])"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\+91[\s-]?)?"
    r"[6-9]\d{9}"
    r"(?!\d)"
)


# ==================================================
# 3. CREDENTIAL DETECTION RULES
# ==================================================

SECRET_PATTERNS = {
    "API key or password assignment": re.compile(
        r"""(?i)\b(?:api_key|secret_key|access_token|password)\b"""
        r"""\s*[:=]\s*["'][^"'\s]{8,}["']"""
    ),

    "Groq API key": re.compile(
        r"\bgsk_[A-Za-z0-9_-]{20,}\b"
    ),

    "GitHub token": re.compile(
        r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"
    ),

    "AWS access key": re.compile(
        r"\bAKIA[0-9A-Z]{16}\b"
    ),

    "Private key marker": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
}

SCANNED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".ps1",
    ".sh",
    ".env",
}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    ".venv-pandasai",
    "venv",
    "node_modules",
    "__pycache__",
    "data",
    "build",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
    "outputs",
    "charts",
}


# ==================================================
# 4. DATASET METADATA AUDIT
# ==================================================

def audit_file_metadata():

    if not DATASET.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET}"
        )

    if not DATASET.is_file():
        raise ValueError(
            "Dataset path is not a regular file."
        )

    stat = DATASET.stat()

    return {
        "filename": DATASET.name,
        "size_bytes": stat.st_size,
        "size_mb": round(
            stat.st_size / (1024 ** 2), 2
        ),
        "extension": DATASET.suffix,
    }


# ==================================================
# 5. EXACT ROW FINGERPRINT
# ==================================================

def generate_row_fingerprint(row):

    normalized_values = []

    for value in row:

        if pd.isna(value):
            normalized_values.append(None)
        else:
            normalized_values.append(str(value))

    serialized = json.dumps(
        normalized_values,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).digest()


# ==================================================
# 6. DATA PRIVACY AND INTEGRITY AUDIT
# ==================================================

def audit_dataset():

    columns = pd.read_csv(
        DATASET,
        nrows=0,
    ).columns.tolist()

    normalized_columns = {
        str(column).strip().lower()
        for column in columns
    }

    missing_pii_columns = (
        POTENTIAL_PII_COLUMNS - normalized_columns
    )

    missing_counts = Counter()

    total_rows = 0

    email_matches = 0
    phone_matches = 0

    email_columns = set()
    phone_columns = set()

    # SHA-256 fingerprints allow duplicate detection
    # across different chunks without storing row values.
    seen_fingerprints = set()

    duplicate_rows = 0

    for chunk in pd.read_csv(
        DATASET,
        chunksize=CHUNK_SIZE,
        dtype=str,
    ):

        total_rows += len(chunk)

        # ------------------------------------------
        # Missing-value analysis
        # ------------------------------------------

        for column, count in chunk.isna().sum().items():

            missing_counts[column] += int(count)

        # ------------------------------------------
        # Duplicate-row detection
        # ------------------------------------------

        for row in chunk.itertuples(
            index=False,
            name=None,
        ):

            fingerprint = generate_row_fingerprint(row)

            if fingerprint in seen_fingerprints:

                duplicate_rows += 1

            else:

                seen_fingerprints.add(fingerprint)

        # ------------------------------------------
        # Privacy pattern detection
        # ------------------------------------------

        for column in chunk.columns:

            normalized = str(column).strip().lower()

            values = chunk[column].dropna().astype(str)

            if values.empty:
                continue

            # Email detection
            email_count = int(
                values.str.contains(
                    EMAIL_PATTERN,
                    na=False,
                ).sum()
            )

            email_matches += email_count

            if email_count > 0:
                email_columns.add(column)

            # Phone detection
            # Exclude identifiers and postal codes
            # to reduce obvious false positives.

            if normalized not in EXCLUDED_PHONE_COLUMNS:

                phone_count = int(
                    values.str.contains(
                        PHONE_PATTERN,
                        na=False,
                    ).sum()
                )

                phone_matches += phone_count

                if phone_count > 0:
                    phone_columns.add(column)

    empty_columns = [
        column
        for column, count in missing_counts.items()
        if count == total_rows
    ]

    return {
        "columns": columns,
        "total_rows": total_rows,
        "missing_counts": dict(missing_counts),
        "duplicate_rows": duplicate_rows,
        "potential_pii_columns": sorted(
            POTENTIAL_PII_COLUMNS & normalized_columns
        ),
        "missing_expected_pii_columns": sorted(
            missing_pii_columns
        ),
        "email_matches": email_matches,
        "email_columns": sorted(email_columns),
        "phone_matches": phone_matches,
        "phone_columns": sorted(phone_columns),
        "empty_columns": empty_columns,
    }


# ==================================================
# 7. SOURCE FILE DISCOVERY
# ==================================================

def discover_source_files():

    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )

    discovered_files = set()

    for relative_path in result.stdout.split("\0"):

        if not relative_path:
            continue

        path = Path(relative_path)

        # Exclude virtual environments, datasets,
        # build artifacts and generated chart folders.
        if any(
            part.lower() in EXCLUDED_DIRECTORIES
            for part in path.parts
        ):
            continue

        if (
            path.suffix.lower() not in SCANNED_EXTENSIONS
            and not path.name.lower().startswith(".env")
        ):
            continue

        full_path = ROOT / path

        try:

            resolved_path = full_path.resolve()

            resolved_path.relative_to(ROOT)

            if not resolved_path.is_file():
                continue

            if resolved_path.stat().st_size > MAX_SOURCE_FILE_SIZE:
                continue

        except (OSError, ValueError):
            continue

        discovered_files.add(resolved_path)

    return sorted(
        discovered_files,
        key=lambda path: str(path).lower(),
    )


# ==================================================
# 8. CREDENTIAL EXPOSURE AUDIT
# ==================================================

def audit_credentials():

    source_files = discover_source_files()

    findings = []

    for path in source_files:

        try:

            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

        except OSError:
            continue

        relative_path = path.relative_to(ROOT).as_posix()

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):

            for category, pattern in SECRET_PATTERNS.items():

                if pattern.search(line):

                    # Never store or print the secret value.

                    findings.append({
                        "file": relative_path,
                        "line": line_number,
                        "category": category,
                    })

    return {
        "scanned_files": len(source_files),
        "findings": findings,
    }


# ==================================================
# 9. WINDOWS FILE PERMISSION AUDIT
# ==================================================

def audit_file_permissions():

    try:

        result = subprocess.run(
            [
                "icacls",
                str(DATASET),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )

        if result.returncode != 0:

            return {
                "status": "REVIEW_REQUIRED",
                "reason": (
                    "Windows ACL inspection unsuccessful."
                ),
            }

        acl_text = result.stdout

        broad_principals = re.compile(
            r"^\s*(?:Everyone|"
            r"BUILTIN\\Users|"
            r"Authenticated Users|"
            r"NT AUTHORITY\\Authenticated Users)"
            r"\s*:",
            re.IGNORECASE,
        )

        write_permissions = re.compile(
            r"\((?:F|M|W|GW|GA)\)",
            re.IGNORECASE,
        )

        broad_write_access = False

        for line in acl_text.splitlines():

            if broad_principals.search(line):

                if write_permissions.search(line):

                    broad_write_access = True
                    break

        if broad_write_access:

            return {
                "status": "REVIEW_REQUIRED",
                "reason": (
                    "Broad principal has potentially "
                    "significant write permissions."
                ),
            }

        return {
            "status": "NO_BROAD_WRITE_GRANT_DETECTED",
            "reason": (
                "Basic ACL screening did not detect "
                "broad write permissions."
            ),
        }

    except FileNotFoundError:

        return {
            "status": "REVIEW_REQUIRED",
            "reason": "icacls command unavailable.",
        }

    except subprocess.TimeoutExpired:

        return {
            "status": "REVIEW_REQUIRED",
            "reason": "Windows ACL inspection timed out.",
        }


# ==================================================
# 10. REPORT GENERATION
# ==================================================

def generate_report(
    metadata,
    data,
    credentials,
    permissions,
):

    missing_total = sum(
        data["missing_counts"].values()
    )

    secret_status = (
        "REVIEW_REQUIRED"
        if credentials["findings"]
        else "NO_MATCHES_DETECTED"
    )

    pii_status = (
        "REVIEW_REQUIRED"
        if data["email_matches"] or data["phone_matches"]
        else "NO_PATTERN_MATCHES_DETECTED"
    )

    lines = [

        "# W12D3 - Security Audit Report",
        "",
        "## 1. Audit Overview",
        "",
        f"- Dataset: `{metadata['filename']}`",
        f"- Dataset size: {metadata['size_mb']} MB",
        f"- Dataset size in bytes: {metadata['size_bytes']:,}",
        f"- Rows inspected: {data['total_rows']:,}",
        f"- Columns inspected: {len(data['columns'])}",
        "- Audit mode: Read-only",
        "- Customer values printed: No",
        "",
        "## 2. Potentially Sensitive Columns",
        "",
    ]

    for column in data["potential_pii_columns"]:

        lines.append(
            f"- `{column}` - Potential location information"
        )

    for column in data["missing_expected_pii_columns"]:

        lines.append(
            f"- `{column}` - Expected field not present"
        )

    lines.extend([

        "",
        "## 3. Privacy Pattern Detection",
        "",

        f"- Email pattern matches: {data['email_matches']}",
        f"- Phone pattern matches: {data['phone_matches']}",

        f"- Email match columns: {data['email_columns']}",
        f"- Phone match columns: {data['phone_columns']}",

        f"- Pattern audit status: {pii_status}",

        "- Matching values are intentionally excluded.",
        "- Pattern matches require manual verification.",
        "",
        "## 4. Data Integrity",
        "",

        f"- Total rows: {data['total_rows']:,}",
        f"- Exact duplicate rows: {data['duplicate_rows']:,}",
        f"- Total missing cells: {missing_total:,}",

        f"- Completely empty columns: {data['empty_columns']}",

        "- Duplicate detection uses SHA-256 row fingerprints.",
        "",
        "### Missing Values by Column",
        "",
        "| Column | Missing values |",
        "|---|---:|",
    ])

    for column, count in sorted(
        data["missing_counts"].items()
    ):

        lines.append(
            f"| {column} | {count:,} |"
        )

    lines.extend([

        "",
        "## 5. Credential Exposure Audit",
        "",

        f"- Source files scanned: {credentials['scanned_files']}",

        f"- Potential findings: {len(credentials['findings'])}",

        f"- Status: {secret_status}",

        "- Both tracked and non-ignored untracked source files are included.",
        "- Virtual environments, datasets and generated artifacts are excluded.",
        "- Secret values are never recorded.",
        "",
        "| File | Line | Finding type |",
        "|---|---:|---|",
    ])

    for finding in credentials["findings"]:

        lines.append(
            f"| `{finding['file']}` "
            f"| {finding['line']} "
            f"| {finding['category']} |"
        )

    lines.extend([

        "",
        "## 6. Windows File Permission Audit",
        "",

        f"- Status: {permissions['status']}",

        f"- Assessment: {permissions['reason']}",

        "- Scope: Dataset file ACL screening.",
        "- This is not a complete review of effective permissions.",
        "",
        "## 7. Security Recommendations",
        "",

        "1. Restrict access to potentially sensitive location information.",
        "2. Avoid exposing customer identifiers in logs and reports.",
        "3. Store API keys in environment variables or a secret manager.",
        "4. Never commit credentials to Git.",
        "5. Review Windows file and directory permissions.",
        "6. Validate incoming datasets before processing.",
        "7. Apply data minimisation and retention policies.",
        "8. Investigate phone and email pattern matches.",
        "9. Review credential scanner findings manually.",
        "10. Introduce automated security checks into CI/CD.",
        "",
        "## 8. Audit Limitations",
        "",

        "- Pattern matching may produce false positives and false negatives.",
        "- No pattern match does not prove that a dataset contains no PII.",
        "- Credential scanning covers configured source extensions only.",
        "- Credential scanning is not a replacement for a dedicated secret scanner.",
        "- ACL screening checks selected broad principals and permissions only.",
        "- SHA-256 fingerprints provide highly reliable duplicate detection, "
        "but are not a mathematical proof of row equality.",
        "- This audit does not establish legal or regulatory compliance.",
        "",
        "## 9. Conclusion",
        "",

        "The automated security audit completed its configured checks. "
        "Potential findings require human verification. "
        "A clean automated scan should not be interpreted as proof "
        "that the platform is completely secure.",
        "",
    ])

    REPORT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ==================================================
# 11. MAIN EXECUTION
# ==================================================

def main():

    print("=" * 55)
    print("W12D3 SECURITY AUDIT")
    print("=" * 55)

    # Dataset metadata

    metadata = audit_file_metadata()

    print("\n[1/5] Dataset metadata checked.")

    # Privacy and integrity

    data = audit_dataset()

    print("[2/5] Privacy and integrity checks completed.")

    # Credentials

    credentials = audit_credentials()

    print("[3/5] Source-code credential scan completed.")

    # Permissions

    permissions = audit_file_permissions()

    print("[4/5] Windows file permission screening completed.")

    # Report

    generate_report(
        metadata,
        data,
        credentials,
        permissions,
    )

    print("[5/5] Security report generated.")

    # Final summary

    print("\n" + "=" * 55)
    print("SECURITY AUDIT SUMMARY")
    print("=" * 55)

    print("Dataset size:", metadata["size_mb"], "MB")

    print("Rows inspected:", data["total_rows"])

    print("Columns inspected:", len(data["columns"]))

    print("Potentially sensitive columns:",
          len(data["potential_pii_columns"]))

    print("Email matches:", data["email_matches"])

    print("Email match columns:", data["email_columns"])

    print("Phone matches:", data["phone_matches"])

    print("Phone match columns:", data["phone_columns"])

    print("Duplicate rows:", data["duplicate_rows"])

    print("Missing cells:",
          sum(data["missing_counts"].values()))

    print("Source files scanned:",
          credentials["scanned_files"])

    print("Potential credential findings:",
          len(credentials["findings"]))

    print("Permission status:", permissions["status"])

    print("\nReport generated:")
    print(REPORT.relative_to(ROOT))

    print("\nSecurity audit completed successfully.")


if __name__ == "__main__":

    main()
