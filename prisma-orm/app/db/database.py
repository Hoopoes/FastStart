import prisma
from datetime import timedelta
from app.utils.logger import LOG


prisma_client = prisma.Prisma(auto_register=True)


async def init_db():
    await prisma_client.connect(timeout=timedelta(seconds=20))
    LOG.info("Successfully connected to Prisma.")


async def close_db():
    await prisma_client.disconnect(timeout=timedelta(seconds=20))
    LOG.info("Successfully disconnected from Prisma")

