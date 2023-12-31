# Схема отеля для валидации отправляемых значений

from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int


# Схема отелей со свободными номерами
class SHotelsRoomsLeft(SHotels):
    rooms_left: int