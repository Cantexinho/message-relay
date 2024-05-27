import pytest
import unittest
import json
from unittest.mock import MagicMock, AsyncMock, patch
from event_propagator.propagator import Propagator


@pytest.mark.asyncio
async def test_initialize():
    mock_token = "mocked_token"
    propagator = Propagator(MockSettings())
    await propagator.initialize()
    propagator.get_token = AsyncMock(return_value=mock_token)
    assert propagator.token == mock_token


def test_get_events():
    mock_data = {"event1": "data1", "event2": "data2"}
    with patch(
        "builtins.open",
        unittest.mock.mock_open(read_data=json.dumps(mock_data)),
    ):
        propagator = Propagator(MockSettings())
        events = propagator.get_events()
    assert events == mock_data


def test_get_random_event():
    mock_events = [{"event": "data1"}, {"event": "data2"}]
    propagator = Propagator(MockSettings())
    propagator.events = mock_events
    random_event = propagator.get_random_event()
    assert random_event in mock_events


@pytest.mark.asyncio
async def test_send_request():
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={"access_token": "mocked_token"}
    )
    mock_session = AsyncMock()
    mock_session.post = AsyncMock(return_value=mock_response)
    propagator = Propagator(MockSettings())
    propagator.get_token = AsyncMock(return_value="mocked_token")
    propagator.get_random_event = MagicMock(return_value={"event": "data"})
    with patch("aiohttp.ClientSession", return_value=mock_session):
        await propagator.send_request()
    mock_session.post.assert_awaited_once_with(
        f"http://event-consumer:8000/{propagator.settings.endpoint_to_post}",
        json=propagator.get_random_event(),
    )


class MockSettings:
    service_name = "mocked_service"
    service_password = "mocked_password"
    scheduler_interval = 5
    endpoint_to_post = "mocked_endpoint"
