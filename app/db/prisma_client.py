import prisma
import asyncio
from datetime import timedelta
from app.utils.logger import LOG


prisma_client = prisma.Prisma(auto_register=True)


async def connect_prisma():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            await prisma_client.connect(timeout=timedelta(seconds=20))
            LOG.info("Successfully connected to Prisma.")
            break
        except Exception as e:
            LOG.error(f"Failed to connect to Prisma (Attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                await asyncio.sleep(3)
    else:
        LOG.error("Unable to connect to Prisma after multiple attempts.")
        raise RuntimeError("Unable to connect to Prisma.")


async def disconnect_prisma():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            await prisma_client.disconnect(timeout=timedelta(seconds=20))
            LOG.info("Successfully disconnected from Prisma")
            break
        except Exception as e:
            LOG.error(f"Failed to disconnect to Prisma (Attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                await asyncio.sleep(3)
    else:
        LOG.error("Unable to disconnect to Prisma after multiple attempts.")
        raise RuntimeError("Unable to disconnect to Prisma.")

    
