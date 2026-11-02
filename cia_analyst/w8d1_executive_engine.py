
import html
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd
from litellm import completion

MODEL = "groq/openai/gpt-oss-120b"


def generate_insights(df):
    insights = []

    rows, columns = df.shape

    # 1. Dataset overview
    insights.append(
        f"Dataset Overview: The dataset contains {rows} rows and {columns} columns."
    )

    # 2. Data completeness
    missing = df.isna().sum()
    total_missing = int(missing.sum())

    if total_missing == 0:
        insights.append("Data Completeness: No missing values were found.")
    else:
        column = missing.idxmax()
        insights.append(
            f"Data Completeness: {total_missing} missing values were found. "
            f"The column with the most missing values is '{column}' "
            f"({int(missing[column])})."
        )

    # 3. Duplicate records
    duplicates = int(df.duplicated().sum())

    insights.append(
        f"Duplicate Records: {duplicates} duplicate rows were found."
    )

    # 4. Numeric analysis - exclude identifier columns
    numeric = df.select_dtypes(include="number")

    numeric = numeric[
        [
            col for col in numeric.columns
            if "id" not in col.lower()
        ]
    ]

    if not numeric.empty:
        preferred = [
            col for col in numeric.columns
            if any(
                term in col.lower()
                for term in ["sales", "revenue", "amount", "profit"]
            )
        ]

        column = preferred[0] if preferred else numeric.columns[0]
        series = numeric[column].dropna()

        if not series.empty:
            insights.append(
                f"Numeric Analysis: '{column}' has a minimum of "
                f"{series.min():.2f}, a mean of {series.mean():.2f}, "
                f"and a maximum of {series.max():.2f}."
            )
        else:
            insights.append(
                "Numeric Analysis: Numeric columns contain no usable values."
            )
    else:
        insights.append(
            "Numeric Analysis: No meaningful numeric columns were found."
        )

    # 5. Category distribution
    categorical = df.select_dtypes(
        include=["object", "category", "bool"]
    )

    if not categorical.empty:
        column = categorical.columns[0]
        counts = df[column].value_counts(dropna=False)

        if not counts.empty:
            top_value = str(counts.index[0])
            percentage = counts.iloc[0] / len(df) * 100

            insights.append(
                f"Category Distribution: The most common value in '{column}' "
                f"is '{top_value}' ({int(counts.iloc[0])} rows, "
                f"{percentage:.1f}%)."
            )
        else:
            insights.append(
                "Category Distribution: No category values were found."
            )
    else:
        insights.append(
            "Category Distribution: No categorical columns were found."
        )

    return insights


def generate_summary(insights):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    response = completion(
        model=MODEL,
        api_key=api_key,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful senior business data analyst. "
                    "Write clear, accurate, evidence-based executive summaries. "
                    "Use only facts explicitly supported by the supplied insights. "
                    "Never invent trends, causes, business performance, "
                    "customer behaviour, profitability, market share, bias, "
                    "or under-representation. "
                    "A category's percentage of rows is not its percentage "
                    "of sales or revenue. "
                    "A minimum, mean, and maximum do not establish customer "
                    "segments or spending behaviour. "
                    "Do not describe data as reliable merely because missing "
                    "values and duplicates are absent. "
                    "Make recommendations as suggested follow-up analyses "
                    "or validation steps, not as proven business conclusions."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Write an approximately 200-word executive summary "
                    "using only the verified dataset insights below.\n\n"
                    "Use these three sections:\n"
                    "Observations\n"
                    "Business Implications\n"
                    "Recommendations\n\n"
                    "Clearly separate measured facts from possible follow-up "
                    "actions. If the insights do not support a business "
                    "implication, explain that further analysis is needed. "
                    "Do not make unsupported claims.\n\n"
                    "Use plain text only. Do not use Markdown bold, italics, "
                    "escaped numbered lists, or HTML entities. "
                    "Use ordinary hyphen bullets if needed.\n\n"
                    "Verified dataset insights:\n"
                    + "\n".join(insights)
                ),
            },
        ],
        temperature=0.2,
        max_tokens=900,
    )

    summary = response.choices[0].message.content

    if not summary:
        raise RuntimeError("Groq returned an empty executive summary.")

    summary = str(summary)

    # Decode HTML entities, including repeatedly encoded entities.
    for _ in range(3):
        decoded = html.unescape(summary)
        if decoded == summary:
            break
        summary = decoded

    # Remove escaped Markdown punctuation.
    summary = re.sub(
        r"\\+([`*_{}\[\]()#+.!|>~-])",
        r"\1",
        summary,
    )

    # Remove Markdown bold and italic markers.
    summary = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        summary,
        flags=re.DOTALL,
    )

    summary = re.sub(
        r"__(.*?)__",
        r"\1",
        summary,
        flags=re.DOTALL,
    )

    summary = re.sub(
        r"(?<!\*)\*([^*\n]+)\*(?!\*)",
        r"\1",
        summary,
    )

    # Normalize special spaces and line breaks.
    summary = re.sub(r"[\u00a0\u202f]", " ", summary)
    summary = re.sub(r"[ \t]+", " ", summary)
    summary = re.sub(r"\n{3,}", "\n\n", summary)

    return summary.strip()


def analyze(csv_path):
    path = Path(csv_path).resolve()

    if not path.is_file() or path.suffix.lower() != ".csv":
        raise ValueError("A valid CSV file path is required.")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The uploaded CSV file contains no rows.")

    insights = generate_insights(df)
    summary = generate_summary(insights)

    return {
        "status": "success",
        "filename": path.name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "insights": insights,
        "summary": summary,
    }


if __name__ == "__main__":
    try:
        payload = json.load(sys.stdin)
        result = analyze(payload["csv_path"])
        print(json.dumps(result))

    except Exception as exc:
        print(
            json.dumps({
                "status": "error",
                "message": str(exc),
            })
        )
        sys.exit(1)
