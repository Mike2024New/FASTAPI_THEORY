from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В декораторах функций операций пути, можно гибко управлять выдаваемыми данными избегая отправки лишних ключей (что может
создать перегруженность у принимающего клиента). Например можно исключать не переданные ключи, или указывать в выдаче
только конкретные ключи.
Всего есть 5 таких режимов:
response_model_exclude_unset = True - исключение ключей которые не были переданы в модель.
response_model_exclude_default = True - ислкючение тех ключей значение которых равно значениям по умолчанию.
response_model_exclude_none = True - исключение ключей значение которых равно None
response_model_exclude = {"key1","key2"} эти ключи будут исключены из выдачи
response_model_include = {"key1","key2"} только заданные в множестве ключи будут возвращены
"""

"""
ex1 -> обзор параметра response_model_exclude_unset=True

Возвращаемым значениям можно также присваивать значения по умолчанию, а также можно отсечь ключи которые явно не указаны
в данных предназначенных для валидации модели (но при этом существующих в модели), для этого используется опция 
response_model_exclude_unset=True, и тогда не будут возвращаться поля которые не указаны явно.
Иными словами позволяет не включать значения по умолчанию в ответ пользователю которые он не указывал явно, но при этом
если он указал значение явно и оно совпадет со значением по умолчанию, то оно будет включено в ответ
"""


# во избежание дублирования кода, повторяющийся код спрятан в одну функцию
def get_user(user_id: str, users_base: dict[str, Any]):
    if user_id in users_base:
        return users_base[user_id]
    # если пользователя нет, то сообщаем клиенту об ошибке
    return JSONResponse(content={"msg": f"Пользователя с id '{user_id}' не существует"}, status_code=404)


class User(BaseModel):
    name: str
    age: int | None = 18
    city: str | None = None  # будет включено только если


# пример дата сета для включенного response_model_exclude_unset=True
users_base_for_ex1 = {
    "1": {"name": "Ivan", "age": 32, "city": "Moscow"},  # -> {"name": "Ivan", "age": 32, "city": "Moscow"}
    "2": {"name": "Maria", "age": 28},  # -> {"name": "Maria", "age": 28} # поле city не будет в ответе клиенту
    "3": {"name": "Mike", "age": 36, "city": None},  # -> {"name": "Mike", "age": 36, "city":None}
}


# http://127.0.0.1:8000/ex1/2/  -> {"name": "Maria", "age": 28}
@app.get("/ex1/{user_id}/", response_model=User, response_model_exclude_unset=True)
def ex1(user_id: str) -> JSONResponse | User:
    return get_user(user_id, users_base=users_base_for_ex1)


"""
ex2 ->
response_model_exclude_defaults=True, исключает из ответа все значения которые совпадают с теми значениями которые есть
по умолчанию, а также исключат из выдачи те ключи которые пользователь не вводил, но для них прописаны значения по 
умолчанию в модели.
"""

# пример дата сета для включенного response_model_exclude_defaults=True
users_base_for_ex2 = {
    "1": {"name": "Ivan", "age": 32, "city": "Moscow"},  # -> {"name": "Ivan", "age": 32, "city": "Moscow"}
    "2": {"name": "Maria", "age": 18},  # -> {"name": "Maria"} / так как age по умолчанию 18, а city=None
    "3": {"name": "Mike", "age": 36, "city": None},  # -> {"name": "Mike", "age": 36} так как city = None
}


# http://127.0.0.1:8000/ex2/2/  -> {"name": "Maria"}
@app.get("/ex2/{user_id}/", response_model=User, response_model_exclude_defaults=True)
def ex2(user_id: str):
    return get_user(user_id, users_base=users_base_for_ex2)


"""
ex3 ->
response_model_include=True нужен для того, чтобы из модели передавались только явно заданные ключи, а остальные 
отсекались из ответа.
"""

# пример дата сета для response_model_include={"age", "city"}
users_base_for_ex3 = {
    "1": {"name": "Ivan", "age": 32, "city": "Moscow"},  # {"age": 32, "city": "Moscow"} т.к. разрешены только age, city
    "2": {"name": "Maria", "age": 18},  # {"age": 18, "city": None} т.к. разрешены только age, city
    "3": {"name": "Mike", "age": 36, "city": None},  # {"age": 36, "city": None} т.к. разрешены только age, city
}


# http://127.0.0.1:8000/ex3/1/  -> {"age": 32, "city": "Moscow"}
@app.get("/ex3/{user_id}/", response_model=User, response_model_include={"age", "city"})
def ex3(user_id: str):
    return get_user(user_id, users_base=users_base_for_ex3)


# пример дата сета для response_model_exclude={"age", "city"}
users_base_for_ex4 = {
    "1": {"name": "Ivan", "age": 32, "city": "Moscow"},  # {"name": "Ivan"} т.к. поля age, city исключены из выдачи
    "2": {"name": "Maria", "age": 18},  # {"name": "Maria"} т.к. поля age, city исключены из выдачи
    "3": {"name": "Mike", "age": 36, "city": None},  # {"name": "Mike"} т.к. поля age, city исключены из выдачи
}


# http://127.0.0.1:8000/ex4/3/  -> {"name": "Ivan"}
@app.get("/ex4/{user_id}/", response_model=User, response_model_exclude={"age", "city"})
def ex4(user_id: str):
    return get_user(user_id, users_base=users_base_for_ex4)


"""
ex5->
response_model_exclude_none=True позволяет исключать из ответа те ключи, значения которых равны None (актуально только
в тех случаях когда в модели предусмотренны значения по умолчанию)
"""

# пример дата сета для response_model_exclude_none=True
users_base_for_ex5 = {
    "1": {"name": "Ivan", "age": 32, "city": "Moscow"},  # {"name": "Ivan", "age": 32, "city": "Moscow"} все указано
    "2": {"name": "Maria", "age": 18},  # {"name": "Maria", "age": 18} т.к. поле city не указано а значит None
    "3": {"name": "Mike", "age": None, "city": None},  # {"name": "Mike"} так как остальные поля None
}


# http://127.0.0.1:8000/ex5/3/  -> {"name": "Ivan"}
@app.get("/ex5/{user_id}/", response_model=User, response_model_exclude_none=True)
def ex5(user_id: str):
    return get_user(user_id, users_base=users_base_for_ex5)


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
