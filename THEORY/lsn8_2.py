import os
from UTILS.read_file import read_file
from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Можно также читать параметры из html форм с методом отправки post, для этого в fastapi предусмотрен объект Form(), 
который принимает в себя данные из полей. Поля можно прописать в параметрах функции отдельно, связав ожидаемый тип
с объектом Form, важно! Body() параметры и Form() не совметстимы, так как формы html кодируют пересылаемы данные в 
другом формате: application/x-www-form-urlencoded (multipart/form-data в случае если это файлы). А body ждет 
application/json, согласно протоколу html передать эти типы данных одновременно не возможно.
--------------------------------------------------------------------------------------------------------------
ВАЖНО! Поля в форме (атрибут name), должны совпадать с параметрами в функциях (или Pydantic моделях).
"""


# http://127.0.0.1:8000/  -> перейти сюда, чтобы форма загрузилась
@app.get("/")
def home():
    """"""
    content = read_file(file_path=os.path.join(os.getcwd(), 'HTML', 'file2.html'))
    return HTMLResponse(content=content, status_code=200)


@app.post("/ex1/")
def ex1(username: Annotated[str, Form()], password: Annotated[str, Form()], password_repeat: Annotated[str, Form()]):
    if password != password_repeat:
        raise HTTPException(status_code=422, detail="Ошибка, пароли должны совпадать")
    return {"username": username}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
