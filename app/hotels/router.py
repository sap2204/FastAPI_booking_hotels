from fastapi import APIRouter
from app.exceptions import HotelNotFound

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels


router = APIRouter(
    prefix="/hotels",
    tags= ["Отели"],
)


# Эндпоинт получения конкретного отеля по id
@router.get("/{hotel_id}")
async def get_certain_hotel(hotel_id: int) -> SHotels:
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelNotFound
    return hotel
    