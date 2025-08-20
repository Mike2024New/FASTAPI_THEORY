from UTILS.APP_RUN import app_run
from fastapi import FastAPI, status
from typing import Literal
from pydantic import BaseModel, ConfigDict
from enum import Enum

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Конфигурация операций пути.
В декораторах энпоинтов можно передавать дополнительные параметры, такие как:
-статус коды (если маршрут обработан безошибочно) -> (ex1).
Ниже приведены параметры которые влияют на качество документации приложения в целом и маршрутов в частности:
-Теги обозначения которые используются для группировки маршрутов в документации, что удобнее для навигации -> (ex2).
-summary - название маршрута в документации (вместо названия функции) -> (ex3)
-description - описание функции (альтернатива docstring) -> (ex3)
-Использование markdown в docstring функции который красиво отобразится в документации -> (ex4).
-описание возвращаемых данных response_description -> (ex5).
-depricated устаревание маршрута и отображение информации об этом в документации -> (ex6).
-----------------------------------------------------------------------
Здесь не акцентируется внимание на логике работы маршрутов, их не обязательно запускать. Основная задача данных примеров
отображение маршрутов в документации.
"""


class User(BaseModel):
    name: str
    age: int
    city: str | None = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {"name": "Mike", "age": 32, "city": "Moscow"}
        ]
    })


"""
ex1 -> указание статус кода через enumerate fastapi (status)
"""


@app.post("/ex1/", response_model=User, status_code=status.HTTP_201_CREATED)
def ex1(user: User):
    return user


"""
ex2 -> группировка маршрутов по тегам, все виды запросов к /ex2/ будут собраны в одной вкладке в документации на docs 
и redoc. Для тегов очень удобно использовать Enum перечисления и константы, чтобы не прописывать каждый раз строку в 
одном эндпоинте и можно было централизовано редактировать их названия.
"""


class Tags(Enum):
    user = "user"  # тег для маршруторв


@app.get("/ex2/", response_model=User, tags=[Tags.user])  # тег это как правило одна строка в списке
async def ex2():
    ...  # внутренняя логика функции маршрута
    return {"name": "Mike", "age": 32, "city": "Moscow"}


@app.post("/ex2/", response_model=User, tags=[Tags.user], status_code=status.HTTP_201_CREATED)
async def ex2_new_user(user: User):
    ...  # внутренняя логика функции маршрута
    return user


@app.put("/ex2/", response_model=User, tags=[Tags.user], status_code=status.HTTP_200_OK)
async def ex2_update_user(user: User):
    ...  # внутренняя логика функции маршрута
    return user


"""
Дополнительная метаинформация
summary - этот текст отобразится на вкладке в redoc и docs (вместо стандартного названия функции обработчика)
description - описание того, что делает этот маршрут (также можно просто прописать docstring у функции)
"""


@app.post(
    "/ex3/",
    response_model=User,
    summary="создание пользователя",  # эта информация будет показана на вкладке документации
    description="Создание пользователя согласно схеме показанной в примере"  # это будет описание того, что делает метод
)
async def ex3(user: User):
    ...  # внутренняя логика функции маршрута
    return user


"""
ex4 -> 
Использование markdown (специальной разметки) в описании функции, так как описания функции могут быть очень большими, то
можно добавлять к функции docstring и он корректно отобразится в документации с учетом markdown разметки.
"""


@app.post(
    "/ex4/",
    response_model=User,
    summary="создание пользователя"
)
async def ex4(user: User, role: Literal["admin", "user"] = "user"):
    """
    Создание пользователя:

    - **user** данные в виде {"name": "Mike", "age": 32, "city": "Moscow"}
    - **role** роль пользователя, admin или user
    """
    ...  # внутренняя логика функции маршрута
    return user, role


"""
ex5 -> описание возвращаемых данных response_description
"""


@app.post("/ex5/", response_model=User, response_description="возвращает пользователя по заданной модели")
async def ex5(user: User):
    ...  # внутренняя логика функции маршрута
    return user


"""
ex6 -> 
обозначение того, что метод устарел, в документации появится предупреждение об этом в виде перечеркнутого описания 
маршрута и надписи "deprecated". Это нужно для устаревших маршрутов.
"""


@app.post("/ex6/", deprecated=True)
async def ex6(user: User):
    ...  # внутренняя логика функции маршрута
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
