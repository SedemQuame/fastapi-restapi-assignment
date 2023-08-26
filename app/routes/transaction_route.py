from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.config.db import conn
from app.utils.tasks_utils import send_sms, update_user_stats
from app.models.transaction_model import Transaction
from app.schemas.transaction_schema import (
    TransactionResponseDict,
    TransactionResponseList,
    ErrorResponse,
)
from bson import ObjectId
from app.utils.tasks_utils import get_user_by_id
from typing import List, Dict

# Create an APIRouter instance
transaction_router = APIRouter()


# MODIFIED ENDPOINT POST DEADLINE.
@transaction_router.post("/create_transaction", response_model=TransactionResponseDict)
async def create_transaction(
    transaction: Transaction, background_tasks: BackgroundTasks
):
    """
    Create a new transaction.

    Args:
        transaction (Transaction): Transaction data to be created.

    Returns:
        TransactionResponse: The created transaction.
    """
    try:
        transaction_data = transaction.model_dump()
        user = get_user_by_id(transaction_data["user_id"])
        # if not user:
        #     raise HTTPException(status_code=404, detail="user_id not found.")

        inserted_transaction = conn.transaction.insert_one(transaction_data)

        if inserted_transaction.inserted_id:
            transaction_data["transaction_id"] = str(inserted_transaction.inserted_id)
            # Create background tasks to do the following.
            # Send an sms to the user
            background_tasks.add_task(send_sms, transaction_data)
            # Calculate new stats and update the user information
            background_tasks.add_task(update_user_stats, transaction_data)
            return {
                "status": "200",
                "message": "Successfully created the transaction record.",
                "data": Transaction(**transaction_data),
            }
        else:
            return {
                "status": "400",
                "message": "Failed to create the transaction record.",
                "data": Transaction(**transaction_data),
            }
            # raise HTTPException(status_code=500, detail="Failed to create transaction")
    except Exception as e:
        error_message = "An error occurred while creating the transaction."
        return ErrorResponse(detail=error_message)


# FIXED ENDPOINT POST DEADLINE.
@transaction_router.get(
    "/find_transactions_by_user/{user_id}", response_model=TransactionResponseList
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
        transactions = list(conn.transaction.find({"user_id": user_id}))
        serialized_transactions = []
        for transaction in transactions:
            transaction["transaction_id"] = str(transaction["_id"])
            serialized_transaction = Transaction(**transaction)
            serialized_transactions.append(serialized_transaction)
        return {
            "status": "200",
            "message": "Successfully returned all transactions associated to a user.",
            "data": serialized_transactions,
        }
    except Exception as e:
        error_message = "An error occurred while fetching transactions."
        return ErrorResponse(detail=error_message)


# MODIFIED ENDPOINT POST DEADLINE.
@transaction_router.get(
    "/find_transactions_by_id/{transaction_id}", response_model=TransactionResponseDict
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
            transaction_data = dict(transaction)
            transaction_data["transaction_id"] = str(transaction_data["_id"])
            return {
                "status": "200",
                "message": "Successfully returned user with the specified transaction_id.",
                "data": Transaction(**transaction_data),
            }
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        error_message = "An error occurred while fetching the transaction."
        return ErrorResponse(detail=error_message)


# TODO: Fix issue with returning the updated data.
@transaction_router.put(
    "/update_transaction/{transaction_id}", response_model=TransactionResponseDict
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
        conn.transaction.find_one_and_update(
            {"_id": ObjectId(transaction_id)}, {"$set": dict(update_payload)}
        )
        updated_transaction = conn.transaction.find_one(
            {"_id": ObjectId(transaction_id)}
        )
        # print(list(update_transaction))

        if updated_transaction:
            transaction_data = dict(updated_transaction)
            transaction_data["transaction_id"] = str(transaction_data["_id"])
            return {
                "status": "200",
                "message": "Successfully updated user record with the specified user_id.",
                "data": Transaction(**transaction_data),
            }
        else:
            raise HTTPException(
                status_code=404, detail="Transaction with specified id not found"
            )
    except Exception as e:
        error_message = "An error occurred while updating the transaction."
        return ErrorResponse(detail=error_message)


@transaction_router.delete(
    "/delete_transactions/{transaction_id}", response_model=TransactionResponseDict
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
            return {
                "status": "200",
                "message": "Successfully deleted transaction record with the specified transaction_id.",
                "data": Transaction(**deleted_transaction),
            }
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        error_message = "An error occurred while deleting the transaction."
        return ErrorResponse(detail=error_message)


# MODIFIED ENDPOINT POST DEADLINE.
@transaction_router.get("/transaction_analytics/{user_id}", response_model=Dict)
def get_transaction_analytics(user_id: str):
    """
    Get the transaction analytics data of a given user_id.

    Args:
        user_id (int): The ID of the user we want to get stats for.

    Returns:
        Transaction Analytics: The transactions analytics of the user.
    """
    try:
        user = list(conn.user.find({"_id": ObjectId(user_id)}))[0]
        if user:
            return {
                "status": "200",
                "message": "Successfully returned the user's transaction analytics data.",
                "data": {
                    "user_id": user_id,
                    "average_transaction_value": user["average_transaction_value"],
                    "date_with_highest_transaction": user[
                        "date_with_highest_transaction"
                    ],
                },
            }
        else:
            return {
                "status": "400",
                "message": "Failed to return analytics for the specified user.",
                "data": {
                    "user_id": user_id,
                    "average_transaction_value": -1.0,
                    "date_with_highest_transaction": -1.0,
                },
            }
    except Exception as e:
        error_message = "An error occurred while fetching transactions."
        return ErrorResponse(detail=error_message)
