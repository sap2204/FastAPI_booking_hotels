# Схемы по комнатам

from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int


class SRoomsLeft(SRooms):
    total_cost: int
    rooms_left: int


