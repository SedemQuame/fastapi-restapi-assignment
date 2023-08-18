from pydantic import BaseModel
from typing import Dict, List


class UserResponse(BaseModel):
    name: str
    email: str
    phone_number: str
    balance: float
    transactions: Dict[str, List[float]] = {}
    credit_score: float = 0.0
    average_transaction_value: float = 0.0
    total_number_of_transactions: float = 0.0
    total_amount_transacted: float = 0.0
    date_with_highest_transaction: str

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str
