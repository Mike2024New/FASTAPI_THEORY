from pydantic import BaseModel, ConfigDict

"""
Реализация частичного обновления полей модели на pydantic (как это работает под капотом у fastapi)
В основе лежит все тот же принцип:
1. Нужно создать модель с ключами со значениями None по умолчанию (чтобы можно было передавать лишь часть параметров)
2. Нужно отсеять отсутствующие ключи в входных данных модели model_dump(exclude_unset=True).
3. Сделать копию с обновлением модели по существующим ключам с помощью update=...
"""

users_base = {
    "user_1": {"name": "Mike", "age": 32, "city": "Moscow"},
    "user_2": {"name": "Maria", "age": 29, "city": "Novgorod"},
    "user_3": {"name": "Dmitry", "age": 45, "city": "Tver"},
}


class User(BaseModel):
    name: str
    age: int
    city: str | None = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {"name": "Mike", "age": 32, "city": "Moscow"}
        ]
    })


class UserUpdate(User):
    name: str | None = None
    age: int | None = None


if __name__ == '__main__':
    print(users_base["user_1"])
    update_data = UserUpdate(age=35)  # входные данные на обновление
    current_user_json = users_base["user_1"]  # текущие данные пользователя
    current_user_model = UserUpdate(**current_user_json)  # текущая модель пользователя
    update_data_json = update_data.model_dump(exclude_unset=True)  # исключить пустые поля
    update_data_model = current_user_model.model_copy(update=update_data_json)  # обновить модель текущего пользователя
    users_base["user_1"] = update_data_model.model_dump()
    print(users_base["user_1"])
