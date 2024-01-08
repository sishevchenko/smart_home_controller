from aiogram import Bot
from aiogram.enums import ParseMode

from src.config import CONFIG

async def bot_main():
    bot: Bot = Bot(token=CONFIG.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await CONFIG.DISPATCHER.start_polling(bot)
