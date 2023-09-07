from datetime import date
from fastapi import APIRouter
from app.exceptions import HotelNotFound
from app.hotels.schemas import SHotelsRoomsLeft
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels


router = APIRouter(
    prefix="/hotels",
    tags= ["Отели"],
)

# Эндпоинт получения списка отелей
@router.get("/{location}")
async def get_list_hotels(location: str, date_from: date, date_to: date) -> list[SHotelsRoomsLeft]:
    return await HotelsDAO.get_hotels_free_rooms(location, date_from, date_to)
    


# Эндпоинт получения конкретного отеля по id
@router.get("/{hotel_id}")
async def get_certain_hotel(hotel_id: int) -> SHotels:
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelNotFound
    return hotel
    