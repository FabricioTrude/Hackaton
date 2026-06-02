import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent/"database.db"
connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY,
    token TEXT NOT NULL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO configuracoes (
    id,
    token
)
VALUES (
    1,
    '123456'
)
""")

connection.commit()

cursor.execute("""
SELECT *
FROM configuracoes
""")

print(cursor.fetchall())

connection.close()
print("Banco Inicializado! ", DB_PATH)
print("Linhas afetadas: ", cursor.rowcount)
