from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Depends, Query
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""
Использование зависимых (Dependency ijection) классов.
Можно также создавать классы, которые будут общими для путей (в примере ниже показано объединение параметров, но также
в этих классах можно реализовывать различную логику, которая дублируется в эндпоинтах).
Из бонусов к этому использование точечной нотации в маршрутах.
Принимаемые в классах параметры можно также аннотировать и это будет отображаться в документации на docs и redoc.
Для сокращния кода зависимый класс объявляется с помощью: commons: Annotated[DiClass, Depends()]

* Как альтернатива для старых версий можно объявлять: commons : DiClass = Depends(DiClass)
"""

fake_site_pages = [f"Контент страницы page_{i + 1}" for i in range(10)]


class CommonQueryParameters:  # зависимый di класс
    def __init__(self,  # параметры в depends можно также аннотировать, для хорошего отображения в документации
                 secret_page: Annotated[bool, Query(description="секретная страница")] = False,
                 start: Annotated[int, Query(description="стартовая страница")] = 0,
                 limit: Annotated[int, Query(description="количество выдаваемых страниц")] = 10,
                 ):
        self.secret_page = secret_page
        self.start = start
        self.limit = limit


# Примеры url для запроса с использованием query параметров
# http://127.0.0.1:8000/ex1/
# http://127.0.0.1:8000/ex1/?start=5&limit=3
# http://127.0.0.1:8000/ex1/?start=5&limit=3&secret_page=true
@app.get("/ex1/")
async def ex1(commons: Annotated[CommonQueryParameters, Depends()]):
    out_pages = fake_site_pages[commons.start:commons.start + commons.limit]
    if commons.secret_page:
        out_pages.append("Секретная страница")
    return out_pages


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
