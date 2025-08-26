from UTILS.APP_RUN import app_run
from fastapi import FastAPI, HTTPException, Header, Depends
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/


"""
В fastapi можно объявлять глобальные di функции. То есть те функции которые будут применены абсолютно к всем ручкам api.
Простой пример, это проверка наличия сессии с пользователем и её установка в случае отсутствия, проверка авторизации и
другие примеры.
Ниже показана сильно упрощенная логика проверки, что на url перешел реальный пользователь а не парсинг бот
"""


async def verify_is_bot_or_real_user(
        user_agent: Annotated[str | None, Header()] = None,
        sec_ch_ua_platform: Annotated[str | None, Header()] = None,
):
    """простейшая псевдо проверка которая проверяет, что подключился не бот а реальный пользователь"""
    print("Проверка, что подключился реальный пользователь")
    if "python" in user_agent.lower() or sec_ch_ua_platform.lower() is None:
        raise HTTPException(status_code=403, detail="Отказано в доступе")


app = FastAPI(dependencies=[Depends(verify_is_bot_or_real_user)])  # в списке устанавливаются глобальные зависимости
app.name = "app"


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/")
async def ex1():  # под капотом теперь вызывает verify_is_bot_or_real_user
    return {"msg": "ex1 приветствует"}


# http://127.0.0.1:8000/ex2/
@app.get("/ex2/")  # под капотом теперь вызывает verify_is_bot_or_real_user
async def ex2():
    return {"msg": "ex2 приветствует"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
