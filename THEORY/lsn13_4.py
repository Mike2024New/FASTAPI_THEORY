from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Зависимости используют кеш (по умолчанию), ниже представлен пример где маршрут ex1, вызывает две зависимые функции
которые под капотом в свою очередь вызывают одну и ту же функцию. И для того, чтобы не вызывать одну и туже функцию
несколько раз, в Fastapi предусмотрен кеш для функций зависимости который помогает оптимизировать производительность
приложения.
Кеширование можно отключить установив в use_cache -> False.
Фактически use_cache, говорит возьми значение из хранилища если оно есть (так как первый вызов в любом случае не будет
использовать кеш так как его просто ещё нет)
"""


async def dependency_func():  # так как use_cache=True, эта функция будет вызвана только 1 раз
    print("Вызов зависимой функции...")
    return "test"


async def dependent_1(val: Annotated[str, Depends(dependency_func, use_cache=True)]):
    ...  # логика первой зависиомой функции, которая под капотом вызвает подзависимость dependency_func()
    return val


async def dependent_2(val: Annotated[str, Depends(dependency_func, use_cache=True)]):
    ...  # логика второй зависиомой функции, которая под капотом вызвает подзависимость dependency_func()
    return val


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/")
async def ex1(dep1: Annotated[str, Depends(dependent_1)], dep2: Annotated[str, Depends(dependent_2)]):
    return {"dep1": dep1, "dep2": dep2}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
