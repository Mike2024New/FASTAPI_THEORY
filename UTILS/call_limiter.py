import threading
import time

"""
Контроль количества вызова функций в заданный промежуток времени.
Вдохновлено самостоятельной реализацией ограничения количества запросов в fastapi (до раздела где показывается как это 
делать ещё не дошел).
А также это может быть полезно например для приложений парсеров, когда сервера отказывают при превышении запросов в 
заданный период времени.
"""


class CallLimitter:
    def __init__(self, call_limit_in=2, time_limit_in=3):
        """
        :param call_limit_in: максимальное количество вызовов функции за период time_limit
        :param time_limit_in: время сброса блокировки запросов, когда снова можно будет вызывать функцию
        """
        self._count = 0
        self._time_limit = time_limit_in
        self._limit = call_limit_in
        self._lock = threading.Lock()
        self._thread = threading.Thread(
            target=self._call_control,  # запускаемый счётчик-контроллер
            daemon=True  # фоновый поток, его остановка происходит когда основной поток завершен
        )
        self._thread.start()  # запуск контроллера

    def _call_control(self):
        while True:
            time.sleep(self._time_limit)
            self._count = 0
            print("## СБРОС ##")

    def call_func(self, func):
        def inner(*args, **kwargs):
            with self._lock:
                if self._count >= self._limit:
                    return "Отказано в вызове..."
            self._count += 1
            return func(*args, **kwargs)

        return inner


if __name__ == '__main__':
    # пример использования
    call_limit = CallLimitter(call_limit_in=2, time_limit_in=3)


    @call_limit.call_func
    def test():
        return f"Функция успешно выполнена"


    while True:
        input()
        res = test()
        print(res)
