from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

app = FastAPI()
app.name = "app"

"""
Иногда нужно сделать так, чтобы данные из модели, были преобразованы в поддерживаемый json тип -> словарь, это может 
быть необходимо для записи данных например в json файл, так как json файл например ни чего не знает про pydantic модель.
Для этого используется jsonable_encoder, который переводит данные из модели в словарь. Под капотом по сути используется
метод model_dump (метод pydantic модели)
"""


class User(BaseModel):
    name: str
    age: int
    city: str | None = None
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {"name": "Mike", "age": 32, "city": "Moscow"}
        ]
    })


users_base = {}


@app.put("/ex1/{user_id}/")
def ex1(user_id: int, user: User):
    json_data = jsonable_encoder(user)  # перевод из модели в json
    json_data_dict = user.model_dump()  # в данном случае это равносильно jsonable_encoder
    print(f"Исходный формат на базе модели:{user}")
    print(f"Формат после применения кодировки:{json_data}")
    print(f"Формат после применения model_dump:{json_data_dict}")
    users_base[user_id] = json_data


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
