from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"

class Transaction(BaseModel):
    user_id: str
    full_name: str
    transaction_date: datetime
    transaction_amount: float
    transaction_type: TransactionType

    class Config:
        orm_mode = True
