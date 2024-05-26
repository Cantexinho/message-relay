from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
import asyncio

import os


async def get_token():
    async with aiohttp.ClientSession() as session:
        data = {
            "username": os.environ.get("SERVICE_NAME"),
            "password": os.environ.get("SERVICE_PASSWORD"),
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


async def send_request():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
            "http://event-consumer:8000/events"
        ) as response:
            print(await response.text())


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_request, "interval", seconds=20)
    scheduler.start()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
