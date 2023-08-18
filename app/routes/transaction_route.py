from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.config.db import conn
from app.utils.tasks_utils import send_sms, update_user_stats
from app.models.transaction_model import Transaction
from app.schemas.transaction_schema import (
    TransactionResponse,
    TransactionListResponse,
    ErrorResponse,
)
from bson import ObjectId
from app.utils.tasks_utils import get_user_by_id
import pprint

# Create an APIRouter instance
transaction_router = APIRouter()


@transaction_router.post("/create_transaction/", response_model=TransactionResponse)
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
        transaction_dict = transaction.model_dump()
        user = get_user_by_id(transaction_dict["user_id"])
        print(f'Transaction id: {transaction_dict["user_id"]}')
        print(f'User: {user}')
        # user_id_exists = await check_user_exists(transaction.user_id)  # Assuming you have a function to check user existence
        # if not user_id_exists:
        #     raise HTTPException(status_code=404, detail="user_id not found.")

        inserted_transaction = conn.transaction.insert_one(transaction_dict)

        if inserted_transaction.inserted_id:
            # Create background tasks to do the following.
            # Send an sms to the user
            background_tasks.add_task(send_sms, transaction_dict)
            # Calculate new stats and update the user information
            background_tasks.add_task(update_user_stats, transaction_dict)
            return TransactionResponse(**transaction_dict)
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
        # TODO: Fix this function
        transactions = conn.transaction.find({"user_id": ObjectId(user_id)})
        response_data = {"transactions": transactions}
        return TransactionListResponse(**transactions)
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
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return TransactionResponse(**transaction)
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

        if not result:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return TransactionResponse(**update_payload.model_dump())
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


@transaction_router.get("/transaction_analytics/{user_id}")
def get_transaction_analytics(user_id: str):
    """
    Get the transaction analytics data of a given user_id.

    Args:
        user_id (int): The ID of the user we want to get stats for.

    Returns:
        Transaction Analytics: The transactions analytics of the user.
    """
    try:
        # TODO: If user does not exist, return message "Specified user not found".
        user = list(conn.user.find({"_id": ObjectId(user_id)}))[0]
        response_data = {
            "status": 201,
            "average_transaction_value": user["average_transaction_value"],
            "date_with_highest_transaction": user["date_with_highest_transaction"],
        }
        return response_data
    except Exception as e:
        error_message = "An error occurred while fetching transactions."
        return ErrorResponse(detail=error_message)
