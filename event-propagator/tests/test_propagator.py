import pytest
import unittest
import json
from unittest.mock import MagicMock, AsyncMock, patch
from event_propagator.propagator import Propagator


@pytest.mark.asyncio
async def test_initialize():
    mock_token = "mocked_token"
    propagator = Propagator(MockSettings())
    propagator.get_token = AsyncMock(return_value=mock_token)
    await propagator.initialize()
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


class MockSettings:
    service_name = "mocked_service"
    service_password = "mocked_password"
    scheduler_interval = 5
    endpoint_to_post = "mocked_endpoint"
