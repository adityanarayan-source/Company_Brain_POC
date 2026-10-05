import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from config import DATABASE_PATH

DB_FILE = Path(__file__).parent / DATABASE_PATH


def connect():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def init_db():
    with connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, user_id TEXT, content TEXT, created_at TEXT)''')
        db.execute('''CREATE TABLE IF NOT EXISTS activity_logs (id INTEGER PRIMARY KEY, user_id TEXT, message TEXT, tool_name TEXT, tool_status TEXT, created_at TEXT)''')


def save_log(user_id, message, tool_name, tool_status):
    with connect() as db:
        db.execute('INSERT INTO activity_logs (user_id, message, tool_name, tool_status, created_at) VALUES (?, ?, ?, ?, ?)', (user_id, message, tool_name, tool_status, datetime.now(timezone.utc).isoformat()))
