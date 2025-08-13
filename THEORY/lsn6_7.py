from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В fastapi можно в response_model указывать возвращаемые типы, и так даже наиболее предподчтительно делать.
Например в ex1 возвращается простой список с целыми числами
"""


@app.get("/ex1/", response_model=list[int])
def ex1():
    return [1, 2, 3, 4, 5, 6]


"""
ex2 ->
также можно указывать словари, и если указаны модели или словари, то можно использовать инструменты управления
ключами, такие как response_model_include и другие (которые рассматривались в lsn6_3.py)
"""


@app.get("/ex2/", response_model=dict[str, int], response_model_include={"val1"})
def ex2():
    return {"val1": 123, "val2": 456, "val3": 789}


"""
ex3 ->
в fastapi можно отправлять списки моделей, для этого в response_model, нужно указать тип список, содержащий эти модели
response_model=list[Model]
"""


class User(BaseModel):
    name: str
    age: int
    city: str | None = None


users = [
    {"name": "Иван", "age": 32, "city": "Москва"},
    {"name": "Мария", "age": 29, "city": "Владимир"},
]


# http://127.0.0.1:8000/
@app.get("/ex3/", response_model=list[User])
def ex3():
    return users


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
