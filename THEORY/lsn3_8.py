from UTILS.APP_RUN import app_run
from fastapi import FastAPI
from pydantic import BaseModel, Field
import datetime

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
pydantic модели могут принимать и более сложные типы, чем базовые int, float, str, и так далее. 
Например datetime, и эти входные значения будут преобразованы в соответствующие типы.
"""


class DataSet(BaseModel):
    start_date: datetime.datetime = Field(examples=["2025-08-07T13:50:00+05:00"], description="Время и дата ISO 8601")
    end_date: datetime.datetime = Field(examples=["2025-08-07T13:50:00+05:00"], description="Время и дата в ISO 8601")
    curent_date: datetime.date = Field(examples=["2025-08-07"], description="Только дата в ISO 8601")
    curent_time: datetime.time = Field(examples=["13:50:00.000"], description="Только время в ISO 8601")
    process_time: datetime.timedelta = Field(examples=["3800"], description="Время в секундах")


@app.post("/ex1/")
def ex1(data_set: DataSet):
    # видно, что преобразование было выполнено, из строки в datitime:
    print(f"start_date {data_set.start_date} - {type(data_set.start_date)}")
    return data_set


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
