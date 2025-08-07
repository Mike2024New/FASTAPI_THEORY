from dataclasses import dataclass
from typing import Literal, Annotated
from pydantic import BaseModel, Field, HttpUrl

descr_orig_url = "передайте сюда оригинальный ulr, который нужно сократить"
descr_custom_shrt = "передайте сюда кастомное сокращение если нужно, тогда оно будет использоваться вместо случайного"


class UrlSet(BaseModel):
    original_url: Annotated[HttpUrl, Field(title="url", description=descr_orig_url, examples=["http://example.com/"])]
    custom_short: Annotated[str | None, Field(description=descr_custom_shrt, examples=["my_url"])] = None


@dataclass
class ShortUrlsParameters:
    protocol: Literal["http", "https"] = "http"
    domen: str = "127.0.0.1:8000"
    prefix: str = "shrt"
    length: int = 4


class NoSuchUrlError(ValueError):
    pass


class UniqueShortNameError(ValueError):
    pass
