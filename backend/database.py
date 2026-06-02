from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def obter_token():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT token 
    FROM configuracoes
    WHERE id = 1
    """)
    token = cursor.fetchone()[0]

    conn.close()
    return token
