from typing import Annotated

from fastapi import HTTPException, Header

"""
Здесь зависимости хранятся в отдельном модуле. Зависимости указанные здесь проверяют наличие заголовков.
"""


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake_super_secret_token":
        raise HTTPException(status_code=400, detail="X_Token header invalid")


async def get_query_token(token: str):
    if token != "Mike":
        raise HTTPException(status_code=400, detail="No Mike token provided")
