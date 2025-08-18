import os

from UTILS.APP_RUN import app_run
from UTILS.read_file import read_file
from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
В fastapi можно также, комбинировать приём данных формы и файлов, то есть поддерживается одновременная кодировка 
multipart/form-data, можно принимать и файлы и формы.
Ниже в примере ex1 показано как принять в одном маршруте оба типа параметров.
"""


@app.get("/")
async def home():
    content = read_file(os.path.join("HTML", "file4.html"))
    return HTMLResponse(status_code=200, content=content)


@app.post("/ex1/")
async def ex1(
        username: Annotated[str, Form()],
        role: Annotated[str, Form(description="роль пользователя")],
        file: Annotated[UploadFile, File(description="отправьте файл")]
):
    try:
        res = await file.read()
        text = res.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail=f"Ошибка кодировки файла {file.filename}, не декодируется в utf-8")
    return {
        "username": username,
        "role": role,
        "file": file.filename,
        "text": text[:20],
    }


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
