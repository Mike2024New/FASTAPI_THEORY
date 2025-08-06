# uvicorn THEORY.lsn2_6:app --reload
from fastapi import FastAPI, Query
import uvicorn
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

"""
дополнительная метаинформация, 
title - название параметра отображаемое в документации
descriptions - описание параметра отобр в документации
depricated - предупреждение об устаревании параметра (то есть он ещё работает, но в доках отображается, что это 
устаревшая технология)
alias - псевдоним параметра, например нужно, чтобы для url он назывался query-par, но для python это имя не валидно, с 
помощью alias, можно связать query-par и query_par. 
include_in_schema - параметр не будет отображаться вдокументации.
"""

app = FastAPI()


# ex1 - title и description
# http://127.0.0.1:8000/ex1/?query_par=test
@app.get("/ex1/")
def ex1(query_par: Annotated[str, Query(title="Тестовый параметр", description="Описание этого тестового параметра")]):
    return query_par


# ex1 - alias (псевдоним) и deprecated -> чтобы увидеть deprecated (устаревание) нужно зайти на docs или redoc
# http://127.0.0.1:8000/ex2/?query-par=test   -> внимание! у query-par используется тире а не нижнее подчеркивание
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
@app.get("/ex2/")
def ex2(query_par: Annotated[str, Query(alias="query-par", deprecated=True)]):
    return query_par


# ex3 исключение параметра из json схемы и из документации
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/ex3/
@app.get("/ex3/")
def ex3(query_par: Annotated[str | None, Query(include_in_schema=False)] = None):
    return query_par


if __name__ == '__main__':
    uvicorn.run(app="lsn2_6:app", reload=True)
