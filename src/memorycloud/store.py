# src/memorycloud/store.py
# MemoryCloud™ — Local SQLite store (deterministic + auto-init)
import os
import sqlite3
from typing import List, Tuple
from .config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database (auto-create directories)."""
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize database schema if missing."""
    conn = get_connection()
    with conn:
        conn.executescript(SCHEMA)
    conn.close()

def insert_memory(content: str) -> int:
    """Insert a memory record and return its ID."""
    conn = get_connection()
    with conn:
        cur = conn.execute("INSERT INTO memories (content) VALUES (?)", (content,))
        conn.commit()
        return cur.lastrowid

def list_memories(limit: int = 50) -> List[Tuple[int, str, str]]:
    """Return the most recent memories."""
    conn = get_connection()
    cur = conn.execute(
        "SELECT id, content, timestamp FROM memories ORDER BY id DESC LIMIT ?", (limit,)
    )
    results = cur.fetchall()
    conn.close()
    return [(r["id"], r["content"], r["timestamp"]) for r in results]

# Auto-init database when module loads (safe for CI)
init_db()
