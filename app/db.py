from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()
metadata = MetaData()

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_session_context_manager():
    async with async_session() as session:
        yield session
