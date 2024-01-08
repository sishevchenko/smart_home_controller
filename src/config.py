import os
import logging
from functools import lru_cache
from typing import final

import uvicorn
from dotenv import load_dotenv

load_dotenv(".env")


@final
class Settings:
	"""Синглтон с настройками приложения"""

	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Settings, cls).__new__(cls)
		return cls.instance

	def __init__(self) -> None:
		self.DEBUG = True
		self.BOT_START = True
		self.APP_HOST = os.getenv("APP_HOST")
		self.APP_PORT = os.getenv("APP_PORT")
		self.SECRET_KEY = os.getenv("SECRET_KEY")
		self.API_KEY = os.getenv("API_KEY")
		self.BOT_URL = os.getenv("BOT_URL")
		self.BOT_TOKEN = os.getenv("BOT_TOKEN")
		self.REGISTER_KEY = os.getenv("REGISTER_KEY")
		self.DB_URL = os.getenv("DB_URL")
		self.ALEMBIC_DB_URL = os.getenv("ALEMBIC_DB_URL")

		config = uvicorn.Config(
			"main:app", 
			host=self.APP_HOST if self.APP_HOST and not self.DEBUG else "127.0.0.1",
			port=self.APP_PORT if self.APP_PORT and not self.DEBUG else 8000,
			reload=True,
			loop="asyncio",
			log_level=logging.DEBUG if self.DEBUG else logging.INFO,
		)
		self.SERVER = uvicorn.Server(config)


@lru_cache()
def get_settings() -> Settings:
	"""Возвращает синглтон с настройками приложения"""
	return Settings()

CONFIG = get_settings()
