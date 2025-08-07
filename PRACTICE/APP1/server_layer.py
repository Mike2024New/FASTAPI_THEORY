from UTILS.APP_RUN import app_run
from typing import Annotated
from fastapi import FastAPI, Path
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.requests import Request
from PRACTICE.APP1.app_layer import ManagerShortUrls
from PRACTICE.APP1.models_layer import UrlSet, ShortUrlsParameters
from PRACTICE.APP1.models_layer import NoSuchUrlError, UniqueShortNameError

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

# инициализация приложения по генерации url с указанием опций
options = ShortUrlsParameters(protocol="http", domen="127.0.0.1:8000", prefix="shrt", length=4)
url_manager = ManagerShortUrls(file_path="BASE/short_urls.json", short_url_set=options)

# инициализация приложения fastapi
short_url_app = FastAPI()
short_url_app.name = "short_url_app"


@short_url_app.exception_handler(UniqueShortNameError)
async def unique_short_error(request: Request, exc: UniqueShortNameError):
    print(f"KeyError: {exc}, path: {request.url}")  # логирование ошибки
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )


@short_url_app.exception_handler(NoSuchUrlError)
async def unique_short_error(request: Request, exc: NoSuchUrlError):
    print(f"KeyError: {exc}, path: {request.url}")  # логирование ошибки
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@short_url_app.get("/")
async def home():
    return "Практическое упражнение, написание приложения для генерации сокращенных url, см. http://127.0.0.1:8000/redoc"


@short_url_app.get("/shrt/{short}/")
async def redir_shotrt_url_to_original(short: Annotated[str, Path(title="сокращение url", examples=["aOiWFg"])]):
    """получение оригинальной ссылки и переход по ней"""
    original_url = url_manager.get_original_url_by_short(short_url=short)
    return RedirectResponse(url=original_url, status_code=302)


@short_url_app.post("/add_url/")
def add_url(url: UrlSet):
    short_url = url_manager.add_short_url(url=url)
    return {"original_url": str(url.original_url), "short_url": short_url}


if __name__ == '__main__':
    app_run(file=__file__, app_name=short_url_app.name)
