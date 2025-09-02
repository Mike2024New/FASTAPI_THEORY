import os
from UTILS.work_file import read_file
from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
from typing import Annotated

app = FastAPI()
app.name = "app"

"""
В этом примере показано как принять из html формы данные введенные пользователем.
В html форма без явного указания метода, отправляет данные в виде query параметров.
Ниже "/" выдаёт клиенту html страницу, за тем, клиент вводит данные и формируется url с query параметрами, который 
обрабатывает ex1.
------------------------------
Для краткости кода и примеров, файлы с html хранится в отдельной папке в файлах, а код их загрузки вынесен в отдельную
утилиту.
"""


class User(BaseModel):
    name: str
    age: int
    city: str | None = None

    @field_validator("city", mode="after")
    @classmethod
    def empty_str_to_none(cls, value):
        """этот валидатор добавлен сюда просто для преобразования пустого поля в None, так как из формы приходит пустая
        строка, если ни чего не введено"""
        if isinstance(value, str) and value == "":
            value = None
        return value


@app.get("/")
def home():
    """"""
    content = read_file(file_path=os.path.join(os.getcwd(), 'HTML', 'register.html'))
    return HTMLResponse(content=content, status_code=200)


@app.get("/ex1/", response_model=User, response_model_exclude_none=True)
def ex1(user: Annotated[User, Query()]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
