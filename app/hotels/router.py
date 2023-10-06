import asyncio
from datetime import date
from fastapi import APIRouter
from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo, HotelNotFound
from app.hotels.schemas import SHotelsRoomsLeft
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/hotels",
    tags= ["Отели"],
)


# Эндпоинт получения списка отелей
@router.get("/{location}")
#@cache(expire=30)
async def get_hotels_location_dates(location: str, date_from: date, date_to: date) -> list[SHotelsRoomsLeft]:  
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelsDAO.get_hotels_location_dates(location, date_from, date_to)
    return hotels

    
# Эндпоинт получения конкретного отеля по id
@router.get("/id/{hotel_id}")
async def get_certain_hotel(hotel_id: int) -> SHotels:
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelNotFound
    return hotel
    
