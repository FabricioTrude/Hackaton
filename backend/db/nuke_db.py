from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database.db"
AUTH_FILE = BASE_DIR / "auth" / "storage.py"

def nuke_db():
    # apaga banco
    if DB_PATH.exists():
        DB_PATH.unlink()

    # apaga storage de auth
    if AUTH_FILE.exists():
        AUTH_FILE.unlink()

    return {
        "db_deleted": DB_PATH.exists() is False,
        "auth_deleted": AUTH_FILE.exists() is False
    }