from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents, get_db
from schemas import Message, Project

app = FastAPI(title="DEMO Portfolio API")

# Allow all origins for demo; frontend will inject correct URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Portfolio API running", "time": datetime.utcnow().isoformat()}


@app.get("/test")
async def test_db():
    db = get_db()
    try:
        # Inspect basic info
        collections = await _list_collections_safe(db)
        return {
            "backend": "fastapi",
            "database": "mongodb",
            "database_url": "hidden",
            "database_name": db.name,
            "connection_status": "ok",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "fastapi", "database": "mongodb", "connection_status": f"error: {e}"}


async def _list_collections_safe(db):
    try:
        return db.list_collection_names()
    except Exception:
        return []


@app.get("/projects", response_model=List[Project])
async def list_projects(limit: int = 50):
    docs = get_documents("project", {}, limit)
    # Map to Project-compatible dicts
    result = []
    for d in docs:
        result.append({
            "title": d.get("title"),
            "stack": d.get("stack", []),
            "description": d.get("description", ""),
            "code_url": d.get("code_url"),
            "live_url": d.get("live_url"),
            "cover": d.get("cover"),
        })
    return result


@app.post("/contact")
async def submit_contact(msg: Message):
    try:
        doc_id = create_document("message", msg.model_dump())
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
