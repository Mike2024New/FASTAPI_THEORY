from passlib.context import CryptContext

"""
механизм хэширования паролей. Хэш пароля создаётся на основании самого пароля и секретного ключа (секретный ключ
хранится только на сервере, что усложняет взлом пароля с помощью радужных таблиц).  Хэшированный пароль не возможно
расшифровать обратно (алгоритм односторонний). В БД на серверах хранятся именно хеши паролей, и когда пользователь
вводит пароль при авторизации на сервере введенный пользователем пароль хэшируется и сравнивается с хэшем существующего
пароля в БД, и если хэши сойдутся, то все ок пользователь авторизуется. Если нет, то пользователю будет отказано в входе
так как пароль не верный.
"""


class HashManager:
    def __init__(self, secret_key: str):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # объект для работы с хэш функциями
        self._secret_key = secret_key  # секретный ключ для усложнения паролей (используется в django,fastapi и так далее)

    def hash_password(self, password_in: str) -> str:
        password_in += self._secret_key
        return self._pwd_context.hash(password_in)

    def verify_password(self, password_checker: str, password_original: str) -> bool:
        password_checker += self._secret_key
        return self._pwd_context.verify(password_checker, password_original)


if __name__ == '__main__':
    # ПРИМЕР ИСПОЛЬЗОВАНИЯ:
    # ВАЖНО!!! Секретные ключи в коде не хранить! Здесь просто показана строка для упрощения примера!
    hash_manager = HashManager(secret_key="secret_key")
    password = hash_manager.hash_password(password_in="secret")  # хеширование пароля для БД
    print(hash_manager.verify_password(password_checker="secret", password_original=password))
