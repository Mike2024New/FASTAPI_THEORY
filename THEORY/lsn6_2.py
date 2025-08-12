from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Первое знакомство с объектом Response, это класс отвечающий за ответ выдаваемый сервером клиенту. Он имеет подклассы:

1. JSONResponse - пользователю отправляется json строка (преобразованный dict) с набором пар ключ значение. 
Автоматически устанавливает заголовок Content-Type: application/json и преобразует python объект в json строку.

2. RedirectResponse - перенаправление пользователя на другую страницу. Имеет статус коды ответа 
301 - постоянное перенаправление
302 - временное перенаправление
есть и другие статус коды, об этом в следующих разделах и уроках
"""

"""
ex1 -> 
Пример такого использования, если пользователь не укажет query параметр равным true, то тогда ему будет отправлен объект
json (JSONResponse), если пользователь укажет эту галочку, то его перенаправит на другую страницу (RedirectResponse)
"""


# http://127.0.0.1:8000/ex1/    -> выдаст сообщение (JSONResponse)
# http://127.0.0.1:8000/ex1/?redirect_to_example=1  -> перебросит на example.com (RedirectResponse)
@app.get("/ex1/")
async def ex1(redirect_to_example: bool = False) -> Response:  # указать объект Response в сигнатуре функции
    if redirect_to_example:
        return RedirectResponse(url="https://www.example.com/", status_code=301)  # 301 постоянное перенаправление
    return JSONResponse(content={"msg": "Установите галочку True, и вы будете перенаправлены на example.com"})


"""
ex2 ->
Особенность указания Response и других типов в сигнатуре функции. 
По умолчанию в декораторах функций операции пути, даже без явного указания значения response_model, автоматически 
подставляется модель Response и fastapi под капотом пытается привести данные к этой модели (это при том случае если
в сигнатуре функции есть Response), но если отправлять например dict, то это будет ошибка типа, так как он не 
преобразуется в эту Response модель.

Чтобы все корректно работало нужно указать response_model=None - это для тех случаев когда в сигнатуре функции в 
выходных данных нужно указать Response и другие типы данных
"""


# http://127.0.0.1:8000/ex2/    -> выдаст сообщение (JSONResponse)
# http://127.0.0.1:8000/ex2/?redirect_to_example=1  -> перебросит на example.com (RedirectResponse)
# @app.get("/ex2/") # -> это приведет к ошибке, Response | dict в сигнатуре функции не корректно без response_model
# это связанно с тем, что по умолчанию response_model будет пытаться строить модель Response
@app.get("/ex2/", response_model=None)
async def ex2(redirect_to_example: bool = False) -> Response | dict:
    if redirect_to_example:
        return RedirectResponse(url="https://www.example.com/", status_code=301)  # 301 постоянное перенаправление
    return JSONResponse(content={"msg": "Установите галочку True, и вы будете перенаправлены на example.com"})


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
