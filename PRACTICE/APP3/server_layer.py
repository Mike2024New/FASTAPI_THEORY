from models import User, UserIn, UserRead, UserUpdate, engine
from sqlmodel import SQLModel, Session, select
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from typing import Annotated


# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/

# noinspection PyUnusedLocal
@asynccontextmanager
async def on_startup(application: FastAPI):
    # действия при запуске приложения fastapi...
    SQLModel.metadata.create_all(engine)  # инициализация БД (если её вдруг нет), создание таблиц если их ещё нет
    yield
    # действия после завершения работы приложения fastapi...


def get_session():  # выдать сессию на 1 запрос пользователя
    with Session(engine) as session:
        yield session


SessionDepends = Annotated[Session, Depends(get_session)]  # общая зависимость для получения сессии

app = FastAPI(lifespan=on_startup)


def create_model_user_read(user: User):
    return UserRead.model_validate(user)  # ВАЖНО! Для такого способа, у модели UserRead разрешить from_attributes


# http://127.0.0.1:8000/users/?limit=1
# выполнение select запроса в БД, получение всех пользователей из таблицы
@app.get("/users/", response_model=list[UserRead])
def get_all_users(session: SessionDepends, offset: int = 0, limit: int = 100):
    statement = select(User)  # select формирует select запрос -> аналог SELECT * FROM users
    statement = statement.offset(offset)
    statement = statement.limit(limit)
    users = session.exec(statement).all()  # exec -> применяет запрос в БД (по аналогии с sqlite cur.execute)
    # для корректной выдачи пользователей на выходе из модели, нужно выполнить преобразование, чтобы
    # выполнялось условие которое записано в response_model (в данном случае список моделей UserRead).
    users = [create_model_user_read(user) for user in users]  # преобразование в вых список UserRead
    return users


# Post запрос для добавления нового пользователя
@app.post("/users/", response_model=UserRead)
def create_user(user: UserIn, session: SessionDepends):
    user = User.model_validate(user)  # из входной модели создаётся ORM модель
    session.add(user)  # модель добавляется в БД
    session.commit()  # изменения применяются
    # в user модель обновляется то есть получает созданные в БД поля (в данном случае id через autoincrement)
    session.refresh(user)  # обновление модели
    # выходная модель явным образом указывается та которая безопасна (не содержит password)
    return create_model_user_read(user)


def get_user_by_id(user_id: int, session: SessionDepends):
    # общая функция для получения пользователя из БД
    user = session.get(User, user_id)  # получение пользователя из БД с конкретным id
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


GetUserDependency = Annotated[get_user_by_id, Depends()]  # общая зависимость для получения пользователя


# http://127.0.0.1:8000/users/1/
@app.get("/users/{user_id}/", response_model=UserRead)
def get_user_by_id_from_base(user: GetUserDependency):
    # пользователь user получен в зависимости get_user_by_id
    return create_model_user_read(user)


def update_user_common(user: User, update_data: dict, session: SessionDepends):
    # обновление пользователя
    for key, value in update_data.items():
        setattr(user, key, value)  # у модели полученной из БД, user перезаписываются поля
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.put("/users/", response_model=UserRead)
def update_user(user: GetUserDependency, user_input: UserIn, session: SessionDepends):
    # пользователь user получен в зависимости get_user_by_id
    update_data = user_input.model_dump()
    user = update_user_common(user, update_data, session)  # логика обновления пользователя вынесена в общий метод
    return create_model_user_read(user)


@app.patch("/users/", response_model=UserRead)
def update_user_partial(user: GetUserDependency, user_update: UserUpdate, session: SessionDepends):
    # пользователь user получен в зависимости get_user_by_id
    update_data = user_update.model_dump(exclude_unset=True)  # отсечь поля которые не были переданы в модель
    user = update_user_common(user, update_data, session)  # логика обновления пользователя вынесена в общий метод
    return create_model_user_read(user)


@app.delete("/users/", response_model=UserRead)
def delete_user(user: GetUserDependency, session: SessionDepends):
    out_user = create_model_user_read(user)  # заранее сделать снимок модели перед удалением
    session.delete(user)  # тупо удалить пользователя полученного по id
    session.commit()  # применить изменения
    return out_user


if __name__ == '__main__':
    uvicorn.run(app="server_layer:app", reload=True)
