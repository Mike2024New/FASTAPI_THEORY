from UTILS.APP_RUN import app_run
from UTILS.GENERATE_UUID_KEY import generate_random_key_uuid
from fastapi import FastAPI, Request, Response

app = FastAPI()
app.name = "app"
session_storage = []


def set_cookie(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    print(f"session_storage: {session_storage}")
    print(f"Текущий session_id: {session_id}")
    if session_id is None or session_id not in session_storage:
        new_session_id = generate_random_key_uuid(length=10)
        response.set_cookie(key="session_id", value=new_session_id, httponly=True, samesite="lax")
        session_storage.append(new_session_id)


@app.get("/")
def home(request: Request, response: Response):
    set_cookie(request, response)
    return {"msg": "Главная страница"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
