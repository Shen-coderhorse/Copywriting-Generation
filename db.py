import sqlite3
import os
import sys
from datetime import datetime, timedelta

def _get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(_get_app_dir(), "data", "copywriting.db")


def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            greeting TEXT NOT NULL,
            body TEXT NOT NULL,
            tags TEXT NOT NULL,
            full_text TEXT NOT NULL,
            mode TEXT DEFAULT 'morning',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_copywriting(date, greeting, body, tags, full_text, mode="morning"):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO history (date, greeting, body, tags, full_text, mode) VALUES (?, ?, ?, ?, ?, ?)",
        (date, greeting, body, tags, full_text, mode),
    )
    conn.commit()
    conn.close()


def get_history(days=365):
    conn = _get_conn()
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute(
        "SELECT * FROM history WHERE date >= ? ORDER BY date DESC, id DESC",
        (since,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_today_exists(date_str, mode="morning"):
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM history WHERE date = ? AND mode = ? ORDER BY id DESC LIMIT 1",
        (date_str, mode),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_generated_texts():
    conn = _get_conn()
    rows = conn.execute("SELECT body FROM history").fetchall()
    conn.close()
    return [r["body"] for r in rows]


def get_config(key, default=None):
    conn = _get_conn()
    row = conn.execute("SELECT value FROM config WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_config(key, value):
    conn = _get_conn()
    conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def get_all_configs():
    conn = _get_conn()
    rows = conn.execute("SELECT key, value FROM config").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}


def save_knowledge(filename, content):
    conn = _get_conn()
    conn.execute("INSERT INTO knowledge (filename, content) VALUES (?, ?)", (filename, content))
    conn.commit()
    conn.close()


def get_all_knowledge():
    conn = _get_conn()
    rows = conn.execute("SELECT id, filename, created_at FROM knowledge ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_knowledge_content(kid):
    conn = _get_conn()
    row = conn.execute("SELECT content FROM knowledge WHERE id = ?", (kid,)).fetchone()
    conn.close()
    return row["content"] if row else None


def delete_knowledge(kid):
    conn = _get_conn()
    conn.execute("DELETE FROM knowledge WHERE id = ?", (kid,))
    conn.commit()
    conn.close()


def get_knowledge_combined():
    conn = _get_conn()
    rows = conn.execute("SELECT filename, content FROM knowledge").fetchall()
    conn.close()
    parts = []
    for r in rows:
        parts.append(f"【{r['filename']}】\n{r['content']}")
    return "\n\n".join(parts)
