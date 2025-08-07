from UTILS.APP_RUN import app_run
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Annotated
from fastapi import FastAPI, Body

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В pydantic модели можно добавлять примеры схем, для отображения в документации на docs и redoc, что может быть 
очень наглядно и удобно. Так можно покрывать все случаи возможных данных. Все примеры хорошо отображаются в swagger 
документации.
Для этого в конфигурации модели, нужно установить опцию json_schema_extra, и в ней в списке examples (название такое
так как это договоренность), можно набросать примеры вводных данных.
"""


class User(BaseModel):
    name: str
    age: float
    city: str | None = None

    model_config = ConfigDict(
        # использ. json_schema_extra для того, чтобы показать примеры
        json_schema_extra={
            "examples": [
                {"name": "Ivan", "age": 22, "city": "Tver"},
                {"name": "Mike", "age": 35, "city": "Moscow"},
                {"name": "Maria", "age": 29},
            ]
        }
    )


@app.post("/ex1/")
def ex1(user: User):
    return user


"""
ex2
Примеры схем для документаций, для вложенных моделей
"""


class Job(BaseModel):
    profession: str
    level: Literal["junior", "middle", "senior"] = "junior"


class UserFull(User):
    job: Job | None
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"name": "Petr", "age": 24, "city": "Moscow", "job": {"profession": "developer", "level": "junior"}},
                {"name": "Svetlana", "age": 32, "job": {"profession": "HR", "level": "senior"}},
                {"name": "Ivan", "age": 18},
            ],
        }
    )


@app.post("/ex2/")
def ex2(user: UserFull):
    return user


"""
ex3
Также примеры можно указывать непосредственно для самих полей модели, используя опцию examples
"""


class Account(BaseModel):
    login: str = Field(examples=["iv2025@", "MikePetrovich@@@"])  # указание примера для атрибута на прямую
    password: str = Field(examples=["f!2#Sd_@wD4"])
    password_repeat: str = Field(examples=["f!2#Sd_@wD4"])


@app.post("/ex3/")
def ex3(account: Account):
    return account


"""
ex4
ещё один способ указать пример модели, можно прямо в функции обработчике, но на мой взгляд это не совсем удобно, лучше
все таки использовать config в модели, либо на крайний случай отдельную переменную со словарём
"""


class File(BaseModel):
    name: str
    file_type: Literal["img", "song", "video"]
    size: float


@app.post("/ex4/")
def ex4(file: Annotated[File, Body(
    examples=[
        {"name": "cats.png", "file_type": "img", "size": 3},
        {"name": "zombie_Cranberries.mp3", "file_type": "song", "size": 24},
        {"name": "funny_cats.mp4", "file_type": "video", "size": 400},
    ])
]):
    return file


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
