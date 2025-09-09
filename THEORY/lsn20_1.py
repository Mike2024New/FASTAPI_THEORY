from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from enum import Enum

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/

description = """
## Разделы api
**users** - описание взаимодействия с маршрутами users
**items** - описание взаимодействия с маршрутами items
"""


class Tags(Enum):
    items = "items"
    users = "users"


# тегам для url можно также добавить описание и оно отобразится в api
tags_metadata = [
    {
        "name": Tags.users,
        "description": "Операции редактирования пользователей"
    },
    {
        "name": Tags.items,
        "description": "Операции с блоком items",
        "externalDocs": {  # в том случае если информация о данном теге хранится на другом url
            "description": "Описание хранится на внешнем url",
            "url": "http://example.com/my-app/items/"
        }
    }
]

# Приложение app при инициализации можно заполнить подробной мета информацией. Такой как описание всего приложения,
# ссылки на контакты и условия использования на информацию об используемой лицензии и так далее.
app = FastAPI(
    title="Название приложения",
    description=description,  # поддерживаются markdown
    summary="Краткое описание приложения",
    version="0.0.1",  # эта версия отобразится рядом с заголовком названия приложения
    terms_of_service="http://example.com/my-app/terms/",  # ссылка на страницу с условиями использования api
    contact={
        "name": "Иван Петрович",
        "url": "http://example.com/my-app/ivan_petrovich/",
        "email": "ivan_petrovich@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    # здесь указывается open api схема адрес (в данном случае указан тот который по умолчанию)
    openapi_url="/openapi.json",
    docs_url="/docs",  # здесь можно отключить docs указав None и указать другой url с документацией.
    redoc_url=None,  # здесь можно отключить redoc указав None и указать другой url с документацией.
)
app.name = "app"


@app.get("/items/", tags=[Tags.items, ])
async def read_items():
    return [{"name": "Mike"}, {"name": "Ivan"}]


@app.get("/users/", tags=[Tags.users, ])
async def get_users():
    return [{"name": "Mike"}, {"name": "Ivan"}]


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
