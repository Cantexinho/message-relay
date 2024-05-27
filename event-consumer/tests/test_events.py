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


def test_get_events(client, access_token):
    response = client.get(
        "/events", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_post_event(client, access_token):
    event_data = {"event_type": "message", "event_payload": "hello"}

    response = client.post(
        "/events/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=event_data,
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
