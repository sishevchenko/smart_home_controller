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

loop = asyncio.get_event_loop()

if CONFIG.DEBUG:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
else:
    logging.basicConfig(level=logging.INFO, filename="server.log", filemode="a")

if CONFIG.BOT_START:
    loop.create_task(bot_main())


if __name__ == "__main__":
    CONFIG.SERVER.run()
