from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.index import app
from unittest.mock import MagicMock
from app.routes.user_route import create_user, find_all_users, find_one_user
from app.models.user_model import User
from app.schemas.user_schema import UserResponse
import pytest

client = TestClient(app)


class MockUserCollection:
    def __init__(self, users):
        self.users = users

    def insert_one(self, data):
        inserted_id = str(len(self.users) + 1)  # Mocking insertion
        self.users.append({**data, "_id": inserted_id})
        return inserted_id

    def find(self):
        return self.users

    def find_one(self, query):
        for user in self.users:
            if str(user['_id']) == str(query['_id']):
                return user
        return None

    def find_one_and_update(self, query, update):
        for user in self.users:
            if str(user['_id']) == str(query['_id']):
                user.update(update['$set'])
                return user
        return None

    def find_one_and_delete(self, query):
        for user in self.users:
            if str(user['_id']) == str(query['_id']):
                self.users.remove(user)
                return user
        return None

@pytest.fixture
def mock_conn(monkeypatch):
    mock = MagicMock()
    mock_user_data = [
        {'_id': '1', 'name': 'John Doe', 'email': 'john@example.com'},
        {'_id': '2', 'name': 'Jane Doe', 'email': 'jane@example.com'}
    ]
    mock.user = MockUserCollection(mock_user_data)
    monkeypatch.setattr('app.config.db.conn', mock)
    return mock

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_user(mock_conn):
    user_data = {
        "name": "sedem",
        "email": "sedema@fidocredit.com",
        "phone_number": "233546744163",
        "password": "loong_pwsd",
        "balance": 0.0,
        "date_with_highest_transaction": "",
    }
    user = User(**user_data)
    response = await create_user(user)
    assert response.name == user_data["name"]
    assert response.email == user_data["email"]


def test_find_all_users(mock_conn):
    response = find_all_users()
    assert isinstance(response, list)

def test_find_one_user(mock_conn):
    response = client.get("/find_one_user/1")
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe'

def test_find_one_user_not_found(mock_conn):
    response = client.get("/find_one_user/3")
    assert response.status_code == 404

def test_update_user(mock_conn):
    new_user_data = {'name': 'Updated User', 'email': 'updated@example.com'}
    response = client.put("/update_user/1", json=new_user_data)
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated User'
    assert response.json()['email'] == 'updated@example.com'

def test_delete_user(mock_conn):
    response = client.delete("/delete_user/1")
    assert response.status_code == 200
    assert response.json()['name'] == 'John Doe'

