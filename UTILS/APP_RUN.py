import os
import uvicorn
from dataclasses import dataclass, asdict


@dataclass
class UvicornParameters:
    reload: bool = True
    host: str = "127.0.0.1"
    port: int = 8000


def get_file_name(file: str, extension_del=False) -> str:
    """
    Вспомогательная функция, которая возвращает имя файла без расширений (опция)
    :param file: путь к файлу
    :param extension_del: удалять расширение файла
    :return: строка с именем файла, с/без расширения
    """
    file = os.path.abspath(file)
    if not os.path.exists(file):
        raise ValueError(f"Файл {file} не существует")
    file_name = os.path.basename(file)
    file_name = os.path.splitext(file_name)[0] if extension_del else file_name
    return file_name


def app_run(file: str, app_name: str, uv_parametrs: UvicornParameters | None = None, **kwargs):
    """
    Универсальный запуск приложения fastapi без привязки к имени файла
    Премимущества такого подхода -> Делает запуск более устойчивым к переименованиям и перемещениям файлов,
    так как нет фиксированных строк.
    :param file: __file__ (ссылка на текущий файл)
    :param app_name: название приложения, крайне рекомендуется для удобства в екземляре Fastapi создавать доп ключ с
    именем приложения, например: app = Fastapi(), -> app.name = "app" и уже эту переменную передавать как app_name
    :param uv_parametrs: передача параметров через Dataclass UvicornParametrs
    ** Также параметры можно пробросить через **kwargs -> эти значения имеют высший приоритет
    (при совпадении параметров uv_parameters и kwargs приоритет отдаётся kwargs)
    :return: None, просто выполняет запуск приложения с помощью uvicorn.
    Пример вызова функции:
        Шаг1: создание приложения:
        app = Fastapi()
        app.name = "app"
        Шаг2: запуск приложения:
        app_run(file = __file__, app_name = app.name)
    --------------------------------------------------------------------
    Функция может быть заменена в коде приложения fastapi строкой:
    uvicorn.run(app="file_name:app_name") # и параметры, например reload=True
    """
    if uv_parametrs is None:
        uv_parametrs = UvicornParameters()
    file_name = get_file_name(file=file, extension_del=True)
    uv_parametrs = asdict(uv_parametrs)
    for key in uv_parametrs:
        if key not in kwargs:  # чтобы не перебивать переданные дополнительные параметры в kwargs
            kwargs[key] = uv_parametrs[key]
    app = f"{file_name}:{app_name}"
    print(f"Запуск uvicorn с параметрами: app={app}, options={kwargs}")
    uvicorn.run(app=app, **kwargs)


if __name__ == '__main__':
    res = get_file_name(file=__file__, extension_del=True)
    print(res)
