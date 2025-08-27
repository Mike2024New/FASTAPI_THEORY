from passlib.context import CryptContext


class HashManager:
    def __init__(self, secret_key: str):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # объект для работы с хэш функциями
        self._secret_key = secret_key  # секретный ключ для усложнения паролей (используется в django,fastapi и так далее)

    def hash_password(self, password_in: str) -> str:
        password_in += self._secret_key
        return self._pwd_context.hash(password_in)

    def verify_password(self, password_checker: str, password_original: str, show_result=False) -> bool:
        password_checker += self._secret_key
        resultat = self._pwd_context.verify(password_checker, password_original)
        if show_result:
            print(resultat)
        return resultat


if __name__ == '__main__':
    # ПРИМЕР ИСПОЛЬЗОВАНИЯ:
    # ВАЖНО!!! Секретные ключи в коде не хранить! Здесь просто показана строка для упрощения примера!
    hash_manager = HashManager(secret_key="secret_key")
    password = hash_manager.hash_password(password_in="secret")  # хеширование пароля для БД
    print(hash_manager.verify_password(password_checker="secret", password_original=password))  # сравнение паролей
