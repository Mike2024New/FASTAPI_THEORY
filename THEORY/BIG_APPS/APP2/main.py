from fastapi import FastAPI, HTTPException, Depends
from .models import User
from .dependencies import check_x_token

fake_db = {
    "Ivan": {"login": "Ivan", "fullname": "Иван Петрович", "age": 30, "city": "Нью-Йорк"},
    "Mike": {"login": "Mike", "fullname": "Михал Палыч", "age": 35, "city": "Москва"},
}

app = FastAPI()


@app.get("/users/{login}", response_model=User, dependencies=[Depends(check_x_token)], tags=["users"])
async def read_user(login: str):
    if login not in fake_db:
        raise HTTPException(status_code=404, detail=f"user login=`{login}` not exists")
    return fake_db[login]
