from functools import wraps
from collections.abc import Callable

"""
Этот декоратор, просто как временный инструмент, так как тема тестирования в документации ещё не скоро, а хочется уже
немного оптимизировать написание тестов убрав избыточный код из функций тестировщиков и запускать тестирование пакетами.
В реальной разработке подход к тестированию другой и он будет изучен позже, при достижении блока "тестирование".
"""


def decorator_run_test_check_list_assertion(description: str | None = None):
    """
    Описание функции для тестирования
    :param description: Описание функции для тестирования
    """

    def decorator(func: Callable[..., list[tuple[bool, str], str]]) -> Callable[..., ...]:
        """
        Запуск Assertion тестирования, декорируемая функция должна возвращать
        :param func: декорируемая функция тестирования, она должна в обязательном порядке возвращать список с
        выражениями и url.
        :return: None
        """

        @wraps(func)
        def inner(*args, **kwargs):
            def run_test(check_list_in: list[tuple[bool, str]], url_in: str, f_name_in: str):
                """выполнение тестирования"""
                errors = []

                # шаг 1: выполнение тестов
                for condition, error_msg in check_list_in:
                    if not condition:
                        errors.append(error_msg)

                # шаг 2: обработка (форматирование) ошибок, если есть
                if errors:
                    errors[0] = f"\t{errors[0]}"
                    errors = ";\n\t".join(errors)
                    errors = f"-> func: '{f_name_in}' url: '{url_in}':\n" + errors
                    if description:
                        errors += f"\ndescription: '{description}'"
                    raise AssertionError(errors)
                else:
                    msg = f"[TESTS OK]: '{f_name_in}' - url '{url_in}'"
                    if description:
                        msg += f"description: '{description}'"
                    print(msg)

            f_name = func.__name__  # имя функции тестирования
            # try:
            check_list, url = func(*args, **kwargs)
            run_test(check_list, url, f_name)  # запуск тестов по чек-листу
            return check_list, url  # возвращение чек-листа и url, чтобы можно было использовать другие декораторы
            # except Exception as error:
            #     raise RuntimeError(f"Ошибка при выполнении теста {f_name}: {error}")

        return inner

    return decorator


if __name__ == '__main__':
    pass
