from UTILS.APP_RUN import app_run
from fastapi import FastAPI, UploadFile, Request, HTTPException, File
from fastapi.templating import Jinja2Templates
from typing import Annotated
from enum import Enum

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"
templates = Jinja2Templates(directory="templates")
"""
Вопрос 10: Реализуй загрузку файла через UploadFile с проверкой типа и размера.
"""


class Tags(Enum):
    file_endpoint = "file_endpoint"


# http://127.0.0.1:8000/load_file/
@app.get("/load_file/", summary="Отправка Html формы клиенту для загрузки файла", tags=[Tags.file_endpoint])
def load_file_get_html(request: Request):
    return templates.TemplateResponse(name="for_rq8_load_file.html", status_code=200, context={"request": request})


@app.post("/load_file/", summary="Загрузка файла пользователя, отправка ему html с метаинформацией о файле",
          tags=[Tags.file_endpoint]
          )
async def load_file_from_form(request: Request, file_user: Annotated[UploadFile, File()]):
    print(file_user.filename)
    if not file_user.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Файл должен иметь расширение txt")
    if file_user.size > 1000:
        raise HTTPException(status_code=400, detail="Файл может быть размером не больше 1 мб.")
    # ниже показана операция чтения файла (просто для примера и чтобы напомнить, что это асинхронная операция)
    file_first_100_chars = await file_user.read()  # чтение данных файла (это асинхронная операция!)
    file_first_100_chars = file_first_100_chars.decode(encoding="utf-8")
    print(file_first_100_chars[:100])
    file_info = {
        "name": file_user.filename,
        "size": file_user.size
    }
    return templates.TemplateResponse(
        name="for_rq8_file_info.html",
        status_code=200,
        context={"request": request, "file": file_info}
    )


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
