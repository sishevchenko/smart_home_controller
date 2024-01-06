from aiogram import Bot
from aiogram.enums import ParseMode

from src.bot.handler import dp
from src.config import BOT_TOKEN

async def bot_main():
    bot: Bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
