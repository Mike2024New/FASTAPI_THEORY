from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Body, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Literal

app = FastAPI()
app.name = "app"
client = TestClient(app)


class Figure(BaseModel):
    type_figure: str | None = None

    def get_description(self):
        raise NotImplementedError("метод должен быть обязательно реализован в классе наследнике!")

    def calc_area(self):
        """расчёт площади фигуры"""
        raise NotImplementedError("метод должен быть обязательно реализован в классе наследнике!")


class Rectangle(Figure):
    type_figure: Literal["rectangle"] = "rectangle"
    a: Annotated[float, Field(gt=0, description="сторона A", example=3)]
    b: Annotated[float, Field(gt=0, description="сторона B", example=2)]
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"type_figure": "rectangle", "a": 3, "b": 2},
        {"type_figure": "rectangle", "a": 1, "b": 4},
    ]})

    def calc_area(self):
        return self.a * self.b

    def get_description(self):
        return f"Прямоугольник со сторонами a={self.a}, b={self.b}"


class Circle(Figure):
    type_figure: Literal["circle"] = "circle"
    radius: Annotated[float, Field(gt=0, description="Радиус окружности", example=4)]
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"type_figure": "circle", "radius": 4},
        {"type_figure": "circle", "radius": 2},
    ]})

    def calc_area(self):
        return (self.radius ** 2) * 3.14

    def get_description(self):
        return f"Окружность с радиусом {self.radius}"


class FigureOut(Figure):
    description: str
    area: float


@app.post("/ex1/", response_model=FigureOut, response_model_exclude={"type_figure"},
          status_code=status.HTTP_201_CREATED)
async def ex1(figure: Annotated[Rectangle | Circle, Body(embed=True)]):
    return FigureOut(description=figure.get_description(), area=figure.calc_area())


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
