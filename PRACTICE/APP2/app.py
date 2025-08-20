from UTILS.APP_RUN import app_run
from UTILS.GENERATE_UUID_KEY import generate_random_key_uuid
from fastapi import FastAPI, Request, Response, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
app.name = "app"
session_storage = {}
users_storage = {}

templates = Jinja2Templates(directory="templates")
app.mount(
    "/static",  # папка содержащая стили
    StaticFiles(directory="static"),  # создаётся объект который работает со статическими файлами
    name="static"  # имя переменной по которой шаблон будет достраивать путь к папке с файлами
)  # с помощью app.mount можно добавить css стили


class UserBase(BaseModel):
    login: str
    name: str
    age: int
    city: str


class UserInput(UserBase):
    password: str
    password_repeat: str


def set_cookie(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    # print(f"session_storage: {session_storage}")
    # print(f"Текущий session_id: {session_id}")
    if session_id is None or session_id not in session_storage:
        session_id = generate_random_key_uuid(length=10)
        response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax")
        session_storage[session_id] = {"login": None, "auth": False}
    return session_id


@app.get("/")
def home(request: Request):
    session_id = request.cookies.get("session_id")  # получить текущий сессионный ключ
    auth = False
    if session_id in session_storage:
        auth = session_storage[session_id]["auth"]
    response = templates.TemplateResponse(name="home.html", context={
        "request": request, "auth": auth
    })
    set_cookie(request, response)  # устанавливаем session_id (если ещё не установлено)
    return response


@app.get("/register/")
def register(request: Request):
    response = templates.TemplateResponse(name="register.html", context={"request": request})
    set_cookie(request, response)  # устанавливаем session_id (если ещё не установлено)
    return response


@app.post("/register/")
def register_user(request: Request, response: Response,
                  login: Annotated[str, Form()], name: Annotated[str, Form()],
                  age: Annotated[int, Form()], city: Annotated[str, Form()],
                  password: Annotated[str, Form()], password_repeat: Annotated[str, Form()]):
    session_id = set_cookie(request, response)  # установка session_id (если ещё не установлено)
    if login in users_storage:
        raise HTTPException(status_code=400, detail=f"пользователь с логином `{login}` уже существует.")
    # проверка, что введенные на сайте данные корректны
    user_input_model = UserInput(login=login, name=name, age=age, city=city, password=password,
                                 password_repeat=password_repeat)
    # сохранение пользователя в магазине
    users_storage[login] = user_input_model.model_dump(exclude={"password_repeat"})
    session_storage[session_id]["login"] = login
    return RedirectResponse(url="http://127.0.0.1:8000/login/", status_code=303)  # важно для post запросов ставить 303


@app.get("/login/")
def register(request: Request):
    response = templates.TemplateResponse(name="login.html", context={"request": request})
    set_cookie(request, response)  # устанавливаем session_id (если ещё не установлено)
    return response


@app.post("/login/")
def login_user(request: Request, login: Annotated[str, Form()], password: Annotated[str, Form()]):
    response = templates.TemplateResponse(name="login.html", context={"request": request})
    session_id = set_cookie(request, response)  # устанавливаем session_id (если ещё не установлено)
    # проверка что такой логин есть в БД
    if login not in users_storage:
        raise HTTPException(status_code=400, detail=f"Пользователь с логином `{login}` не существует в БД.")
    # проверка пароля
    if not users_storage[login]["password"] == password:
        raise HTTPException(status_code=400, detail="Неверный пароль")
    session_storage[session_id]["auth"] = True
    return RedirectResponse(url="http://127.0.0.1:8000/", status_code=303)


@app.get("/profile/")
def profile(request: Request, response: Response):
    session_id = request.cookies.get("session_id")  # получить текущий сессионный ключ
    if session_id not in session_storage:
        session_id = set_cookie(request, response)  # устанавливаем session_id (если ещё не установлено)
    user_key = session_storage[session_id]["login"]
    auth = session_storage[session_id]["auth"]
    if not auth:
        return RedirectResponse(url="http://127.0.0.1:8000/login/",
                                status_code=303)  # важно для post запросов ставить 303
    user = users_storage[user_key]
    response = templates.TemplateResponse(name="profile.html", context={"request": request, "user": user})
    set_cookie(request, response)  # устанавливаем session_id (если ещё не установлено)
    return response


@app.get("/logout/")
def logout(request: Request):
    session_id = request.cookies.get("session_id")  # получить текущий сессионный ключ
    if session_id in session_storage:
        session_storage[session_id]["auth"] = False
    return RedirectResponse(url="http://127.0.0.1:8000/login/",
                            status_code=303)  # важно для post запросов ставить 303


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
