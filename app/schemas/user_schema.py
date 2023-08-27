from pydantic import BaseModel
from typing import Dict, List
from app.models.user_model import User


# MODIFIED MODEL POST DEADLINE.
class UserResponseDict(BaseModel):
    status: str
    message: str
    data: User


class UserResponseList(BaseModel):
    status: str
    message: str
    data: List


class ErrorResponse(BaseModel):
    detail: str
