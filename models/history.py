import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict

from .mongo_connection import get_collection

TEMP_FOLDER = os.getenv("TEMP_FOLDER", "./_temp")
os.makedirs(TEMP_FOLDER, exist_ok=True)
_LOCAL_DB_FILE = os.path.join(TEMP_FOLDER, "local_chats.json")

def _load_local_db() -> Dict:
    if not os.path.exists(_LOCAL_DB_FILE):
        return {}
    try:
        with open(_LOCAL_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_local_db(db: Dict):
    with open(_LOCAL_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def create_chat(user_id: str, title: str = "") -> str:
    collection = get_collection()
    chat_id = f"chat_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    chat_doc = {
        "chat_id": chat_id,
        "user_id": user_id,
        "title": title or chat_id,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "messages": []
    }
    if collection:
        collection.insert_one(chat_doc)
    else:
        db = _load_local_db()
        user_chats = db.setdefault(user_id, {})
        user_chats[chat_id] = chat_doc
        _save_local_db(db)
    return chat_id

def update_chat(user_id: str, chat_id: str, role: str, content: str) -> bool:
    collection = get_collection()
    msg = {"role": role, "content": content, "timestamp": _now_iso()}
    if collection:
        res = collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$push": {"messages": msg}, "$set": {"updated_at": _now_iso()}}
        )
        return res.modified_count > 0
    else:
        db = _load_local_db()
        user_chats = db.get(user_id, {})
        chat = user_chats.get(chat_id)
        if not chat:
            return False
        chat.setdefault("messages", []).append(msg)
        chat["updated_at"] = _now_iso()
        _save_local_db(db)
        return True

def list_last_chats(user_id: str) -> List[Dict]:
    collection = get_collection()
    if collection:
        cursor = collection.find({"user_id": user_id}).sort("updated_at", -1)
        result = []
        for c in cursor:
            result.append({
                "chat_id": c.get("chat_id"),
                "title": c.get("title"),
                "created_at": c.get("created_at"),
                "updated_at": c.get("updated_at"),
                "message_count": len(c.get("messages", []))
            })
        return result
    else:
        db = _load_local_db()
        user_chats = db.get(user_id, {})
        result = []
        for chat in user_chats.values():
            result.append({
                "chat_id": chat.get("chat_id"),
                "title": chat.get("title"),
                "created_at": chat.get("created_at"),
                "updated_at": chat.get("updated_at"),
                "message_count": len(chat.get("messages", []))
            })
        # order by updated_at desc
        return sorted(result, key=lambda x: x.get("updated_at", ""), reverse=True)

def get_chat_info(user_id: str, chat_id: str) -> Optional[Dict]:
    collection = get_collection()
    if collection:
        return collection.find_one({"user_id": user_id, "chat_id": chat_id}, {"_id": 0})
    else:
        db = _load_local_db()
        return db.get(user_id, {}).get(chat_id)

def get_chat_messages(user_id: str, chat_id: str) -> Dict:
    chat = get_chat_info(user_id, chat_id)
    if not chat:
        return {"messages": []}
    return {"messages": chat.get("messages", [])}

def delete_conversation(user_id: str, chat_id: str) -> bool:
    collection = get_collection()
    if collection:
        res = collection.delete_one({"user_id": user_id, "chat_id": chat_id})
        return res.deleted_count > 0
    else:
        db = _load_local_db()
        user_chats = db.get(user_id, {})
        if chat_id in user_chats:
            del user_chats[chat_id]
            _save_local_db(db)
            return True
        return False