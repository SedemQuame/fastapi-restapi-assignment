"""
Utility Functions Module

This module contains utility functions for various tasks related to transaction processing and user management.
It includes functions for sending SMS notifications, calculating transaction scores, updating user data and statistics,
and retrieving user information from the database.
"""

from typing import Dict, List
from app.config.db import conn
from bson import ObjectId
from app.models.transaction_model import TransactionType
from app.models.user_model import User
from datetime import datetime
from twilio.rest import Client
import os
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Define constants for transaction score calculation
GLOBAL_TRANSACTION_SCORE_MAX = 5
GLOBAL_TRANSACTION_AMOUNT_DIVISOR = 100


def send_sms(transaction: Dict) -> None:
    """
    Send an SMS notification using Twilio Trial API.

    Args:
        transaction (Dict): The transaction details.

    Raises:
        Exception: If there's an error sending the SMS.
    """
    user_id = transaction["user_id"]
    user = get_user_by_id(user_id)
    phone_number = user["phone_number"]
    transaction_amount = transaction["transaction_amount"]
    transaction_type = get_transaction_type(transaction)

    message = f'Hi {transaction["full_name"]},\nYour account has been {transaction_type}ed, GHS {transaction_amount}'

    try:
        client = Client(
            os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]
        )
        sms = client.messages.create(
            body=message, from_="+19498280706", to=phone_number
        )
        logger.info("SMS sent successfully. SID: %s", sms.sid)
    except Exception as e:
        logger.error("Error sending SMS: %s", str(e))


def calculate_average_transaction_score(transactions: List) -> int:
    """
    Calculate the average transaction score based on a list of transactions.

    Args:
        transactions (List): List of transactions.

    Returns:
        int: The calculated average transaction score.

    Raises:
        Exception: If there's an error during calculation.
    """
    try:
        total_amount = sum(t.transaction_amount for t in transactions)
        average_amount = total_amount / len(transactions)
        scaled_score = max(
            min(
                int(
                    (average_amount / GLOBAL_TRANSACTION_AMOUNT_DIVISOR)
                    * GLOBAL_TRANSACTION_SCORE_MAX
                ),
                GLOBAL_TRANSACTION_SCORE_MAX,
            ),
            1,
        )
        return scaled_score
    except ZeroDivisionError:
        return 0
    except Exception as e:
        logger.error("Error calculating average transaction score: %s", str(e))
        return 0


def update_user_stats(transaction: Dict):
    """
    Update user statistics and balance based on a new transaction.

    Args:
        transaction (Dict): The new transaction data.

    Raises:
        Exception: If there's an error during the update process.
    """
    user_id = transaction["user_id"]
    user = get_user_by_id(user_id)
    transaction_amount = transaction["transaction_amount"]
    transaction_type = get_transaction_type(transaction)

    user = update_user_balance(user, transaction_amount, transaction_type)
    update_user_transaction_data(
        user, transaction_amount, transaction["transaction_date"]
    )
    update_user_statistics(user)

    # calculate the credit score if needed
    # user["credit_score"] = calculate_average_transaction_score(user["transactions"])

    update_user_in_db(user)


def get_user_by_id(user_id: str) -> User:
    """
    Retrieve a user from the database by their ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        User: The retrieved user data.
    """
    return conn.user.find_one({"_id": ObjectId(user_id)})


def get_transaction_type(transaction: Dict) -> str:
    """
    Determine the type of transaction based on its details.

    Args:
        transaction (Dict): The transaction details.

    Returns:
        str: The type of transaction, either "credit" or "debit".
    """
    return (
        "credit"
        if TransactionType(transaction.get("transaction_type"))
        == TransactionType.credit
        else "debit"
    )


def update_user_balance(
    user: User, transaction_amount: float, transaction_type: str
) -> User:
    """
    Update user's balance based on a transaction.

    Args:
        user (User): The user object.
        transaction_amount (float): The amount of the transaction.
        transaction_type (str): The type of transaction, either "credit" or "debit".

    Returns:
        User: The updated user object.
    """
    if transaction_type == "credit":
        user["balance"] += transaction_amount
    elif transaction_type == "debit":
        user["balance"] -= transaction_amount
    return user


def update_user_transaction_data(
    user: User, transaction_amount: float, transaction_date: datetime
):
    """
    Update user's transaction data with a new transaction.

    Args:
        user (User): The user object.
        transaction_amount (float): The amount of the transaction.
        transaction_date (datetime): The date of the transaction.
    """
    transaction_date_str = transaction_date.strftime("%Y-%m-%d")
    user["transactions"].setdefault(transaction_date_str, []).append(transaction_amount)


def update_user_statistics(user: User) -> None:
    """
    Calculate relevant statistics for the user, and modify the user object entered.

    Args:
        user (User): The user's data.
    """
    user["total_number_of_transactions"] += 1
    user["total_amount_transacted"] += abs(user["balance"])
    user["average_transaction_value"] = (
        user["total_amount_transacted"] / user["total_number_of_transactions"]
    )
    user["date_with_highest_transaction"] = find_date_with_highest_amount(user)


def find_date_with_highest_amount(user: User) -> str:
    """
    Find the date with the highest transaction amount for a user.

    Args:
        user (User): The user's data.

    Returns:
        str: The date with the highest transaction amount.
    """
    max_amount = float("-inf")
    max_date = ""
    for date, amounts in user["transactions"].items():
        total_amount = sum(amounts)
        if total_amount > max_amount:
            max_amount = total_amount
            max_date = date
    return max_date


def update_user_in_db(user: User):
    """
    Update user data in the database.

    Args:
        user (User): The user object with updated data.

    Raises:
        Exception: If there's an error during the database update.
    """
    try:
        conn.user.find_one_and_update({"_id": user["_id"]}, {"$set": dict(user)})
        logger.info("User data updated successfully.")
    except Exception as e:
        logger.error("Error updating user data: %s", str(e))
