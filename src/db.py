from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker


BaseMeta: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True, future=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        return session
