import uuid
import base64

"""
генерация рандомного ключа, вынесено в отдельную утилиту после написания сократителя url в APP1
"""


def generate_random_key_uuid(length: int = 4) -> str:
    """
    генерация уникального значения uuid
    :param length: длина ключа
    :return: сгенерированное рандомное значение
    """
    short_bytes = uuid.uuid4().bytes[:length]
    short_key = base64.urlsafe_b64encode(short_bytes).decode('utf-8').rstrip("=")
    return short_key


if __name__ == '__main__':
    res = generate_random_key_uuid(length=32)
    print(res)
