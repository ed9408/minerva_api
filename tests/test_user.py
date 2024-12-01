from fastapi import status
from fastapi.testclient import TestClient

from src.models.user import UserCreate


def test_create_user(client: TestClient):
    endpoint: str = "/api/v1/users"
    user_data: UserCreate = {
        "name": "John Doe",
        "email": "john.doe@mail.com",
        "password": "password",
        "role": "user",
    }

    response = client.post(endpoint, json=user_data)

    print(response.url)

    assert response.status_code == status.HTTP_201_CREATED


def test_login_user(client: TestClient):
    endpoint: str = "/api/v1"
    user_data: UserCreate = {
        "name": "John Doe",
        "email": "john.doe@mail.com",
        "password": "password",
        "role": "user",
    }

    create_response = client.post(f"{endpoint}/users", json=user_data)

    assert create_response.status_code == status.HTTP_201_CREATED

    login_response = client.post(
        f"{endpoint}/auth/login",
        data={"username": "john.doe@mail.com", "password": "password"},
    )

    assert login_response.status_code == status.HTTP_200_OK
