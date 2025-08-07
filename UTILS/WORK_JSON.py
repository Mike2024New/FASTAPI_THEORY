import json
import os
import warnings

"""
реализовать декоратор для многопоточности от одновременного доступа нескольких пользователей к одному файлу записи
"""


class WorkJson:
    def __init__(self, file_path: str, reset_file: bool = False, data: dict | None = None,
                 show_warning: bool = True) -> None:
        """

        :param file_path: путь к файлу с названием файла, (если каталог текущий то можно просто название файла)
        :param reset_file: сбросить json файл? устанавливает {} или начальную структуру из data
        :param data: начальная структура json файла, например: {"done":{},"pending":{}}
        :param show_warning: выводить предупреждение?
        """
        # проверка, что директория существует
        directory = os.path.split(file_path)[0]
        if directory != "" and not os.path.exists(directory):
            raise FileNotFoundError(f"Не найдена директория: '{directory}'")
        self._file_path = file_path
        if not os.path.exists(self._file_path) or reset_file:
            self.rec_json_file(
                data=data if data else {}
            )
            return
        if data and show_warning:
            warnings.warn(
                "(WorkJson инициализация) указана новая структура json в поле 'data', "
                "но файл уже существует и флаг 'reset_file' не установлен... Если вы уверены в необходимости"
                "перезаписи, то установите флаг reset_file в 'True'.",
                stacklevel=2  # будет указана именно строка вызова всего метода
            )

    def rec_json_file(self, data: dict | str) -> None:
        """
        Запись данных в json
        :param data: словарь или json строка
        :return: None
        """
        try:
            with open(self._file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as err:
            raise Exception(f"Ошибка при чтении json {err}")

    def read_json_file(self) -> dict:
        """
        Чтение json файла
        :return: возвращает json преобразованный в dict
        """
        try:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self._file_path} не найден.")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Ошибка при разборе JSON: {e.msg}", e.doc, e.pos
            ) from e
        except Exception as e:
            raise Exception(f"Произошла непредвиденная ошибка: {e}")


if __name__ == '__main__':
    js = WorkJson(
        file_path=os.path.join(os.getcwd(), 'test_json', 'test.json'),
        data={"archive": {}, "process": {}},
        reset_file=False,
        show_warning=False,  # если нужно отключить предупреждение о поле data
    )
    js.rec_json_file(data={"archive": {"tst": "123"}, "process": {}})
