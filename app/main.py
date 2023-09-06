from datetime import date
from fastapi import FastAPI, Query
from typing import Optional 
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

class SHotel(BaseModel):
    address: str
    name: str 
    stars: int
    has_spa: bool

list[SHotel]
"""
@app.get("/hotels")
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: Optional[bool]=None,
    stars: Optional[int]=Query(None, ge=1, le=5)
) -> list[SHotel]:
    hotels = [
        {
            "address": "ул. Гагарина, 1, Алтай",
            "name": "Super Hotel",
            "stars": 5,
            "has_spa": "no"
        },

        {
            "address": "ул. Луначарского, 30, Тараз",
            "name": "Тараз Hotel",
            "stars": 4,
            "has_spa": "yes"
        }
    ]
    return hotels
"""





