from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Cookie
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict
from typing import Literal, Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Для Cookie также как и для Query, Body и Head параметров можно прописывать модели pydantic, для сбора нужных ключей в 
одном запросе. Также можно устанавливать запрет на передачу лишних атрибутов не указанных в модели, с помощью опции
конфигурации extra="forbid"
------------------------------------------------------------
Для того, чтобы браузер мог отправить Cookie их нужно сначала установить, для этого в этом уроке немного забегаю вперед
используя объект Response, который принимается в запросе (и также отправляется клиенту), и в нем можно использовать 
метод set_cookie, для установки куков в браузере клиента.

В данном примере сперва нужно зайти на главную страницу: http://127.0.0.1:8000/
на ней установятся куки (куки без дополнительной настройки стираются при каждом закрытии браузера)

"""


class Cookies(BaseModel):
    session_id: str
    site_theme: Literal["black", "white"] = "black"

    # этот параметр запрещает передачу посторонних ключей не указанных в модели
    model_config = ConfigDict(extra="forbid")


@app.get("/")
def home(response: Response):
    # каждый вызов set_cookie, задаёт один cookie параметр
    response.set_cookie(
        key="session_id",
        value="test_session_id",
        httponly=True,  # запрет на доступ к кукам из JavaScript
        # secure=True,  # передача только по HTTPS (отключено для учебного примера здесь)
        samesite="lax"  # защита от CSRF атак (межсетевых запросов) в cookie добавляется дополнительный csrf токен
    )  # установка ключа сессии
    response.set_cookie(
        key="site_theme",
        value="black",
        httponly=True,  # запрет на доступ к кукам из JavaScript
        # secure=True,  # передача только по HTTPS (отключено для учебного примера здесь)
        samesite="lax"  # защита от CSRF атак (межсетевых запросов) в cookie добавляется дополнительный csrf токен
    )  # установка ключа сессии
    return f"куки установлены"


"""
ex1
здесь на вход ожидается модель Cookies, с анотацией Cookie, но для того, чтобы этот маршрут работал корректно, нужно 
сначала перейти на страницу: http://127.0.0.1:8000/
На ней (в маршруте "/"-home) будут установлены cookie.
"""


@app.get("/ex1/")
def ex1(cookies: Annotated[Cookies, Cookie()]):
    return cookies


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
