from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import BaseMeta

class BotUser(BaseMeta):
	__tablename__ = "bot_user"

	chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
	username: Mapped[str] = mapped_column(String, nullable=True)
