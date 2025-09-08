from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
import sqlite3
import re


def regexp(expr, item):
    if item is None:
        return False
    try:
        return re.search(expr, item) is not None
    except re.error:
        return False


class RootBase:
    def __init__(self, base_path: str, echo=False):
        self.__engine = create_engine(f"sqlite:///{base_path}", echo=echo)
        SQLModel.metadata.create_all(bind=self.__engine)

    @contextmanager
    def get_session(self):
        with Session(self.__engine) as session:
            yield session

    def __init_settings_bd(self):
        """Здесь можно добавить пользовательские функции, например для того же sqlite3, который не корректно работает
        с кириллицей на регистро независимом поиске, для этого здесь переопределены функции LOWER, UPPER, но можно также
        добавлять и другие функции"""

        # noinspection PyUnusedLocal
        @event.listens_for(self.__engine, "connect")
        def connect(dbapi_connection, connection_record):  # параметр connection_record не используется
            if isinstance(dbapi_connection, sqlite3.Connection):  # настройки для sqlite3
                # установка первичного ключа, для того, чтобы в связанных таблицах данные не создавались при отсутствии
                # связанных полей в главных таблицах
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON;")
                cursor.close()
                # добавить функцию LOWER для регистро независимого поиска
                dbapi_connection.create_function(
                    "LOWER", 1, lambda string: string.lower() if isinstance(string, str) else string
                )  # Параметры: 1)название функции, 2)количество аргументов которое она принимает, 3)сама функция
                # добавить функцию UPPER для регистро независимого поиска
                dbapi_connection.create_function(
                    "UPPER", 1, lambda string: string.upper() if isinstance(string, str) else string
                )  # Параметры: 1)название функции, 2)количество аргументов которое она принимает, 3)сама функция
                # функция для поддрежки регулярных выражений в sqlite
                dbapi_connection.create_function(
                    "REGEXP", 2, regexp
                )
