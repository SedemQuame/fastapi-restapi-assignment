from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.config.db import conn
from app.schemas.user_schema import UserResponse
from bson import ObjectId
from typing import List

# Create an APIRouter instance
user_router = APIRouter()


@user_router.post("/create_user", response_model=UserResponse)
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
            user_data["_id"] = str(inserted_user.inserted_id)
            return UserResponse(**user_data)
        else:
            raise HTTPException(status_code=500, detail="Failed to insert user data")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@user_router.get("/find_all_users", response_model=List[UserResponse])
async def find_all_users():
    """
    Get all users.

    Returns:
        List[UserResponse]: List of serialized user data.
    """
    try:
        users = conn.user.find()
        serialized_users = []
        for user in users:
            user_data = dict(user)
            user_data["_id"] = str(user_data["_id"])
            serialized_users.append(UserResponse(**user_data))
        return serialized_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.get("/find_one_user/{id}", response_model=UserResponse)
async def find_one_user(id: str):
    """
    Get a user by ID.

    Args:
        id (str): The ID of the user.

    Returns:
        UserResponse: Serialized user data.
    """
    try:
        user = conn.user.find_one({"_id": ObjectId(id)})
        if user:
            user_data = dict(user)
            user_data["_id"] = str(user_data["_id"])
            return UserResponse(**user_data)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.put("/update_user/{id}", response_model=UserResponse)
async def update_user(id: str, user: User):
    """
    Update a user by ID.

    Args:
        id (str): The ID of the user to update.
        user (User): Updated user data.

    Returns:
        UserResponse: Serialized user data after update.
    """
    try:
        conn.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
        updated_user = conn.user.find_one({"_id": ObjectId(id)})
        if updated_user:
            user_data = dict(updated_user)
            user_data["_id"] = str(user_data["_id"])
            return UserResponse(**user_data)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.delete("/delete_user/{id}", response_model=UserResponse)
async def delete_user(id: str):
    """
    Delete a user by ID.

    Args:
        id (str): The ID of the user to delete.

    Returns:
        UserResponse: Serialized user data of the deleted user.
    """
    try:
        deleted_user = conn.user.find_one_and_delete({"_id": ObjectId(id)})
        if deleted_user:
            user_data = dict(deleted_user)
            user_data["_id"] = str(user_data["_id"])
            return UserResponse(**user_data)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
