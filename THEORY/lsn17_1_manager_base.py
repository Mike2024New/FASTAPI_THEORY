from UTILS.SQL_ALCHEMY.BASE_CLASS import RootBase, BASE
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.exc import IntegrityError


class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String)


class BaseManager(RootBase):
    def create_user(self, username, hash_password):
        with self._get_session() as session:
            try:
                user = User(username=username, password=hash_password)
                session.add(user)
                session.commit()
            except IntegrityError as err:
                session.rollback()
                print(f"Ошибка при создании пользователя: {err}")
                raise


if __name__ == '__main__':
    pass
