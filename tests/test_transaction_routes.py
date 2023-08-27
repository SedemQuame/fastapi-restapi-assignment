from fastapi.testclient import TestClient
from app.index import app
import pytest

client = TestClient(app)


@pytest.fixture
def create_transaction():
    response = client.post(
        "/api/create_transaction",
        json={
            "user_id": "64e9fabf5ca336038d18015c",
            "full_name": "sedem_amekpewu",
            "transaction_date": "2023-08-18T15:30:00Z",
            "transaction_amount": 21.00,
            "transaction_type": "credit",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_find_all_transactions(create_transaction):
    transaction_id = create_transaction["data"]["transaction_id"]
    response = client.get(f"/api/find_transactions_by_user/{transaction_id}")
    assert response.status_code == 200


def test_find_one_transaction(create_transaction):
    transaction_id = create_transaction["data"]["transaction_id"]
    response = client.get(f"/api/find_transactions_by_id/{transaction_id}")
    assert response.status_code == 200


def test_update_transaction(create_transaction):
    transaction_id = create_transaction["data"]["transaction_id"]
    response = client.put(
        f"/api/update_transaction/{transaction_id}",
        json={
            "transaction_id": "",
            "user_id": "64e9fabf5ca336038d18015c",
            "full_name": "abrantie_sedem_da_first",
            "transaction_date": "2023-08-18T15:30:00",
            "transaction_amount": 21.00,
            "transaction_type": "credit",
        },
    )
    assert response.status_code == 200


def test_delete_transaction(create_transaction):
    transaction_id = create_transaction["data"]["transaction_id"]
    response = client.delete(f"/api/delete_transactions/{transaction_id}")
    assert response.status_code == 200
