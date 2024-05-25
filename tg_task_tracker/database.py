from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import cfg

engine = create_async_engine(cfg.get_db_url())
sessionmaker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    ...


class AsyncSessionFactory:
    async def get_session(self) -> AsyncSession:
        async with sessionmaker() as session:
            return session
