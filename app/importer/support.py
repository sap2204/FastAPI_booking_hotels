from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelsDAO
from app.rooms.dao import RoomsDAO


# Модели классов для работы с БД
TABLE_MODEL = {
    "bookings": BookingDAO,
    "hotels": HotelsDAO,
    "rooms": RoomsDAO
}