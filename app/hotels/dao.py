# Работа с БД для отелей


from datetime import date

from sqlalchemy import and_, func, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker
from app.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels


    @classmethod
    async def get_hotels_location_dates(cls, location: str, date_from: date, date_to: date):
        location = location.strip().capitalize()

        """
         WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE date_from <= '2023-09-20' AND date_to >= '2023-05-15'
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            GROUP BY hotel_id
        )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%'
        """

        # Количество заброннированных комнат каждого типа номера
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked")).
            select_from(Bookings).
            where(
                and_(Bookings.date_from <= date_to,
                     Bookings.date_to >= date_from)
            ).group_by(Bookings.room_id).cte("booked_rooms")
        )

        # Количество свободных номеров в отелях
        booked_hotels = (
            select(Rooms.hotel_id, func.sum(
                Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left")
                ).select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .group_by(Rooms.hotel_id).cte("booked_hotels")
        )

        # Итоговый запрос по датам и месту
        get_hotels_with_rooms = (
            # Код ниже можно было бы расписать так:
            # select(
            #     Hotels
            #     booked_hotels.c.rooms_left,
            # )
            # Но используется конструкция Hotels.__table__.columns. Почему? Таким образом алхимия отдает
            # все столбцы по одному, как отдельный атрибут. Если передать всю модель Hotels и
            # один дополнительный столбец rooms_left, то будет проблематично для Pydantic распарсить
            # такую структуру данных. То есть проблема кроется именно в парсинге ответа алхимии 
            # Пайдентиком.
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%")
                )
            )
        )

        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()


    


                            


    
            
                       

