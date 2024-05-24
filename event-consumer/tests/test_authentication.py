from fastapi.testclient import TestClient
import pytest

from event_consumer.main import app
from event_consumer.settings import Settings

settings = Settings()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def access_token(client):
    response = client.post(
        "/token",
        data={
            "username": settings.service_name,
            "password": settings.service_password,
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login(client):
    response = client.post(
        "/token",
        data={
            "username": settings.service_name,
            "password": settings.service_password,
        },
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_get_events(client, access_token):
    response = client.get(
        "/events", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == settings.service_name
