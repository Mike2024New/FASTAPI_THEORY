from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

"""
Вопрос 14: Реализуй редирект с кодом 302.
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"


# http://127.0.0.1:8000/
@app.get("/")
def home():
    return RedirectResponse(url="/ex2/", status_code=302)


@app.get("/ex2/")
def ex2():
    return {"msg": "Область маршрута ex2"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
