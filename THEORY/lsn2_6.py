# uvicorn THEORY.lsn2_6:app --reload
from fastapi import FastAPI  # Query
import uvicorn

# from typing import Annotated

"""
Продолжить отсюда:
# https://fastapi.tiangolo.com/ru/tutorial/query-params-str-validations/#_7
"""

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(app="lsn2_6:app", reload=True)
