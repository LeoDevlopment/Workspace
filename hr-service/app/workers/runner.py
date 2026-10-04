import asyncio
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("worker")


async def main() -> None:
    log.info("Worker started (no jobs yet)")
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())