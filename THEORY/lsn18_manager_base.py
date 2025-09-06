from UTILS.SQL_MODEL.BASE_CLASS import RootBase
from sqlmodel import SQLModel, Field, Session
from sqlalchemy.exc import IntegrityError
from pydantic import ConfigDict, BaseModel


# эта модель отвечает за структуру таблицы
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)


# модель выдваемых данных без поля с паролем
class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


# модель для добавления пользователя
class UserInput(BaseModel):
    username: str
    password: str


class BaseManager(RootBase):
    def add_user(self, username: str, password: str) -> User:
        with self.get_session() as session:
            try:
                session: Session  # для удобства, нотации типов иначе редактор не видит её
                user = User(username=username, password=password)
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except IntegrityError as err:
                print(f"Ошибка данный пользователь {username} уже есть в БД.{err}")
                session.rollback()
            except Exception as err:
                print(f"Непредвиденная ошибка при добавлении пользователя с username={username}.{err}")
                session.rollback()


if __name__ == '__main__':
    base_manager = BaseManager(base_path="lsn18_database.db")
    base_manager.add_user(username="Petr", password="qwerty")
