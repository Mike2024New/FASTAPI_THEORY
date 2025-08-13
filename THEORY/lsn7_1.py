from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body, status
from fastapi.responses import RedirectResponse
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В декораторах операций пути, можно указывать статус коды
1xx - для разработчиков
2хх - успешная обработка запроса
3хх - перенаправления на дргуие ресурсы (редиректы)
4хх - ошибка на стороне клиента
5хх - ошибка на стороне сервера
"""

"""
ex1 ->
пользователь отправляет post Запрос к примеру создаёт свой аккаунт (в примере упрощенно передает свое имя)
На что получает статус код 201* который означает что, Запрос успешен, ресурсы созданы (например, POST создал новый 
объект).
-----------------------
*Если он укажет валидные данные естественно (и не получит 422 ошибку например).
"""


# http://127.0.0.1:8000/ex1/
@app.post("/ex1/", status_code=201, response_model=dict[str, str])  # status 201 -> ресурс успешно создан
def ex1(name: Annotated[str, Body(example="Иван")]):
    ...  # внутренняя логика создания аккаунта
    return {"msg": f"Ресурс с именем `{name}` успешно создан"}


"""
Разработчики fastapi позаботились о том, чтобы не запоминать статус коды.
Из fastapi можно импортировать модуль status, и у него есть подсказки в названиях переменных, например:
status.HTTP_201_CREATED , что напоминает о том, что этот статус относится к созданию ресурса.
"""


# http://127.0.0.1:8000/ex2/
@app.post("/ex2/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
def ex2(name: Annotated[str, Body(example="Иван")]):
    ...  # внутренняя логика создания аккаунта
    return {"msg": f"Ресурс с именем `{name}` успешно создан"}


# http://127.0.0.1:8000/ex3/
@app.get("/ex3/")
def ex3():
    return RedirectResponse(url="https://example.com/", status_code=status.HTTP_301_MOVED_PERMANENTLY)


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
