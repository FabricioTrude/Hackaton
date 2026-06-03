from fastapi import Header, HTTPException, Depends, Request

from backend.database import get_connection
from backend.logger import Logger
from .storage import TOKENS

def verify_user(request: Request, x_isy_token: str = Header(..., alias="X-Isy-Token")):
    if not x_isy_token or x_isy_token not in TOKENS:
        Logger(request, get_connection).erro(request.url.path, "Token inválido")
        raise HTTPException(status_code=403, detail="Token inválido")

    return TOKENS[x_isy_token]  

def verify_token(request: Request, x_isy_token: str = Header(..., alias="X-Isy-Token")):
    if not x_isy_token or x_isy_token not in TOKENS:
        Logger(request, get_connection).erro(request.url.path, "Token inválido")
        print(str(request), x_isy_token)
        raise HTTPException(status_code=403, detail="Token inválido")
    
    return x_isy_token