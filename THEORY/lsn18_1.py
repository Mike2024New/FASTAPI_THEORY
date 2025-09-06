from UTILS.HASH_MANAGER import HashManager
from fastapi import FastAPI
from lsn18_manager_base import BaseManager, UserInput, UserRead
import uvicorn

hash_manager = HashManager(secret_key="aed2d16c52f6bad08df35fdd9b49549495ab5f65c725d8c3c4bcec66b0569947")
base_manager = BaseManager(base_path="lsn20_database.db")

app = FastAPI()
app.name = "app"


@app.post("/add_user/", response_model=UserRead)
def add_new_user(user: UserInput):
    hash_password = hash_manager.hash_password(password_in=user.password)
    user = base_manager.add_user(username=user.username, password=hash_password)
    return UserRead(id=user.id, username=user.username)


if __name__ == '__main__':
    uvicorn.run(app="lsn20_1:app", reload=True)
