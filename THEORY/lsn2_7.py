from UTILS.APP_RUN import app_run
from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, ConfigDict

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
pydantic модель для query параметров (по аналогии с body параметрами), можно создавать pydantic модель которая будет 
группировать поля и в ней удобно прописывать свойства атрибутов.
Для того, чтобы использовать Query группировку, нужно использовать Annotated, с указанием типа модели и объекта Query
если этого не сделать, то параметры будут восприниматься как параметры тела (body параметры)
=====================================================================================================
ВАЖНЫЙ НЮАНС! ПРИ ОБЪЯВЛЕНИИ QUERY ПАРАМЕТРОВ, НЕ ИСПОЛЬЗОВАТЬ ПСЕВДОНИМЫ (ALIAS) ТАК КАК ЭТО ПРИВОДИТ К НЕОЖИДАННЫМ
РЕЗУЛЬТАТАМ ОСОБЕННО С МАССИВАМИ, В ТАКИХ СЛУЧАЯХ ЛУЧШЕ ПРОПИСЫВАТЬ ЭТИ ПАРАМЕТРЫ ОТДЕЛЬНО БЕЗ ГРУППИРОВКИ.
"""


class PrintOptions(BaseModel):
    max_pages: int = Field(default=10, gt=0, le=100, title="максимальное кол-во страниц")
    pages_nums: list[int] = Field(default_factory=list, title="конкретные страницы")  # проблемы с alias
    color_mode: Literal["color", "black"] = Field(default="black", title="режим печати")


# http://127.0.0.1:8000/ex1/
# http://127.0.0.1:8000/ex1/?max_pages=5&pages_num=1&pages_num=2&color_mode=color
@app.get("/ex1/")
def ex1(print_options: Annotated[PrintOptions, Query()]):
    return {
        "msg": "Печать будет выполнена с переданными настройками",
        "options": print_options.dict()
    }


"""
В модели pydantic можно запрещать передачу неуказанных атрибутов, для этого нужно установить конфигурацию в модели 
extra="forbid"
=========================
Напоминание: передавать чувствительные параметры через query параметры категорически запрещено, для этого используются
body параметры.
"""


class User(BaseModel):
    name: str
    age: int = Field(ge=18, lt=60)
    model_config = ConfigDict(extra="forbid")


# http://127.0.0.1:8000/ex2/?name=Mike&age=32   -> корректно, так как нет лишних параметров
# http://127.0.0.1:8000/ex2/?name=Mike&age=32&city=Moscow    -> вызовет ошибку, так как city не указан в модели
@app.get("/ex2/")
def ex2(user: Annotated[User, Query()]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name, reload=True)
