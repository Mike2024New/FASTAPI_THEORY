# uvicorn THEORY.lsn1_4:app --reload
from fastapi import FastAPI
from UTILS.REQUEST_TEST import get_request

app = FastAPI()

"""
Опция starlette -> path.
Пути в параметрах пути, бывает такая ситуация, что необходимо в url передать путь к ресурсу, но ведь пути содержат 
символы "/", что как бы ломает маршрут. Для этого нужно определить префиксную часть, а после указать параметр path 
который принимает путь на вход и использовать для этого опцию starlette -> path, это обозначит, что внутри этого 
параметра можно будет пробрасывать пути.
Также можно комбинировать параметры path с путем и другие, см. обработчик get_img
В таком случае если есть ещё более общий случай (как select_directory) то нужно общий случай помещать в самом низу
иначе он будет перехватывать запросы и с другими параметрами, так как может их интерпретировать как пути.
"""


# ВАЖНО! УЧИТЫВАТЬ ПОРЯДОК РАЗМЕЩЕНИЯ МАРШРУТОВ С УЧЁТОМ БОЛЕЕ СПЕЦИФИЧНЫЕ МАРШРУТЫ (КОТОРЫЕ ЯВЛЯЮТСЯ ЧАСТНЫМИ СЛУЧАЯМИ
# ОБЩИХ) В ВЕРХУ, ОБЩИЕ В НИЗУ.

# параметр Path с указанным путём в ulr комбинированный с простым path параметром
# комбинированный url который содержит несколько параметров пути
@app.get("/images/{directory:path}/img/{img_num}/")
async def get_img(directory: str, img_num: int):
    """
    Пример url для теста:
    http://127.0.0.1:8000/images/animals/funny_cats/img/2/
    """
    return f"Получено изображение {img_num} из директории {directory}"


# этот пример более простой он содержит только путь (должен находиться после более персонализированного url в
# обработчике get_img, так как url типа http://127.0.0.1:8000/images/animals/funny_cats/img/2/, будет представлен
# полностью как путь animals/funny_cats/img/2/ в обработчике select_directory
@app.get("/images/{directory:path}/")
async def select_directory(directory: str):
    """
    Пример url для теста
    http://127.0.0.1:8000/images/animals/funny_cats/
    """
    return f"Выбрана директория {directory}"


def test_case():
    """
    Небольшой тест кейс эндпоинтов, тоже самое можно сделать и из строки браузера и из интерактивной документации docs
    Пока что тесты реализованы на requests, в дальнейшем для этого будет изучен модуль fastapi.testcliend
    """
    # пример теста url обработчика select_directory
    res = get_request(url="http://127.0.0.1:8000/images/animals/funny_cats/")
    assert res.text == "\"Выбрана директория animals/funny_cats\""  # fastapi возвращает под капотом json строку с кавычками
    # пример теста url обработчика get_img
    res = get_request(url="http://127.0.0.1:8000/images/animals/funny_cats/img/3/")
    assert res.text == "\"Получено изображение 3 из директории animals/funny_cats\""


if __name__ == '__main__':
    test_case()
