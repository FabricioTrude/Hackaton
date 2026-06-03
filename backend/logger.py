from backend.database import get_connection
from datetime import datetime 
import json

class Logger:
    def __init__(self, request, get_connection):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.ip = request.client.host
        self.horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def registrar(self, script, parametros, status, tempo_execucao = None, output = None):

        self.cursor.execute("""
        INSERT INTO logs (
            horario,
            script,
            parametros,
            log_status,
            ip,
            tempo_execucao,
            output
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.horario,
            script,
            json.dumps(parametros) if parametros else None,
            status,
            self.ip,
            tempo_execucao,
            json.dumps(output) if output else None
        ))

        self.conn.commit()
    def sucesso(self, script, parametros, tempo_execucao, output):
        self.registrar(
            script=script, # Swagger Script Name
            parametros=json.dumps(parametros or {}),
            status="sucesso",
            tempo_execucao=tempo_execucao or None,
            output=output or None
        )

    def erro(self, script, mensagem):
        self.registrar(
            script=script,
            parametros=json.dumps({"script": script}),
            status=f"erro: {mensagem}"
        )