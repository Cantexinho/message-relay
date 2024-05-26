from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from propagator import Propagator


async def main():
    propagator = Propagator()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(propagator.send_request, "interval", seconds=20)
    scheduler.start()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
