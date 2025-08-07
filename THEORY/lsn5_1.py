from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Иногда бывает необходимость перенаправить пользователя с эндпоинта на другую страницу, сделать редирект, для этого 
используется RedirectResponse, с указанием url и статус кода
Статус коды для редиректа:
301 - постоянное перенаправление
302 - временное перенаправление (ставится по умолчанию если не указать параметр status_code)
303 - перенаправление после POST (после успешной обработки формы например)
"""


# https://127.0.0.1/ex1/
@app.get("/ex1/")
def ex1():
    return RedirectResponse(url="https://example.com/", status_code=302)  # редирект на другой url адрес


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
