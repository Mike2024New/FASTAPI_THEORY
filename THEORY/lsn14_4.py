from datetime import timedelta
from typing import Annotated
from pydantic import BaseModel
from UTILS.APP_RUN import app_run
from UTILS.JWT_MANAGER import JWTManager
from UTILS.HASH_MANAGER import HashManager
from UTILS.work_file import WorkFile
from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

"""
Пример того как можно автоматизировать авторизацию по токенам через сервер.
Идея такая, что токен устанавливается в куках пользователя сервером. А значит фронтенд полностью разгружен.
Особо важно выставить параметры защиты:
secure=True, # включить при использовании https
httponly=True,  # токен передаётся только по HTTP, доступ из JS запрещён
samesite="lax"  # защита от csrf межсетевых запросов
---------------------------------------------------------------------------------------------------------
Опасность остается только в том плане если клиент даёт свой ПК с входом в учетные записи чужим людям.
(то есть человек сам передаёт данные злоумышленникам)
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

SECRET_FOR_TOKEN = "3737d10b4d4a5360edac60e737ef94f26d6b97b9b902ef5c0794a48cd24fce1a"
SECRET_FOR_PSW = "7e3606348ced78ce090651ed0377188de376bd79029acb4dd8cb7003ce487898"
jwt_manager = JWTManager(secret_key=SECRET_FOR_TOKEN, token_action=timedelta(minutes=30))
hash_manager = HashManager(secret_key=SECRET_FOR_PSW)
file_manager = WorkFile(file_path="lsn14_4_STOP_TOKEN.txt")  # для работы с токенами
oauth2_scheme = OAuth2PasswordBearer("login")

# псевдо БД:
fake_db_users = {
    "ivan25@": {  # чтобы пройти авторизацию здесь для примера, ввести: username: 'ivan25@', passowrd: 'secret'
        "username": "ivan25@",
        "first_name": "Иван",
        "last_name": "Иванов",
        "hashed_password": "$2b$12$NZaRuO5OEnzNHG11zmvSmusxyfy2NDJ7oR79UnFuXXr0J5lSiVuOO",
    }
}


# модель пользователя из БД
class User(BaseModel):
    username: str  # это логин
    first_name: str | None = None
    last_name: str | None = None


# расширенная модель пользователя с хешированным паролем
class UserInDB(User):
    hashed_password: str


def get_user(db, username: str) -> UserInDB | None:
    """
    получение пользователя из БД, возвращает его запись если пользователь найден или None если нет
    Метод не защищён! Для его защиты требуется отдельная логика, модель на выходе выдаётся с хешем пароля, при запросе
    на прямую нужно учитывать это, чтобы не отправить хеш пользователю!
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# эта функция защита для маршрутов, чтобы не авторизованные пользователи не могли попасть на недоступные страницы
async def verify_token(access_token: Annotated[str, Cookie()]):
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ошибка токена, нужна повторная авторизация"
    )
    # проверить, что токен не содержится в стоп листе (не отозван)
    if file_manager.is_find_string_in_file(string=access_token):
        raise auth_error
    try:
        jwt_manager.verify_token(token_in=access_token)
        payload = jwt_manager.get_payload_from_token_verify(token_in=access_token)
        print(payload)
    except Exception:
        print("Токен не валиден...")  # логирование
        raise auth_error
    print("Токен валиден...")


# http://127.0.0.1:8000/
@app.get("/")
async def home():
    return {"msg": "Добро пожаловать на главную страницу. Перейдите и авторизуйтесь на /login/"}


@app.get("/ex2/", dependencies=[Depends(verify_token)])
async def test_verify():
    return {"msg": "Выдаю контент, доступный авторизованным пользователям"}


@app.get("/logout/")
async def logout_user(access_token: Annotated[str, Cookie()]):
    file_manager.rec_file(data=access_token, mode="a", new_row=True)  # внести токен в stop лист
    return {"msg": "Вы вышли из системы"}


async def autenticate_user(db, username, password) -> User | bool:
    """механизм аутентификации пользователя, он нужен только во время авторизации пользователя"""
    user = get_user(db=db, username=username)
    if user is None:
        return False
    if not hash_manager.verify_password(password_checker=password, password_original=user.hashed_password):
        return False
    user = User.model_validate(user.model_dump(exclude={"hashed_password"}))
    return user


@app.post("/login/")
async def login_user(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await autenticate_user(db=fake_db_users, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не корректный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    data = {"sub": user.username}
    token = jwt_manager.create_token(data=data)
    response.set_cookie(
        key="access_token",
        value=token,
        # secure=True, # включить при использовании https
        httponly=True,  # токен передаётся только по HTTP, доступ из JS запрещён
        samesite="lax"  # защита от csrf межсетевых запросов
    )
    return {"msg": "токен установлен"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
