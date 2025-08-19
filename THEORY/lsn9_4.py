from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В примере ниже, ошибка неверно введенных пользователем данных, вынесена в отдельный обработчик, и в нём к ошибке 
отправляется дополнительная информация, "body" информация о теле запроса, что клиент ввел неправильно.
То есть выводится стандартное pydantic сообщение об ошибке и то что клиент ввел и отправил на сервер.
"""


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """переопределение стандартной логики ошибок валидации ValidationError"""
    ...  # расширение логики обработки стандартного RequestValidationError
    print(request.url)
    print(f"Данные содержащиеся в exc:")
    print(exc.errors())  # доступен список ошибок (под капотом используется Pydantic)
    print(exc.args)  # параметры запроса, дублируется с exc.errors()
    print(exc.body)  # тело запроса (это работает только с телом запроса
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )


class User(BaseModel):
    name: str
    age: int


@app.post("/ex1/")
async def ex1(user: User):
    return user


# http://127.0.0.1:8000/ex2/2/?user_id=12 -> корректный запрос
# http://127.0.0.1:8000/ex2/2/?user_id=dfasdasf -> неправильный запрос с 1 ошибкой валидации (page)
# http://127.0.0.1:8000/ex2/2/?user_id=dfasdasf -> неправильный запрос с 1 ошибкой валидации (user_id)
# http://127.0.0.1:8000/ex2/fdsafd/?user_id=dfasdasf    -> заведомо неправильный запрос с 2 ошибками валидации
@app.get("/ex2/{page}/")
async def ex2(page: int, user_id: int):
    return {"page": page, "user_id": user_id}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
