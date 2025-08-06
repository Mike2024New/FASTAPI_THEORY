from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
У тела запроса, можно также объявлять поля модели, через Field, устанавливая различные условия валидации, например
максимальная и минимальная длины строки, диапазон чисел, и так далее.
Также можно прикреплять метаинформацию title, description, можно задавать alias и так далее.
==========================================================================================
Если указаны alias то они в теле запроса будут возвращаться поля с их названиями, под капотом fastapi устанавливает
галочку by_alias=True при сериализации ответа в json.
Для того, чтобы можно было передавать аргументы не только по псевдонимам используется опция конфигурации модели 
populate_by_name=True
"""


class User(BaseModel):
    name: str = Field(min_length=2, max_length=50, title="Имя", alias="user_name")
    age: int = Field(ge=18, lt=60, title="Возраст", alias="user_age")
    # эта опция позволяет использовать как алиасы (псевдонимы), так и названия атрибутов
    model_config = ConfigDict(populate_by_name=True)


@app.put("/ex1/")
def ex1(user: Annotated[User, Body(embed=True)]):  # embed задаёт явную отправку по ключу (см. lsn3_3)
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
