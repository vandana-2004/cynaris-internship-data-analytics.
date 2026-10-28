import logging
import os
import re
from pathlib import Path

import pandas as pd
from pandasai import Agent
from pandasai_litellm.litellm import LiteLLM

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "python-pandas" / "sales_data.csv"
OUT = ROOT / "reports" / "w7d1"
OUT.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=OUT / "pandasai_errors.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)

df = pd.read_csv(DATA)

llm = LiteLLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.environ["GROQ_API_KEY"],
)
agent = Agent(df, config={"llm": llm, "verbose": False})

questions = [
    ("total_sales", "What is the total sales?"),
    ("total_quantity", "What is the total quantity sold?"),
    ("order_count", "How many orders are in the dataset?"),
    ("average_sales", "What is the average sales per order?"),
    ("sales_by_region", "What is the total sales for each region?"),
    ("sales_by_category", "What is the total sales for each category?"),
    ("top_category", "Which category has the highest total sales?"),
    ("top_order", "What is the order ID with the highest sales?"),
    ("top_region", "Which region has the highest total sales?"),
    ("electronics_sales", "What is the total sales for Electronics?"),
]

manual = {
    "total_sales": df["sales"].sum(),
    "total_quantity": df["quantity"].sum(),
    "order_count": len(df),
}

results = {}
query_rows = []

for query_id, question in questions:
    try:
        answer = agent.chat(question)
        results[query_id] = str(answer)
        query_rows.append({
            "query_id": query_id,
            "question": question,
            "result": str(answer),
            "status": "success",
        })
        print(f"[OK] {query_id}: {answer}")
    except Exception as exc:
        results[query_id] = None
        query_rows.append({
            "query_id": query_id,
            "question": question,
            "result": "",
            "status": "failed",
        })
        logging.exception("Query %s failed: %s", query_id, question)
        print(f"[FAILED] {query_id}: {type(exc).__name__}: {exc}")

pd.DataFrame(query_rows).to_csv(OUT / "query_results.csv", index=False)

comparison_rows = []
for query_id, expected in manual.items():
    actual = results.get(query_id)
    numbers = re.findall(r"-?\d+(?:,\d{3})*(?:\.\d+)?", actual or "")
    numeric_match = False
    if numbers:
        try:
            numeric_match = any(
                abs(float(n.replace(",", "")) - float(expected)) < 0.01
                for n in numbers
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
    OUT / "manual_comparison.csv", index=False
)

print("\nManual Pandas reference results:")
for key, value in manual.items():
    print(f"{key}: {value}")

print(f"\nResults saved to: {OUT}")
print("Review query_results.csv and manual_comparison.csv.")
print("See pandasai_errors.log if any query failed.")
