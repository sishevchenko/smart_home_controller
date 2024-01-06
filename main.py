import sys
import asyncio
import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI

from src.config import (
    DEBUG,
    BOT_START,
    APP_HOST,
    APP_PORT,
)
from src.bot.bot import bot_main

_logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Home Controller",
    debug=DEBUG,
    version="0.1.0"
)

loop = asyncio.get_event_loop()

if DEBUG:
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
else:
    logging.basicConfig(level=logging.INFO, filename="server.log", filemode="a")

if BOT_START:
    loop.create_task(bot_main())


if __name__ == "__main__":
    config = uvicorn.Config(
        "main:app", 
        host=APP_HOST if APP_HOST and not DEBUG else "127.0.0.1",
        port=APP_PORT if APP_PORT and not DEBUG else 8000,
        reload=True,
        loop="asyncio",
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()
