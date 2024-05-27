"""
    Propagator service entry point.
    Uses async for the possibility of sending request concurently.
    Creates propagator object to send requests.
    Creates scheduler using AsyncIOScheduler() to schedule jobs.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from propagator import Propagator
from settings import Settings


async def main():
    settings = Settings()
    propagator = Propagator(settings)
    await propagator.initialize()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        propagator.send_request,
        "interval",
        seconds=int(settings.scheduler_interval),
    )
    scheduler.start()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
