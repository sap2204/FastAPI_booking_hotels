from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_location_dates
from app.rooms.router import get_rooms_from_hotel


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)


templates = Jinja2Templates(directory="app/templates")


# Эндпоинт для графического отображения списка отелей
@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels = Depends(get_hotels_location_dates)
):
    return templates.TemplateResponse(
        name="hotels.html",
         context={"request": request, "hotels": hotels})


# Эндпоинт для графического отображения номеров отеля
@router.get("/rooms")
async def get_rooms_hotel_page(
    request: Request,
    rooms = Depends(get_rooms_from_hotel)
):
    return templates.TemplateResponse(
        name="rooms.html",
        context={"request": request, "rooms": rooms})
    


