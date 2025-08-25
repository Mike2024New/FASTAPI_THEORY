from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Query
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 11: Напиши эндпоинт с query параметром с alias.  -> ex1
Вопрос 13: Реализуй эндпоинт с несколькими query параметрами-списками.  -> ex2
"""


# http://127.0.0.1:8000/ex1/?par=test
@app.get("/ex1/")
def ex1(parametr: Annotated[str, Query(alias="par")]):  # alias даёт возможность клиенту указывать псевдоним
    return parametr


# дополнительно! Можно создать pydantic модель даже для 1 параметра и установить конфигурацию populate_by_name, тогда
# можно будет вводить параметры не только по псевдониму но и по названию атрибута в модели.


class Parametr(BaseModel):
    parametr: Annotated[str, Field(alias="par")]
    model_config = ConfigDict(populate_by_name=True)


# http://127.0.0.1:8000/ex2/?par=1&par=2&par=3
@app.get("/ex2/")
def ex2(par: Annotated[list[int], Query()]):  # благодаря аннотации list[...] можно принимать список параметров
    return par


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
