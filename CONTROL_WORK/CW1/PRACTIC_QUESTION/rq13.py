from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body
from typing import Annotated
from pydantic import BaseModel, ConfigDict

"""
Вопрос 16: Создай вложенную Pydantic модель, обслуживаемую эндпоинтом.
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"


class Job(BaseModel):
    profession: str
    salary: float


class User(BaseModel):
    name: str
    age: int
    city: str | None = None
    job: Job | None = None
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"name": "Элеонора", "age": 18, "city": "Москва", "job": {"profession": "hr manager", "salary": "150000"}},
        {"name": "Станислав", "age": 18, "job": {"profession": "python developer", "salary": "120000"}},
        {"name": "Мария", "age": 18, "city": "Екатеринбург"},
    ]})


@app.post("/ex1/", response_model=User, response_model_exclude_none=True)
def ex1(user: Annotated[User, Body()]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
