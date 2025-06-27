from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pathlib


BASE_DIR = pathlib.Path(__file__).parent.resolve()
DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR / 'CryptoTracker.db'}"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# async def create_db_file():
#     async with engine.connect() as conn:
#         print('DB created')
#         pass

