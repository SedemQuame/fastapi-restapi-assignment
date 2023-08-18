import os
from pymongo import MongoClient

client = MongoClient(
    os.getenv("MONGO_URI")
)
conn = client.get_database(os.getenv("MONGO_DB_NAME"))
