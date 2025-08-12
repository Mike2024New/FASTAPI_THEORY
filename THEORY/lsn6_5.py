from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
пример использования моделей, альтернативный способ записи моделей (относительно примера lsn6_4.py), отличие в том, что
используется наследование, за счёт чего в моделях не нужно дублировать поля. 
Используется главная родительская модель UserBase, где содержатся основные поля которые видны всем моделям, а в дочерних
моделях прописаных уже опциональные специфичные под них поля.
В остальном логика остается такой же как в lsn6_4.py, модели обслуживают цепочку:
входные данные -> сохранение данных -> выходные данные
"""


# базовая модель, она содержит поля которые не страшно если уйдут с сервера
class UserBase(BaseModel):
    username: Annotated[str, Field(example="Иван")]
    full_name: Annotated[str | None, Field(example="Иван Петрович")] = None
    email: Annotated[EmailStr, Field(example="user@example.com")]


# входные данные пользователя, все то, что определено в UserBase, и плюс пароль
class UserInput(UserBase):
    password: Annotated[str, Field(min_length=8, example="q#*_FcD1@")]


# вообще можно отправить пользователю и UserBase, но такой подход выглядит более структурированным
class UserOut(UserBase):
    pass


# слой сохранения данных пользователя, все то, что определено в UserBase, и плюс хэшированный пароль
class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    """
    псевдо хеширование пароля (пароли в БД ни когда не хранятся в чистом виде), если пользователь потерял пароль то
    старый пароль перезаписывается новым.
    :param raw_password: исходный пароль
    :return: псевдо хэшированный пароль
    ВНИМАНИЕ!!! Эта функция чисто для демонстрации, в реальности естественно в таком виде пароли не сохраняются в БД,
    здесь эта функция просто для примера блока псевдогенерации пароля, в реале нужно хешировать пароль с помощью
    библиотек (bcrypt/argon2 или других)
    """
    return "supersecret" + raw_password


def fake_save_user(user_in: UserInput):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_data = user_in.model_dump()
    user_in_db = UserInDB(**user_in_data, hashed_password=hashed_password)
    print(f"Пользователь '{user_in_db.username}', email '{user_in_db.email}' сохранён в БД...")
    return user_in_db


@app.post("/ex1/", response_model=UserOut)
def ex1(user_input: UserInput):
    fake_save_user(user_in=user_input)
    return user_input  # преобразуется в BaseUser, так как она указана в response_model


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
