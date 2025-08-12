from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Union

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Указание нескольких вариаций моделей ответа в response_model (как в typing Union, используется когда тип может быть 
одним из перечисляемых, также и модель может быть одной из перечисляемых).

Например есть базовый класс Figure, и от него наследуются различные фигуры, и все они могут быть возвращены в эндпоинте
/ex1/ и это нужно указать в качестве возвращаемой модели, для этого используется response_model в которой можно указать
несколько типов через Union
"""


class Figure(BaseModel):
    description: str
    model_type: str


class Rectangle(Figure):
    model_type: str = "rectangle"
    side_a: Annotated[int, Field(example=3, gt=0)]
    side_b: Annotated[int, Field(example=5, gt=0)]


class Cylinder(Figure):
    model_type: str = "cylinder"
    radius: Annotated[int, Field(example=4, gt=0)]


class Ellipse(Figure):
    model_type: str = "ellipse"
    radius1: Annotated[int, Field(example=4, gt=0)]
    radius2: Annotated[int, Field(example=4, gt=0)]


figures = {
    "1": {"description": "Прямоугольник со сторанами 100 и 50", "model_type": "rectangle", "side_a": 100, "side_b": 50},
    "2": {"description": "Цилиндр с радиусом 21", "model_type": "cylinder", "radius": 21},
    "3": {"description": "Эллипс с радиусами 3, и 4", "model_type": "ellipse", "radius1": 3, "radius2": 4},
}
"""
В документации говорится, что такой способ прописывания возвращаемых моделей, вызовет ошибку:
@app.get("/ex1/", response_model=Rectangle | Cylinder)
а именно:
response_model=Rectangle | Cylinder,
и лучше использовать Union, хотя и тот способ тоже работает, но такой способ лучше для совместимости со старыми версиями
python до 3.10
"""


@app.get("/ex1/", response_model=Union[Rectangle, Cylinder, Ellipse])
def ex1(figure_id: str):
    if figure_id not in figures:
        return JSONResponse(content={"msg": f"Фигуры с id '{figure_id}' не существует"}, status_code=404)
    return figures[figure_id]


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
