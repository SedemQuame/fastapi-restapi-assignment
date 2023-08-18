from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://fido-user-transactions:hGWUd302ncxUupi4@cluster0.xj1fc76.mongodb.net/NEW_DATABASE_NAME?retryWrites=true&w=majority"
)
# print(client.list_database_names())  # Print available databases
conn = client.get_database("NEW_DATABASE_NAME")  # Get the desired database
# print(conn.list_collection_names())  # Print collections in the database
