import re
from functools import wraps

"""
Дополнительный материал к теории
В этом примере предоставлена упрощенная модель fastapi, как в нем реализован паттерн декораторов, например как он 
под капотом связывает url и функцию обработчик, как извлекает параметры пути.

Есть класс Fastapi, который внутри себя содержит регистратор маршрутов routes в котором хранится связка url->обработчик, 
методы (get,post,put,delete и другие), а также метод с запуском simulate_request, который при входном url находит 
обработчик если он есть, и выдаёт результат, а точнее активирует функцию обработчик.

--------------------------------------------------------------------------------
Модель сильно упрощена! Логика работы fastapi, на много сложнее, там под капотом и валидация через pydantic и ядро в
виде starlette и многое другое. Данный пример лишь для общего понимания а как устроен паттерн на базовом уровне 
абстракции.
"""


class Fastapi:
    def __init__(self):
        self.routes = {}  # здесь хранятся связи url и функций обработчиков этих url

    def get(self, url):
        def decorator(func):
            # при инициализаторе декоратора, происходит добавление маршрута и его обработчика в routes
            self.routes[url] = func
            # сбор параметров пути, если они есть
            path_parametrs = re.findall(r"{(.+?)}", url)

            @wraps(func)
            def wrapper(*args, **kwargs):
                if not kwargs and path_parametrs:
                    raise ValueError(f"Не переданы параметры пути")
                for parametr in kwargs:
                    if parametr not in path_parametrs:
                        raise ValueError(f"Непредвиденный параметр {parametr}")
                ...  # здесь внутренняя логика fastapi, c валидацией на pydantic
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def simulate_request(self, url: str, **kwargs) -> None:
        # в этой точке, якобы из браузера отправляется запрос, происходит обработка введенного url по соотвествующему
        # маршруту
        func = self.routes.get(url)
        if not func:
            raise ValueError("Маршрут не найден, статус код 404")
        return func(**kwargs)


app = Fastapi()


# url с фиксированным путем
@app.get("/")
def home():
    print(f"Добро пожаловать на главную страницу сайта")


# url с path параметром
@app.get("/posts/{post_id}/")
def posts(post_id: int):
    print(f"Страница {post_id}")


if __name__ == '__main__':
    # это иммитация перехода на url из строки браузера
    app.simulate_request("/")
    app.simulate_request("/posts/{post_id}/", post_id=10)
