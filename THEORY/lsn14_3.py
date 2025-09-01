from typing import Annotated
from UTILS.APP_RUN import app_run
from UTILS.HASH_MANAGER import HashManager
from UTILS.JWT_MANAGER import JWTManager
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

"""
Пример полного взаимодействия пользователя и сервера с помощью токена, теперь пользователь авторизуется, получает токен
и на его основании взаимодействует с сервером.
В lsn14_3_r.py показан упрощенный клиент который подключается к этому api
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

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


# Инициализация настроек и модулей безопасности:
SECRET_KEY = "7e3606348ced78ce090651ed0377188de376bd79029acb4dd8cb7003ce487898"  # ! НЕ ХРАНИТЬ СЕКРЕТНЫЕ КЛЮЧИ В КОДЕ !
jwt_manager = JWTManager(secret_key=SECRET_KEY, token_action=timedelta(seconds=5), algoritm="HS256")  # работа с JWT
hash_manager = HashManager(secret_key=SECRET_KEY)  # хеширование и сравнение хешей паролей
oauth2_scheme = OAuth2PasswordBearer("login")  # схема авторизации пользователя


def get_user(db, username: str) -> UserInDB | None:
    """
    получение пользователя из БД, возвращает его запись если пользователь найден или None если нет
    Метод не защищён! Для его защиты требуется отдельная логика, модель на выходе выдаётся с хешем пароля, при запросе
    на прямую нужно учитывать это, чтобы не отправить хеш пользователю!
    """
    if username in db:
        user_dict = db[username]
        print(user_dict)
        return UserInDB(**user_dict)


def autenticate_user(db, username, password) -> User | bool:
    """
    проверка, пользователя, что он существует в БД, что введенный пароль и хеш в БД совпадают и если все верно, то
    выдача пользователя
    """
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not hash_manager.verify_password(password_checker=password, password_original=user.hashed_password):
        return False
    # пароли проверены, больше расширенная модель не нужнв
    user = User.model_validate(user.model_dump(exclude={"hashed_password"}))  # явн исключ хеша из вых модели
    return user


# этот метод создаёт токен для пользователя по адресу https://127.0.0.1/login/
@app.post("/login")
async def login_for_acces_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    """
    Этот метод возвращает токен и тип токена ["access_token","type_token"] пользователю
    :param form_data: данные из форм (в html форме поля должны называться username, и password)
    :return: сгенерированный ключ токен
    ------------------------------------------------------------------------------------------------
    Внимание! Этот метод он ни чего не устанавливает в браузер пользователя. Он просто генерит jwt токен и отправляет
    его пользователю. А далее пользователь уже сам сохраняет jwt токен и подвешивает его к последующим запросам (обычно
    это реализует js на фронтенде который устанавливает токен в LocalStorage или другое защищенное хранилище). Если
    токен устарел, то на сервер отправляется запрос об обновлении токена.
    ------------------------------------------------------------------------------------------------
    OAuth2PasswordREquestForm служит лишь для проверки, что в полях формы содержатся ключи username, password, client_id,
    client_secret и другие, и является по сути моделью этих данных на этом его назначение заканчивается. Такой же подход
    можно реализовать и на своих моделях
    """
    # шаг1: проверка что пользователь есть в БД и логин и пароли валидны
    user = autenticate_user(db=fake_db_users, username=form_data.username, password=form_data.password)
    if not user:  # проверка не пройдена? Возбудить исключение
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не корректный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    data = {"sub": user.username}  # извлечение имени пользователя из модели
    token = jwt_manager.create_token(data=data, token_action=timedelta())
    return {"access_token": token, "type_token": "bearer"}  # вернуть клиенту данные о токене


async def get_current_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    """Данный метод обеспечивает проверку валидности токена"""
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не верные данные для входа",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_manager.get_payload_from_token_verify(token_in=token)
        username = payload.get("sub")
        if username is None:
            raise auth_error
    except Exception as err:  # проброс исключения наружу
        print(f"Ошибка чтения jwt токена: {err}")
        raise auth_error
    user = get_user(db=fake_db_users, username=username)
    if user is None:
        raise auth_error


async def get_user_public(username: str):
    """так как несколько функций используют этот код, вынесен в отдельный модуль и подключается как зависимость"""
    user_in_db = get_user(db=fake_db_users, username=username)  # получение пользователя из get_user
    if user_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пользователь с логином `{username}` не существует")
    user = User.model_validate(user_in_db.model_dump(exclude={"hashed_password"}))  # явн исключ хеша из вых модели
    return user


"""
ex1 ->
ex2 ->
Функции маршрутов /ex1/{username}/ и /ex2/{username}/ идентичны, они обе берут пользователя из БД через зависимость
get_user_public, которая проводит явное преобразование модели и выброс ошибки если пользователя не существует.
Но ex1 не защищена токеном и любой даже не авторизованный пользователь может получить эти данные. А функция ex2 защищена
с помощью функции зависимости (side effect) get_current_user_from_token, которая с помощью OAuth2 запросит заголовок с 
токеном из headers, выполнит его проверку и только лишь потом даст зеленый свет на дальнейшую работу функции операции
пути или остановит действие функции выбросив 401 если токен отсутствует или не валиден.
"""


# http://127.0.0.1:8000/ex2/ivan25@/
# этот маршрут уже защищен, сюда без ввода токена не попасть, иначе будет ошибка 404
# в Depends декоратора функции операции пути, подключена функция проверки токена
@app.get("/ex2/{username}/", dependencies=[Depends(get_current_user_from_token)], response_model=User)
async def ex2(user: Annotated[get_user_public, Depends()]):
    return user


# http://127.0.0.1:8000/ex1/ivan25@/
# пример получения данных напрямую без защиты (метод исключительно демонстрационно-отладочный для get_user)
@app.get("/ex1/{username}/", response_model=User)
async def ex1(user: Annotated[get_user_public, Depends()]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
