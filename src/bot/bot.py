from aiogram import Bot
from aiogram.enums import ParseMode

from src.config import CONFIG
from src.bot.handler import DISPATCHER

async def bot_main():
    bot: Bot = Bot(token=CONFIG.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await DISPATCHER.start_polling(bot)
