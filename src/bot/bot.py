from aiogram import Bot
from aiogram.enums import ParseMode

from src.config import CONFIG
from src.bot.handler import dp

async def bot_main():
    bot: Bot = Bot(token=CONFIG.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
