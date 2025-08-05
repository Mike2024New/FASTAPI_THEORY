# uvicorn THEORY.lsn2_4:app --reload
from fastapi import FastAPI, Query
import uvicorn

# безопасный импорт Annotated:
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

app = FastAPI()

"""
Регулярные выражения в query задаются с помощью pattern
"""


# http://127.0.0.1:8000/ex1/ -> вызовет ошибку, так как query обязательный параметр
# http://127.0.0.1:8000/ex1/?lsn=lsn1_2  -> выбран урок (заданный по шаблону в регулярных выражениях)
@app.get("/ex1/")
def ex1(
        lsn: Annotated[str, Query(pattern=r"^lsn\d{1,3}_\d{1,3}$", min_length=6, max_length=10)]
):
    """
    :param lsn: принимает на вход строки соответствующие шаблону, например lsn1_2, так как значение по умолчанию не
    определено то параметр обязательный.
    """
    return f"Выбран урок {lsn}"


"""
Обязательный query параметр который может быть и None, но без присвоения значения по умолчанию обрабатывается внутри
обработчика в ручную
"""


# http://127.0.0.1:8000/ex2/?key=test   -> верно, на входе строка, все правильно
# http://127.0.0.1:8000/ex2/?key=null   -> будет интерпретирован как null
# http://127.0.0.1:8000/ex2/    -> не верно, так как не указан обязательный query параметр key
@app.get("/ex2/")
def ex2(
        key: Annotated[str | None, Query()]
):
    if key is None or key.lower() == "null":  # ручная обработка отсутствующего значения
        return "не передан ключ"
    return key


"""
Примечание к ex2, случай рассмотренный в этом примере используется в тех случаях когда query параметр нужнжо передавать 
в любом случае, то есть сделать его обязательным.
"""

if __name__ == '__main__':
    uvicorn.run(app="lsn2_4:app", reload=True)
