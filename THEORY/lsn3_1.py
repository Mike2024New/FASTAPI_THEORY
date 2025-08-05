# uvicorn THEORY.lsn3_1:app --reload
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Literal, Optional

app = FastAPI()

"""
body параметры (тело запроса) - данные которые отправляются клиентом в закрытом режиме в виде json (как правило), именно
через них можно передавать чувствительные данные, так как они не хранятся в логах.
body параметры передаются через POST, PUT, DELETE запросы (в теории можно и через GET, но так делать настоятельно не 
рекомендуется).
Для формирования структуры тела запроса используются pydantic модели, в которых прописаны типы полей, значения по 
умолчанию и другие метаатрибуты.
--------------------------------------------------------------------------------------------------------------------
Для работы с примерами из этого урока рекомендуется перейти на http://127.0.0.1:8000/docs для интерактивной отправки
запросов содержащих тело запроса body параметры.
"""


# pydantic модель описывающая входной тип данных
class User(BaseModel):
    name: str
    age: int
    city: Optional[str] = None  # необязательный параметр
    role: Literal["user", "admin", "super"] = "user"  # необязательный атрибут модели, так как он установлен по умолчан


@app.post("/users/")
async def ex1(user: User):  # теперь fastapi точно знает, что это данные на базе модели User
    # очень удобно работать с pydantic моделями, потому, что можно использовать точечную нотацию для автодополнения IDE
    return f"Ваше имя {user.name.capitalize()}, вам {user.age} лет, город {user.city}, права {user.role}"


"""
ex2
Комбинация body тела запроса и параметров пути path.
fastapi видит, что user_id параметр относящийся к url, то есть path параметр который объявлен в {}.
А модель user, остается такой же как и объявлено в User.
В этом примере имитируется обновление пользователя в воображаемой БД.
"""


@app.put("/users/{user_id}/")
async def ex2(user: User, user_id: int):
    return {"msg": f"Изменения пользователя user_id: `{user_id}` применены", "parametrs": user}


"""
ex3
комбинация параметров path + query +  body
fastapi без проблем различает варианты параметров по правилам:
path параметры обозначены в url в скобках {}
query параметры объявлены в функции контроллере но отсутствуют в url
body параметры базируются на Pydantic модели и представляют собой json структуру
"""


@app.put("/lib/users/{user_id}/")
async def ex3(user: User, user_id: int, notes: Optional[str] = None):
    result = {
        "msg": f"Изменения пользователя user_id: `{user_id}` применены",
        "parametrs": user
    }
    if notes:
        result["notes"] = notes
    return result


if __name__ == '__main__':
    uvicorn.run(app="lsn3_1:app", reload=True)
