import os
from typing import Dict
from bson import ObjectId
from config.db import conn
# from celery.app import Celery

# redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# celery_app = Celery(__name__, broker=redis_url, backend=redis_url)


# @celery_app.task
def send_sms(transaction: Dict):
    # Put your Infobip SMS sending logic here
    # Example: Call Infobip API to send SMS
    # TODO: Setup the sms function to send actual smses
    # user_id = transaction["user_id"]
    # user = conn.user.find_one({"_id": ObjectId(user_id)})
    # phone_number = user["phone_number"]
    phone_number = "233546744163"
    message = f'Hi {transaction["full_name"]},\nYour account has been {transaction["transaction_type"]}ed, GHS {transaction["transaction_amount"]}.00'
    print(f"Sending SMS to {phone_number}: {message}")


# @celery_app.task
def update_user_stats(transaction: Dict):
    # use the user_id to return the user's record.
    # credit/debit the user's account (by doing +/-transaction_amount)
    # depending on transaction_type (credit/debit).

    # update the transaction list information
    # sample data should look like
    # {
    #     "name": "",
    #     "email": "",
    #     "phone_number": "",
    #     "password": "",
    #     "balance": 0,
    #     "transactions":[
    #         "2023-08-18T15:30:00Z": ["+amount", "+amount", "-amount"]
    #     ]
    #     "credit_score": ""
    # }
    print("Calculating statistics")
