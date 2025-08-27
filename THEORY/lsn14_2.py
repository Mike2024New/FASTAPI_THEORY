from typing import Annotated

from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

"""
Базовый принцип авторизации по токену по протоколу OAuth2
(см. также lsn14_2_r -> там показано как происходит авторизация на клиенте)
----------------------------------------------------------------------------
Как работает код ниже:
При авторизации (переходе на url "/token"):
1.При переходе на url "/token", пользователь отправляет "username", "password", то есть данные авторизации.
2.На эндпоинте "/token", выполняется коннект с БД, чтобы проверить, что такой пользователь реально существует, что 
введенный пароль после хеширования, совпадает с хешированным паролем в БД.
3.В случае успеха, пользователю в header устанавливаются заголовки {"acces_token": ..., "token_type": "bearer"} по 
которым он может заходить на маршруты и при этом ему не нужно будет вводить учётные данные заново.

При получении своего профиля (переход по url "/ex1/"):
1. Вызывается зависимость (di функция) get_current_user которая под капотом через di использует OAuth2, который 
проверяет что: 1.в заголовках содержится поле "Authorization", извлекает из него токен, и передаёт его уже в эту 
функцию (get_current_user) для выполнения проверки этого токена на корректность и если всё ок, то подключившийся
получает данные своего профиля, если нет, то ошибка.
---------------------------------------------------------------------------------------------------------
* В fake_users_db хранятся пользователи (то есть они уже заранее созданы, зарегистрированы).
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# псевдо БД
fake_users_db = {
    "Mike": {
        "username": "Mike",
        "full_name": "Mike M",
        "email": "mk2021@yandex.ru",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "Ivan": {
        "username": "Ivan",
        "full_name": "Ivan I",
        "email": "iv2018@yandex.ru",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
}


# псевдо функция хеширования пароля (не в коем случае не хранить пароли в чистом виде)
def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):  # псевдо CRUD контоллер получающий пользователя из БД
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def fake_decode_token(token):  # в этой функции токен должен проверяться (здесь для упрощения проверка опущена)
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # вот в этой точке в qauth2_scheme как раз и отрабатывает, он проверяет есть ли заголовок authorization, содержит
    # ли он в себе запись формата "Bearer token", извлекает этот токен и передаёт сюда, это и есть весь процесс который
    # находится под капотом у quauth2_scheme, дальше логика обработки токена находится уже на сервере и реализуется
    # разработчиками самостоятельно.
    user = fake_decode_token(token)  # вызов функции которая по токену получает пользователя (если он есть)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не верные учётные данные для проверки...",
            headers={"WWW-Authenticate": "Bearer"}  # этот заголовок требуется OAuth2 спецификацией
        )
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:  # проверка, что у пользователя статус активный (просто для примера расширенной логики)
        raise HTTPException(status_code=400, detail="пользователь не активен")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Получение токена. Внимание токена к уже существующему пользователю"""
    # В form_data полученные данные из формы (multipart/form-data) -> поля должны строго называться username и password
    user_dict = fake_users_db.get(form_data.username)  # получение пользователя из псевдо БД
    if not user_dict:  # пользователь не найден? ошибка
        raise HTTPException(status_code=400, detail="не корректное имя пользователя или пароль")
    user = UserInDB(**user_dict)  # создание модели пользователя (для удобства работы нежели с обычным словарем)
    hashed_password = fake_hash_password(form_data.password)  # получение пароля из формы и его хеширование для сравнен
    if not hashed_password == user.hashed_password:  # пароли не совпадают? ошибка
        raise HTTPException(status_code=400, detail="не корректное имя пользователя или пароль")
    # здесь очень сильное упрощение, в реале естественно username не может быть токеном, токен это более сложная запись
    # и вообще для созадния токенов есть отдельный алгоритм (будет рассмотрен в уроках дальше)
    return {"acces_token": user.username, "token_type": "bearer"}


"http://127.0.0.1:8000/ex1/"


@app.get("/ex1/")
async def ex1(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
