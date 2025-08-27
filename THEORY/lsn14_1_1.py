from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
как работает OAuth2PasswordBearer под капотом?
"""


async def verify_token(token: str) -> bool:
    return token == "test"


async def auth(authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=401, detail="вы не авторизованы, получить токен можно по url www...")
    if not await verify_token(token=authorization):
        raise HTTPException(status_code=422, detail="Неверный токен, отказано в доступе...")


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/", dependencies=[Depends(auth)])
async def ex1():
    return {"msg": "test content"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
