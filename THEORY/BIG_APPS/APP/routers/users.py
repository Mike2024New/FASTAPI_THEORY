from fastapi import APIRouter

"""
APIRouter можно представить как урезанная версия FastAPI(). Этот объект нужен для того, чтобы прописывать маршруты в 
отдельных модулях пакетов, а потом подключать эти маршруты в главном приложении. То есть сами по себе APIRouter не 
запускаются их нужно потом добавлять в основное FastAPI приложение через include_router.
Router также поддерживают зависимости Depends, теги и теже параметры что и стандартные FastAPI маршруты.
-------------------
Назначение APIRouter - вынос логики объявления маршрутов в отдельные пакеты без запуска.
"""
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Михаил"}, {"username": "Василиса"}, ]


@router.get("/users/me", tags=["users"])
async def read_user_my():
    return {"username": "Текущий пользователь"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
