from fastapi.testclient import TestClient
from event_consumer.main import app

client = TestClient(app)


def test_readiness():
    response = client.get("/ready/")
    assert response.status_code == 200
    assert response.text == "ok"
