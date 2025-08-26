from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends, Header, HTTPException, Cookie, Response
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Зависимости в декораторах функций пути - используются в тех случаях когда нужно выполнить внешнюю логику, но при этом
не нужно возвращать результаты (да эти функции не возвращают результат, строки с return будут проигнорированы).
Такие функции объявляются в списке dependencies декоратора ручки, последовательность имеет значение. Такие функции
могут использоваться например для валидации заголовков, проверки куков и так далее.
Важно помнить, что результаты такие функции не возвращают.
Такой способ называют side-effect когда функция выполняется не совсем в прямой связи с логикой ручки.
--------------------------------------------------------------------------------
Зависимости также поддерживают возбуждение исключений, и работу с response и request
"""


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "test_token":
        raise HTTPException(status_code=400, detail="Не корректный токен")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "test_key":
        raise HTTPException(status_code=400, detail="Не корректный тестовый ключ")
    return x_key  # Важно! В таком контексте, эта строка не имеет смысл, так как функции dependencies не возвращают результаты
    # если уж нужно внести отсюда изменения, то тогда можно записать значения в хранилище или в сессию


# верхние примеры из документации, добавил от себя проверку куков verify_cookie, чтобы продемонстрировать где ещё может
# быть полезен такой способ использования функций зависимости
async def verify_cookie(response: Response, session_id: Annotated[str | None, Cookie()] = None):
    if session_id is None:
        response.set_cookie(key="session_id", value="1", httponly=True, samesite="lax")
    print(session_id)


"""
просто для примера, добавлю ещё функцию которая считает количество вызовов маршрута /ex1/
Например появилась задача определить насколько страница популярна и как часто по ней переходят.
"""
ex1_count = 0


async def ex1_call_count():
    global ex1_count
    ex1_count += 1


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/",
         dependencies=[Depends(verify_token), Depends(verify_key), Depends(verify_cookie), Depends(ex1_call_count)])
async def ex1():
    ...  # логика функции
    print(f"Функция была вызвана уже {ex1_count} раз.")
    return "test"


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
