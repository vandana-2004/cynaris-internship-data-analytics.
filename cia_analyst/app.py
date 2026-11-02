
import json
import os
import secrets
import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from cia_analyst.w8d1_ppt_export import create_presentation


BASE_DIR = Path(__file__).resolve().parent
ENGINE_PATH = BASE_DIR / "w7d5_engine.py"
W8D1_ENGINE_PATH = BASE_DIR / "w8d1_executive_engine.py"
STATIC_DIR = BASE_DIR / "static"

PANDASAI_PYTHON = (
    BASE_DIR.parent / ".venv-pandasai" / "Scripts" / "python.exe"
)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
sessions = {}

app = FastAPI(title="W8D1 CIA Executive Data Analyst")

STATIC_DIR.mkdir(exist_ok=True)


class QueryRequest(BaseModel):
    session_id: str
    question: str = Field(min_length=1, max_length=1000)


class ExecutiveSummaryRequest(BaseModel):
    session_id: str


def create_chart(result: dict) -> dict | None:
    columns = result.get("columns", [])
    data = result.get("data", [])

    if not data or len(columns) < 2:
        return None

    df = pd.DataFrame(data)

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if not numeric_columns:
        return None

    label_columns = [
        column for column in df.columns
        if column not in numeric_columns
    ]

    if label_columns:
        fig = px.bar(
            df,
            x=label_columns[0],
            y=numeric_columns[0],
            title="CIA Data Analysis",
        )
    else:
        fig = px.bar(
            df,
            y=numeric_columns[0],
            title="CIA Data Analysis",
        )

    return json.loads(fig.to_json())


def create_chartjs(result: dict) -> dict | None:
    columns = result.get("columns", [])
    data = result.get("data", [])

    if not data or len(columns) < 2:
        return None

    df = pd.DataFrame(data)

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if not numeric_columns:
        return None

    label_columns = [
        column for column in df.columns
        if column not in numeric_columns
    ]

    labels = (
        df[label_columns[0]].astype(str).tolist()
        if label_columns
        else list(range(len(df)))
    )

    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": numeric_columns[0],
                "data": df[numeric_columns[0]].tolist(),
            }],
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
        },
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine_available": ENGINE_PATH.exists(),
        "w8d1_engine_available": W8D1_ENGINE_PATH.exists(),
        "pandasai_python_available": PANDASAI_PYTHON.exists(),
    }


@app.get("/")
def home():
    index_file = STATIC_DIR / "index.html"

    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Frontend not created yet.",
        )

    return FileResponse(index_file)


@app.post("/cia/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Upload a CSV file.",
        )

    if not ENGINE_PATH.exists() or not PANDASAI_PYTHON.exists():
        raise HTTPException(
            status_code=500,
            detail="AI engine is unavailable.",
        )

    session_id = secrets.token_urlsafe(24)
    session_dir = Path(tempfile.mkdtemp(prefix="cia_w8d1_"))
    csv_path = session_dir / "uploaded.csv"

    try:
        size = 0

        with csv_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)

                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(
                        status_code=413,
                        detail="CSV must be 10 MB or smaller.",
                    )

                destination.write(chunk)

        df = pd.read_csv(csv_path, nrows=5)

        if df.empty or len(df.columns) == 0:
            raise ValueError("CSV has no usable data.")

        sessions[session_id] = {
            "directory": session_dir,
            "csv_path": csv_path,
            "filename": Path(file.filename).name,
            "executive_result": None,
        }

        return {
            "session_id": session_id,
            "filename": Path(file.filename).name,
            "columns": df.columns.tolist(),
            "preview": df.fillna("").to_dict(orient="records"),
        }

    except HTTPException:
        shutil.rmtree(session_dir, ignore_errors=True)
        raise

    except Exception as exc:
        shutil.rmtree(session_dir, ignore_errors=True)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid CSV: {type(exc).__name__}",
        ) from exc

    finally:
        await file.close()


@app.post("/cia/query")
def query_csv(request: QueryRequest):
    session = sessions.get(request.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    environment = os.environ.copy()

    if not environment.get("GROQ_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Groq API key unavailable.",
        )

    payload = json.dumps({
        "csv_path": str(session["csv_path"]),
        "question": question,
    })

    try:
        process = subprocess.run(
            [str(PANDASAI_PYTHON), str(ENGINE_PATH)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=90,
            env=environment,
            cwd=str(BASE_DIR.parent),
            check=False,
        )

        if process.returncode != 0 or not process.stdout.strip():
            raise RuntimeError("PandasAI engine request failed.")

        result = json.loads(process.stdout.strip().splitlines()[-1])

        if "error" in result:
            raise RuntimeError(
                result.get("message", result.get("detail", "AI query failed."))
            )

        return {
            "question": question,
            "answer": result.get("answer"),
            "chart": create_chart(result),
            "chartjs": create_chartjs(result),
        }

    except subprocess.TimeoutExpired as exc:
        raise HTTPException(
            status_code=504,
            detail="AI query timed out.",
        ) from exc

    except (RuntimeError, ValueError, json.JSONDecodeError, IndexError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI analysis failed: {type(exc).__name__}",
        ) from exc


@app.post("/cia/executive-summary")
def executive_summary(request: ExecutiveSummaryRequest):
    session = sessions.get(request.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    if session.get("executive_result"):
        return session["executive_result"]

    if not W8D1_ENGINE_PATH.exists() or not PANDASAI_PYTHON.exists():
        raise HTTPException(
            status_code=500,
            detail="Executive engine is unavailable.",
        )

    environment = os.environ.copy()

    if not environment.get("GROQ_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Groq API key unavailable.",
        )

    payload = json.dumps({
        "csv_path": str(session["csv_path"]),
    })

    try:
        process = subprocess.run(
            [str(PANDASAI_PYTHON), str(W8D1_ENGINE_PATH)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=120,
            env=environment,
            cwd=str(BASE_DIR.parent),
            check=False,
        )

        if process.returncode != 0 or not process.stdout.strip():
            raise RuntimeError("Executive analysis failed.")

        result = json.loads(process.stdout.strip().splitlines()[-1])

        if result.get("status") != "success":
            raise RuntimeError(
                result.get("message", "Executive analysis failed.")
            )

        session["executive_result"] = result

        return result

    except subprocess.TimeoutExpired as exc:
        raise HTTPException(
            status_code=504,
            detail="Executive summary generation timed out.",
        ) from exc

    except (RuntimeError, ValueError, json.JSONDecodeError, IndexError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Executive analysis failed: {type(exc).__name__}",
        ) from exc


@app.get("/cia/executive-summary/ppt/{session_id}")
def download_executive_presentation(session_id: str):
    session = sessions.get(session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    result = session.get("executive_result")

    if not result:
        raise HTTPException(
            status_code=409,
            detail="Generate the executive summary before downloading the presentation.",
        )

    output_path = session["directory"] / "executive_summary.pptx"

    try:
        create_presentation(
            output_path=output_path,
            filename=result["filename"],
            summary=result["summary"],
            insights=result["insights"],
        )

        return FileResponse(
            path=output_path,
            filename="CIA_Executive_Summary.pptx",
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
            ),
        )

    except (KeyError, ValueError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not generate the PowerPoint presentation.",
        ) from exc


@app.delete("/cia/session/{session_id}")
def delete_session(session_id: str):
    session = sessions.pop(session_id, None)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    shutil.rmtree(session["directory"], ignore_errors=True)

    return {"status": "deleted"}