import os
from typing import Literal


class WorkFile:
    def __init__(self, file_path: str):
        self._file_path = file_path

    def read_file(self, encoding: str = "utf-8", split_row: bool = False) -> str | list[str]:
        if not os.path.exists(self._file_path):
            raise FileNotFoundError(f"Не найден файл {self._file_path}!")
        with open(file=self._file_path, mode='r', encoding=encoding) as f:
            content = f.read()
            content = content.split("\n") if split_row else content  # разделить текст на строки
            return content

    def rec_file(self, data: str, encoding: str = "utf-8", mode: Literal["a", "w"] = "a", new_row: bool = True) -> None:
        """
        запись данных в файл, в режиме 'a' - добавить к записи, 'w'- перезаписать
        по умолчанию текст добавляется с новой строки
        """
        data = "\n" + data if new_row else data  # добавить перенос на новую строку
        with open(file=self._file_path, mode=mode, encoding=encoding) as f:
            f.write(data)

    def is_find_string_in_file(self, string: str) -> bool:
        """проверка содержится ли строка в тексте (можно использовать проверку для листа токенов)"""
        content = self.read_file(split_row=False)  # проверка совпадения по целому тексту
        return string in content


def read_file(file_path, encoding="utf-8"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Не найден файл {file_path}!")
    with open(file=file_path, mode='r', encoding=encoding) as f:
        return f.read()


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'work_file.py')
    read_file(file_path=path)
