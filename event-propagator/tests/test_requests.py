import pytest
from aioresponses import aioresponses
from event_propagator.propagator import Propagator


@pytest.fixture
def propagator():
    return Propagator()


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("SERVICE_NAME", "test_user")
    monkeypatch.setenv("SERVICE_PASSWORD", "test_password")


@pytest.mark.asyncio
async def test_get_token_success(mock_env, propagator):
    with aioresponses() as mock_service:
        mock_service.post(
            "http://event-consumer:8000/token",
            payload={"access_token": "test_token", "token_type": "bearer"},
        )

        token = await propagator.get_token()
        assert token == "test_token"


@pytest.mark.asyncio
async def test_get_token_failure(mock_env, propagator):
    with aioresponses() as mock_service:
        mock_service.post("http://event-consumer:8000/token", status=401)

        with pytest.raises(ValueError) as excinfo:
            await propagator.get_token()
        assert "Failed to obtain access token" in str(excinfo.value)


@pytest.mark.asyncio
async def test_send_request_success(mock_env, propagator):
    with aioresponses() as mock_service:
        mock_service.post(
            "http://event-consumer:8000/token",
            payload={"access_token": "test_token", "token_type": "bearer"},
        )
        mock_service.post(
            "http://event-consumer:8000/events",
            payload={
                "type": "message",
                "payload": "hello",
            },
        )
        await propagator.send_request()
