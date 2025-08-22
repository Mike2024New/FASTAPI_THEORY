from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/

"""
Вопрос 9: Сделай HTML форму для ввода данных, создай GET и POST эндпоинты для работы с ней.
"""

app = FastAPI()
app.name = "app"
templates = Jinja2Templates(directory="templates")


class AccountBase(BaseModel):
    login: str
    name: str | None = None
    age: int | None = Field(default=None, ge=18, le=99)
    city: str | None = None


class AccountInput(AccountBase):
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_password_eq(self):
        if self.password != self.password_repeat:
            raise ValidationError("Пароли должны совпадать")
        return self


# http://127.0.0.1:8000/register/
@app.get("/register/", summary="отправка пользователю html страницы с формой регистрации")
def register_get_html(request: Request):
    return templates.TemplateResponse(name="for_rq7_register.html", status_code=200, context={"request": request})


# ВАЖНО! При работе с шаблонами response_model не используется, и status код указывается в TemplateResponse
@app.post("/register/", summary="регистрация пользователя, выдача ему страницы с данными")
def registe_new_user(request: Request, user: Annotated[AccountInput, Form()]):
    ...  # логика по заведению пользователя на основании данных из формы
    user = jsonable_encoder(user, exclude={"password", "password_repeat"})  # извлечение данных из форм в json
    return templates.TemplateResponse(name="for_rq7_profile.html", status_code=201,
                                      context={"request": request, "user": user})


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
