from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Header
from fastapi.responses import Response
from typing import Annotated
from pydantic import BaseModel, field_validator

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Для заголовков можно объявлять pydantic модели.
Заголовки поддреживают повторяющиеся одни и те же ключи, их значения будут автоматически преобразованы
в массив (как у Query и Cookie параметров), но это будет строка, и её нужно дополнительно преобразовать, для этого
используется field_validator с режимом before, который преобразовывает эту строку в нужный формат (в данном случае
в словарь).
Для того, чтобы Cookie приходили в ex2, их нужно установить перейдя на ex1
"""


# http://127.0.0.1:8000/ex1/
# для того чтобы в ex2, отображались Cookie, нужно установить их в ex1
@app.get("/ex1/")
def ex1(response: Response):
    response.set_cookie(
        key="session_id",
        value="test123",
        # secure=True,
        httponly=True,
        samesite="lax",
    )
    response.set_cookie(
        key="theme",
        value="white",
        # secure=True,
        httponly=True,
        samesite="lax",
    )
    return f"Cookie установлены"


class TestHeaders(BaseModel):
    host: str
    sec_ch_ua_platform: str
    connection: str
    user_agent: str
    cookie: dict[str, str] = None  # на вход будет принята строка с 1 элементом

    @field_validator('cookie', mode='before')
    @classmethod
    def cookie_to_arr(cls, value):
        # валидатор который преобразует строку в словарь (про валидаторы рассказано в репозитории про pydantic V2)
        if isinstance(value, str) and ";" in value:
            cookie = value.split(";")
            value = {}
            for val in cookie:
                part = val.split("=")
                value[part[0].lstrip()] = part[1].lstrip()
        return value


# http://127.0.0.1:8000/ex2/
# для того чтобы в ex2, отображались Cookie, нужно установить их в ex1
@app.get("/ex2/")
def ex2(headers: Annotated[TestHeaders, Header()]):
    if not headers.cookie:
        return "Вы не установили Cookie, перейдите по http://127.0.0.1:8000/ex2/"
    return headers


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
