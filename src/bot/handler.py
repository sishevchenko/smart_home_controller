from datetime import datetime
import logging
import json

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

from src.config import BOT_TOKEN, OWNERS_IDS
from src.bot import state_machine
from src.bot.responses import bot_response


dp: Dispatcher = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """Стартовая информация"""
    if message.chat.id in OWNERS_IDS.keys():
        await message.answer(bot_response["start"])
    logging.info(f"{datetime.utcnow()}: {message.chat.id} {message.chat.username} - Get start info")

@dp.message(Command(commands=['help']))
async def command_help_handler(message: Message):
    """Все комманды с расшифровкой"""
    if message.chat.id in OWNERS_IDS.keys():
        await message.answer(bot_response["help"])
    logging.info(f"{datetime.utcnow()}: {message.chat.id} {message.chat.username} - Get help info")

@dp.message(Command(commands=['get_json']))
async def get_json_handler(message: Message):
    # if message.chat.id in OWNERS_IDS.keys():
        res = "Chat json info:\n\n"
        js = json.loads(message.chat.model_dump_json())
        for k, v in js.items():
            res += f"{k}: {v}\n"
        await message.answer(res)

@dp.message()
async def echo_handler(message: Message):
    """Отвечаю сообщением, которое мне отправили"""
    if message.chat.id in OWNERS_IDS.keys():
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text="Ой, что-то пошло не так :(\n/help")
            logging.info(f"{datetime.utcnow()}: {message.chat.id} {message.chat.username} - Type error in get echo")
    logging.info(f"{datetime.utcnow()}: {message.chat.id} {message.chat.username} - Get echo")


async def bot_main():
    bot: Bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
