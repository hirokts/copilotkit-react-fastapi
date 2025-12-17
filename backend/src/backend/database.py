import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings


def get_db():
    conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
    return conn


def init_db() -> None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            preferences JSONB
        )
    """)
    cur.execute("""
        INSERT INTO users (id, name, preferences)
        VALUES ('user_123', 'コパイロットキッズ', '{"theme": "dark", "language": "ja"}')
        ON CONFLICT (id) DO NOTHING
    """)
    conn.commit()
    cur.close()
    conn.close()
