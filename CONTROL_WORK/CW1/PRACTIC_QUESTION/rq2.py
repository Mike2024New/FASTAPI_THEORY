from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body
from pydantic import BaseModel, ConfigDict
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 3: Напиши POST эндпоинт с Pydantic моделью, исключающей приватные поля из ответа.
"""


class UserBase(BaseModel):  # базовая модель (публичная модель)
    login: str
    name: str
    city: str | None = None


class UserInput(UserBase):  # модель с приватными полями
    password: str
    password_repeat: str
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"login": "iv25", "name": "Иван", "password": "1234", "password_repeat": "1234"}
    ]})


# явно указано, что возращена будет публичная модель без приватных полей
@app.post("/ex1/", response_model=UserBase, response_model_exclude_unset=True)
def ex1(user: Annotated[UserInput, Body()]):  # на вход поступает модель которая включает приватные поля
    ...  # логика работы с поступившей моделью
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
