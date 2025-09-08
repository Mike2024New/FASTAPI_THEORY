from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
# запуск через терминал: uvicorn THEORY.BIG_APPS.APP.main:app --reload

app = FastAPI(
    dependencies=[Depends(get_query_token)]  # применение общей зависимости (к абсолютно всем маршрутам)
)
app.name = "app"

app.include_router(users.router)  # подключение маршрутов приложения users
app.include_router(items.router)  # подключение маршрутов приложения items
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "Я чайник"}}
)


@app.get("/", tags=["main app"])
async def root():
    return {"message": "Главная страница сайта"}
