from backend.database import get_connection


def obter_token():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT token FROM configuracoes WHERE id = 1 """)
    token = cursor.fetchone()
    conn.close()
    return token[0] if token else None

def validar_token(token:str):
    return token == obter_token()

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