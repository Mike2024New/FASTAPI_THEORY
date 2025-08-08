from UTILS.APP_RUN import app_run
from UTILS.GENERATE_UUID_KEY import generate_random_key_uuid
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, Cookie, Body
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В данном примере простой прототип приложения с использованием Cookie, к примеру при первом запросе клиента на
http://127.0.0.1:8000/auth/     -> происходит его авторизация (в post запросе он должен передать свой логин, иммитация
ввода данных из формы). За тем он спокойно может переходить по остальным маршрутам.
=========================
Здесь та реализация где данные хранятся на сервере, а в cookie хранится лишь идентификатор на эти данные
=========================================================================================================
Внимание! В проде, нужно использовать исключительно https, с шифрованием передаваемых данных, установив настройки от
csrf атак (межсетевых запросов), от получения куков с помощью JS.
"""

users = {}  # упрощенная модель хранения данных пользователя по id сессии


class UserNoExistsError(ValueError):
    pass


@app.exception_handler(UserNoExistsError)
async def unique_short_error(request: Request, exc: UserNoExistsError):
    print(f"KeyError: {exc}, path: {request.url}")  # логирование ошибки
    return JSONResponse(
        status_code=401,  # пользователь не авторизован
        content={"detail": str(exc)}
    )


@app.post("/auth/")
async def set_cookie(login: Annotated[str, Body(description="Ваш логин", embed=True)], response: Response):
    """
    Авторизация пользователя по login, создает нового пользователя в псевдо БД, users, с применением к нему заводских
    настроек.
    :param login: логин пользователя
    :param response: информация от браузера
    :return: сообщение о том, что безопасное соединение создано
    """
    value = generate_random_key_uuid(length=4)
    print(f"Создан пользователь '{login}', ID сессии '{value}'")  # print здесь просто для теста
    # ВНИМАНИЕ! Здесь установка Cookie упрощена, но на проде нужно ставить флаги httponly, secure, samesite
    response.set_cookie(
        key="session_id",
        value=value,
        httponly=True,  # запрет на доступ к кукам из JavaScript
        # secure=True,  # передача только по HTTPS (отключено для учебного примера здесь)
        samesite="lax"  # защита от CSRF атак (межсетевых запросов) в cookie добавляется дополнительный csrf токен
    )  # установка ключа сессии
    users[value] = {"theme": "black", "login": login}  # установка настроек с хранением их на сервере
    # так естественно id сессии ни кто не передает, это для примера на docs
    # данные Cookie установленные в response отправляются браузеру в фоне
    return {"msg": f"безопасное соединение установлено, id сессии {value}"}


async def check_exist_user(session_id):
    if not session_id or session_id not in users:
        raise UserNoExistsError("Вы не авторизованы")


# http://127.0.0.1:8000/my_profile/     -> не сработает если не выполнен вход на auth
@app.get("/my_profile/")
async def my_profile(session_id: str | None = Cookie(default=None)):
    """
    получение данных о профиле пользователя, доступно только если установлено соединение, точнее если пользователь
    перешел на auth и передал свой логин.
    :param session_id: сессия идентификатора (берется из cookie после установки соединения)
    :return: информацию о пользователе, если соединение установлено, или же ошибку 401, отказано по причине
    неавторизованности
    """
    await check_exist_user(session_id)  # проверить, что пользователь авторизован
    return users[session_id]


# http://127.0.0.1:8000/logout/
@app.get("/logout/")
async def logout(response: Response, session_id: str | None = Cookie(default=None)):
    """
    Выход из текущей установленной Cookie сессии
    :param response: информация от браузера
    :param session_id: номер сессии берется из куков (то есть пользователь этого не видит)
    :return: выход из сессии если такой пользователь есть в users, или же 401 ошибка авторизации
    """
    await check_exist_user(session_id)  # проверить, что пользователь авторизован
    response.delete_cookie("session_id")
    users.pop(session_id)
    return {"msg": "Вы вышли из системы"}


# http://127.0.0.1:8000/set_theme/
@app.get("/set_theme/")
async def set_theme(session_id: str | None = Cookie(default=None)):
    """
    Изменение настройки темы сайта (пример как редактируется информация в куках)
    :param session_id: номер сессии берется из куков (то есть пользователь этого не видит)
    :return: выход из сессии если такой пользователь есть в users, или же 401 ошибка авторизации
    """
    await check_exist_user(session_id)  # проверить, что пользователь авторизован
    users[session_id]["theme"] = "black" if users[session_id]["theme"] == "white" else "white"
    return {"msg": f"Тема '{users[session_id]['theme']}' установлена"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
