from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

"""
Механизм отлова внутренних ошибок сервера.
Для 500 статус кодов (для ошибок HTTP лучше всего использовать отдельные handler обработчики, так рекомендует 
документация fastapi)
----------------------------
Не использовать этот способ для HTTP ошибок. Этот механизм стоит использовать для питоновских ошибок, то есть тех 
ошибок, которые могут быть в серверной логике, например: ValueError, FileNotFound и другие.
"""

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(exc)}
        )


# http://127.0.0.1:8000/ex1/22/
@app.get("/ex1/{user_id}/")
async def ex1(user_id: int):
    if user_id > 10:
        raise ValueError("Ошибка пользователей в базе не может быть больше 10")
    return {"msg": "ex1"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
