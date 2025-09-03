from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"
templates = Jinja2Templates(directory="HTML")

"""
Внимание! приложение запускается с порта 8080
ex1 отправляет простой html с java script в котором прописан базовый ajax запрос (который нацелен на url с портом 8000 
из lsn16_1.py), и если порт 8090 находится в  разрешенных, то выполняется запрос. Если нет то ошибка.
------------
Этот домен указан в приложении запущенном на порте 8000, поэтому он может выполнять ajax запросы.
"""


# http://localhost:8080/
@app.get("/")
async def ex1(request: Request):
    return templates.TemplateResponse(name="file5.html", context={"request": request})


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name, host="127.0.0.1", port=8080)
