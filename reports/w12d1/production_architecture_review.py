from pathlib import Path
import json
import time
import platform
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# W12D1: Production Architecture Review
# Project: Indian Business Sales EDA
# ============================================================

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "w8d3" / "indian_business_sales.csv"
OUT = ROOT / "reports" / "w12d1" / "outputs"

OUT.mkdir(parents=True, exist_ok=True)

REQUIRED_COLUMNS = [
    "Date", "Status", "Fulfilment", "Category",
    "Amount", "ship-state", "B2B"
]

print("=" * 65)
print("W12D1 PRODUCTION ARCHITECTURE REVIEW")
print("=" * 65)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

# 1. Ingestion and performance measurement
start = time.perf_counter()
df = pd.read_csv(DATA_FILE, low_memory=False)
load_seconds = time.perf_counter() - start

df.columns = df.columns.str.strip()

missing_columns = [
    col for col in REQUIRED_COLUMNS if col not in df.columns
]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# 2. Data quality assessment
quality_rows = []

for col in df.columns:
    missing = int(df[col].isna().sum())
    quality_rows.append({
        "column": col,
        "data_type": str(df[col].dtype),
        "missing_count": missing,
        "missing_percentage": round(
            missing / len(df) * 100, 2
        ),
        "unique_values": int(df[col].nunique(dropna=True))
    })

quality = pd.DataFrame(quality_rows)
quality.to_csv(OUT / "data_quality_report.csv", index=False)

duplicate_rows = int(df.duplicated().sum())

# 3. Type validation
amount = pd.to_numeric(df["Amount"], errors="coerce")
dates = pd.to_datetime(
    df["Date"], format="%m-%d-%y", errors="coerce"
)

invalid_amount = int(
    (df["Amount"].notna() & amount.isna()).sum()
)
invalid_dates = int(
    (df["Date"].notna() & dates.isna()).sum()
)

# 4. Resource and processing metrics
memory_mb = round(
    df.memory_usage(deep=True).sum() / (1024 ** 2), 2
)

metrics = {
    "project": "W12D1 Production Architecture Review",
    "dataset": str(DATA_FILE.relative_to(ROOT)),
    "rows": int(len(df)),
    "columns": int(len(df.columns)),
    "file_size_bytes": int(DATA_FILE.stat().st_size),
    "memory_usage_mb": memory_mb,
    "load_time_seconds": round(load_seconds, 3),
    "duplicate_rows": duplicate_rows,
    "invalid_amount_values": invalid_amount,
    "invalid_date_values": invalid_dates,
    "amount_missing_values": int(amount.isna().sum()),
    "amount_missing_percentage": round(amount.isna().mean() * 100, 2),
    "date_missing_values": int(dates.isna().sum()),
    "date_min": (
        str(dates.min().date()) if dates.notna().any() else None
    ),
    "date_max": (
        str(dates.max().date()) if dates.notna().any() else None
    ),
    "python_version": platform.python_version(),
    "pandas_version": pd.__version__
}

with open(OUT / "architecture_metrics.json", "w",
          encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

# 5. Architecture review documentation
review = """# W12D1 Production Architecture Review

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
"""

(OUT.parent / "architecture_review.md").write_text(
    review, encoding="utf-8"
)

# 6. Architecture diagram
fig, ax = plt.subplots(figsize=(11, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

layers = [
    ("Source Data", "Indian Business Sales CSV"),
    ("Ingestion", "Pandas CSV loading"),
    ("Validation", "Schema and quality checks"),
    ("Processing", "Cleaning and transformation"),
    ("Storage", "Curated analytical data"),
    ("Consumption", "EDA and BI reporting"),
    ("Governance", "Monitoring and access controls")
]

positions = [9, 7.8, 6.6, 5.4, 4.2, 3.0, 1.8]

for (heading, detail), y in zip(layers, positions):
    ax.text(
        5, y, f"{heading}\n{detail}",
        ha="center", va="center", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.6", alpha=0.15)
    )

for y in positions[:-1]:
    ax.annotate(
        "", xy=(5, y - 0.55), xytext=(5, y - 0.15),
        arrowprops=dict(arrowstyle="->", lw=1.3)
    )

ax.set_title(
    "W12D1 - Production Data Architecture",
    fontsize=15, pad=15
)
fig.tight_layout()
fig.savefig(
    OUT / "architecture_diagram.png",
    dpi=160, bbox_inches="tight"
)
plt.close(fig)

# 7. Console summary
print("\nARCHITECTURE METRICS")
for key, value in metrics.items():
    print(f"{key}: {value}")

print("\nOUTPUT FILES")
for path in sorted(OUT.iterdir()):
    print(f"{path.name}: {path.stat().st_size:,} bytes")

print("\nVALIDATION: PASS")

