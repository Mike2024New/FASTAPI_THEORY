import asyncio
from typing import Annotated
from UTILS.APP_RUN import app_run
from fastapi import FastAPI, BackgroundTasks, status, Depends
from datetime import datetime

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
BackgroundTasks это запуск фоновых задач. Это может пригодиться в тех случаях когда пользователь отправил запрос, но 
этот запрос требует обработки, например он прислал файл который обрабатывается внутри базы данных и естественно это 
занимает время. Чтобы маршрут не зависал задача помещается в фон, а пользователю отправляется статус код 202, о том
что запрос успешно выполнен и файл получен, но пока ещё в процессе обработки.
"""


async def write_user_msg(message: str = ""):
    await asyncio.sleep(5)  # иммитация длительной операции
    with open(file="lsn19_1_log.txt", mode="a") as f:
        message = f"\nЗапись {datetime.now()}:{message}"
        f.write(message)
    print(f"{datetime.now()} -> время записи файла.")  # см. время запроса в консоли


# зависимость с сохранением данных в файл, с назначением задачи в фоне
async def msg_write_depends(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_user_msg, message)  # задача поместится в корутину в фоне
    return message


@app.post("/ex1/", status_code=status.HTTP_202_ACCEPTED)  # так как задача требует времени, то статус код 202
async def ex1(message: Annotated[msg_write_depends, Depends()]):
    print(f"{datetime.now()} -> время запроса.")  # см. время запроса в консоли
    return {"msg": "Ваше сообщение принято и записано.", "part_msg": message[:20]}


# этот маршрут сделан просто дополнительно, чтобы доказать, что маршрут принявший файл не завис
@app.get("/")
async def home():
    return {"msg": "Можно перейти на страницу '/ex1/' и отправить файл"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
