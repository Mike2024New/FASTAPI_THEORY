import logging
from UTILS.APP_RUN import app_run
from typing import Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"
logging.basicConfig(level=logging.INFO)

"""
Вопрос 12: Создай кастомный обработчик HTTPException с логированием и ответом.
"""


class ResourceNotFound(HTTPException):
    def __init__(self, resource: Any, url: str):
        detail = {"msg": f"Ошибка, ресурс `{resource}`, по url `{url}` не найден"}
        super().__init__(status_code=404, detail=detail)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"❌Ошибка: {exc.detail}\nМаршрут ошибки: {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail}, headers={"X-headers": "error"})


users_base = ["Иван", "Полина", "Василий"]  # псевдо БД в которой индекс и есть ключ пользователя


# http://127.0.0.1:8000/ex1/4/
@app.get("/ex1/{user_id}/", status_code=200)
def ex1(user_id: int, request: Request):
    if user_id >= len(users_base):
        # возбуждение исключения, пользователя не оказалось в БД
        raise ResourceNotFound(resource=f"user_id={user_id}", url=str(request.url))
    logging.info(f"Запрошен пользователь {user_id}")
    return {"user": users_base[user_id]}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
