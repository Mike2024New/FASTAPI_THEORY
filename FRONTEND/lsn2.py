from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.name = "app"
templates = Jinja2Templates(directory="TEMPLATES")  # необходимо создать экземпляр Jinja2, указав директорию с шаблонами

"""
В шаблонах можно указывать циклы for, в виде {% for var in arr %}, но цикл также требуется обязательно закрыть ->
{% endfor %}. Также у цикла предусмотрен объект класс loop. который может быть полезен для обработки элементов цикла, 
например: 
loop.index - показывает текущий номер итерации (начиная с 1)
loop.index0 - тоже самое что и loop.index, но с 0
loop.revindex - обратный индекс начиная с 1
loop.revindex0 - обратный индекс начиная с 0
loop.first - False значение если это первая итерация
loop.last - True если это последняя итерация
----------------------------------------------------------------------
Для понимания материала см. шаблон TEMPLATES/temp2.html
"""

users = {
    1: {"name": "Иван", "age": 32, "city": "Москва", "hobby": ["Волейбол", "бильярд", "экскурсии", "теннис"]},
    2: {"name": "Мария", "age": 40, "city": "Новгород", "hobby": ["программирование"]},
    3: {"name": "Виталий", "age": 25, "city": "Санкт-Петербург", "hobby": ["чтение", "прогулки", "авиамоделирование"]},
}


@app.get("/ex1/{user_id}/", response_class=HTMLResponse)
async def ex1(user_id: int, request: Request):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"Пользователя с идентификатором `{user_id}` не существует.")
    return templates.TemplateResponse(
        name="temp2.html",
        context={
            "request": request,
            "user_id": user_id,
            "user": users[user_id]
        }
    )


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
