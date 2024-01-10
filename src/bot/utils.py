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


def _get_log_info(id: int=0, username: str="undefined", other_info: str="", func_name: str="undefined") -> str:
	"""Возвращает стандартную строку логирования"""
	return f"{datetime.utcnow()}: {id=} {username=} {other_info}- {func_name}"


def _check_user_rights(func):
	"""Декоратор для проверки пользовательских прав.
	В хендлерах используется после декоратора перехватчика"""

	async def wraper(message: Message):
		session: AsyncSession = await get_async_session()
		query = select(BotUser).where(BotUser.id == message.from_user.id)
		user = await session.execute(query)
		if user.scalars().first():
			_logger.info(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))
			await func(message)
		else:
			await message.answer("Отказано в доступе!")
			_logger.warning(_get_log_info(message.from_user.id, message.from_user.username, _get_func_name()))
	return wraper
