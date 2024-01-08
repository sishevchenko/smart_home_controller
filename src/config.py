import os
import logging
import asyncio
from functools import lru_cache
from typing import Self, final
from pathlib import Path
from types import NoneType

import uvicorn
from aiogram import Dispatcher
from dotenv import load_dotenv

env_is_load = load_dotenv(".env")

if not env_is_load:
	raise FileExistsError("\".env\" file was not found")


@final
class Settings:
	"""Синглтон с настройками приложения"""

	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Settings, cls).__new__(cls)
		return cls.instance

	def __init__(self) -> None:
		self.BASE_DIR: Path = Path(__file__).resolve().parent.parent
		self.DEBUG: bool = True
		self.BOT_START: bool = True
		self._DISPATCHER: Dispatcher | None = None
		self.APP_HOST: str | None = os.getenv("APP_HOST")
		self.APP_PORT: str | None = os.getenv("APP_PORT")
		self.SECRET_KEY: str | None = os.getenv("SECRET_KEY")
		self.API_KEY: str | None = os.getenv("API_KEY")
		self.BOT_URL: str | None = os.getenv("BOT_URL")
		self.BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
		self.REGISTER_KEY: str | None = os.getenv("REGISTER_KEY")
		self.DB_URL: str | None = os.getenv("DB_URL")
		self.ALEMBIC_DB_URL: str | None = os.getenv("ALEMBIC_DB_URL")
		self._SERVER: uvicorn.Server | None = None

	def _get_server(self) -> uvicorn.Server:
		if isinstance(self._SERVER, NoneType):
			self._set_server()
		return self._SERVER

	def _set_server(self) -> None:
		if isinstance(self._SERVER, NoneType):
			config = uvicorn.Config(
				"main:app", 
				host=self.APP_HOST if self.APP_HOST and not self.DEBUG else "127.0.0.1",
				port=self.APP_PORT if self.APP_PORT and not self.DEBUG else 8000,
				reload=True,
				loop="asyncio",
				log_level=logging.DEBUG if self.DEBUG else logging.INFO,
			)
			self._SERVER = uvicorn.Server(config)

	def _del_server(self) -> None:
		if not isinstance(self._SERVER, NoneType):
			loop = asyncio.get_event_loop()
			loop.create_task(self._SERVER.shutdown())
		self._SERVER = None

	SERVER: uvicorn.Server = property(_get_server, _set_server, _del_server)

	def _get_dispatcher(self) -> Dispatcher:
		if isinstance(self._DISPATCHER, NoneType):
			self._set_dispatcher()
		return self._DISPATCHER

	def _set_dispatcher(self) -> None:
		if isinstance(self._DISPATCHER, NoneType):
			self._DISPATCHER = Dispatcher()

	def _del_dispatcher(self) -> None:
		self._DISPATCHER = None

	DISPATCHER = property(_get_dispatcher, _set_dispatcher, _del_dispatcher)

@lru_cache()
def get_settings() -> Settings:
	"""Возвращает синглтон с настройками приложения"""
	return Settings()

CONFIG = get_settings()
