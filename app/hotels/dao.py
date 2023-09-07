# Работа с БД для отелей


from datetime import date

from sqlalchemy import and_, func, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.database import async_session_maker
from app.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels


    # Метод для получения списка отелей по месту, датам проживания с минимум 1 свободным номером
    @classmethod
    async def get_hotels_free_rooms(cls, location: str, date_from: date, date_to: date):
        location: str = location.strip().capitalize()
        """
        WITH booked_rooms AS ( 
        SELECT room_id , COUNT(room_id) as sum_rooms FROM bookings
        WHERE date_from <= '2023-09-20' AND date_to >= '2023-05-15'
        GROUP BY room_id
        )
        SELECT hotels.id, hotels.name, hotels.location, hotels.services, hotels.rooms_quantity,
        hotels.image_id, 
        (hotels.rooms_quantity - SUM(booked_rooms.sum_rooms)) as rooms_left
        FROM rooms
        LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        LEFT JOIN hotels ON hotels.id = rooms.hotel_id
        GROUP BY hotels.id
        HAVING (hotels.location LIKE '%Алтай%' AND (hotels.rooms_quantity - SUM(booked_rooms.sum_rooms)) >=1)
        """

        async with async_session_maker() as session:
            # 1 часть запроса. Количество бронирований каждого типа номера на переданные даты
            booked_rooms = select(
                                Bookings.room_id, (func.count(Bookings.room_id)).label("sum_rooms")
                                    ).select_from(Bookings).where(
                                        and_(Bookings.date_from <= date_to,
                                             Bookings.date_to >= date_from
                                            )
                                        ).group_by(Bookings.room_id).cte("booked_rooms")
            
            # 2 Часть запроса
            """
            SELECT hotels.id, hotels.name, hotels.location, hotels.services, hotels.rooms_quantity,
            hotels.image_id, 
            (hotels.rooms_quantity - SUM(booked_rooms.sum_rooms)) as rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
            LEFT JOIN hotels ON hotels.id = rooms.hotel_id
            GROUP BY hotels.id
            HAVING (hotels.location LIKE '%Алтай%' AND (hotels.rooms_quantity - SUM(booked_rooms.sum_rooms)) >=1)
            """

            get_hotels_rooms_left = select(
                Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity,
                Hotels.image_id, (Hotels.rooms_quantity - func.sum(booked_rooms.c.sum_rooms)).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).join(
                Hotels, Hotels.id == Rooms.hotel_id, isouter=True
            ).group_by(Hotels.id).having(
                and_(Hotels.location.ilike(f"%{location}%"),
                     (Hotels.rooms_quantity - func.sum(booked_rooms.c.sum_rooms)) >=1
                    )
            )

            hotels_rooms_left = await session.execute(get_hotels_rooms_left)
            return hotels_rooms_left.mappings().all()
                            
            
                         

