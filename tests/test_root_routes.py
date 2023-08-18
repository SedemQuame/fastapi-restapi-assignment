from fastapi.testclient import TestClient
from app.index import app
import sys

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "To view the documentations @ http://127.0.0.1:8000/docs"}


def test_root_api_endpoint():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"msg": "To view the documentations @ http://127.0.0.1:8000/docs"}
