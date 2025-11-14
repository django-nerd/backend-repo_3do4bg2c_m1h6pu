import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection

# Read from environment (Auto-provided in this environment)
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[MongoClient] = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db


def get_collection(name: str) -> Collection:
    db = get_db()
    return db[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> str:
    col = get_collection(collection_name)
    now = datetime.utcnow()
    data_with_meta = {
        **data,
        "created_at": now,
        "updated_at": now,
    }
    result = col.insert_one(data_with_meta)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    col = get_collection(collection_name)
    filter_dict = filter_dict or {}
    docs = list(col.find(filter_dict).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])  # make JSON serializable
    return docs
