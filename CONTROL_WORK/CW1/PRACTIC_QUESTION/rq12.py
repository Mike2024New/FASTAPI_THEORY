from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import Literal

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 15: Используй response_model_exclude_none и response_model_include для кастомизации ответов.
"""


class User(BaseModel):
    name: str
    age: int
    city: str | None = None
    role: Literal["user", "admin"] = "user"
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"name": "Пётр", "age": 32, "city": None},
        {"name": "Василий", "age": 44, "city": "Москва"},
    ]})


@app.post("/ex1/", response_model=User,
          response_model_exclude_none=True,
          response_model_include={"name", "age", "city"}
          )
def ex1(user: User):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
