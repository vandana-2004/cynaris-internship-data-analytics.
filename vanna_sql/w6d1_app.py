
import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import RequestContext, User, UserResolver
from vanna.tools import RunSqlTool
from vanna.integrations.openai import OpenAILlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sales.db"

TRAINING_EXAMPLES = [
    {
        "question": "How many orders are there?",
        "sql": "SELECT COUNT(*) AS total_orders FROM orders",
    },
    {
        "question": "What are total sales by region?",
        "sql": "SELECT region, SUM(quantity * unit_price * (1 - COALESCE(discount, 0) / 100.0)) AS total_sales FROM orders GROUP BY region",
    },
    {
        "question": "Which products have the highest quantity sold?",
        "sql": "SELECT product, SUM(quantity) AS total_quantity FROM orders GROUP BY product ORDER BY total_quantity DESC",
    },
    {
        "question": "What is the average order quantity?",
        "sql": "SELECT AVG(quantity) AS average_quantity FROM orders",
    },
    {
        "question": "How many orders are in each category?",
        "sql": "SELECT category, COUNT(*) AS order_count FROM orders GROUP BY category",
    },
]


class QueryRequest(BaseModel):
    question: str


class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="local-analyst",
            username="local-analyst",
            group_memberships=["user"],
        )


def build_agent() -> Agent:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    llm = OpenAILlmService(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    tools = ToolRegistry()
    tools.register_local_tool(
        RunSqlTool(
            sql_runner=SqliteRunner(database_path=str(DB_PATH)),
            custom_tool_name="run_sales_sql",
            custom_tool_description=(
                "Query the sales orders database. Use SELECT statements only."
            ),
        ),
        access_groups=["user"],
    )

    return Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=SimpleUserResolver(),
        agent_memory=DemoAgentMemory(max_items=100),
    )


app = FastAPI(title="W6D1 Vanna SQL Analyst")
agent = build_agent()


@app.get("/health")
def health():
    return {"status": "ok", "database": DB_PATH.name}


@app.post("/cia/sql-analyst")
async def sql_analyst(request: QueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    examples = "\n".join(
        f"Question: {item['question']}\nSQL: {item['sql']}"
        for item in TRAINING_EXAMPLES
    )

    prompt = (
        "You are a careful SQLite sales analyst. "
        "Use the orders table and its columns: order_id, customer_name, "
        "product, category, quantity, unit_price, order_date, region, "
        "sales_rep, discount. Use SELECT queries only; never modify data. "
        "Treat discount as a fraction when calculating discounted sales. "
        "Here are examples of question-to-SQL patterns:\n"
        f"{examples}\n\n"
        f"Answer this question and use the SQL tool when needed: {question}"
    )

    try:
        context = RequestContext(cookies={}, headers={})
        components = []

        async for component in agent.send_message(context, prompt):
            if hasattr(component, "model_dump"):
                components.append(component.model_dump(mode="json"))
            else:
                components.append(str(component))

        return {"question": question, "response": components}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"SQL analyst request failed: {type(exc).__name__}",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
