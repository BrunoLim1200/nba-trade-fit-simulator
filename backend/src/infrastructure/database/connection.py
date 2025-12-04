from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from src.core.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base class para todos os models SQLAlchemy"""
    pass


# Engine assíncrona para SQLite
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Session factory assíncrona
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para injetar sessão do banco"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Cria todas as tabelas no banco"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)