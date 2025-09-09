from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    login: str
    fullname: str
    age: int
    city: str | None = None
    model_config = ConfigDict(
        json_schema_extra={"examples": [
            {"login": "Maria", "fullname": "Мария Анатольевна", "age": 26, "city": "Москва"}
        ]}
    )
