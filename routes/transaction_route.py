from fastapi import APIRouter, HTTPException
from config.db import conn
from typing import List
from models.transaction_model import Transaction

# from schemas.transaction_schema import serializeDict, serializeList
from schemas.transaction_schema import (
    TransactionResponse,
    TransactionListResponse,
    ErrorResponse,
)
from bson import ObjectId

# Create an APIRouter instance
transaction_router = APIRouter()


@transaction_router.post("/create_transaction/", response_model=TransactionResponse)
async def create_transaction(transaction: Transaction):
    """
    Create a new transaction.

    Args:
        transaction (Transaction): Transaction data to be created.

    Returns:
        TransactionResponse: The created transaction.
    """
    try:
        # Convert the Transaction instance to a dictionary before inserting
        transaction_dict = transaction.model_dump()

        # Insert the transaction dictionary into the database
        inserted_transaction = conn.transaction.insert_one(transaction_dict)

        # Check if the insertion was successful
        if inserted_transaction.inserted_id:
            #TODO: Create background tasks to do the following.
            #TODO: 1. Send an sms to the user stating a change has been made to the account.
            #TODO: 2. Calculate new stats and update the user information, to enable easy and fast lookup.
            return transaction
        else:
            raise HTTPException(status_code=500, detail="Failed to create transaction")
    except Exception as e:
        error_message = "An error occurred while creating the transaction."
        return ErrorResponse(detail=error_message)


@transaction_router.get(
    "/find_transactions_by_user/{user_id}", response_model=TransactionListResponse
)
async def read_user_transaction_history(user_id: str):
    """
    Get transaction history for a user by user ID.

    Args:
        user_id (str): The ID of the user whose transactions are to be fetched.

    Returns:
        List[Transaction]: List of transactions for the user.
    """
    try:
        transactions = conn.transaction.find({"user_id": user_id})
        response_data = {"transactions": transactions}
        return TransactionListResponse(**response_data)
    except Exception as e:
        error_message = "An error occurred while fetching transactions."
        return ErrorResponse(detail=error_message)


@transaction_router.get(
    "/find_transactions_by_id/{transaction_id}", response_model=TransactionResponse
)
def read_transaction_history_by_id(transaction_id: str):
    """
    Get transaction history by transaction ID.

    Args:
        transaction_id (str): The ID of the transaction to be fetched.

    Returns:
        TransactionResponse: The transaction with the given ID.
    """
    try:
        transaction = conn.transaction.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            return TransactionResponse(**transaction)
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        error_message = "An error occurred while fetching the transaction."
        return ErrorResponse(detail=error_message)


@transaction_router.put(
    "/update_transaction/{transaction_id}", response_model=TransactionResponse
)
def update_transaction(transaction_id: str, update_payload: Transaction):
    """
    Update a transaction by transaction ID.

    Args:
        transaction_id (str): The ID of the transaction to be updated.
        update_payload (Transaction): Updated transaction data.

    Returns:
        Transaction: The updated transaction.
    """
    try:
        result = conn.transaction.find_one_and_update(
            {"_id": ObjectId(transaction_id)}, {"$set": dict(update_payload)}
        )

        if result:
            return TransactionResponse(**update_payload.model_dump())
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        error_message = "An error occurred while updating the transaction."
        return ErrorResponse(detail=error_message)


@transaction_router.delete(
    "/delete_transactions/{transaction_id}", response_model=TransactionResponse
)
def delete_transaction(transaction_id: str):
    """
    Delete a transaction by transaction ID.

    Args:
        transaction_id (int): The ID of the transaction to be deleted.

    Returns:
        Transaction: The deleted transaction.
    """
    try:
        deleted_transaction = conn.transaction.find_one_and_delete(
            {"_id": ObjectId(transaction_id)}
        )
        if deleted_transaction:
            return TransactionResponse(**deleted_transaction)
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        error_message = "An error occurred while deleting the transaction."
        return ErrorResponse(detail=error_message)
