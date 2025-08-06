# uvicorn THEORY.lsn2_3:app --reload
from fastapi import FastAPI, Query
from typing import Annotated
import uvicorn

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()

"""
Объект Query позволяет явно объявить что параметр является именно параметром запроса (Query).
Также объект Query позволяет устанавливать дополнительные условия входного значения, например ограничения по длине
строки.
---------------------
Annotated служит для присвоения атрибуту метаинформации, до python 3.9 Annotated импортируется из typing_extensions
"""


# Примеры url для тестирования /ex1/
# http://127.0.0.1:8000/ex1/?text=example  -> коректный запрос, длина строки от 2 до 10
# http://127.0.0.1:8000/ex1/?text=e -> ошибка строка меньше чем min_length
# http://127.0.0.1:8000/ex1/?text=example_long_overflow  -> ошибка превышения max_length
@app.get("/ex1/")
def ex1(
        text: Annotated[str | None, Query(min_length=2, max_length=10)] = None,  # современный Annotaded способ записи
):
    return {"text": text}


"""
ex2 -> устаревший вариант использоания Query без Annotated через присвоение Query в качестве значения
В более старых версиях Fastapi (до 0.95.0) может встретиться такой тип объявления параметров
q: Union[str | None] = Query(default=None)
В таком случае значение по умолчанию задаётся через default
"""


# Примеры url для тестирования /ex2/
# http://127.0.0.1:8000/ex2/?text=example  -> коректный запрос, длина строки от 2 до 10
# http://127.0.0.1:8000/ex2/?text=e -> ошибка строка меньше чем min_length
# http://127.0.0.1:8000/ex2/?text=example_long_overflow  -> ошибка превышения max_length
@app.get("/ex2/")
def ex2(
        text: str | None = Query(default=None, min_length=2, max_length=10),  # старый способ записи в fastapi до 0.95.0
):
    return {"text": text}


if __name__ == '__main__':
    uvicorn.run(app="lsn2_3:app", reload=True)
