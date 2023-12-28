from datetime import date
from fastapi import APIRouter, Depends, Request
from pydantic import TypeAdapter, parse_obj_as
from sqlalchemy import select
from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking, SBookingsWithRoomsDescription, SNewBooking
from fastapi_versioning import  version


from app.database import async_session_maker
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix= "/bookings",
    tags= ["Бронирования"],
)


# Эндпоинт получения бронирований конкретного юзера
@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


# Эндпоинт получения бронирований конкретного юзера с описанием комнаты
@router.get("/bookings")
async def get_bookings_user_with_rooms_desc(user: Users = Depends(get_current_user)) -> list[SBookingsWithRoomsDescription]:
    return await BookingDAO.get_bookings_with_rooms_description(user.id)
    

# Эндпоинт добавления бронирований
@router.post("")
@version(2)
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SBooking).validate_python(booking).model_dump()
    #send_booking_confirmation_email(booking, user.email)
    return booking
    

# Эндпоинт удаления брони зарегистрированным юзером
@router.delete("/{booking_id}")
async def delete_booking_by_auth_user(booking_id: int,
                                      current_user: Users = Depends(get_current_user)):
    await BookingDAO.delete(id = booking_id, user_id = current_user.id)
