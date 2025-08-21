from UTILS.APP_RUN import app_run
from UTILS.GENERATE_UUID_KEY import generate_random_key_uuid
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вопрос 4: Реализуй проверку и чтение cookie в FastAPI с выдачей 401 при отсутствии.
"""

sessions_storage = []  # псевдохранилище сессий


def set_new_session(response: Response, session_id: str = None):
    """установка новой сессии с пользователем"""
    print(f"Сейчас сессия:{session_id}")
    print(f"session_storage:{sessions_storage}")
    set_session = False  # переключатель (записывать сессию или нет)
    # если сессия ещё не была установлена
    if session_id is None:
        set_session = True
    # если произошло подключение, пришли куки с сессией, но их нет в session_storage, то перезаписать их
    if session_id is not None and session_id not in sessions_storage:  # если сессии нет в хранилище
        set_session = True
    if set_session:
        session_id = generate_random_key_uuid(length=10)
        # для https нужно добавить параметр secure=True, чтобы куки передавались в зашифрованном виде
        response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax")
        sessions_storage.append(session_id)  # добавить новую сессию
    return session_id


@app.get("/")
def home(request: Request):
    """
    здесь выполняется установка куков (в упрощенном примере за это отвечает домашняя страница)
    Внимание на то как устанавливаются куки для PlainTextResponse!
    """
    session_id = request.cookies.get("session_id")  # получение id сессии
    response = PlainTextResponse(status_code=200, content=f"Домашняя страница, ваша сессия {session_id}")
    set_new_session(response, session_id)
    return response


@app.get("/ex1/")
def ex1(request: Request):
    """
    Якобы страница с полезным контентом, проверяется сперва установлена ли сессия с пользователем, если нет, то
    переход на домашнюю страницу.
    """
    session_id = request.cookies.get("session_id")  # получение id сессии
    if session_id is None or session_id and session_id not in sessions_storage:
        raise HTTPException(status_code=401, detail=f"Контент доступен только для авторизованных пользователей")
    return {"msg": f"Отлично, вам открыт доступ к контенту"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
