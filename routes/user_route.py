from fastapi import APIRouter
from models.user_model import User
from config.db import conn
from schemas.user_schema import serializeDict, serializeList, userEntity
from bson import ObjectId
from typing import List, Dict
import pprint

# Create an APIRouter instance
user_router = APIRouter()


@user_router.post("/create_user")
async def create_user(user: User):
    """
    Create a new user.

    Args:
        user (User): User data to be created.

    Returns:
        list: List of serialized user data.
    """
    inserted_user = conn.user.insert_one(dict(user))
    serialized_user = serializeList(conn.user.find())
    return serialized_user


@user_router.get("/find_all_users", response_model=List[User])
async def find_all_users():
    """
    Get all users.

    Returns:
        list: List of serialized user data.
    """
    return serializeList(conn.user.find())


@user_router.get("/find_one_user/{id}", response_model=User)
async def find_one_user(id: str):
    """
    Get a user by ID.

    Args:
        id (str): The ID of the user.

    Returns:
        dict: Serialized user data.
    """
    return serializeDict(conn.user.find_one({"_id": ObjectId(id)}))


@user_router.put("/update_user/{id}", response_model=User)
async def update_user(id: str, user: User):
    """
    Update a user by ID.

    Args:
        id (str): The ID of the user to update.
        user (User): Updated user data.

    Returns:
        dict: Serialized user data after update.
    """
    conn.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return serializeDict(conn.user.find_one({"_id": ObjectId(id)}))


@user_router.delete("/delete_user/{id}", response_model=User)
async def delete_user(id: str):
    """
    Delete a user by ID.

    Args:
        id (str): The ID of the user to delete.

    Returns:
        dict: Serialized user data of the deleted user.
    """
    return serializeDict(conn.user.find_one_and_delete({"_id": ObjectId(id)}))
