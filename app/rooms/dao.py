# Работа с БД по комнатам (rooms)

from datetime import date

from sqlalchemy import and_, func, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.rooms.models import Rooms
from app.database import async_session_maker

class RoomsDAO(BaseDAO):
    model = Rooms


    # Получение списка номеров конкретного отеля со свободными комнатами на определенные даты
    @classmethod
    async def get_rooms_from_hotel(cls, 
                    hotel_id: int, 
                    date_from: date, 
                    date_to: date):
        
        # Кол-во дней проживания
        total_days = (date_to - date_from).days
        """
        -- Заезд '2023-05-15'
        -- Выезд '2023-09-20'

        WITH booked_rooms AS(
            SELECT room_id, COUNT(room_id) AS booked_rooms FROM bookings
            WHERE date_from <= '2023-09-20' AND date_to >= '2023-05-15'
            GROUP BY room_id
        )
        SELECT  rooms.*, (rooms. quantity - COALESCE(booked_rooms.booked_rooms, 0)) AS rooms_left FROM rooms
        LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE rooms.hotel_id = 3
        """

        # 1 часть запроса. Кол-во бронирований каждого номера
        booked_rooms = (
            select(Bookings.room_id, 
                   func.count(Bookings.room_id).label("booked_rooms"))
                   .select_from(Bookings)
                   .where(
                       and_(Bookings.date_from <= date_to,
                            Bookings.date_to >= date_from)
                   ).group_by(Bookings.room_id)
                   .cte("booked_rooms")
        )

        # 2 часть запроса. Получение таблицы номеров с кол-вом свободных номеров и итоговой ценой
        rooms_with_free_rooms = (
            select(Rooms.__table__.columns,
                   (Rooms.price * total_days).label("total_cost"),
                   (Rooms.quantity - func.coalesce(booked_rooms.c.booked_rooms, 0)).label("rooms_left"))
                   .select_from(Rooms)
                   .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                   .where(Rooms.hotel_id == hotel_id)
        )

        

        async with async_session_maker() as session:
            rooms_with_free_rooms = await session.execute(rooms_with_free_rooms)
            return rooms_with_free_rooms.mappings().all()


    
                
            
            


            
            
        