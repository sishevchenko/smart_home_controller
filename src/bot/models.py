from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import BaseMeta

class BotUser(BaseMeta):
	"""Класс описывающий пользователей телеграм Бота"""

	__tablename__ = "bot_user"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
	username: Mapped[str] = mapped_column(String, nullable=True)

	def __repr__(self):
		return "{0.__class__.__name__}(id={0.id}, username={0.username})".format(self)
	
	def __bool__(self) -> bool:
		return True if self.id or self.username else False
