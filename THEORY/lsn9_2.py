from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

"""
В fastapi предусмотрена возможность создания обработчиков пользовательских исключенией.
exception_handler(ExceptionError)
Это позволяет изолировать логику обработки ошибки, сократив код в эндпоинтах.
"""


class PageNotFoundError(ValueError):
    def __init__(self, page_num):
        self.page_num = page_num


app = FastAPI()
app.name = "app"

fake_db = {f"page_{i}": f"content from page_{i}" for i in range(10)}


@app.exception_handler(PageNotFoundError)
async def page_not_found_handler(request: Request, exc: PageNotFoundError):
    """теперь логика обработки исключения вынесена в отдельную функцию"""
    print(request)  # например здесь можно выполнить логирование
    return JSONResponse(
        status_code=404,
        content={"message": f"Страница '{exc.page_num}' не найдена"},
        headers={"X-error": "pageNotFoundError"}
    )


@app.get("/ex1/{page_num}/")
def ex1(page_num: int):
    page = f"page_{page_num}"
    if page not in fake_db:  # а здесь теперь просто компактная проверка
        raise PageNotFoundError(page_num=page_num)
    return fake_db[page]


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
