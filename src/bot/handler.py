from logging import getLogger
import json

from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from src.config import CONFIG
from src.db import async_session_maker
from src.bot.state_machine import StateRegister
from src.bot.response import BOT_RESPONSE
from src.bot.utils import _check_user_rights, _get_func_name, _get_log_info
from src.bot.models import BotUser
from src.config import CONFIG

_logger = getLogger(__name__)


@CONFIG.DISPATCHER.message(CommandStart())
async def command_start_handler(message: Message):
    """Стартовая информация"""
    await message.answer(BOT_RESPONSE.START)
    _logger.info(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))


@CONFIG.DISPATCHER.message(Command(commands=['help']))
async def command_help_handler(message: Message):
    """Все комманды с расшифровкой"""
    await message.answer(BOT_RESPONSE.HELP)
    _logger.info(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))


@CONFIG.DISPATCHER.message(Command(commands=['register']))
async def user_register_handler(message: Message, state: FSMContext):
    """Начало регистрации в боте нового пользователя или обновление его данных"""

    if message.from_user.id != message.chat.id:
        await message.answer("Пройти регистрацию можно только в личном чате с ботом!")
        return

    await message.answer("Введите ключ доступа")
    await state.set_state(StateRegister.INPUT_REGISTER_KEY)
    _logger.info(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))


@CONFIG.DISPATCHER.message(StateRegister.INPUT_REGISTER_KEY)
async def create_new_user_handler(message: Message, state: FSMContext):
    """Второй этап регистрации пользователя с проверкой ключа доступа"""

    async with async_session_maker() as session:
        regiter_key = message.text.strip()
        if regiter_key == CONFIG.REGISTER_KEY:
            query = insert(BotUser).values(id=message.from_user.id, username=message.chat.username)
            on_conflict_do_update_query = query.on_conflict_do_update(set_=dict(username=message.chat.username))
            await session.execute(on_conflict_do_update_query)
            await session.commit()
            await message.answer("Данные успешно обновлены!")
            _logger.info(_get_log_info(message.from_user.id, message.chat.username, _get_func_name()))
            return
        else:
            await message.answer("Неверный ключ регистрации!")
            _logger.warning(_get_log_info(message.from_user.id, message.chat.username, _get_func_name()))
    await state.clear()


@CONFIG.DISPATCHER.message(Command(commands=['id']))
@_check_user_rights
async def get_id_handler(message: Message):
    """Возвращает идентификатор пользователя"""
    await message.answer(f"id = {message.from_user.id}")


@CONFIG.DISPATCHER.message(Command(commands=['chat_id']))
@_check_user_rights
async def get_chat_id_handler(message: Message):
    """Возвращает идентификатор чата"""
    await message.answer(f"chat_id = {message.chat.id}")


@CONFIG.DISPATCHER.message(Command(commands=['chat_info']))
@_check_user_rights
async def get_json_handler(message: Message):
    """Возвращает json информацию о чате"""

    res = "Информация о чате:\n\n"
    _json = json.loads(message.chat.model_dump_json())
    for k, v in _json.items():
        res += f"{k}: {v}\n"
    await message.answer(res)
    _logger.info(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))


@CONFIG.DISPATCHER.message(Command(commands=['user_info']))
@_check_user_rights
async def get_user_info_handler(message: Message):
    """Возвращает данные пользователя из базы данных"""

    async with async_session_maker() as session:
        query = select(BotUser).where(BotUser.id == message.from_user.id).limit(1)
        user: BotUser = await session.execute(query)
        user = user.scalars().first()
        if user:
            id = user.id
            username = user.username
            await message.answer(f"{id=}\n{username=}")
            _logger.info(_get_log_info(id, username, _get_func_name()))
            return
    await message.answer(f"Пользователь id={message.from_user.id} username={message.from_user.username} не найден:(")
    _logger.info(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))


@CONFIG.DISPATCHER.message()
@_check_user_rights
async def echo_handler(message: Message):
    try:
        await message.answer("Простите, я не понимаю\nПожалуйста, посмотрите инструкцию по команде\n/help")
    except TypeError:
        await message.reply(text="Ой, что-то пошло не так :(\n/help")
        _logger.error(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
    _logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
