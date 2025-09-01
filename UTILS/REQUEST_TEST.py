from typing import Literal

import requests


def get_request(url):
    # пример обращения к api, get_file
    res = requests.get(url)
    if res.status_code != 200:
        print("Вероятно сервер не запущен, использ команду в терминале \nuvicorn file:app --reload\n")
    return res


# новый метод для выполнения запросов
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
