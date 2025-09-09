from fastapi.testclient import TestClient
from THEORY.BIG_APPS.APP2.main import app  # для возможности запуска именно отсюда сделан абсолютный импорт

"""
Этот модуль отвечает за тесты api ручек. Создается экземпляр TestClient и через него выполняются запросы. Механика такая
же как и с библиотекой requests. Тесты выполняются с помощью assert.
Если после запуска из main (либо через pytest) ни чего не произойдёт значит тесты прошли отлично.
При запуске тестов через pytest будет выведен такой результат:

============================= test session starts =============================
collecting ... collected 4 items

test_main.py::test_read_user PASSED                                      [ 25%]
test_main.py::test_read_user_bad_token PASSED                            [ 50%]
test_main.py::test_read_user_nonexistent_user PASSED                     [ 75%]
test_main.py::test_read_user_no_token PASSED                             [100%]

============================== 4 passed in 0.33s ==============================

Что обозначает, что тесты прошли корректно.

Важно также:
функции тестирования должны начинаться со слова test, такова договоренность pytest. Также это поможет запускать тесты
при использовании утилиты pytest, такие функции автоматически будут распознаваться. Следом идёт название тестируемой 
функции (api ручки), за тем что этот тест делает.
Например:
test_read_user_novalid_token , где test указывает, что это тестируемая функция, read_user указывает название 
тестируемого маршрута. novalid_token указывает, что идёт тестирование некоректно введенного токена 
"""

client = TestClient(app)  # создать экземпляр приложения


def test_read_user() -> None:
    """
    Тест получения пользователя по идентификатору
    """
    response = client.get("/users/Mike", headers={"X-token": "test_token"})
    assert response.status_code == 200
    assert response.json() == {
        "login": "Mike",
        "fullname": "Михал Палыч",
        "age": 35,
        "city": "Москва"
    }


def test_read_user_bad_token() -> None:
    """тестирование переданного токена"""
    response = client.get("/users/Mike", headers={"X-token": "qwerty"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_user_nonexistent_user() -> None:
    """тестирование обращения к несуществующему пользователю"""
    response = client.get("/users/Fedor", headers={"X-token": "test_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "user login=`Fedor` not exists"}


def test_read_user_no_token() -> None:
    """тестирование, что будет если не передать токен"""
    response = client.get("/users/Mike", headers={})
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'type': 'missing', 'loc': ['header', 'x-token'], 'msg': 'Field required', 'input': None}]
    }


if __name__ == '__main__':
    test_read_user()
    test_read_user_bad_token()
    test_read_user_nonexistent_user()
    test_read_user_no_token()
