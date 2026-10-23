"""
Week 5 Day 1: PandasAI Analysis
Loads sales data, runs 10 natural-language queries,
compares AI answers with manual Pandas results, and logs errors.
"""

import json
import os
import logging
from pathlib import Path

import pandas as pd

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR.parent / "sales_data.csv"
RESULTS_PATH = SCRIPT_DIR / "query_results.json"
COMPARISON_PATH = SCRIPT_DIR / "pandas_comparison.md"
ERRORS_PATH = SCRIPT_DIR / "errors.log"

# Error logging
logging.basicConfig(
    filename=str(ERRORS_PATH),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Ten natural-language questions
QUESTIONS = [
    "What is the total sales?",
    "What is the average sales?",
    "Which order has the highest sales?",
    "Which order has the lowest sales?",
    "What are total sales by region?",
    "What are total sales by category?",
    "What is the total quantity sold?",
    "Which customer has the highest sales?",
    "Rank the regions from highest to lowest total sales.",
    "How many orders are in the dataset?",
]


def calculate_manual_results(df):
    """Calculate answers using regular Pandas."""
    results = {
        "total_sales": float(df["sales"].sum()),
        "average_sales": float(df["sales"].mean()),
        "highest_sales": float(df["sales"].max()),
        "lowest_sales": float(df["sales"].min()),
        "sales_by_region": {
            str(key): float(value)
            for key, value in (
                df.groupby("region")["sales"].sum().sort_values(ascending=False)
            ).items()
        },
        "sales_by_category": {
            str(key): float(value)
            for key, value in (
                df.groupby("category")["sales"].sum().sort_values(ascending=False)
            ).items()
        },
        "total_quantity": int(df["quantity"].sum()),
        "top_customer": str(
            df.groupby("customer")["sales"].sum().idxmax()
        ),
        "regions_ranked": [
            {"region": str(region), "sales": float(sales)}
            for region, sales in (
                df.groupby("region")["sales"].sum()
                .sort_values(ascending=False)
                .items()
            )
        ],
        "order_count": int(df["order_id"].nunique()),
    }
    return results


def main():
    # Load dataset
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = {
        "order_id", "customer", "region",
        "category", "sales", "quantity"
    }
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    print(f"Loaded dataset: {DATA_PATH.name}")
    print(f"Rows: {len(df)}, columns: {len(df.columns)}")

    # Manual Pandas analysis
    manual_results = calculate_manual_results(df)

    # Three comparisons between manual Pandas and PandasAI
    comparison_questions = {
        QUESTIONS[0]: manual_results["total_sales"],
        QUESTIONS[1]: manual_results["average_sales"],
        QUESTIONS[4]: manual_results["sales_by_region"],
    }

    results = {
        "dataset": DATA_PATH.name,
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "manual_pandas_results": manual_results,
        "pandasai_results": [],
    }

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print(
            "\nGROQ_API_KEY is not configured. "
            "Manual Pandas results will be saved; AI queries are skipped."
    
        results["ai_status"] = "skipped_no_api_key"
    else:
        try:
            import pandasai as pai
            from pandasai_litellm.litellm import LiteLLM

            llm = LiteLLM(
                model="groq/openai/gpt-oss-120b",
                api_key=api_key,
            )

            pai.config.set({
                "llm": llm,
                "save_logs": True,
                "verbose": False,
            })

            ai_df = pai.read_csv(str(DATA_PATH))
            successful_queries = 0

            for question in QUESTIONS:
                print(f"\nQuery: {question}")

                try:
                    answer = ai_df.chat(question)
                    answer_text = str(answer)

                    results["pandasai_results"].append({
                        "question": question,
                        "status": "success",
                        "answer": answer_text,
                    })

                    successful_queries += 1
                    print(f"Answer: {answer_text}")

                except Exception as exc:
                    logging.exception(
                        "PandasAI query failed: %s", question
                    )

                    results["pandasai_results"].append({
                        "question": question,
                        "status": "error",
                        "error": str(exc),
                    })

                    print(f"Query failed: {exc}")

            results["ai_status"] = "completed"
            results["successful_queries"] = successful_queries
            results["total_queries"] = len(QUESTIONS)

        except Exception as exc:
            logging.exception("PandasAI setup failed")
            results["ai_status"] = "setup_error"
            results["setup_error"] = str(exc)
            print(f"\nPandasAI setup failed: {exc}")

    # Save JSON results
    RESULTS_PATH.write_text(
        json.dumps(results, indent=2, default=str),
        encoding="utf-8",
    )

    # Save comparison report
    report_lines = [
        "# PandasAI vs Manual Pandas Comparison",
        "",
        f"- Dataset: `{DATA_PATH.name}`",
        f"- Rows: {len(df)}",
        "- Comparison questions: 3",
        "",
        "## Results",
        "",
        "| Question | Manual Pandas result | PandasAI result | Status |",
        "|---|---|---|---|",
    ]

    ai_lookup = {
        item["question"]: item
        for item in results["pandasai_results"]
    }

    for question, manual_answer in comparison_questions.items():
        ai_result = ai_lookup.get(question)

        if ai_result and ai_result["status"] == "success":
            ai_answer = ai_result["answer"].replace("|", "\\|")
            status = "AI answer received"
        elif ai_result and ai_result["status"] == "error":
            ai_answer = ai_result["error"].replace("|", "\\|")
            status = "AI query failed"
        else:
            ai_answer = "Not run"
            status = "Skipped"

        manual_text = json.dumps(manual_answer, default=str)
        report_lines.append(
            f"| {question} | `{manual_text}` | "
            f"{ai_answer} | {status} |"
        )

    report_lines.extend([
        "",
        "## AI Query Summary",
        "",
        f"- AI status: `{results.get('ai_status', 'unknown')}`",
        f"- Successful queries: "
        f"{results.get('successful_queries', 0)}",
        f"- Total questions: {len(QUESTIONS)}",
        "",
        "## Error Handling",
        "",
        "Individual query errors are recorded in `errors.log`.",
        "AI results are saved in `query_results.json`.",
    ])

    COMPARISON_PATH.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print(f"\nSaved results: {RESULTS_PATH}")
    print(f"Saved comparison: {COMPARISON_PATH}")

    if ERRORS_PATH.exists():
        print(f"Check errors if needed: {ERRORS_PATH}")
    else:
        print("No errors were logged.")


if __name__ == "__main__":
    main()