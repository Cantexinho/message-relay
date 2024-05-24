from fastapi.testclient import TestClient
from ..event_consumer.main import app
from ..event_consumer.settings import Settings

settings = Settings()

client = TestClient(app)


def test_login():
    response = client.post(
        "/token",
        data={"username": "your_username", "password": "your_password"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_get_events():
    response = client.get(
        "/events", headers={"Authorization": "Bearer your_access_token"}
    )
    assert response.status_code == 200
    assert response.json() == {settings.service_name}
