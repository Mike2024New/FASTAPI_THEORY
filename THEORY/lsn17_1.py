from UTILS.APP_RUN import app_run
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from lsn17_1_manager_base import BaseManager
from sqlalchemy.exc import IntegrityError
from UTILS.HASH_MANAGER import HashManager

# ключ здесь просто для упрощения, но ни когда не ставить в код ключи!
hash_manager = HashManager(secret_key="aed2d16c52f6bad08df35fdd9b49549495ab5f65c725d8c3c4bcec66b0569947")
base_manager = BaseManager(base_path="lsn17_1_base.db")

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"


class User(BaseModel):
    username: str


class UserIn(User):
    password: str
    model_config = ConfigDict(json_schema_extra={"examples": [{"username": "Иван", "password": "qwerty"}]})


@app.post("/create_user/", response_model=User)
async def create_user(user: UserIn):
    try:
        hash_password = hash_manager.hash_password(user.password)  # сохранение хешированного пароля в БД
        base_manager.create_user(username=user.username, hash_password=hash_password)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует.")


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
