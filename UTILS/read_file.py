import os


def read_file(file_path, encoding="utf-8"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Не найден файл {file_path}!")
    with open(file=file_path, mode='r', encoding=encoding) as f:
        return f.read()


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'read_file.py')
    read_file(file_path=path)
