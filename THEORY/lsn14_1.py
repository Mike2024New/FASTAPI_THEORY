from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pydantic import BaseModel

"""
[ ! код здесь пока не рабочий это псевдокод для объяснения концепции ! ]
Здесь показан объект OAuth2PasswordBearer, который обеспечивает авторизацию токеном по логину (имени) и паролю.
(простейший сильно упрощенный разбор того как это работает под капотом показан в lsn14_1_2.py и lsn14_1_r).
Суть этого объекта в том, что создаётся его экземпляр OAuth2PasswordBearer с передачей tokenUrl - то есть url который 
будет отображен в документации (docs, redoc). 
Теперь эта di функция будет проверять, что в заголовках есть Authorisation, который содержит в себе токен в Bearer 
формате, например {"authorization": f"Bearer token"}, извлекает токен (отсекая Bearer), и возвращает его на сервер.
Если же токена нет, в заголовках или не корректный формат, то вызывает ошибку 401 (unauthorisation).
Развернутый пример этой логики показан в lsn14_1_2.py.
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    if token == "test":  # сильно упрощенная проверка, чтобы показать, что она вообще должна здесь быть
        return User(
            username=token + "fakedecoded", email="mk2021@yandex.ru", full_name="Mike Mk"
        )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)  # здесь должна быть логика проверки извлеченного токена
    return user


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/")
async def ex1(current_user: Annotated[str, Depends(get_current_user)]):
    # эта функция должна возвращать личные данные пользователя, но защищена. Под капотом используется зависимость
    # get_current_user, которая в свою очередь вызывает под капотом функцию получения токена oauth2_scheme, и если
    # токен не валидный то выбрасывает исключение HTTPException с ошибкой 401.
    return current_user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
