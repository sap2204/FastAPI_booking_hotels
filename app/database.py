# Подключение к БД

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settiings

DATABASE_URL = settiings.get_database_url

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# класс для миграций. Все модели будут наследоваться от Base
class Base(DeclarativeBase):
    pass 


