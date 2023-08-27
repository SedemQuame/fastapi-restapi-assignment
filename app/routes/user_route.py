from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.config.db import conn
from app.schemas.user_schema import UserResponseDict, UserResponseList
from bson import ObjectId
from typing import List, Dict
import pprint

# Create an APIRouter instance
user_router = APIRouter()


@user_router.post("/create_user", response_model=UserResponseDict)
async def create_user(user: User):
    """
    Create a new user.

    Args:
        user (User): User data to be created.

    Returns:
        UserResponse: Serialized user data.
    """
    try:
        inserted_user = conn.user.insert_one(dict(user))
        if inserted_user.inserted_id:
            user_data = dict(user)
            user_data["user_id"] = str(inserted_user.inserted_id)
            return {
                "status": "200",
                "message": "Successfully created the user.",
                "data": User(**user_data),
            }
        else:
            return {
                "status": "400",
                "message": "Unable to process request.",
                "data": User(**user_data),
            }
        # raise HTTPException(status_code=500, detail="Failed to create user.")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@user_router.get("/find_all_users", response_model=UserResponseList)
async def find_all_users():
    """
    Get all users.

    Returns:
        List[User]: List of serialized user data.
    """
    try:
        users = conn.user.find()
        serialized_users = []
        for user in users:
            user_data = dict(user)
            user_data["user_id"] = str(user_data["_id"])
            serialized_users.append(User(**user_data))
        return {
            "status": "200",
            "message": "Successfully returned all users.",
            "data": serialized_users,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.get("/find_one_user/{user_id}", response_model=UserResponseDict)
async def find_one_user(user_id: str):
    """
    Get a user by ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        UserResponse: Serialized user data.
    """
    try:
        user = conn.user.find_one({"_id": ObjectId(user_id)})
        if user:
            user_data = dict(user)
            user_data["user_id"] = str(user_data["_id"])
            return {
                "status": "200",
                "message": "Successfully returned user with the specified user_id.",
                "data": User(**user_data),
            }
        else:
            raise HTTPException(
                status_code=404, detail="User with specified id not found"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.put("/update_user/{user_id}", response_model=UserResponseDict)
async def update_user(user_id: str, update_payload: User):
    """
    Update a user by ID.

    Args:
        user_id (str): The ID of the user to update.
        update_payload (User): Updated user data.

    Returns:
        UserResponse: Serialized user data after update.
    """
    try:
        conn.user.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": dict(update_payload)})
        updated_user = conn.user.find_one({"_id": ObjectId(user_id)})
        if updated_user:
            user_data = dict(updated_user)
            user_data["user_id"] = str(user_data["_id"])
            return {
                "status": "200",
                "message": "Successfully updated user record with the specified user_id.",
                "data": User(**user_data),
            }
        else:
            raise HTTPException(
                status_code=404, detail="User with specified id not found"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.delete("/delete_user/{user_id}", response_model=UserResponseDict)
async def delete_user(user_id: str):
    """
    Delete a user by ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        UserResponse: Serialized user data of the deleted user.
    """
    try:
        deleted_user = conn.user.find_one_and_delete({"_id": ObjectId(user_id)})
        if deleted_user:
            user_data = dict(deleted_user)
            user_data["user_id"] = str(user_data["_id"])
            return {
                "status": "200",
                "message": "Successfully deleted user record with the specified user_id.",
                "data": User(**user_data),
            }
        else:
            raise HTTPException(
                status_code=404, detail="User with specified id not found"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
