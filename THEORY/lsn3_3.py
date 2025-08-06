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
Если модель объявлена всего 1, то есть 1 параметр тела запроса, то по умолчанию он передаётся без ключа, например
ex1 ждет данные в виде:
{
  "name": "string",
  "age": 0
}
"""


class User(BaseModel):
    name: str
    age: int


@app.post("/ex1/")
def ex1(user: User):
    return user


"""
ex2
Но может возникнуть ситуация когда нужно передавать даже единственное тело запроса по ключу, для этого
предусмотрен параметр embed=True в Body, теперь ex2 ожидает на вход:
{
  "user": {
    "name": "string",
    "age": 0
  }
}
"""


@app.post("/ex2/")
def ex2(user: Annotated[User, Body(embed=True)]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
