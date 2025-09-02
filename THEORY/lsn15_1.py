import time
from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request, Response
from typing import Callable, Awaitable

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Middleware (промежуточный слой)
По сути эта функция напоминает поведение декоратора в python, она также является оберткой "до" и "после", но только
вместо традиционной функции у неё api ручка со своей логикой. 
Точно также она перехватывает параметры в виде Request от клиента, и Respone в виде результата работы функции операции
пути.
В этом слое можно взять всю информацию про клиента, модифицировать Response, например в данном случае устанавливается
дополнительный заголовок с данными, о времени работы api ручки.
"""


@app.middleware("http")
async def add_process_time_header(
        request: Request,  # объект запроса пользователя
        call_next: Callable[[Request], Awaitable[Response]]  # функция обработчика (вызов эндпоинта)
):
    # действие до срабатывания endpoint (api ручки)
    start_time = time.perf_counter()
    response = await call_next(request)  # точка отработки маршрута?
    # действия после отработки логики в endpoint
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)  # в данном случае просто ставим заголовок пользователю
    return response


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/")
async def ex1():
    return {"msg": "ex1"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
