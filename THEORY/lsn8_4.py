from UTILS.APP_RUN import app_run
from fastapi import FastAPI

app = FastAPI()
app.name = "app"


@app.get("/")
def home():
    return


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
