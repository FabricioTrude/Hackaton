# py -m venv .venv # baixar a venv
# .venv\Scripts\activate # activar a venv
# py -m uvicorn main:app --reload # ativar o site da fastapi
# taskkill /F /IM python.exe # matar o site se der pau

import shutil
from typing import Literal

from fastapi import APIRouter, Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import sys
import time
import os

from auth.dependencies import verify_token
from auth.storage import TOKENS
from backend.database import atualizar_script, obter_script, obter_scripts, cadastrar_script, get_connection, setar_script
from backend.db.init_db import init_db
from backend.logger import Logger
from auth.tokens import alterar_token, obter_token, validar_token

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

route = APIRouter()
os.makedirs("scripts", exist_ok=True)


class TokenValidation(BaseModel):
    token: str


class ScriptRequest(BaseModel):
    id: str


class TokenRequest(BaseModel):
    new_token: str


class ScriptRequestAdmin(BaseModel):
    nome: str
    caminho: str
    parametros: str
    descricao: str


class NovoTokenRequest(BaseModel):
    new_token: str


@app.get("/")
def home():
    return {
        "token": obter_token()
    }


@app.post("/dev/init-db")
def create_db():
    init_db()
    return {"status": "db criado"}


@app.post("/dev/nuke-db")
def nuke_db(token=Depends(verify_token)):
    return nuke_db(confirm=True)


@app.post("/auth/novo_token")
def novo_token(
        request: Request,
        new_token: str = Form(...),
        token=Depends(verify_token)
):
    inicio = time.time()
    log = Logger(request, get_connection)

    new_token = new_token.new_token

    if token == new_token:
        log.erro("novo_token", "erro: o token não pode ser o mesmo")
        return {
            "status": "erro",
            "mensagem": "token repetido"
        }

    alterar_token(new_token)

    with open("auth/storage.py", "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo = conteudo.replace(token, new_token)

    with open("auth/storage.py", "w", encoding="utf-8") as f:
        f.write(conteudo)

    fim = time.time()

    log.sucesso(
        script=request.url.path,
        parametros=new_token,
        tempo_execucao=round(fim - inicio, 4),
        output="Token alterado com sucesso"
    )

    return {
        "status": "sucesso",
        "mensagem": "novo token cadastrado"
    }


@app.post("/scripts/executar")
def executar(request: Request, id: str = Form(...), token=Depends(verify_token)):
    inicio = time.time()
    logger = Logger(request, get_connection)

    script = obter_script(id)

    if not script:
        logger.erro(id, f"script com id {id} não encontrado")
        return {"status": "erro", "mensagem": f"script com id {id} não encontrado"}

    id, nome, caminho, parametros, descricao, ativo = script

    if ativo == 0:
        logger.erro(id, "script desativado")
        return {"status": "erro", "mensagem": f"script de id {id} desativado"}

    try:
        resultado = subprocess.run(
            [sys.executable, caminho, *parametros],
            capture_output=True,
            text=True
        )

        fim = time.time()

        logger.sucesso(
            script=nome,
            parametros={"script": nome},
            tempo_execucao=round(fim - inicio, 4),
            output=resultado.stdout
        )

        return {
            "status": "sucesso",
            "stdout": resultado.stdout,
            "stderr": resultado.stderr
        }

    except Exception as e:
        logger.erro(id, str(e))

        return {
            "status": "erro",
            "mensagem": str(e)
        }


@app.get("/scripts/listar")
def listar_scripts(request: Request, token=Depends(verify_token)):
    inicio = time.time()
    log = Logger(request, get_connection)

    if not validar_token(token):
        log.erro(request.url.path, "token inválido")
        return {
            "status": "erro",
            "mensagem": "token inválido"
        }

    scripts = obter_scripts()

    fim = time.time()

    log.sucesso(
        script=request.url.path,
        parametros=token,
        tempo_execucao=round(fim - inicio, 4),
        output=scripts
    )

    return {
        "status": "sucesso",
        "scripts": scripts
    }


@app.post("/scripts/upload")
def upload_script(
        request: Request,
        name: str = Form(...),
        parametros: str = Form(""),
        descricao: str = Form(""),
        file: UploadFile = File(...),
        token=Depends(verify_token)
):
    inicio = time.time()
    log = Logger(request, get_connection)

    file_path = os.path.join("scripts", file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    try:
        cadastrar_script(
            name,
            file_path,
            parametros,
            descricao
        )

        fim = time.time()

        log.sucesso(
            script=request.url.path,
            parametros=parametros,
            tempo_execucao=round(fim - inicio, 4),
            output=f"Script {name} criado com sucesso"
        )

        return {
            "status": f"Script {name} criado com sucesso!"
        }

    except Exception as e:
        if str(e) == "UNIQUE constraint failed: scripts.nome":
            return {
                "status": "erro",
                "mensagem": "Script com esse nome já existe"
            }


@app.post("/scripts/update_script")
def update_script(
        request: Request,
        token=Depends(verify_token),
        id: str = Form(...),
        parametros: str = Form(""),
        descricao: str = Form(""),
        file: UploadFile = File(...)
):
    inicio = time.time()
    log = Logger(request, get_connection)

    try:
        script = obter_script(id)

        if not script:
            raise HTTPException(
                status_code=404,
                detail="Script não encontrado"
            )

        caminho = script[2]

        if os.path.exists(caminho):
            os.remove(caminho)

        with open(caminho, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        novos_parametros = parametros if parametros.strip() else script[3]
        nova_descricao = descricao if descricao.strip() else script[4]

        atualizar_script(
            id=id,
            parametros=novos_parametros,
            descricao=nova_descricao
        )

        fim = time.time()

        log.sucesso(
            script=request.url.path,
            parametros=novos_parametros,
            tempo_execucao=round(fim - inicio, 4),
            output=f"Script {file.filename} alterado com sucesso"
        )

        return {
            "status": "sucesso",
            "mensagem": f"Script {file.filename} alterado com sucesso!"
        }

    except HTTPException:
        raise
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e)
        }


@app.post("/scripts/set_script")
def set_script(
        request: Request,
        token=Depends(verify_token),
        id: str = Form(...),
        ativo: Literal["0", "1"] = Form(..., description="0 para desativar ou 1 reativar")
):
    inicio = time.time()
    log = Logger(request, get_connection)

    ativo = int(ativo)

    script = obter_script(id)

    if not script:
        log.erro(request.url.path, "Erro: Script inválido")
        return {"status": "erro", "mensagem": "script inválido"}

    if script[5] == 0 and ativo == 0:
        log.erro(request.url.path, f"Erro: Script {script[2]} já desativado")
        return {"status": "erro", "mensagem": "script já está desativado"}

    if script[5] == 1 and ativo == 1:
        log.erro(request.url.path, f"Erro: Script {script[2]} já está ativo")
        return {"status": "erro", "mensagem": "script já está ativo"}

    setar_script(id, ativo)

    fim = time.time()

    if ativo == 1:
        log.sucesso(
            script=script[1],
            parametros={"script": script[1]},
            tempo_execucao=round(fim - inicio, 4),
            output=f"Script {script[2]} reativado com sucesso!"
        )
        return {"status": "sucesso", "mensagem": "script reativado com sucesso!"}

    if ativo == 0:
        log.sucesso(
            script=script[1],
            parametros={"script": script[1]},
            tempo_execucao=round(fim - inicio, 4),
            output=f"Script {script[2]} desativado com sucesso!"
        )
        return {"status": "sucesso", "mensagem": "script desativado com sucesso"}