import requests


def get_request(url):
    # пример обращения к api, get_file
    res = requests.get(url)
    if res.status_code != 200:
        print("Вероятно сервер не запущен, использ команду в терминале \nuvicorn file:app --reload\n")
    return res
