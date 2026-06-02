# py -m uvicorn main:app --reload
# taskkill /F /IM python.exe

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys

from backend.database import obter_script, obter_token, cadastrar_script

from backend.database import alterar_token

app = FastAPI()


class ScriptRequest(BaseModel):
    token: str
    script: str


class TokenRequest(BaseModel):
    old_token: str
    new_token: str


class ScriptRequestAdmin(BaseModel):
    nome: str
    caminho: str
    parametros: str
    descricao: str

SCRIPTS = {
    "teste": "scripts/teste.py",
    "criar": "backend/database.py"
}


@app.get("/")
def home():
    return {
        "token": obter_token()
    }


@app.post("/novo_token")
def novo_token(dados: TokenRequest):
    token_correto = obter_token()

    if dados.old_token != token_correto:
        return {
            "status": "erro",
            "mensagem": "token inválido"
        }

    alterar_token(dados.new_token)

    return {
        "status": "sucesso",
        "mensagem": "novo token cadastrado"
    }


@app.post("/admin/script")
def cadastrar_script_api(dados: ScriptRequestAdmin):
    cadastrar_script(
        dados.nome,
        dados.caminho,
        dados.parametros,
        dados.descricao
    )
    return {
        "status":"sucesso"
    }


@app.post("/executar")
def executar(dados: ScriptRequest):
    token_correto = obter_token()

    if dados.token != token_correto:
        return{ "status": "erro", "mensagem": "token inválido"}

    script = obter_script(dados.script)

    if not script:
        return { "status": "erro", "mensagem": "script não encontrado" }

    caminho, parametros, ativo = script

    if ativo == 0:
        return {"status": "erro", "mensagem": "script desativado"}

    try:
        resultado = subprocess.run(
            [sys.executable, caminho],
            capture_output=True,
            text=True
        )

        return {
            "status": "sucesso",
            "stdout": resultado.stdout,
            "stderr": resultado.stderr
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }