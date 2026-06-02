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


def alterar_token(novo_token):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE configuracoes
    SET token = ?
    WHERE id = 1
    """, (novo_token,))
    conn.commit()
    conn.close()


def cadastrar_script(nome, caminho, parametros, descricao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO scripts (
        nome,
        caminho,
        parametros,
        descricao
    ) 
    VALUES (?,?,?,?)
    """, (nome, caminho, parametros, descricao))
    conn.commit()
    conn.close()

def obter_script(nome):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT caminho, parametros, ativo
    FROM scripts
    WHERE nome = ?
    """,(nome,))
    script = cursor.fetchone()
    conn.close()
    return script