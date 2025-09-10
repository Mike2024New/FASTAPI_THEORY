import os


def create_new_app_file(file_name: str, content: str):
    if os.path.exists(file_name):
        raise ValueError(f"Файл '{file_name}' уже существует!")
    with open(file=file_name, mode="w", encoding="utf-8") as f:
        f.write(content)


cntnt = '''from UTILS.APP_RUN import app_run
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
    app_run(file=__file__, app_name=app.name)'''

if __name__ == '__main__':
    create_new_app_file(file_name=r"C:\Users\MikeCoder\Documents\LESSONS\FASTAPI\THEORY\lsn15_4.py", content=cntnt)
