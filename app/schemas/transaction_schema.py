from typing import List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.models.transaction_model import Transaction


# MODIFIED MODEL POST DEADLINE.
class TransactionResponseDict(BaseModel):
    status: str
    message: str
    data: Transaction


class TransactionResponseList(BaseModel):
    status: str
    message: str
    data: List


class ErrorResponse(BaseModel):
    detail: str
