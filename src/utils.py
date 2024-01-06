import sys
from datetime import datetime
from logging import getLogger

from aiogram.types import Message

from sqlalchemy import select

from src.config import OWNERS_IDS
from src.bot.models import BotUser

_logger = getLogger(__name__)


def _get_func_name() -> str:
	"""Возвращает имя текущей функции"""
	return sys._getframe(1).f_code.co_name


def _get_log_info(id: int=0, username: str="default", func_name: str="default") -> str:
	return f"{datetime.utcnow()}: {id=} {username=} - {func_name}"


def _check_user_rights(func):
	"""Декоратор для проверки пользовательских прав.
	В хендлерах используется после декоратора перехватчика"""

	async def wraper(message: Message):
		users = select(BotUser).column(BotUser.username)
		if message.chat.id in OWNERS_IDS.keys():
			_logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
			await func(message)
		else:
			await message.answer("Permission denied")
			_logger.warning(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
	return wraper
