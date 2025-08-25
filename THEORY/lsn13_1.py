from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends, Request
from typing import Annotated, Literal

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

'''
Первое понятие зависимости dependency injection.
Это такая функция которая собирает в себе логику которая повторяется в разных маршрутах.
В примере ниже показано как работать с параметрами: оба маршрута ex1 и ex2, ждут два одинаковых параметра это
user_id и role, которые можно как раз поместить в одну функцию ожидания и задать возвращаемый тип, в данном случае 
это словарь из параметров.
Также иньекций зависимости может быть несколько, например в ex2 подключена ещё одна common функция, которая даёт 
дополнительный query параметр со значением по умолчанию.
'''


async def common_parametrs(user_id: int, role: Literal["user", "admin"] = "user"):
    return {"user_id": user_id, "role": role}


async def common_parametrs_add(show_options: bool = False):
    return {"show_options": show_options}


# объявление обобщенного типа переменной (которая явно ссылается на функцию common_parametrs)
depend_common_parametrs = Annotated[dict, Depends(common_parametrs)]
depend_common_parametrs_add = Annotated[dict, Depends(common_parametrs_add)]


# параметры ex1, централизовано объявлены в depend_common_parametrs
# http://127.0.0.1:8000/ex1/
@app.get("/ex1/{user_id}/")
async def ex1(request: Request, commons: depend_common_parametrs):
    return {"msg": f"Прочитаны входные параметры: `{commons}`, по адресу `{request.url}`"}


# К ex2 добавлено две зависимых функции в порядке очередности, все параметры отобразятся в документации
# http://127.0.0.1:8000/ex2/
@app.get("/ex2/{user_id}/")
async def ex2(request: Request, commons: depend_common_parametrs, commons_add: depend_common_parametrs_add):
    commons.update(commons_add)  # соединение двух результатов полученных из зависимых функций
    return {"msg": f"Прочитаны входные параметры: `{commons}`, по адресу `{request.url}`"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
