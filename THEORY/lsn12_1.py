from UTILS.APP_RUN import app_run
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict
from enum import Enum

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В примерах ниже показано как сделать обновление данных через Body запросы.
В PUT ex1 слое модель перезаписывается, то есть новые данные должны закрывать все поля модели User.
В PATH ex1 слое, поля обновляются частично, то есть новые данные могут содержать лишь часть атрибутов модели или вообще
не содержать не единого атрибута. Важно! при таком подходе нужно создать дополнительную модель поля у которой имеют 
значения по умолчанию (в данных примерах это UserUpdate).
Частичное обновление достигается за счёт model_dump(exclude_unset=True), входной модели обновления, что исключает
отсутствующие в входной модели ключи, а также за счёт метода модели copy, с включенным update=True, что вызовет 
обновление значений по переданным ключам. 
"""


class Tags(Enum):
    user = "user CRUD"


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


users_base = {
    "user_1": {"name": "Mike", "age": 32, "city": "Moscow"},
    "user_2": {"name": "Maria", "age": 29, "city": "Novgorod"},
    "user_3": {"name": "Dmitry", "age": 45, "city": "Tver"},
}


def get_user_key(user_id: int):
    user_key = f"user_{user_id}"
    if user_key not in users_base:
        raise HTTPException(status_code=404, detail=f"Пользователя с `{user_id}` не существует.")
    return user_key


@app.get("/ex1/{user_id}/", response_model=User, tags=[Tags.user])
async def ex1(user_id: int):
    user_key = get_user_key(user_id)
    return users_base[user_key]


"""
Реализация PUT в ex1 полностью перезаписывает данные в users_base (по аналогии с операцией write при чтении файла).
"""


@app.put("/ex1/{user_id}/", response_model=User, tags=[Tags.user], summary="Полное обновление пользователя")
async def ex1_update_user(user_id: int, user: User):
    user_key = get_user_key(user_id)
    user_data_json = jsonable_encoder(user)
    users_base[user_key] = user_data_json
    return user_data_json


"""
В запросе PATH, реализовано частичное обновление данных, только по переданным параметрам.
Важно! для того, чтобы можно было обновлять абсолютно каждый параметр отдельно, целесообразным будет создать ещё одну
модель, в которой у полей добавить поля со значением None, что позволит передавать лишь часть ключей, или вообще не
передавать ни одного ключа. А реализация в слое PATH ex1, гарантирует, что обновлены будут только переданные ключи. 
"""


@app.patch("/ex1/{user_id}", response_model=UserUpdate, tags=[Tags.user], summary="Частичное обновление пользователя")
async def ex1_update_path(user_id: int, user: UserUpdate):
    user_id = get_user_key(user_id)
    # 1. получение существующего пользователя из БД и создание модели
    current_user_json = users_base[user_id]  # промежуточный json
    current_user_model = UserUpdate(**current_user_json)  # модель текущего пользователя (взятого из БД)
    # 2. получение данных обновления введенных пользователем
    update_user_json = user.model_dump(exclude_unset=True)  # КЛЮЧЕВОЕ! здесь удаляются пустые ключи!
    update_user = current_user_model.copy(update=update_user_json)  # КЛЮЧЕВОЕ! модель существующ польз. обновляется
    # 3. Запись изменений в БД
    users_base[user_id] = jsonable_encoder(update_user)
    return update_user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
