import uuid
import base64
from UTILS.WORK_JSON import WorkJson
from PRACTICE.APP1.models_layer import UrlSet, ShortUrlsParameters
from PRACTICE.APP1.models_layer import NoSuchUrlError, UniqueShortNameError


class ManagerShortUrls:
    """
    Менеджер сокращения URL
    Отвечает за преобразование url в короткие адреса заданной длины и сохранение их в БД (в учебных целях в качестве
    БД выбран простой json).
    Пример базы URL:
    {
        "http://shrt/127.0.0.1:8000/gPEfOA/": "https://example.com/", # ключи всегда разные, даже если url одинаковы
        "http://shrt/127.0.0.1:8000/2lh0Tg/": "https://example.com/",
        "http://shrt/127.0.0.1:8000/XPk8dQ/": "https://example.com/"
    }

    Особенности:
    1. Гарантируется уникальность url.
    2. Логика класса изолирована от какого либо ui, можно использовать с fastapi, django, tkinter, консоль и так далее.
    3. К url добавляется префикс

    Примечание:
    На примере "http://127.0.0.1:8000/gPEfOA/": "https://example.com/", конечно смотрится смешно, он скорее как
    удлинитель получается. Но на примере когда url слишком длинный, например:
    https://example.com/test/documents/reports/2025/5211034/ и когда домен не локальный уже выглядит очень удобно
    """

    def __init__(self, file_path: str, short_url_set: ShortUrlsParameters | None = None) -> None:
        """
        :param file_path: путь к БД (в данном примере к json)
        :param short_url_set: [необязательно] настройки сокращенного url
        """
        # применение настроек к short_url
        self._short_url_set = short_url_set if short_url_set else ShortUrlsParameters()
        # псевдо БД (WorkJson - гарантированно создаёт файл если его нет)
        self._json_manager = WorkJson(file_path)

    def get_original_url_by_short(self, short_url: str) -> str:
        """
        получение оригинального url из БД (если он есть)
        :param short_url: сокращенная ссылка
        :return: оригинальный url если он есть в БД / возбуждение NoSuchUrlError если url отсутствует
        """
        # чтение БД
        data = self._json_manager.read_json_file()
        short_url = self._assembly_url(short_key=short_url)
        if short_url not in data:
            raise NoSuchUrlError(f"url '{short_url}' не найден.")  # в серверных web приложениях это будет вызывать 404
        # url найден, вернуть его пользователю
        return data[short_url]

    def add_short_url(self, url: UrlSet) -> str:
        """
        Добавление url в БД
        :param url: модель с url и пользовательским сокращением
        :return: Возвращает сокращенный url для клиента
        """
        url, custom_short_name = str(url.original_url), url.custom_short
        # получение списка url из json (здесь упрощено в базах данных лучше использовать генераторы для экономии памяти)
        data = self._json_manager.read_json_file()
        # проверка коллизии (что крайне маловероятно даже для урезанного uuid)
        while True:
            # если пользователь передал свой шорт-нейм, то тогда генератор не нужен / нет? генерир uuid
            short_url = custom_short_name if custom_short_name else self._generate_unique_short_url()
            short_url = self._assembly_url(short_url)  # выполнить сборку url
            if short_url in data.keys():
                if custom_short_name:  # для кастомных url, просто оповестить пользователя, что это сокращение уже занято
                    raise UniqueShortNameError(f"Сокращение '{custom_short_name}' уже занято.")
                continue
            break
        # запись url в выходной json (псевдо БД)
        data[short_url] = url
        self._json_manager.rec_json_file(data)
        return short_url

    def _assembly_url(self, short_key) -> str:
        """
        Сборка url, по заданной в SHORT_URL_LENGTH длине и заданному домену в DOMEN
        :param short_key: сокращенная часть url, например: 'ttts' для 'http://127.0.0.1:8000/shrt/ttts'
        :return: собранный url
        """
        short_url = self._short_url_set.protocol + "://"
        short_url += "/".join((self._short_url_set.domen, self._short_url_set.prefix, short_key))
        return short_url

    def _generate_unique_short_url(self) -> str:
        """генерация уникального значения для сокращенного url"""
        short_bytes = uuid.uuid4().bytes[:self._short_url_set.length]
        short_key = base64.urlsafe_b64encode(short_bytes).decode('utf-8').rstrip("=")
        return short_key


if __name__ == '__main__':
    url_manager = ManagerShortUrls(file_path="short_urls_exmp.json")
    url_set = UrlSet(original_url="https://example.com/", custom_short="my_site")
    url_manager.add_short_url(url_set)
