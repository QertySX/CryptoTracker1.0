from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///./CryptoTracker.db"

engine = create_async_engine(DATABASE_URL)

async def create_db_file():
    async with engine.connect() as conn:
        print('DB created')
        pass  

asyncio.run(create_db_file())
