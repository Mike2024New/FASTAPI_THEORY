"""
Утилита для копирования полного текста конспекта
версия 1.0 от 01.05.2025
"""
import os


# получение содержимого файла
def get_code_files(file_name):
    try:
        with open(file=file_name, mode="r", encoding="utf-8") as f:
            return f.read()
    except Exception as err:
        raise Exception(f"Произошла ошибка при чтении файла {err}")


# получение дерева проекта и кода всех файлов (кроме тех которые нельзя)
def show_three_project(main_directory, exclude_directory, exclude_files):
    three_project = ""
    code_files = ""
    project_name = os.path.split(main_directory)[-1]

    for root, dirs, files in os.walk(main_directory):
        if any(word in root for word in exclude_directory):
            continue

        directory = os.path.split(root)[-1]
        directory = os.path.join(os.path.split(root)[0], directory)
        directory = directory.replace(main_directory, "")
        directory = project_name + directory
        directory = directory.replace("\\", "/")
        three_project += f"📂 {directory}:\n"

        for file in files:
            if any(word in file for word in exclude_files):
                continue
            file_name = os.path.join(directory, file)
            file_name = file_name.replace("\\", "/")
            code_files += "=" * 50 + f'\nФайл  {file_name}:\n' + "\n"
            code_files += get_code_files(file_name=os.path.join(root, file))
            code_files += "\n\n"

            three_project += f"\t📄 {file}\n"
        three_project += "\n"
    return "\nДерево проекта:\n" + three_project + "\n\n" + code_files


if __name__ == '__main__':
    root_dir = os.path.split(os.getcwd())[0]
    res = show_three_project(
        # main_directory=os.path.join(root_dir, 'THEORY'),
        main_directory=os.path.join(root_dir),
        # main_directory=r"C:\Users\MikeCoder\Documents\LESSONS\PYDANTIC",
        # main_directory=r"C:\Users\MikeCoder\Documents\projects\web_design\THEORY\HTML_THEORY",
        exclude_directory=("idea", "venv", "pycache", ".git", ".venv", ".idea"),
        exclude_files=(".git", "requirements.txt"),
    )
    print(res)
