from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.testclient import TestClient

"""
Первый урок по тестированию, в fastapi предусмотрен механизм для тестирования.
TestClient из пакета fastapi.testclient, это модуль построенный по аналогии с библиотекой requests.
Преимущество такого подхода заключается в том, что TestClient интегрируется с fastapi приложением и запускает приложение
локально в памяти, без реальных сетевых запросов (как это есть у requests), и запросы выполняются мгновенно.
====================================================================
Внимание для работы тестов, необходимо установить библиотеку httpx:
pip install httpx
"""

app = FastAPI()  # приложение
app.name = "app"
client = TestClient(app)  # приложение тестирования


# маршрут подвергшийся тестированию
@app.get("/")
def home():
    return {"msg": 123}


def test_home():
    response = client.get("/")
    assert response.status_code == 200, f"статус код не равен 200"
    assert response.json().get("msg") == 123, f"сообщение сервера 'msg' не соотвествует заданному 123"


def run_tests():
    test_home()
    print("Тесты завершены успешно!")


if __name__ == '__main__':
    try:
        run_tests()
        app_run(file=__file__, app_name=app.name)
    except AssertionError as err:
        print(f"тесты провалены {err}")
        print(f"Приложение запускать нельзя")
    except Exception as err:
        print(f"Произошла ошибка\n{err}")
        print(f"Приложение запускать нельзя")
