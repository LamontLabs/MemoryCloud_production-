CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    indicator BOOLEAN,
    created_at TEXT,
    encrypted BLOB
);
