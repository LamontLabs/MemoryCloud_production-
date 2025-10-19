import sqlite3
import os
import json
from datetime import datetime, timedelta
from src.memorycloud.config import settings

os.makedirs(os.path.dirname(settings.db_path), exist_ok=True)

def init_db():
    conn = sqlite3.connect(settings.db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        indicator BOOLEAN,
        created_at TEXT,
        encrypted BLOB
    )""")
    conn.commit()
    conn.close()

def insert_memory(text: str, indicator: bool, encrypted: bytes):
    conn = sqlite3.connect(settings.db_path)
    c = conn.cursor()
    c.execute("INSERT INTO memories (text, indicator, created_at, encrypted) VALUES (?, ?, ?, ?)",
              (text, indicator, datetime.utcnow().isoformat(), encrypted))
    conn.commit()
    conn.close()

def list_memories(query: str | None = None):
    conn = sqlite3.connect(settings.db_path)
    c = conn.cursor()
    if query:
        c.execute("SELECT id, text, indicator, created_at FROM memories WHERE text LIKE ?", (f"%{query}%",))
    else:
        c.execute("SELECT id, text, indicator, created_at FROM memories")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "text": r[1], "indicator": bool(r[2]), "created_at": r[3]} for r in rows]

def cleanup_old_memories():
    cutoff = datetime.utcnow() - timedelta(days=settings.retention_days)
    conn = sqlite3.connect(settings.db_path)
    c = conn.cursor()
    c.execute("DELETE FROM memories WHERE datetime(created_at) < ?", (cutoff.isoformat(),))
    conn.commit()
    conn.close()
