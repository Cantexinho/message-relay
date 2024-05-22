from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
import asyncio


async def send_request():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/events") as response:
            print(await response.text())


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_request, "interval", seconds=20)
    scheduler.start()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
