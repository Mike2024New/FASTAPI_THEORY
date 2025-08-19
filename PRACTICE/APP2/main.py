from UTILS.APP_RUN import app_run
from UTILS.GENERATE_UUID_KEY import generate_random_key_uuid
from fastapi import FastAPI, Response, Cookie, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.name = "app"
app.mount(
    "/static",  # папка содержащая стили
    StaticFiles(directory="static"),  # создаётся объект который работает со статическими файлами
    name="static"  # имя переменной по которой шаблон будет достраивать путь к папке с файлами
)  # с помощью app.mount можно добавить css стили

"""
sessions -> идентификаторы сессии, хранят в себе уникальный идентификатор и сслыку на пользователя (например на его 
логин).
users -> здесь хранится информация о пользователе для бизнес логики, его имя, пароль (в хэшированном виде), и другие 
данные которые могут быть полезны для работы с сайтом, например баланс кошелька.
Также в куках на клиенте хранятся отдельные настройки предпочтений, например тема сайта и другие.
"""

users = {}  # хранилище самих настроек пользователя
sessions = {}  # хранилище сессий (потом вынесу в отдельный json)


def set_session(session_id, response: Response):
    """проверка, что сессия с клиентом уже установлена"""
    if session_id and session_id in sessions:  # проверка, что сессия есть и в sessions (чтобы не работать с "мертовой" сессий)
        return session_id  # отлично, соединение с пользователем уже было установлено ранее
    # создание новой сессии
    new_session_id = generate_random_key_uuid()
    response.set_cookie(
        key="session_id",
        value=new_session_id,
        httponly=True,  # запрет на доступ к кукам из JavaScript
        # secure=True,  # передача только по HTTPS (отключено для учебного примера здесь)
        samesite="lax"  # защита от CSRF атак (межсетевых запросов) в cookie добавляется дополнительный csrf токен
    )
    sessions[new_session_id] = {"login": None, "auth": False}  # здесь будет записан номер пользователя и ссылка на него
    return new_session_id


# http://127.0.0.1:8000/
@app.get("/")
def home(response: Response, session_id: str | None = Cookie(default=None)):
    set_session(session_id, response)  # проверка что установлена сессия id
    return "Главная страница"


@app.get("/login/")
def login_get_form(request: Request, response: Response, session_id: str | None = Cookie(default=None)):
    actual_session_id = set_session(session_id, response=response)
    if sessions.get(actual_session_id) and sessions[actual_session_id]["auth"]:
        return f"Вы уже зарегистрированы"
    return templates.TemplateResponse(
        name="login.html",
        context={"request": request}
    )


@app.post("/login/")
def login_user(response: Response, login=Form(), password=Form(), session_id: str | None = Cookie(default=None)):
    actual_session_id = set_session(session_id, response)  # проверка, что сессия уже установлена
    if login not in users:
        raise HTTPException(status_code=400, detail=f"Не верный логин `{login}`.")
    else:
        if users[login]["password"] != password:
            raise HTTPException(status_code=400, detail=f"Не верный пароль `{login}`")
    # будет перезаписана старая сессия, либо создастся новая
    sessions[actual_session_id] = {"login": login, "auth": True}  # запись в сессию, что пользователь успешно вошел
    return f"Вы вошли"


@app.get("/register/")
def register_get_form(request: Request, response: Response, session_id: str | None = Cookie(default=None)):
    set_session(session_id, response=response)
    return templates.TemplateResponse(
        name="register.html",  # вернуть шаблон с формой регистрации
        context={"request": request, "state_register": False}
    )


@app.post("/register/")
def register_user(
        response: Response,
        request: Request,
        login=Form(), password=Form(), password_repeat=Form(),
        session_id: str | None = Cookie(default=None)
):
    # базовые проверки введенных пользователем данных
    if login in users:
        raise HTTPException(status_code=400, detail=f"Пользователь с логином `{login}` уже существует!")
    if password != password_repeat:
        raise HTTPException(status_code=400, detail="Пароли должны совпадать!")

    actual_session_id = set_session(session_id, response)  # проверка что установлена сессия id
    # пользователь создаётся в БД
    users[login] = {
        "password": password,  # внимание здесь упрощение, в реале: ПАРОЛЬ В ЧИСТОМ ВИДЕ НЕ ХРАНИТЬ!
        "posts": []  # иммитация полезной нагрузки
    }
    sessions[actual_session_id] = {
        "login": login,  # привязать к сессии этого пользователя
        "auth": False  # состояние пользователя, зарегистрирован или нет
    }
    return templates.TemplateResponse(
        name="register.html",  # вернуть шаблон с формой регистрации и уведомлением что все ок
        context={"request": request, "state_register": True}
    )


@app.get("/my_profile/")
def my_profile(request: Request, session_id: str | None = Cookie(default=None)):
    print(session_id)
    print(sessions)
    if sessions.get(session_id) and not sessions[session_id]["auth"]:
        return HTTPException(status_code=401, detail="доступ только авторизованным пользователям")
    return templates.TemplateResponse(name="my_profile.html", context={
        "request": request, "username": sessions[session_id]["login"]
    })


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
