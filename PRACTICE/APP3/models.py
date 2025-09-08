from sqlmodel import create_engine, SQLModel, Field
from pydantic import BaseModel, ConfigDict


class User(SQLModel, table=True):  # структура таблицы в БД
    id: int | None = Field(default=None, primary_key=True)
    login: str = Field(nullable=False, unique=True, max_length=50)
    password: str = Field(nullable=False, min_length=8, max_length=50)


class UserIn(BaseModel):  # модель для добавления нового пользователя и полного обновления уже сущ. пользователя
    login: str = Field(nullable=False, max_length=50)
    password: str = Field(nullable=False, min_length=8, max_length=50)


class UserRead(BaseModel):  # безопасная модель (без пароля) для отправки клиенту
    id: int
    login: str
    model_config = ConfigDict(from_attributes=True)  # разрешить на вход не только json но и классы (др. модели)


class UserUpdate(BaseModel):  # Эта модель для частичного обновления пользователя
    login: str | None = None
    password: str | None = None


connect_args = {"check_same_thread": False}  # разрешить Fastapi работать с БД из разных потоков
engine = create_engine(url="sqlite:///database.db", connect_args=connect_args)
