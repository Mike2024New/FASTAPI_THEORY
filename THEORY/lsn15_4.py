from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Request
# для работы с этим слоем нужно установить pip list itsdangerous
from starlette.middleware.sessions import SessionMiddleware

"""
http://127.0.0.1:8000/ - главная страница приложения
http://127.0.0.1:8000/docs/ - интерактивная документация
http://127.0.0.1:8000/redoc/ - лаконичная и краткая документация
"""

app = FastAPI()
app.name = "app"

"""
SessionMiddleware под капотом создаёт сессию с пользователем устанавливая ему уникальный ключ контакта с ним. 
А также добавляет в request.session этот самый идентификатор пользователя как ключ, и можно добавлять туда уже свои ключи.
Также session гарантирует безопасную передачу сессию с помощью cookie по сети в зашифрованном виде. Если cookie у клиента отсутствует, то 
этот слой создаст соединение с клиентом. Важно помнить что ключ должен быть сложным и защищённым, а также не допустимо хранить его в коде.
"""
# естественно нужно использовать более сложные ключи и не хранить их в коде
app.add_middleware(SessionMiddleware, secret_key="test secret")


@app.get("/set_message/")  # http://127.0.0.1:8000/set_message/
def set_message(request: Request):
    request.session['flash_message'] = "Это сообщение установленное в сессию."
    return {"message": "Сообщение установлено."}


@app.get("/get_message/")  # http://127.0.0.1:8000/get_message/
def get_message(request: Request):
    msg = request.session.pop('flash_message')  # получение и удаление сообщения
    return {"flash_message": msg}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
