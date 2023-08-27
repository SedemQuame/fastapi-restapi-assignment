from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    credit: str = "credit"
    debit: str = "debit"


class Transaction(BaseModel):
    transaction_id: str = ""
    user_id: str = ""
    full_name: str = ""
    transaction_date: datetime
    transaction_amount: float = 0.0
    transaction_type: TransactionType

    class Config:
        orm_mode = True
