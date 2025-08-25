from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Вложенные зависимости.
Зависимые функции не связанные на прямую с параметрами также могут содержать дополнительно объявленные в себе параметры.
например функция get_content выдаёт страницы псевдосайта (fake_site_pages), но делает она это на основании фильтров 
которые определены в pages_filters_extract. То есть между функцией операции пути и pages_filters_extract нет прямой 
связи, но при этом параметры объявленные в pages_filters_extract учитываются и отображаются в документации и принимаются
в url. 
"""
fake_site_pages = [f"Контент страницы page_{i + 1}" for i in range(10)]
pages_forbiden = [1, 5]


# самая глубок. зависимость в этом примере, принимает query
def pages_filters_extract(start: int = 1, limit: int = 10):
    return start, limit


# эта зависим. ссылается на другую
def get_content(filter_settings: Annotated[tuple, Depends(pages_filters_extract)]):
    # пример якобы расширенной логики получения данных, и использования подзависимости для получения фильтров
    start = filter_settings[0]
    limit = filter_settings[1]
    content = fake_site_pages[start: start + limit]
    content = [page for page in content if int(page.split("_")[-1]) not in pages_forbiden]
    return {"content": content}


# после внедрения всех зависимостей энпоинт стал достаточно простым и содержит мало кода
# http://127.0.0.1:8000/ex1/
# http://127.0.0.1:8000/ex1/?start=5&limit=3
@app.get("/ex1/")
async def ex1(content: Annotated[dict, Depends(get_content)]):
    return content


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
