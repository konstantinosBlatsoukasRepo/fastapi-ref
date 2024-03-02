from jose import jwt
from app.config import settings


# references the clients from the fixture
def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "el_caabi@osfp.com", "password": "test"}
    )
    print(response.json())
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    res = response.json()
    print(res)
    payload = jwt.decode(
        res["access_token"], settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert response.status_code == 200
