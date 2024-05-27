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

    async def get_token(self):
        async with aiohttp.ClientSession() as session:
            data = {
                "username": self.settings.service_name,
                "password": self.settings.service_password,
            }
            async with session.post(
                "http://event-consumer:8000/token", data=data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    access_token = data.get("access_token")
                    if access_token:
                        return access_token.strip()
                else:
                    raise ValueError(
                        f"Failed to obtain access token: "
                        f"{response.status} {response.reason}"
                    )

    def get_events(self):
        try:
            with open("/app/data/data.json", "r") as f:
                data = json.load(f)
            return data
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
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                f"http://event-consumer:8000/{self.settings.endpoint_to_post}",
                json=event,
            ) as response:
                print(await response.text())
