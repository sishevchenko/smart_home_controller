from logging import getLogger
import json

from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import CONFIG
from src.db import get_async_session
from src.bot.state_machine import StateRegister
from src.bot.response import bot_response
from src.bot.utils import _check_user_rights, _get_func_name, _get_log_info
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
    """Начало регистрации в боте нового пользователя или обновление его данных"""

    if message.from_user.id != message.chat.id:
        await message.answer("Пройти регистрацию можно только в личном чате с ботом!")
        return

    await message.answer("Введите ключ доступа")
    await state.set_state(StateRegister.INPUT_REGISTER_KEY)
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message(StateRegister.INPUT_REGISTER_KEY)
async def create_new_user_handler(message: Message, state: FSMContext):
    """Второй этап регистрации пользователя с проверкой ключа доступа"""

    session: AsyncSession = await get_async_session()
    regiter_key = message.text.strip()
    if regiter_key == CONFIG.REGISTER_KEY:
        query = insert(BotUser).values(username=message.chat.username, chat_id=message.chat.id)
        on_conflict_do_update_query = query.on_conflict_do_update(set_=dict(username=message.chat.username))
        await session.execute(on_conflict_do_update_query)
        await session.commit()
        await message.answer("Данные успешно обновлены!")
        await state.clear()
        _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
    else:
        await message.answer("Неверный ключ регистрации!")
        _logger.warning(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message(Command(commands=['id']))
@_check_user_rights
async def get_id_handler(message: Message):
    """Возвращает идентификатор пользователя"""
    await message.answer(f"id = {message.from_user.id}")


@dp.message(Command(commands=['chat_id']))
@_check_user_rights
async def get_chat_id_handler(message: Message):
    """Возвращает идентификатор чата"""
    await message.answer(f"chat_id = {message.chat.id}")


@dp.message(Command(commands=['chat_info']))
@_check_user_rights
async def get_json_handler(message: Message):
    res = "Информация о чате:\n\n"
    _json = json.loads(message.chat.model_dump_json())
    for k, v in _json.items():
        res += f"{k}: {v}\n"
    await message.answer(res)
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))


@dp.message(Command(commands=['user_info']))
@_check_user_rights
async def get_user_info_handler(message: Message):
    """Возвращает данные пользователя из базы данных"""
    session: AsyncSession = await get_async_session()
    query = select(BotUser).where(BotUser.username == message.chat.username)
    user = await session.execute(query)
    user = user.scalars().first()
    chat_id = user.chat_id
    username = user.username
    await message.answer(f"chat_id = {chat_id}\nusername = {username}")


@dp.message()
# @_check_user_rights
async def echo_handler(message: Message):
    """Отвечаю сообщением, которое мне отправили"""
    try:
        await message.answer("Простите, я не понимаю\nПожалуйста, посмотрите инструкцию по команде\n/help")
    except TypeError:
        await message.reply(text="Ой, что-то пошло не так :(\n/help")
        _logger.error(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
