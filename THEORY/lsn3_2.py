from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
ex1
Несколько моделей Body, раздельные тела запроса.
В случае если тел запроса несколько, то каждое тело запроса нужно передать по конкретному ключу, например для ex1, тело
запроса будет выглядеть так:
{
  "user": {
    "name": "string",
    "age": 0
  },
  "job": {
    "profession": "string",
    "salary": 0
  }
}
"""


class User(BaseModel):
    name: str
    age: int


class Job(BaseModel):
    profession: str
    salary: float


# для выполнения этого запроса нужно перейти на docs, либо выполнить запрос через requests с передачей данных
# Эндпоинт ожидает два ключа (параметра) с значениями структурами определенными в моделях User и Job
@app.post("/ex1/")
async def ex1(
        user: User,
        job: Job | None = None
):
    return {"user": user, "job": job}


"""
ex2
С помощью объекта body можно явно указывать, что параметры являются телом запроса (Body). Это может быть полезно для
передачи доплнительных данных (в том числе и чувствительных данных)
Ожидаемая в ex2 структура:
{
  "par1": "string",
  "par2": "string"
}
"""


# эта функция ждет 2 body параметра
@app.post("/ex2/")
async def ex2(par1: Annotated[str, Body()], par2: Annotated[str, Body()]):
    return {"par1": par1, "par2": par2}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
