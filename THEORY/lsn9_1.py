from UTILS.APP_RUN import app_run
from fastapi import FastAPI, HTTPException

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()
app.name = "app"

"""
ex1 ->
в примере выполняется запрос к псевдо бд fake_db, и если в ней отсутствует элемент с запрашиваемым ключом, то происходит
возбуждение исключения HTTPException, который содержит в себе:
status_code -> 400-499 (ошибка на стороне клиента)
detail -> что именно пошло не так
headers -> заголовки ответа, если заголовок начинается с префикса X-, то это обозначает, что заголовок кастомный, то 
есть не предусмотрен headers, и разработчик его добавляет на свое усмотрение. Это может быть полезным для 
дополнительного информирования клиента (приложения клиента).
"""

fake_db = {f"page_{i}": f"content from page_{i}" for i in range(3)}


# http://127.0.0.1:8000/ex1/1/  -> статус код 200, всё ок, получит контент
# http://127.0.0.1:8000/ex1/99999/  -> такой страницы не существует, исключение HTTPException и статус будет 404
@app.get("/ex1/{page_num}/")
def ex1(page_num: int):
    page = f"page_{page_num}"
    if page not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Страницы не существует...",
            headers={"X-error": "No such resourse"}
        )
    return fake_db[page]


if __name__ == '__main__':
    app_run(file=__file__, app_name=app.name)
