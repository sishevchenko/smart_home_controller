import sys
import asyncio
import logging

from fastapi import FastAPI

from src.config import CONFIG
from src.bot.bot import bot_main

_logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Home Controller",
    debug=CONFIG.DEBUG,
    version="0.1.0"
)

async def main():
    if CONFIG.DEBUG:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    else:
        logging.basicConfig(level=logging.INFO, filename="server.log", filemode="a")

    tasks = []
    if CONFIG.BOT_START:
        tasks.append(bot_main())
    if CONFIG.API_START:
        tasks.append(CONFIG.SERVER.serve())
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
else:
    if CONFIG.BOT_START:
        loop = asyncio.get_event_loop()
        loop.create_task(bot_main())
