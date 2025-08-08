import requests
from requests.exceptions import ConnectionError

"""
Ручное тестирование приложения с cookie в bs3, с помощью requests
"""


def example1():
    # шаг 1: авторизация через post запрос с указанием login
    res = requests.post(
        url="http://127.0.0.1:8000/auth/",
        json={"login": "Mike"}
    )
    print(f"{res.status_code} {res.json()}")
    # шаг 2: из полученного запроса нужно сохранить куки (иначе будет ошибка авторизация не прйдена)
    cookies = dict(res.cookies)  # в том числе они хранят id сессии

    # шаг 3: переход на информацию с профилем, чтобы авторизация не слетела нужно передать session_id
    res = requests.get(url="http://127.0.0.1:8000/my_profile/", cookies=cookies)
    print(f"{res.status_code} {res.json()}")
    # шаг 3 вариант 2: (если здесь не передать cookie, то выпадет status код 401)
    res = requests.get(url="http://127.0.0.1:8000/my_profile/")
    print(f"{res.status_code} {res.json()}")
    # шаг 4: использование метода который на сервере редактирует данные
    res = requests.get(url="http://127.0.0.1:8000/set_theme/", cookies=cookies)
    print(f"{res.status_code} {res.json()}")
    # шаг 5: выход из системы
    res = requests.get(url="http://127.0.0.1:8000/logout/", cookies=cookies)
    print(f"{res.status_code} {res.json()}")
    # шаг 6: проверка, что из системы действительно выполнен выход:
    res = requests.get(url="http://127.0.0.1:8000/my_profile/", cookies=cookies)
    print(f"{res.status_code} {res.json()}")


def example2():
    """
    Более правильный и короткий способ ручного тестирования приложения, через request.Sessions, он гарантирует, что
    сессия будет корректно передаваться между запросами со своевременным обновлением данных
    """
    with requests.Session() as session:
        # шаг 1: авторизация через post запрос с указанием login
        res = session.post("http://127.0.0.1:8000/auth/", json={"login": "Mike"})
        print(f"{res.status_code} {res.json()}")
        # шаг 2: переход на информацию с профилем, чтобы авторизация не слетела нужно передать session_id
        res = session.get(url="http://127.0.0.1:8000/my_profile/")
        print(f"{res.status_code} {res.json()}")
        # шаг 3: использование метода который на сервере редактирует данные
        res = session.get(url="http://127.0.0.1:8000/set_theme/")
        print(f"{res.status_code} {res.json()}")
        # шаг 5: выход из системы
        res = session.get(url="http://127.0.0.1:8000/logout/")
        print(f"{res.status_code} {res.json()}")
        # шаг 6: проверка, что из системы действительно выполнен выход:
        res = session.get(url="http://127.0.0.1:8000/my_profile/")
        print(f"{res.status_code} {res.json()}")


if __name__ == '__main__':
    try:
        # example1()  # подробный способ работы с приложением с ручным управлением Cookie
        example2()  # более предподчтительный и автоматизированный способ для работы с Cookie
    except ConnectionError:
        print(f"Время подключения истекло, Вероятно не включен сервер в примере bs3.py")
