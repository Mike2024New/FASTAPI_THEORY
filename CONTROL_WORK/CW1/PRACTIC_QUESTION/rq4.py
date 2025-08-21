from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 5: Используй starlette path параметр для приема полного пути к файлу, вернуть только имя.
"""


# http://127.0.0.1:8000/resources/my_data/  -> тот случай когда есть ещё статичный адрес, этот маршрут расположен сверху
@app.get("/resources/my_data/")
def ex0():
    return PlainTextResponse(status_code=200, content=f"Мои данные")


# http://127.0.0.1:8000/resources/images/city/Moscow.jpg/   -> пример url содержащего путь images/city/Moscow.jpg/
@app.get("/resources/{file_path:path}/")
def ex1(file_path: str):
    file_name = os.path.split(file_path)[-1]  # извлечение имени файла
    return PlainTextResponse(status_code=200, content=f"Ресурс получен, файл '{file_name}'")


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
