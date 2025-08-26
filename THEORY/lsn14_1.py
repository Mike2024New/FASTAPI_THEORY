from UTILS.APP_RUN import app_run
from fastapi import FastAPI

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc/
app = FastAPI()
app.name = "app"

"""

"""


# http://127.0.0.1:8000/ex1/
@app.get("/ex1/")
async def ex1():
    return {"msg": "ex1"}


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)