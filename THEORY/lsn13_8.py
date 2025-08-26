from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Query, Depends
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/

"""
Пример комбинирования подходов подключения функций зависимости
"""

ex_count = {"ex1": 0, "ex2": 0, "all_call_count": 0}


async def all_call_count():  # общая функция считает все запросы
    ex_count["all_call_count"] += 1


app = FastAPI(dependencies=[Depends(all_call_count)])
app.name = "app"

fake_site = [f"page_{i + 1}" for i in range(10)]  # псевдо БД


async def filter_extract(  # вложенная функция зависимости, не общается на прямую с ex1, но расширяет её параметры
        start_page: Annotated[int | None, Query()] = 0,
        limit_pages: Annotated[int | None, Query()] = 100
):
    return start_page, limit_pages


async def filter_parametrs(filters: Annotated[tuple, Depends(filter_extract)]):
    start = filters[0]
    chunk = filters[1]
    return fake_site[start: start + chunk]


async def ex1_call_counter():  # функция персонально только для ex1, не вызываемая напрямую side-effect
    global ex_count
    ex_count["ex1"] += 1


async def ex2_call_counter():  # функция персонально только для ex2, не вызываемая напрямую side-effect
    global ex_count
    ex_count["ex2"] += 1


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/", dependencies=[Depends(ex1_call_counter, use_cache=False)])
async def ex1(content: Annotated[list, Depends(filter_parametrs)]):
    return {"content": content}


# http://127.0.0.1:8000/ex2/
@app.get("/ex2/", dependencies=[Depends(ex2_call_counter, use_cache=False)])
async def ex2(content: Annotated[list, Depends(filter_parametrs)]):
    return {"content": content}


# http://127.0.0.1:8000/ex3/
@app.get("/ex3/")
async def ex3():
    return {"результаты счётчика": ex_count}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
