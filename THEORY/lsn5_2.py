from UTILS.APP_RUN import app_run
from fastapi import FastAPI

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
