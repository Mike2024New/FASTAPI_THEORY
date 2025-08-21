from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Path, Query
from fastapi.responses import PlainTextResponse
from typing import Annotated
from enum import Enum

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
"""
Вопрос 1: Реализуй GET эндпоинт с path параметром с проверкой диапазона числа.  -> ex1
Вопрос 2: Создай GET эндпоинт с query параметрами и ограничениями (min_length, enum).   ->ex2
"""
app = FastAPI()
app.name = "app"


@app.get("/ex1/book/{page_num}/")
def ex1(page_num: Annotated[int, Path(gt=0, le=100)]):
    ...  # внутренняя логика работы функции с данными
    return PlainTextResponse(status_code=200, content=f"Контент страницы {page_num}")


class Modes(Enum):
    mode1 = "mode1"
    mode2 = "mode2"
    mode3 = "mode3"


@app.get("/ex2/")
def ex2(string: Annotated[str, Query(min_length=5)], mode: Annotated[Modes, Query()]):
    ...  # внутренняя логика работы функции с данными
    return {"string": string, "mode": mode}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
