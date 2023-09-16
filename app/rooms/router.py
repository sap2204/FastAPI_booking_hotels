from datetime import date
from fastapi import APIRouter
from app.rooms.dao import RoomsDAO
from app.rooms.schemas import SRoomsLeftTotalCost
from app.exceptions import DateFromCannotBeAfterDateTo
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/rooms",
    tags=["Номера"],
)


# Эндпоинт получения списка номеров по hotel_id и датам бронирования
@router.get("/{hotel_id}")
@cache(expire=30)
async def get_rooms_from_hotel(hotel_id: int, date_from: date, date_to: date) -> list[SRoomsLeftTotalCost]:
    rooms_with_free_rooms = await RoomsDAO.get_rooms_from_hotel(hotel_id, date_from, date_to)
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    return rooms_with_free_rooms