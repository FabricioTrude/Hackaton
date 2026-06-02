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

cursor.execute("""
CREATE TABLE IF NOT EXISTS scripts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    caminho TEXT NOT NULL,
    parametros TEXT,
    descricao TEXT,
    ativo INTEGER NOT NULL DEFAULT 1
)
""")

connection.commit()

cursor.execute("""
SELECT *
FROM configuracoes
""")

connection.close()