# uvicorn THEORY.lsn2_5:app --reload
from fastapi import FastAPI, Query
import uvicorn
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()

"""
Для того, чтобы передать список (набор параметров в Query), нужно использовать соответствующую аннотацию типов, а также
передать нужное количество Query параметров после url, дублируя их, например:  ?lst=1&lst=2, что будет преобразовано 
в {"lst":[1,2]} (в эндпоинте ex1) 
"""


# http://127.0.0.1:8000/ex1/?lst=1&lst=2
@app.get("/ex1/")
async def ex1(lst: Annotated[list[int] | None, Query()] = None):
    print(lst)
    return {"lst": lst}


"""
также можно задать значение по умолчанию, присвоив immutable коллекцию кортеж. 
"""


# http://127.0.0.1:8000/ex2/    -> используются значения по умолчанию
# http://127.0.0.1:8000/ex2/?lst=1&lst=2&lst=3&lst=4    -> это равно предыдущему url, потому, что в нем уже установлены эти значения
@app.get("/ex2/")
async def ex2(lst: Annotated[list[int], Query()] = (1, 2, 3, 4)):
    return {"lst": lst}


"""
ex3
Важно!
Если по умолчанию нужно чтобы создавался пустой список, то использовать default_factory, так как особенность python в
том, что если напрямую указать mutable коллекцию через оператор присвоения то создастся список общий для всех 
экземпляров:
lst: Annotated[list, Query()] = [] # категорически не допустимо!
lst: Annotated[list, Query(default_factory=list)] # отлично, default_factory гарантирует независимую копию списка
"""


# http://127.0.0.1:8000/ex3/
@app.get("/ex3/")
async def ex3(lst: Annotated[list, Query(default_factory=list)]):
    return {"lst": lst}


if __name__ == '__main__':
    uvicorn.run(app="lsn2_5:app", reload=True)
