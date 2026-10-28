

import logging
import os
import re
from pathlib import Path

import pandas as pd
from pandasai import Agent
from pandasai_litellm.litellm import LiteLLM

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "python-pandas" / "amazon_india_sales_sample.csv"
OUT = ROOT / "reports" / "w7d1"
OUT.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=OUT / "pandasai_errors.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Load and clean the Indian e-commerce sample.
df = pd.read_csv(DATA)

df = df[
    (df["currency"] == "INR")
    & (df["Status"] != "Cancelled")
    & df["Amount"].notna()
].copy()

df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
df = df.dropna(subset=["Amount", "Qty"])

if df.empty:
    raise ValueError("No usable INR records remain after cleaning.")

# Configure the language model.
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is not set in this PowerShell session."
    )

llm = LiteLLM(
    model="groq/openai/gpt-oss-120b",
    api_key=api_key,
)

agent = Agent(df, config={"llm": llm, "verbose": False})

questions = [
    ("total_sales", "What is the total Amount?"),
    ("total_quantity", "What is the total Qty?"),
    ("order_count", "How many unique Order ID values are there?"),
    ("average_sales", "What is the average Amount per row?"),
    ("sales_by_state", "What is the total Amount for each ship-state?"),
    ("sales_by_category", "What is the total Amount for each Category?"),
    ("top_category", "Which Category has the highest total Amount?"),
    ("top_order", "Which Order ID has the highest Amount?"),
    ("top_state", "Which ship-state has the highest total Amount?"),
    ("kurta_sales", "What is the total Amount for Category kurta?"),
]

# Independent Pandas reference calculations.
manual = {
    "total_sales": df["Amount"].sum(),
    "total_quantity": df["Qty"].sum(),
    "order_count": df["Order ID"].nunique(),
}

# Load existing results so successful queries are not repeated.
results_path = OUT / "query_results.csv"

if results_path.exists():
    existing_df = pd.read_csv(results_path).fillna("")
    query_rows = existing_df.to_dict("records")

    results = {
        row["query_id"]: (
            row["result"] if row["status"] == "success" else None
        )
        for row in query_rows
    }
else:
    query_rows = []
    results = {}

row_by_id = {
    row["query_id"]: i for i, row in enumerate(query_rows)
}

# Skip successful queries and retry only failed or missing queries.
for query_id, question in questions:
    if results.get(query_id) is not None:
        print(f"[SKIP] {query_id}: already successful")
        continue

    try:
        answer = agent.chat(question)
        answer_text = str(answer)
        results[query_id] = answer_text

        new_row = {
            "query_id": query_id,
            "question": question,
            "result": answer_text,
            "status": "success",
        }
        print(f"[OK] {query_id}: {answer_text}")

    except Exception as exc:
        results[query_id] = None

        new_row = {
            "query_id": query_id,
            "question": question,
            "result": "",
            "status": "failed",
        }

        logging.exception("Query %s failed: %s", query_id, question)
        print(f"[FAILED] {query_id}: {type(exc).__name__}: {exc}")

    # Update existing rows instead of creating duplicates.
    if query_id in row_by_id:
        query_rows[row_by_id[query_id]] = new_row
    else:
        row_by_id[query_id] = len(query_rows)
        query_rows.append(new_row)

# Save all results, including previous successes.
pd.DataFrame(query_rows).to_csv(results_path, index=False)

# Compare numeric answers against independent Pandas calculations.
comparison_rows = []

for query_id, expected in manual.items():
    actual = results.get(query_id)

    numbers = re.findall(
        r"-?\d+(?:,\d{3})*(?:\.\d+)?",
        actual or "",
    )

    numeric_match = False

    if numbers:
        try:
            numeric_match = any(
                abs(
                    float(number.replace(",", "")) - float(expected)
                ) < 0.01
                for number in numbers
            )
        except ValueError:
            pass

    comparison_rows.append({
        "query_id": query_id,
        "manual_pandas_result": expected,
        "pandasai_result": actual or "",
        "numeric_match": numeric_match,
        "status": "success" if actual is not None else "failed",
    })

pd.DataFrame(comparison_rows).to_csv(
    OUT / "manual_comparison.csv",
    index=False,
)

print("\nManual Pandas reference results:")
for key, value in manual.items():
    print(f"{key}: {value}")

print("\nFinal query status:")
print(
    pd.DataFrame(query_rows)["status"]
    .value_counts()
    .to_string()
)

print(f"\nResults saved to: {OUT}")
print("Check manual_comparison.csv for numeric validation.")
print("Check pandasai_errors.log if any query failed.")
