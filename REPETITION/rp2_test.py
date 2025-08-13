from UTILS.FASTAPI_TEST.FASTAPI_TEST_ASSERTION import decorator_run_test_check_list_assertion
from UTILS.FASTAPI_TEST.RUN_TESTS_AND_APP import run_tests_and_app
from rp2 import app
from fastapi.testclient import TestClient

"""
В этом модуле, тесты для приложения из rp2.py
Запуск выполняется через утилиты:
@decorator_run_test_check_list_assertion    - пакетный запуск проверок в рамках одной тестовой функции
run_tests_and_app   -пакетный запуск функций тестирования
"""

client = TestClient(app)


@decorator_run_test_check_list_assertion(description="тесты общего назначения")
def ex1_test_1():
    url = "/ex1/"
    response = client.post(url, json={"figure": {"type_figure": "circle", "radius": 4}})
    json_data = response.json()
    check_list = [
        (response.status_code == 201, "ожидается статус код 201"),
        (isinstance(json_data, dict), "ответ должен быть json объектом"),
        ("description" in json_data, "в json должен содержаться ключ 'description'"),
        ("area" in json_data, "в json должен содержаться ключ 'area'"),
    ]
    return check_list, url


@decorator_run_test_check_list_assertion(description="тесты расчёта прямоугольника")
def ex1_test_2():
    url = "/ex1/"
    response = client.post(url, json={"figure": {"type_figure": "rectangle", "a": 3, "b": 2}})
    json_data = response.json()
    check_list = [
        (json_data.get("description") == "Прямоугольник со сторонами a=3.0, b=2.0",
         "неверное описание, при a=3, b=2 на выходе должно быть 'Прямоугольник со сторонами a=3.0, b=2.0'"),
        (json_data.get("area") == 6, "неверная площадь, при a=3, b=2, площадь должа быть 6"),
    ]
    return check_list, url


@decorator_run_test_check_list_assertion(description="тесты неправильного ввода (прямоугольник)")
def ex1_test_3():
    url = "/ex1/"
    res_a = client.post(url, json={"figure": {"type_figure": "rectangle", "a": "a", "b": 2}})
    res_b = client.post(url, json={"figure": {"type_figure": "rectangle", "a": 2, "b": "b"}})
    res_c = client.post(url, json={"figure": {"type_figure": "test", "a": 2, "b": 3}})
    check_list = [
        (res_a.status_code == 422, "не верный статус код при неверно введенном параметре a"),
        (res_b.status_code == 422, "не верный статус код при неверно введенном параметре b"),
        (res_c.status_code == 422, "не верный статус код при неверно введенном параметре type_figure"),
    ]
    return check_list, url


@decorator_run_test_check_list_assertion(description="тесты расчёта круга")
def ex1_test_4():
    url = "/ex1/"
    response = client.post(url, json={"figure": {"type_figure": "circle", "radius": 4}})
    json_data = response.json()
    check_list = [
        (json_data.get("description") == "Окружность с радиусом 4.0",
         "Неверное описание модели, для круга с радиусом 4, оно должно быть 'Окружность с радиусом 4.0'"),
        (json_data.get("area") == 50.24, "не верное значение площади, для круга с радиусом 4, должно быть 50.24")
    ]
    return check_list, url


@decorator_run_test_check_list_assertion(description="тесты неправильного ввода (круг)")
def ex1_test_5():
    url = "/ex1/"
    res1 = client.post(url, json={"figure": {"type_figure": "circle", "radius": "F"}})
    res2 = client.post(url, json={"figure": {"type_figure": "none", "radius": 4}})
    check_list = [
        (res1.status_code == 422, "не верный статус код при неверно введенном параметре радиуса"),
        (res2.status_code == 422, "не верный статус код при неверно введенном параметре type_figure"),
    ]
    return check_list, url


if __name__ == '__main__':
    run_tests_and_app(
        tests_funcs=[ex1_test_1, ex1_test_2, ex1_test_3, ex1_test_4, ex1_test_5],
        app_file=__file__,
        app_name=app.name,
        app_start=True
    )
