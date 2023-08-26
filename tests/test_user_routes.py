from fastapi.testclient import TestClient
from app.index import app
import pytest

client = TestClient(app)


@pytest.fixture
def create_user():
    response = client.post(
        "/api/create_user",
        json={
            "name": "sedem",
            "email": "sedema@fidocredit.com",
            "phone_number": "233546744163",
            "password": "loong_pwsd",
            "balance": "0.0",
            "date_with_highest_transaction": "",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_find_all_users(create_user):
    response = client.get("/api/find_all_users")
    assert response.status_code == 200
    assert create_user["data"]["name"] == "sedem"


def test_find_one_user(create_user):
    user_id = create_user["data"]["user_id"]
    response = client.get(f"/api/find_one_user/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "sedem"


def test_update_user(create_user):
    user_id = create_user["data"]["user_id"]
    response = client.put(
        f"/api/update_user/{user_id}",
        json={
            "name": "Sedem Quame Amekpewu",
            "email": "sedema@fidocredit.com",
            "phone_number": "0546744163",
            "password": "changed_pwsd",
            "balance": 0.0,
            "date_with_highest_transaction": "",
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Sedem Quame Amekpewu"


def test_delete_user(create_user):
    user_id = create_user["data"]["user_id"]
    response = client.delete(f"/api/delete_user/{user_id}")
    assert response.status_code == 200
