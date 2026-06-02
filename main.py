# py -m uvicorn main:app --reload
# taskkill /F /IM python.exe

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys

from backend.database import obter_token

app = FastAPI()


class ScriptRequest(BaseModel):
    token: str
    script: str


class TokenRequest(BaseModel):
    old_token: str
    new_token: str


SCRIPTS = {
    "teste": "scripts/teste.py",
    "criar": "backend/database.py"
}


@app.get("/")
def home():
    return {
        "message": "Welcome!"
    }


@app.post("/executar")
def executar(dados: ScriptRequest):
    token_correto = obter_token()

    if dados.token != token_correto:
        return{
            "status": "erro",
            "mensagem": "token inválido"
        }

    if dados.script not in SCRIPTS:
        return {
            "status": "erro",
            "mensagem": "script não encontrado"
        }

    caminho_script = SCRIPTS[dados.script]

    try:
        resultado = subprocess.run(
            [sys.executable, caminho_script],
            capture_output=True,
            text=True
        )

        return {
            "status": "sucesso",
            "stdout": resultado.stdout,
            "stderr": resultado.stderr,
            "codigo_retorno": resultado.returncode
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }