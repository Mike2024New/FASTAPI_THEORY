from UTILS.APP_RUN import app_run
from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()
app.name = "app"


class User(BaseModel):
    name: Annotated[str, Field(alias="username")]
    model_config = ConfigDict(populate_by_name=True)


@app.get("/ex1/")
async def ex1(user: Annotated[User, Query()]):
    return user


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
