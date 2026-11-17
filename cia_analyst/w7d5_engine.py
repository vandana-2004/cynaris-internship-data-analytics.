
import json
import os
import sys
from pathlib import Path

import pandas as pd
from pandasai import Agent
from pandasai_litellm.litellm import LiteLLM


def analyze_csv(csv_path: str, question: str) -> dict:
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not configured.")

    path = Path(csv_path).resolve()

    if not path.is_file() or path.suffix.lower() != ".csv":
        raise ValueError("A valid CSV file is required.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The uploaded CSV contains no data.")

    llm = LiteLLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        api_base="https://api.groq.com/openai/v1",
    )

    agent = Agent(
        df,
        config={
            "llm": llm,
            "verbose": False,
        },
    )

    result = agent.chat(question, output_type="dataframe")

    # Extract the DataFrame from PandasAI's response wrapper.
    if not isinstance(result, (pd.DataFrame, pd.Series)):
        for attribute in ("value", "dataframe", "df", "data"):
            candidate = getattr(result, attribute, None)

            if isinstance(candidate, (pd.DataFrame, pd.Series)):
                result = candidate
                break

    # Handle a DataFrame result.
    if isinstance(result, pd.DataFrame):
        return {
            "answer": f"Query returned {len(result)} rows.",
            "columns": result.columns.tolist(),
            "data": result.to_dict(orient="records"),
        }

    # Handle a Series result.
    if isinstance(result, pd.Series):
        return {
            "answer": str(result.to_dict()),
            "columns": result.index.tolist(),
            "data": [result.to_dict()],
        }

    # Handle scalar or text results.
    return {
        "answer": str(result),
        "columns": [],
        "data": [],
    }


if __name__ == "__main__":
    try:
        payload = json.load(sys.stdin)

        output = analyze_csv(
            payload["csv_path"],
            payload["question"],
        )

        print(json.dumps(output, default=str))

    except Exception as exc:
        print(json.dumps({
            "error": type(exc).__name__,
            "detail": str(exc),
        }))
        sys.exit(1)
