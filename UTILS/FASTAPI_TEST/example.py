from UTILS.APP_RUN import app_run
from UTILS.FASTAPI_TEST.FASTAPI_TEST_ASSERTION import decorator_run_test_check_list_assertion
from fastapi import FastAPI
from fastapi.testclient import TestClient

"""
Пример использования декоратора run_test_check_list_assertion
для выполнения Asertion запросов
"""

app = FastAPI()  # приложение
app.name = "app"
client = TestClient(app)  # приложение тестирования


# маршрут подвергшийся тестированию
@app.get("/")
def home():
    return {"msg": 123}


@decorator_run_test_check_list_assertion
def test_home():
    """
    тестирование маршрута http://127.0.0.1:8000/
    :return None, возбуждает исключение AssertionError, если тесты не прошли
    """
    url = "/"
    response = client.get(url)
    tests = [
        (response.status_code == 200, f"статус код не равен 200"),
        (response.json().get("msg") == 123, f"сообщение сервера 'msg' не соотвествует заданному 123"),
    ]
    return tests, url


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
