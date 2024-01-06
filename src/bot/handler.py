from logging import getLogger
import json

from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

# from sqlalchemy import text
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import REGISTER_KEY
from src.bot.state_machine import StateRegister
from src.bot.response import bot_response
from src.db import get_async_session
from src.utils import _check_user_rights, _get_func_name, _get_log_info
from src.bot.models import BotUser

_logger = getLogger(__name__)

dp: Dispatcher = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """Стартовая информация"""
    await message.answer(bot_response["start"])
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message(Command(commands=['help']))
async def command_help_handler(message: Message):
    """Все комманды с расшифровкой"""
    await message.answer(bot_response["help"])
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))

@dp.message(Command(commands=['register']))
async def user_register_handler(message: Message, state: FSMContext):
    await message.answer("Input REGISTER_KEY")
    await state.set_state(StateRegister.INPUT_REGISTER_KEY)
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message(StateRegister.INPUT_REGISTER_KEY)
async def create_new_user_handler(message: Message, state: FSMContext):
    session: AsyncSession = await get_async_session()
    regiter_key = message.text.strip()
    if regiter_key == REGISTER_KEY:
        query = insert(BotUser).values(username=message.chat.username, chat_id=message.chat.id)
        # await session.execute(query)
        await message.answer(str(query))
        await state.clear()
        _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
    else:
        _logger.warning(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message(Command(commands=['get_json']))
@_check_user_rights
async def get_json_handler(message: Message):
    res = "Chat json info:\n\n"
    _json = json.loads(message.chat.model_dump_json())
    for k, v in _json.items():
        res += f"{k}: {v}\n"
    await message.answer(res)
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message()
@_check_user_rights
async def echo_handler(message: Message):
    """Отвечаю сообщением, которое мне отправили"""
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Ой, что-то пошло не так :(\n/help")
        _logger.error(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
