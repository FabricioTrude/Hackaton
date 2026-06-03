# db/init_db.py
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"

def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    auth_dir = (Path(__file__).parent / "../../auth").resolve()
    auth_dir.mkdir(exist_ok=True)

    file_path = auth_dir / "storage.py"

    if not file_path.exists():
        file_path.write_text(
            'TOKENS = {"123456": {"user": "admin"}}\n',
            encoding="utf-8"
        )

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS configuracoes (
                                                                id INTEGER PRIMARY KEY,
                                                                token TEXT NOT NULL
                   )
                   """)

    cursor.execute("""
                   INSERT OR IGNORE INTO configuracoes (id, token)
    VALUES (1, '123456')
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

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS logs(
                                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                      horario TEXT NOT NULL,
                                                      script TEXT NOT NULL,
                                                      parametros TEXT,
                                                      log_status TEXT NOT NULL,
                                                      ip TEXT,
                                                      tempo_execucao REAL,
                                                      output TEXT
                   )
                   """)

    connection.commit()
    connection.close()