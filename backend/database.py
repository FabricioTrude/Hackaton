from datetime import datetime
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

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


def atualizar_script(id, parametros, descricao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE scripts
        SET
            parametros = ?,
            descricao = ?
        WHERE id = ?; """, (parametros, descricao, id))
    conn.commit()
    conn.close()

def obter_script(identifier):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" SELECT * FROM scripts WHERE id = ? """,(identifier,))
    script = cursor.fetchone()
    if script:
        conn.close()
        return script
    cursor.execute(""" SELECT * FROM scripts WHERE nome = ? """,(identifier,))
    script = cursor.fetchone()
    conn.close()
    return script

def obter_scripts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM scripts
    """)
    scripts = cursor.fetchall()
    conn.close()
    return {
        "status": "sucesso",
        "scripts": scripts
    }

def setar_script(id, identifier):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE scripts SET ativo = ? WHERE id = ?; """, (identifier, id))
    conn.commit()
    conn.close()