from typing import Annotated
from fastapi import HTTPException, Header

fake_x_token = "test_token"


async def check_x_token(x_token: Annotated[str, Header()]):
    if x_token != fake_x_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
