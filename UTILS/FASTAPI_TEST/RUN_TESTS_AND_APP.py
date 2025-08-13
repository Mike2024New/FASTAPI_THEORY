from UTILS.APP_RUN import app_run


def run_tests_and_app(tests_funcs, app_file=None, app_name=None, app_start=False):
    """
    Пакетный запуск тестов
    :param tests_funcs: список функций с тестами
    :param app_file: имя файла запускаемого приложения
    :param app_name: имя запускаемого приложения
    :param app_start: запускать приложение или только тесты?
    :return:
    """
    errors = []
    for tst_func in tests_funcs:
        try:
            tst_func()
        except AssertionError as err:
            errors.append(err)
        except Exception as err:
            errors.append(err)
    if errors:
        print("\n".join(map(str, errors)))
        print(f"[TESTS ERROR]: Приложение запускать нельзя!")
    else:
        print(f"[ALL TESTS OK]: Все тесты успешно пройдены")
        if app_file and app_name and app_start:
            app_run(file=app_file, app_name=app_name)
