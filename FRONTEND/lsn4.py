from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.name = "app"

templates = Jinja2Templates(directory="TEMPLATES")  # необходимо создать экземпляр Jinja2, указав директорию с шаблонами
app.mount(
    "/static",  # папка содержащая стили
    StaticFiles(directory="static"),  # создаётся объект который работает со статическими файлами
    name="static"  # имя переменной по которой шаблон будет достраивать путь к папке с файлами
)  # с помощью app.mount можно добавить css стили


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="temp3.html",
        context={
            "request": request,
        }
    )


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
