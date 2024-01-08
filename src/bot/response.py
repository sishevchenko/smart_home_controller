from functools import lru_cache
from typing import Self

from src.config import CONFIG


class BotResponse:
	"""Класс отвечающий за основные стандартные ответы бота"""

	def __new__(cls) -> Self:
		if not hasattr(cls, 'instance'):
			cls.instance = super(BotResponse, cls).__new__(cls)
		return cls.instance

	def __init__(self) -> None:
		self.START = "Привет! Я Бот для управления умным домом с возможностью получить дополнительную техническую информацию из Telegram"
		self.HELP = (
			"/start - Стартовая информация\n"
			"/register - Для получения доступа к основным функциям бота пройдите простую регистрацию. "
			f"Для прохождения регистрации нужен код, который можно узнать у {CONFIG.OWNER}.\n"
			"/id - Показывает идентификатор пользователя Telegram отправившего боту сообщение. "
			"Для получения ```id``` требуется регистрация\n"
			"/chat_id - Показывает идентификатор чата, из которого вызвана команда. "
			"Для получения ```chat_id``` требуется регистрация\n"
			"/chat_info - Показывает всю техническую информацию о чате. "
			"Для получения ```chat_info``` требуется регистрация\n"
			"/user_info - Показывает информацию хранящуюся в базе данных запросившего пользователя. "
			"Для получения ```user_info``` требуется регистрация\n"
		)

@lru_cache()
def get_bot_response() -> BotResponse:
	"""Возвращает синглтон с настройками приложения"""
	return BotResponse()

BOT_RESPONSE = get_bot_response()
