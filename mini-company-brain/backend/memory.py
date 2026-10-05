from datetime import datetime, timezone
from database import connect


def get_memories(user_id, query=''):
    # SQLite is the reliable local fallback; Supermemory can be added inside this file later.
    with connect() as db:
        rows = db.execute('SELECT content FROM memories WHERE user_id = ? ORDER BY id DESC LIMIT 10', (user_id,)).fetchall()
    return [row[0] for row in rows]


def save_memory(user_id, content):
    with connect() as db:
        db.execute('INSERT INTO memories (user_id, content, created_at) VALUES (?, ?, ?)', (user_id, content, datetime.now(timezone.utc).isoformat()))
