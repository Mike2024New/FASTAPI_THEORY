from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 8: Напиши функцию сериализации модели через jsonable_encoder и обратного создания.
"""


class User(BaseModel):  # базовая модель пользователя
    name: str
    age: int = Field(ge=18, le=100)
    city: str | None = None
    hobby: list[str] = Field(default_factory=list)
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"name": "Василий", "age": 25, "city": "Москва", "hobby": ["бег", "программирование"]},
    ]})


@app.post("/ex1/", response_model=User, status_code=200, summary="сериализация/десериализация модели")
def ex1(user: Annotated[User, Body()]):
    # jsonable_encoder дублируется с model_dump, а в Pydantic модели в конфигурации можно задать свой способ кодировки
    data_jsonable = jsonable_encoder(user)  # входная модель преобразована в json поддерживающие данные
    print(data_jsonable)
    model_from_data = User.model_validate(data_jsonable)  # обратная конвертация json данных в модель
    return model_from_data


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
