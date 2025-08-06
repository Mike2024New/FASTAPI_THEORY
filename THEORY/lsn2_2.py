# uvicorn THEORY.lsn2_2:app --reload
from typing import Literal
from fastapi import FastAPI
import uvicorn

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()

"""
смешивание параметров path и query. 
fastapi под капотом понимает и видит разницу между path и query параметрами, так как query параметры не объявляются
в url как это происходит с path параметрами (которые объявляются в {})
"""


# http://127.0.0.1:8000/images/100/ -> size применится по умолчанию, а идентификатор изображения 100
# http://127.0.0.1:8000/images/100/?size=small  -> size выбран, а идентификатор изображения 100
@app.get("/images/{image_id}/")
async def ex1(image_id: int, size: Literal["small", "mid", "big"] = "big"):
    return f"Получено изображение {image_id}, размер {size}"


if __name__ == '__main__':
    uvicorn.run(app="lsn2_2:app", reload=True)
