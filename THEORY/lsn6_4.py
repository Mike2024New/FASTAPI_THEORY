from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В примере ниже показано, как несколько моделей могут обслуживать одну операцию пути, например цепочку:
1.пользователь авторизовывается -> 2.данные сохраняются на сервере  -> 3.пользователь получает обратную связь об успехе
За каждую из этих операций отвечает отдельная модель, в примере ниже:
1.пользователь авторизовывается - за это отвечает модель UserInput
2.данные сохраняются на сервере - за это отвечает модель UserInDB, например пароль должен быть в хешированном виде и в 
этой модели есть специальное поле для этого. UserInDB не отправляется клиенту и ни как с ним не взаимодействует, это 
чисто серверная история. (нельзя чтобы хешированный пароль попал во вне сервера).
3.пользователь получает обратную связь об успехе - за это отвечает модель UserOutput, которая не содержит в себе 
чувствительные данные.
------------------------------------
По сути модель UserInDB это промежуточная модель, которая отвечает за действие внутри серверной логики.
------------------------------------

"""


class UserInput(BaseModel):  # эта модель принимает данные от пользователя через post метод | иммитация регистрации
    username: Annotated[str, Field(example="Иван")]
    password: Annotated[str, Field(min_length=8, example="q#*_FcD1@")]
    email: Annotated[EmailStr, Field(example="user@example.com")]
    full_name: Annotated[str | None, Field(example="Иван Петрович")] = None


class UserOutput(BaseModel):  # выходная модель которая вернется пользователю | иммитация обратной связи, об успехе
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):  # это промежуточная модель, которая записывает данные в БД (пароль захеширован hash)
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


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
    # в Fastapi документации рекомендуется так:
    # user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    # Но для dict() в pydantic V2 выдается depricated, и возможно лучше использовать model_dump()
    user_in_data = user_in.model_dump()  # в этой точке модель user_in распаковывается dict, для передачи в модель UserInDB
    # ** даёт возможность частичного проброса ключей через именованные параметры, а остальное распакуется из словаря
    user_in_db = UserInDB(**user_in_data, hashed_password=hashed_password)
    print(f"Пользователь '{user_in_db.username}', email '{user_in_db.email}' сохранён в БД...")
    return user_in_db


# использование response_model=UserOutput гарантирует, что данные из модели UserIn будут преобразованы в соотвествии с
# атрибутами задекларированными в UserOutput
@app.post("/user/", response_model=UserOutput)
async def create_user(user_in: UserInput):
    user_saved = fake_save_user(user_in)  # вызов функции которая, сохраняет пользователя в БД
    return user_saved


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
