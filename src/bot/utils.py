import sys
from datetime import datetime
from logging import getLogger

from aiogram.types import Message

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.models import BotUser
from src.db import get_async_session

_logger = getLogger(__name__)


def _get_func_name() -> str:
	"""Возвращает имя текущей функции"""
	return sys._getframe(1).f_code.co_name


def _get_log_info(id: int=0, username: str="default", other_info: str="", func_name: str="default") -> str:
	"""Возвращает стандартную строку логирования"""
	return f"{datetime.utcnow()}: {id=} {username=} {other_info}- {func_name}"


def _check_user_rights(func):
	"""Декоратор для проверки пользовательских прав.
	В хендлерах используется после декоратора перехватчика"""

	async def wraper(message: Message):
		session: AsyncSession = await get_async_session()
		query = select(BotUser).where(BotUser.username == message.chat.username)
		user = await session.execute(query)
		if user.scalars().first():
			_logger.info(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
			await func(message)
		else:
			await message.answer("Permission denied")
			_logger.warning(_get_log_info(message.chat.id, message.chat.username, _get_func_name()))
	return wraper
