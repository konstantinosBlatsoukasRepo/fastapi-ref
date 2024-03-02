from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_hello_world():
    response = client.get("/")
    print(response)
