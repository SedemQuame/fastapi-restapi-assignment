from typing import List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class TransactionResponse(BaseModel):
    user_id: str
    full_name: str
    transaction_date: datetime
    transaction_amount: float
    transaction_type: str


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]


class ErrorResponse(BaseModel):
    detail: str
