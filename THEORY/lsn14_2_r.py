import requests

"""
Приложение к уроку lsn14_2.py, показана клиентская сторона в действии
"""

# шаг1: клиент авторизовывается введя свои учетные данные (поля должны строго называться username и password)
url_token = "http://127.0.0.1:8000/token/"
res = requests.post(url_token, data={"username": "Mike", "password": "secret"})
print(f"Авторизация: статус-код:{res.status_code}, ответный json:{res.json()}")
# шаг2: авторизация вернула токен, сохранить его (в браузере он просто устанавливается в заголовке)
token = res.json().get("acces_token")
# шаг3: переход к контенту отображаемому авторизованным пользователям, с использованием токена
url_get_user = "http://127.0.0.1:8000/ex1/"
res = requests.get(url_get_user, headers={"authorization": f"Bearer {token}"})
print(f"Мой профиль: статус-код:{res.status_code}, ответный json:{res.json()}")
