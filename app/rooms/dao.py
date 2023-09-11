# Работа с БД по комнатам (rooms)

from datetime import date

from sqlalchemy import and_, func, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.rooms.models import Rooms
from app.database import async_session_maker

class RoomsDAO(BaseDAO):
    model = Rooms


    @classmethod
    async def get_list_rooms_free(cls, hotel_id: int, date_from: date, date_to: date):
        total_days = (date_to - date_from).days

        # SQL запрос на свободные комнаты конкретного отеля
        """
        -- ЗАЕЗД 2023-05-15
        -- ВЫЕЗД 2023-09-20

        WITH booked_rooms AS(
            SELECT room_id, COUNT(room_id) as booked_quantity FROM bookings
            WHERE date_from <= '2023-09-20' AND date_to >= '2023-05-15'
            GROUP BY room_id
        )
        SELECT 
        (rooms.quantity - booked_rooms.booked_quantity) as free_rooms FROM rooms
        LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE rooms.hotel_id = 1
        """

        async with async_session_maker() as session:
            # 1 часть запроса. Количество заброннированных номеров каждого типа на конкретные даты
            booked_rooms = select(
                Bookings.room_id, (func.count(Bookings.room_id)).label("booked_quantity")
            ).select_from(Bookings).where(
                and_(Bookings.date_from <= date_to,
                     Bookings.date_to >= date_from
                     )
            ).group_by(Bookings.room_id).cte("booked_rooms")

            # 2 часть запроса. Получение свободных номеров
            rooms_left = select(
                (Rooms.quantity - booked_rooms.c.booked_quantity).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).where(Rooms.hotel_id == hotel_id).subquery()

                          
            
            query = select(Rooms.__table__.columns, (rooms_left)).where(
                    Rooms.hotel_id == hotel_id)
            result = await session.execute(query)
            return result.mappings().all()
                
            
            


            
            
        