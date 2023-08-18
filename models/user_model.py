from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str

    class Config:
        orm_mode = True
