# uvicorn REPETITION.rp1:app --reload
from enum import Enum
from fastapi import FastAPI

app = FastAPI()


class Colors(Enum):
    red: str = "255_0_0"
    green: str = "0_255_0"
    blue: str = "0_0_255"


@app.get("/")
async def home():
    return {"msg": "Добро пожаловать!"}


# ниже обозреваются эндпоинты параметров путей, get_my_img и get_img_by_id, видно, что порядок важен, если поменять
# их местами, то запрос со строкой "my_img" которая не может быть преобразована в int вызовет ошибку.

# http://127.0.0.1:8000/images/my_img/
@app.get("/images/my_img/")
async def get_my_img():
    return {"img": f"Ваше личное изображение получено"}


# http://127.0.0.1:8000/images/25/
@app.get("/images/{img_id}/")
async def get_img_by_id(img_id: int):
    return {"img": f"изображение {img_id}"}


# пример предопределения значений из Enum перечислений
@app.get("/select_color/{color}/")
async def select_color(color: Colors):
    if color.value == "255_0_0":  # http://127.0.0.1:8000/select_color/255_0_0/
        return "Выбран красный цвет"
    elif color is Colors.green:  # http://127.0.0.1:8000/select_color/0_255_0/
        return "Выбран зеленый цвет"
    return "Выбран синий цвет"  # http://127.0.0.1:8000/select_color/0_0_255/


# ниже пример обработки пути, который может содержаться в url, а также комбинация параметров пути и path параметров
# (идентификатора)

# http://127.0.0.1:8000/files/test/2025/docs/100/
@app.get("/files/{file_path:path}/docs/{file_id}/")
async def get_doc_from_docs(file_path: str, file_id: int):
    return f"Получен файл из директории {file_path} с идентификатором {file_id}"


# http://127.0.0.1:8000/files/documents/reports/lessons.xlsx/
@app.get("/files/{file_path:path}/")
async def get_file_by_file_path(file_path: str):
    return f"Получен файл по пути {file_path}"
