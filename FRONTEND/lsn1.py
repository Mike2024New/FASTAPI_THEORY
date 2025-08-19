from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

"""
Простая html страница которая динамически подставляет данные, шаблонизатор для выдачи клиента понятной html страницы а 
не json. По сути это уже такой упрощенный frontend (понятный и удобный для пользователя интерфейс).
Есть html страница с карточкой пользователя, вот фрагмент из неё:
===============================================
<body>
<h2>Карточка пользователя №{{ user_id }}</h2>
<ul>
    <li>Имя: {{ user.name }}</li>
    <li>Возраст: {{ user.age }}</li>
    <li>Город: {{ user.city }}</li>
</ul>
</body>
===============================================
Задача обработчика маршрута отдать эту страницу клиенту через HTMLResponse, передав значения user_id и объект User 
(в данном случае это json словарь).
"""

app = FastAPI()
app.name = "app"
templates = Jinja2Templates(directory="TEMPLATES")  # необходимо создать экземпляр Jinja2, указав директорию с шаблонами

# Данные пользователей, в этом словаре подстроенны под структуру html страницы
users = {
    1: {"name": "Иван", "age": 32, "city": "Москва"},
    2: {"name": "Мария", "age": 40, "city": "Новгород"},
    3: {"name": "Виталий", "age": 25, "city": "Санкт-Петербург"},
}


@app.get("/ex1/{user_id}/", response_class=HTMLResponse)
async def ex1(user_id: int, request: Request):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"Пользователя с идентификатором `{user_id}` не существует.")
    return templates.TemplateResponse(
        name="temp1.html",  # имя файла шаблона (не путь а имя, так как путь указан в directory при создании templates)
        context={  # передача данных для подстановки их в html шаблоне
            "request": request,
            "user_id": user_id,
            "user": users[user_id]
        })


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
