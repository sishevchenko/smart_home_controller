from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import CONFIG

BaseMeta: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(CONFIG.DB_URL, echo=True, future=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Используется в связке с fastapi.Depends для получения асинхронных сессий"""
    async with async_session_maker() as session:
        yield session
