import jwt
from datetime import datetime, timedelta, timezone


class JWTManager:
    def __init__(self, secret_key: str, token_action: timedelta = timedelta(minutes=30), algoritm="HS256"):
        self._secret_key = secret_key
        self._token_action = token_action
        self._algoritm = algoritm

    def create_token(self, data: dict):
        """
        создание токена, токен создаётся из 3 компонентов разделенных ".", где:
        1. HEADER -  в нем находится метаинформация, алгоритм и тип, например: {'alg': 'HS256', 'typ': 'JWT'}
        формируется автоматически.  (в токене хранится в незашифрованном виде а лишь в кодированном в base64
        виде, и человек получивший токен может декодировать эту часть и прочитать её значения).

        2. PAYLOAD - полезная нагрузка, в нем хранятся дата создания токена ключ "iat", и через какое время токен
        истечет в ключе "exp", а также информация переданная сервером например имя пользователя и его права на сервере
        или информация о подписке и так далее. (в токене хранится в незашифрованном виде а лишь в кодированном в base64
        виде, и человек получивший токен может декодировать эту часть и прочитать её значения).

        3. SIGNATURE - цифровая подпись, эта часть создаёт хеш который вычисляется из HEADER+PAYLOAD+SECRET_KEY. То есть
        если даже злоумышленник получит доступ к токену и изменит первые две части (которые хранятся в незашифрованном
        виде а лишь в кодировке base64), то при получении такого токена сервером, алгоритм jwt увидит, что цифровая
        подпись (вычисленная из HEADER+PAYLOAD+SECRET_KEY) не совпадёт с первыми двумя компонентами, так как их
        обновленный хэш не будет совпадать с исходным и выдаст информацию об ошибке, что токен не валидный.
        """
        iat = datetime.now(timezone.utc)  # явное указание, что это стандартное мировое время UTC.
        exp = iat + self._token_action
        payload = {
            "iat": iat,  # текущее время в секундах в сек. с 01.01.1970
            "exp": exp,  # вермя действия токена в сек. с 01.01.1970
        }
        payload.update(data)  # добавление пользовательских данных
        token_out = jwt.encode(payload, self._secret_key, algorithm=self._algoritm)
        return token_out

    def _decode_token(self, token_in) -> dict:
        """
        # декодирование токена из байтов обратно в строку
        :param token_in: токен, формата "header.payload.signature"
        :return: возвращает данные из .payload.
        """
        decoded = jwt.decode(
            token_in,
            self._secret_key,
            algorithms=[self._algoritm],
            options={"verify_exp": True},  # провеярть дату токена
            leeway=10,  # разрешить просрочку токена (время в секундах)
        )
        return decoded

    def verify_token(self, token_in) -> None:
        """
        Проверка валидности токена - под капотом при декодировке алгоритм jwt создаёт хэш из первых двух компонентов
        header и payload с присадкой в виде секретного ключа, и смотрит сходится ли этот хэш с переданным в проверяемом
        токене хэшем и если нет, то выбрасывает исключение jwt.InvalidTokenError
        """
        try:
            self._decode_token(token_in)  # проверка что токен декодируется
        except jwt.ExpiredSignatureError:  # здесь зашита проверка времени действия токена
            raise jwt.ExpiredSignatureError("Срок действия токена истёк")
        except jwt.InvalidTokenError:  # проверка правильности написания токена
            raise jwt.InvalidTokenError("Невеный токен")

    def get_payload_from_token_verify(self, token_in: str) -> dict:
        self.verify_token(token_in=token_in)  # проверка валидности токена
        return self._decode_token(token_in)


if __name__ == '__main__':
    # ПРИМЕР ИСПОЛЬЗОВАНИЯ:
    # ВАЖНО!!! Секретные ключи в коде не хранить! Здесь просто показана строка для упрощения примера!
    jwt_manager = JWTManager(secret_key="secret")
    token = jwt_manager.create_token(data={"login": "iv25@", "role": "admin"})
    print(token)
    res = jwt_manager.get_payload_from_token_verify(token_in=token)
    # print(res)
