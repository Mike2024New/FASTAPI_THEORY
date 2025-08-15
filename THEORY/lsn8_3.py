import os
from UTILS.read_file import read_file
from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, model_validator
from typing import Annotated

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
Использование pydantic моделей, для работы с формами, Form() поддерживает модели, но в таком случае их нужно связать 
через Annotated (тип модели и объект Form())
--------------------------------------------------------------------------------------------------------------
ВАЖНО! Поля в форме (атрибут name), должны совпадать с параметрами в функциях (или Pydantic моделях). 
"""


class BaseUser(BaseModel):
    username: str


class UserInput(BaseUser):
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_pasword(self):
        if self.password != self.password_repeat:
            raise HTTPException(status_code=422, detail="пароли должны совпадать")
        return self


class UserOut(BaseUser):
    pass


# http://127.0.0.1:8000/  -> перейти сюда, чтобы форма загрузилась
@app.get("/")
def home():
    """"""
    content = read_file(file_path=os.path.join(os.getcwd(), 'HTML', 'file2.html'))
    return HTMLResponse(content=content, status_code=200)


@app.post("/ex1/", response_model=UserOut)
def ex1(user: Annotated[UserInput, Form()]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
