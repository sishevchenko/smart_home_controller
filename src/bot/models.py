from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import BaseMeta

class BotUser(BaseMeta):
	__tablename__ = "bot_user"

	username: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
	chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
