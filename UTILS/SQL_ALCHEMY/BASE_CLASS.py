from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlite3
import re

"""
Реализация работы с БД через класс как универсальный менеджер.
Этот класс инициализирует первичные настройки БД, создаёт таблицы, и выдаёт сессии при запросе из метода _get_session, 
важно, нужно использовать сессии в менеджере контекста, и обеспечить им обработку _callback и _rollback в идемпотентных
методах (которые изменяют данные в БД)
"""


def regexp(expr, item):
    if item is None:
        return False
    try:
        return re.search(expr, item) is not None
    except re.error:
        return False


# ШАГ 1: создать фундаментальный объект работы с БД
BASE = declarative_base()


# ШАГ 2: Определить системный класс который выполняет общие настройки и выдаёт рычаги управления, а также создаёт сессию
# в методе _get_session, для последующих подключений
class RootBase:
    def __init__(self, base_path):
        self.__engine = create_engine(f"sqlite:///{base_path}")
        self.__init_settings_bd()  # добавление пользовательских функций к БД
        BASE.metadata.create_all(self.__engine)
        self.__Session = sessionmaker(bind=self.__engine)  # фабрика каждый раз будет создавать новый объект engine

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

    def _get_session(self):
        """важно! Для web приложений сессия должна пересоздаваться для новых запросов, этот метод реализует это"""
        return self.__Session()


if __name__ == '__main__':
    pass
