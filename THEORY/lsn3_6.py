from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal, Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Иногда может возникнуть ситуация когда моделей более глубокого уровня вложенности может быть несколько (то есть имеется
в виду, что выбор из нескольких моделей) и все эти модели могут быть записаны в список модели верхнего уровня. 
И вот если использовать тип: Model1 | Model2, то в случае ошибки входных данных не будет получена точная локализация 
ошибки, так как Pydantic увидит первую ошибку и выпадет в исключение. Для этого лучше использовать поле дискриминатор,
и обобщающий модели одного уровня тип.
"""


# классы Image и Song "равносильны", то есть они оба являются подмоделями модели Directory
class File(BaseModel):
    name: str
    size: float


class Image(File):
    type: Literal["img"] = "img"  # поле дискриминатор -> оно же ссылка для pydantic именно к этой модели при валидации
    resolution: list[float]


class Song(File):
    type: Literal["song"] = "song"  # поле дискриминатор -> оно же ссылка для pydantic к этой модели при валидации
    duration: float


# в FylesType две равносильные модели Image и Song, связываются в единый тип, с объяснением того какое поле укзавает на тип
FylesType = Annotated[Image | Song, Field(discriminator="type")]


class Directory(BaseModel):
    # files: list[Image | Song] # так делать категорически не следует, не точность локализации в случае ошибки
    files: list[FylesType]  # нужно использовать переменную обобщающую типы

    def total_size_mb(self) -> float:  # в модели можно также добавлять методы для действий с полями
        """
        Подсчёт размера всех файлов
        """
        all_files_size = sum(f.size for f in self.files)
        return round(all_files_size, 2)


@app.post("/ex1/")
def ex1(directory: Directory):
    return {"files": directory, "total_size_mb": directory.total_size_mb()}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
