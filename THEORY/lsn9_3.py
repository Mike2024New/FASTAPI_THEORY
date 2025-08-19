from UTILS.APP_RUN import app_run
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

fake_db = {f"page_{i}": f"content from page {i}" for i in range(10)}

"""
В fastapi можно переопределить поведение стандартных исключений, например исключения которое отвечает за обработку
неправильных входных данных (связано с исключением ValidationError в pydantic). А также централизованно обрабатывать 
исключения HTTPException.
PlainTextResponse, отправляет просто строку (вместо json).
"""


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc):
    """
    В этом обработчике ловятся все исключения которые помечены как HTTPException, за счёт того, что
    HTTPException наследуется на StarletteHTTPException. Суть этого обработчика в переопределении поведения стандартных
    обработчиков этого типа. Здесь можно централизованно обработать HTTP ошибки.
    """
    print("Ошибка HTTPException")
    print(request.url)
    ...  # здесь логика внутренней обработки ошибок, например логирование
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    """
    В этом обработчике можно переопределить исключения возникающие при ошибках валидации данных входящих запросов
    например пользователь ввел неверный тип данных и pydantic под капотом выбросил ValidationError, тогда в этом
    обработчике можно определить логику обработки таких ошибок.
    """
    print("Ошибка валидации пользовательского ввода")
    print(request.url)
    ...  # здесь логика внутренней обработки ошибок, например логирование
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/ex1/{page_num}/")
async def ex1(page_num: int):
    page = f"page_{page_num}"
    if page not in fake_db:
        raise HTTPException(status_code=404, detail=f"Страница '{page}' не существует.")
    return {"page_content": fake_db[page]}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
