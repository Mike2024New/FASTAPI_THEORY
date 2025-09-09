from UTILS.APP_RUN import app_run
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
В fastapi можно создавать свои кастомные классы и их обработчики
"""


class MyCustomException(HTTPException):  # кастомный класс исключения
    def __init__(self, detail: str, header_error: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.header_error = header_error


@app.exception_handler(MyCustomException)  # обработчик кастомного исключения
async def my_custom_exception_handler(request: Request, exc: MyCustomException):
    print(request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Custom error: {exc.detail}"},
        headers={"X-error": exc.header_error},  # доступны дополнительные поля определенные в кастомном классе
    )


# http://127.0.0.1:8000/
@app.get("/")
async def ex1():
    raise MyCustomException("Возникла ошибка просто так.", header_error="error")


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
