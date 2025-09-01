import time
from typing import Literal

import requests

"""
Демонстрация того как работает клиент с сервером из lsn14_3.py
"""


def execute_requests(url, data: dict | None = None, json: dict | None = None, headers: dict | None = None,
                     method: Literal["get", "post"] = "get", show_result=False):
    req_result = None
    try:
        if method == "get":
            req_result = requests.get(url=url, headers=headers)
        elif method == "post":
            req_result = requests.post(url, headers=headers, data=data, json=json)
        if req_result.status_code != 200:
            print(f"!Ошибка запроса {req_result.status_code}!")
            return req_result.json()
    except Exception as err:
        print(err)
        raise
    if show_result:
        print(req_result.status_code)
        print(req_result.json())
    return req_result


# Шаг1: перейти на страницу с авторизацией
res = execute_requests(
    url="http://127.0.0.1:8000/login/", data={"username": "ivan25@", "password": "secret"},
    method="post", show_result=True
)
# Шаг2: токен нужно сохранить и использовать его в последующих запросах без необходимости по новой авторизовываться
# токен передаётся в заголовках в виде authorisation Bearer
token = res.json().get("access_token")  # получение токена
# Шаг 3: выполнить запрос к защищённому маршруту с использованием токена в заголовке
time.sleep(10)
execute_requests(
    url="http://127.0.0.1:8000/ex2/ivan25@/", method="get",
    headers={"Authorization": f"Bearer {token}"}, show_result=True
)
