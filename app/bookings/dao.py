# Работа с БД для бронирований

from datetime import date
from fastapi import Depends
from sqlalchemy import and_, delete, func, insert, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Rooms
from app.users.dependencies import get_current_user
from app.users.models import Users


class BookingDAO(BaseDAO):
    model = Bookings

    # Метод добавления бронирования
    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date,):
                 
        
        """
        
        WITH booked_rooms AS(
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_to <= '2023-05-15' OR date_from <= '2023-06-20' )
        )
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE rooms.id = 1
            GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(Bookings.room_id == room_id,
                    or_(Bookings.date_to <= date_from,
                        Bookings.date_from <= date_to
                        )
                    )
                ).cte("booked_rooms") # это первая часть запроса (ранее забронированные комнаты)
                
            get_rooms_left = select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                    ).select_from(Rooms).join(
                        booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                    ).where(Rooms.id == room_id).group_by(
                        Rooms.quantity, booked_rooms.c.room_id
                    )

            # Количество свободных комнат
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            # Проверка возможности бронирования комнаты
            if rooms_left > 0:
                
                # Запрос на получение цены за 1 день проживания
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar() # получение единственного значения (1 столбец, 1 строка)

                # Запрос на добавление брони
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings) # возвращение полностью строки, добавленной в БД

                # Выполнение запроса к БД
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None
            
    
    # Получение бронирований конкретного юзера с описанием номера
    @classmethod
    async def get_bookings_with_rooms_description(cls, user_id):
        """
        SELECT bookings.*, rooms.image_id, rooms.name, 
        rooms.description, rooms.services 
        FROM bookings
        LEFT JOIN rooms ON bookings.room_id = rooms.id
        WHERE bookings.user_id = 2
        """

                
        list_bookings = (
            select(Bookings.__table__.columns,
                   Rooms.image_id, Rooms.name, Rooms.description, Rooms.services)
                   .select_from(Bookings)
                   .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                   .where(Bookings.user_id == user_id)
        )

        async with async_session_maker() as session:
            list_bookings = await session.execute(list_bookings)
            return list_bookings.mappings().all()
        
    
    
                            

