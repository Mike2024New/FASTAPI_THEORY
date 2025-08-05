# uvicorn THEORY.lsn2_1:app --reload
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# псевдосайт со страницами
pages = [{"page": f"страница {i + 1}"} for i in range(10)]

"""
query параметры, прописываются в функции обработчике, но при этом отсутствуют в пути.
query параметры это как правило дополнительные опциональные параметры (хотя если не указать им значение по умолчанию
то они становятся обязательными)
Эти параметры представляют собой наборы пар ключ-значение, и пишутся согласно синтаксису 
url?parametr1=value1&parametr2=value2
то есть query параметры добавляются к url.
Важно, в этих параметрах нельзя передавать чувствительные данные, так как они отображаются в истории браузера и видны
в url адресах. Для этой цели используются body параметры которые будут изучены в уроках lsn3_x серии.
"""


# http://127.0.0.1:8000/ex1/   -> так как параметры по умолчанию установлены, то это минимальный url
# http://127.0.0.1:8000/ex1/?skip=2&limit=3 -> url с query параметрами
@app.get("/ex1/")
async def ex1(skip: int = 0, limit: int = 20):  # query параметры
    return pages[skip: skip + limit]


"""
Обязательные параметры (ex2)
ex2 -> пример где есть обязательный query параметр only_even, а значит минимальный запрос должен выглядеть так:
http://127.0.0.1:8000/ex2/?only_even=0  -> здесь параметр отключен
"""


# http://127.0.0.1:8000/ex2/?only_even=0   -> так как only_even сделан обязательным
# http://127.0.0.1:8000/ex2/?only_even=0&skip=2&limit=3  -> предустановленый диапазон страниц
@app.get("/ex2/")
async def ex2(only_even: bool, skip: int = 0, limit: int = 20):  # query параметры
    out_pages = pages
    if only_even:
        out_pages = [page for page in out_pages if int(page["page"].split()[-1]) % 2 == 0]
    return out_pages[skip: skip + limit]


"""
Необязательные параметры (ex3)
query параметры могут быть и None по умолчанию как в примере ex3 параметр add_text, он предустановлен по умолчанию в 
None и если он будет передан, то в выходной словарь с результатом добавится дополнительный ключ add_text
"""


# http://127.0.0.1:8000/ex3/    -> так как здесь query параметры не обязательны можно передать базовый url
# http://127.0.0.1:8000/ex3/?add_text=test  -> установлен специальный опциональный параметр add_text
# http://127.0.0.1:8000/ex2/?add_text=test&skip=2&limit=3   -> установлены все query параметры
@app.get("/ex3/")
async def ex3(add_text: str | None = None, skip: int = 0, limit: int = 20):
    result = {"pages": pages[skip: skip + limit]}
    # необязательный параметр, если он передан, то добавится ключ add_text
    if add_text:
        result["add_text"] = add_text
    return result


"""
ex4
Булевый тип в параметрах True/False, см примеры url ниже для того, чтобы передать в query True/False
"""


# url для True:
# http://127.0.0.1:8000/ex4/?test=1
# http://127.0.0.1:8000/ex4/?test=true
# http://127.0.0.1:8000/ex4/?test=True
# http://127.0.0.1:8000/ex4/?test=on
# http://127.0.0.1:8000/ex4/?test=yes
# url для False:
# http://127.0.0.1:8000/ex4/?test=0
# http://127.0.0.1:8000/ex4/?test=false
# http://127.0.0.1:8000/ex4/?test=False
# http://127.0.0.1:8000/ex4/?test=off
# http://127.0.0.1:8000/ex4/?test=no
@app.get("/ex4/")
async def ex4(test: bool):
    return {"test": test}


if __name__ == '__main__':
    uvicorn.run(app="lsn2_1:app", reload=True)
