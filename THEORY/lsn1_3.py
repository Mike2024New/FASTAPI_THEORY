# uvicorn THEORY.lsn1_3:app --reload
from enum import Enum
from fastapi import FastAPI

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
"""
В ситуации когда нужно заранее предопределить значения, стоит использовать Enum.
Тогда можно будет выбрать только конкретные значения. И это удобно отображается в интерактивной документации в виде
combobox.
То есть пример ниже позволяет принимать только 3 входных параметра пути определенные в классе OsName
"""


class OsName(str, Enum):
    win95 = "windows95"
    win98 = "windows98"
    winXP = "windowsXP"


app = FastAPI()


@app.get("/os/{os_name}/")
async def info_os(os_name: OsName):  # указание типа OsName, теперь жестко говорит, что значения предопределены
    # разводка по ресурсу Enum -> os_name -> стандартная работа с перечислениями python
    if os_name is OsName.win95:
        return f"Выбрана ОС {OsName.win95}"

    if os_name.value == "windows98":
        return f"Выбрана ОС {OsName.win98}"

    return f"Выбрана ОС {OsName.winXP}"
