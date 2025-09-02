from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request, Response
from typing import Awaitable, Callable

"""
Ещё один пример middleware функции, в данном случае эта функция подсчитывает количество вызовов каждого маршрута.

В принципе такую реализацию можно заменить с помощью dependencies в app, указав функцию подсчёта и она также глобально
применится ко всем маршрутам, а если использовать yield, то получится фактически тот же самый механизм.
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

counter_call = {}


@app.middleware("http")
async def counter(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    url = request.url.path
    if not counter_call.get(url):
        counter_call[url] = 0
    counter_call[url] += 1
    response = await call_next(request)
    return response


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/")
async def ex1():
    return {"msg": "ex1"}


# http://127.0.0.1:8000/ex2/
@app.get("/ex2/")
async def ex2():
    return {"msg": "ex2"}


# http://127.0.0.1:8000/ex3/
@app.get("/ex3/")
async def ex3():
    return {"msg": "ex3"}


# http://127.0.0.1:8000/stat/
@app.get("/stat/")
async def stat():
    return {"stat": counter_call}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
