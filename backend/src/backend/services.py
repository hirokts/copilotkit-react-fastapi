from .database import get_db


def get_user_profile(user_id: str) -> dict | None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "id": row["id"],
            "name": row["name"],
            "preferences": row["preferences"] or {},
        }
    return None
