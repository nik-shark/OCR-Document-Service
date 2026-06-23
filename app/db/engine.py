import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{os.getenv('POSTGRES_USER')}:'
    f'{os.getenv('POSTGRES_PASSWORD')}@'
    f'db/'
    f'{os.getenv('POSTGRES_DB')}'
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db