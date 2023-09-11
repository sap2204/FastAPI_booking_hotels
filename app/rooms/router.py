from datetime import date
from fastapi import APIRouter
from app.rooms.dao import RoomsDAO


router = APIRouter(
    prefix="/rooms",
    tags=["Номера"],
)


# Эндпоинт получения списка номеров по hotel_id и датам бронирования
@router.get("/{hotel_id}")
async def get_list_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomsDAO.get_list_rooms_free(hotel_id, date_from, date_to)