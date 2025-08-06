from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
ex1
Ниже представлена модель двойной вложенности.
Создаётся класс User, допустим у него есть работа, и вот для описания работы используется отдельный класс Job, который
позволяет описать дополнительные детали, при этом привязываясь к классу User. Также в классе Job, есть отдельное поле
с классом Company, это дополнительная информация про компанию.
Плюс такого подхода логическая изоляция смысловых блоков информации, при этом сохраняя связь между ними.
Здесь модели сильно упрощены, но полей может быть очень много, нереально много и для этого как раз лучше всего 
использовать логическую стурктуру с группировкой по смыслу, что и позволяют сделать вложенные модели pydantic. 
ex1 ожидает следующие примеры данных:
1. Без класса job, так как у него установлено значение по умолчанию, например сейчас человек не имеет работы:
{
  "name": "string",
  "age": 18
}

2. Полная модель с учетом вложенных моделей, человек указал информацию о работе и инфо о компании:
{
  "name": "string",
  "age": 18,
  "job": {
    "profession": "string",
    "salary": 0,
    "company": {
      "name": "string",
      "phone": "string",
      "email": "https://example.com/"  # поле жестко валидируется за счёт HttpUrl
    }
  }
}
"""


class Company(BaseModel):
    name: str
    phone: str
    email: HttpUrl  # HttpUrl содержит шаблоны и алгоритмы для валидации напсания email


class Job(BaseModel):
    profession: str = Field(min_length=3, max_length=100)
    salary: float
    company: Company  # тип Company указывает, что это модель


class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, lt=60)
    job: Job | None = Field(default=None, title="работа")  # тип Job указывает, что это ссылка на модель Job


@app.post("/ex1/")
def ex1(user: User):
    result = {"data": user}
    # демонстрация того, как можно работать через точечную нотацию с вложенными моделями
    if user.job:
        result["msg"] = (
            f"Ваша должность {user.job.profession},"  # спуск в модель на 1 уровень вложенности
            f" компания {user.job.company.name}"  # в этой точке обращение к самой глубокой модели
        )
    return result


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
