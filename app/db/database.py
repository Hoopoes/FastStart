from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from config import CONFIG
from app.utils.logger import LOG
from app.models.db_models import Base


DATABASE_URL = CONFIG.database_url  # For local SQLite file


engine = create_async_engine(
    url=DATABASE_URL,
    # Logs SQL queries (useful for debugging, disable in production if noisy)
    echo=True,
    # Checks connection health before using it
    # Prevents stale connection errors after idle time
    pool_pre_ping=True,
    # Number of persistent DB connections kept open
    # Good baseline for small to medium apps
    pool_size=5,
    # Max time (seconds) to wait if all connections are busy
    pool_timeout=30,
    # Extra temporary connections allowed beyond pool_size
    max_overflow=10,
    # How long a connection can live before being recycled
    # -1 means "never recycle automatically"
    pool_recycle=-1,
)

# Session local
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Async DB dependency
async def get_db():
    LOG.info("Opening database session")
    async with SessionLocal() as db:
        LOG.info("Database session opened")
        try:
            yield db
        finally:
            LOG.info("Database session closed")


async def init_db():
    async with engine.begin() as conn:
        # Creates tables asynchronously
        await conn.run_sync(Base.metadata.create_all)
    LOG.info("Successfully connected to Database.")


async def close_db():
    await engine.dispose()
    LOG.info("Successfully disconnected from Database")
