from fastapi import Header, HTTPException, Request, Depends
from typing import Optional

from auth.storage import TOKENS
from backend.database import get_connection
from backend.logger import Logger


def verify_token(
        request: Request,
        x_isy_token: Optional[str] = Header(default=None, alias="X-Isy-Token")
):
    if not x_isy_token:
        Logger(request, get_connection).erro(request.url.path, "Token ausente")
        raise HTTPException(status_code=403, detail="Token ausente")

    if x_isy_token not in TOKENS:
        Logger(request, get_connection).erro(request.url.path, "Token inválido")
        raise HTTPException(status_code=403, detail="Token inválido")

    return x_isy_token