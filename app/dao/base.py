# Базовый класс для работы с БД (юзеры, отели и т.д.)

from sqlalchemy import delete, insert, select
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.exceptions import CannotImportDataInDatabase
from app.hotels.models import Hotels
from app.rooms.models import Rooms


class BaseDAO:
    model = None

    # Метод поиска по id
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()


    # Метод поиска чего-то одного или возврат НИЧЕГО
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()


    # Метод получения ВСЕХ записей
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        
    
    # Добавление новой строки в БД
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    
    # Удаление строки из БД
    @classmethod
    async def delete(cls, **filter):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter)
            await session.execute(query)
            await session.commit()


# Множественная вставка данных из csv-файла
async def import_data_in_database(file_name, data):
    try:
        if file_name == "bookings":
            async with async_session_maker() as session:
                for i in data:
                    query = insert(Bookings)
                    result = await session.execute(query, i)
                await session.commit()
        

        if file_name == "hotels":
            async with async_session_maker() as session:
                for i in data:
                    query = insert(Hotels)
                    result = await session.execute(query, i)
                await session.commit()

        if file_name == "rooms":
            async with async_session_maker() as session:
                for i in data:
                    query = insert(Rooms)
                    result = await session.execute(query, i)
                await session.commit()

    except:
        raise CannotImportDataInDatabase

            
        