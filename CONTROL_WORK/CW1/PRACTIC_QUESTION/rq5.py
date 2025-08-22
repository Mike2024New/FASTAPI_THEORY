from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body, Path, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 6: Реализуй PUT эндпоинт с полной перезаписью пользователя.  -> user_update()
Вопрос 7: Реализуй PATCH эндпоинт с отдельной моделью и частичным обновлением.  -> user_update_partial()
"""

users_base = {
    "user_0": {"name": "Иван", "age": 32, "city": "Москва", "hobby": ["компьютерные игры", "теннис"]},
    "user_1": {"name": "Мария", "age": 28, "city": "Санкт-Петербург", "hobby": ["бильярд", "чтение книг"]},
    "user_2": {"name": "Анатолий", "age": 42, "city": "Новгород", "hobby": ["походы"]},
}


class User(BaseModel):  # базовая модель пользователя
    name: str
    age: int = Field(ge=18, le=100)
    city: str | None = None
    hobby: list[str] = Field(default_factory=list)
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"name": "Василий", "age": 25, "city": "Москва", "hobby": ["бег", "программирование"]},
    ]})


@app.get("/show_users/", response_model=dict[str, User])
def show_users():
    return users_base


@app.put("/user/{user_id}/", response_model=User, response_model_exclude_none=True,
         status_code=200, summary="полная замена данных о пользователе")
def user_update(user_id: Annotated[int, Path()], user: Annotated[User, Body()]):
    user_id = f"user_{user_id}"
    # если пользователь не существует то будет создан новый (но можно это перепределить, если нужно чтобы обновлялись только существующие)
    users_base[user_id] = user.model_dump()
    return user


class UserUpdate(User):  # модель для обновления
    name: str | None = None
    age: int | None = None


@app.patch("/user/{user_id}/", response_model=User, status_code=200, summary="Частичное обновление пользователя")
def user_update_partial(user_id: Annotated[int, Path()], user: Annotated[UserUpdate, Body()]):
    user_id = f"user_{user_id}"
    # если пользователя не существует, то вызывать ошибку
    if user_id not in users_base:
        raise HTTPException(status_code=404, detail=f"Пользователя с `{user_id}` не существует.")
    curent_user_model = User.model_validate(users_base[user_id])  # чтение нужного пользователя из БД
    user_update_json = user.model_dump(exclude_unset=True)  # передача только явно указанных ключей из входной модели
    user_update_model = curent_user_model.model_copy(update=user_update_json)  # копия модели с обновлением ключей
    users_base[user_id] = user_update_model  # запись обновленного пользователя в БД
    return user_update_model


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
