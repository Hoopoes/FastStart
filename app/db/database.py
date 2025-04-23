from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import CONFIG
from app.utils.logger import LOG


DATABASE_URL = CONFIG.database_url  # For local SQLite file

# Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

# Async DB dependency
async def get_db():
    async with SessionLocal() as db:
        yield db  # This is your DB session

async def init_db():
    async with engine.begin() as conn:
        # Creates tables asynchronously
        await conn.run_sync(Base.metadata.create_all)
    LOG.info("Successfully connected to Prisma.")


async def close_db():
    await engine.dispose()
    LOG.info("Successfully disconnected from Prisma")

