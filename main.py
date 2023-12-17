import sys
import asyncio
import logging
from datetime import datetime

from fastapi import FastAPI

from src.config import DEBUG, BOT_START
from src.bot.handler import bot_main


app = FastAPI(
    title="Smart Home Controller",
    debug=DEBUG,
    version="0.0.1"
)


loop = asyncio.get_running_loop()

if DEBUG:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
else:
    logging.basicConfig(level=logging.INFO, filename="server.log", filemode="a")

logging.info(f"{datetime.utcnow()} - Project started")

if BOT_START:
    loop.create_task(bot_main())
    logging.info(f"{datetime.utcnow()} - Bot started")
