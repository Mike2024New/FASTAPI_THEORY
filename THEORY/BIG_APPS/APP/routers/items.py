from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header  # относительный импорт из родительского пакета (на уровень выше)

# общее применение настроек ко всем маршрутам определенным далее
router = APIRouter(
    prefix="/items",  # такой путь будет достроен к домену, связывая его и маршруты определенные здесь в модуле
    tags=["items"],  # общие теги, которые теперь применятся к всем маршрутам ниже
    dependencies=[Depends(get_token_header)],  # depends будет применена ко всем маршрутам (но ни чего не возвращает)
    responses={404: {"descrpition": "Not found"}}  # общий вариант возвращаемого заголовка (для openAPI документации)
)

fake_items_db = {"Mike": {"name": "Михаил"}, "Ivan": {"name": "Иван"}, "Maria": {"name": "Мария"}, }


@router.get("/")  # -> "http://127.0.0.1:8000/items/" (так как /items указан в prefix)
async def read_items():
    return fake_items_db


@router.get("/{item_id}")  # -> "http://127.0.0.1:8000/items/1/" (так как /items указан в prefix)
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail={"Item not found"})


@router.put("/{item_id}", tags=["custom_items"], responses={403: {"description": "Operation forbidden"}})
async def update_item(item_id: str):
    if item_id != "Mike":
        raise HTTPException(
            status_code=403, detail="Можно обновить только пользователя Mike."
        )
    return {"item_id": item_id, "name": "Данные изменены"}
