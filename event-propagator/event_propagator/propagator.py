"""
    Event propagator class used to encapsulate functions
    to succesfully propagate events.
    get_token() -> used for authentication with consumer.
    get_events() -> pulls events from file.
    get_random_event() -> randomly chooses event to post.
    send_request() -> posts event to specified endpoint.
"""

import aiohttp

import json
import random


class Propagator:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.token = None
        self.events = self.get_events()

    async def initialize(self):
        self.token = await self.get_token()

    # REVIEW COMMENT:
    # Ideally, no method or function should have more than 2 nesting levels.
    # This one has 4, which makes it hard to read and test. Could be split into at least 2 methods IMO.
    async def get_token(self):
        async with aiohttp.ClientSession() as session:
            data = {
                "username": self.settings.service_name,
                "password": self.settings.service_password,
            }
            # REVIEW COMMENT:
            # Same as in check_events.py, this url should be moved to settings.
            async with session.post(
                "http://event-consumer:8000/token", data=data
            ) as response:
                # REVIEW COMMENT:
                # As mentioned in check_events.py, this could be replaced with response.raise_for_status(),
                # which would remove an additional nesting layer.
                if response.status == 200:
                    data = await response.json()
                    access_token = data.get("access_token")
                    # REVIEW COMMENT:
                    # What if there is no access token? Seems like it would return None and cause an auth error later on, causing unexpected behaviour.
                    # I believe some exception should be raised in this situation, so it's clear what went wrong.
                    if access_token:
                        return access_token.strip()
                else:
                    # REVIEW COMMENT:
                    # Should this be a ValueError?
                    # A ValueError represents an unexpected value, while this is more to do with the token request failing.
                    raise ValueError(
                        f"Failed to obtain access token: "
                        f"{response.status} {response.reason}"
                    )

    def get_events(self):
        try:
            # REVIEW COMMENT:
            # Paths to static files should also be declared in the settings class.
            with open("/app/data/data.json", "r") as f:
                data = json.load(f)
            return data
        # REVIEW COMMENT:
        # Returning None here would cause an unexpected TypeError in the `get_random_event` method,
        # since random.choice() expects an iterable. Would be better to just reraise the exception.
        except FileNotFoundError:
            print("Error: File not found.")
            return None
        except json.JSONDecodeError:
            print("Error: JSON decoding failed.")
            return None

    def get_random_event(self):
        return random.choice(self.events)

    async def send_request(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        event = self.get_random_event()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                # REVIEW COMMENT:
                # Nitpick, but it's a better practise to use something like urllib.parse.urljoin() here, so it's safe.
                # F.E. this would break if `self.settings.endpoint_to_post` would be declared with a `/` (/event).
                f"http://event-consumer:8000/{self.settings.endpoint_to_post}",
                headers=headers,
                json=event,
            ) as response:
                print(await response.text())
