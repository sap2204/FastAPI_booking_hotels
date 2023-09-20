from datetime import date
from fastapi import FastAPI
from typing import Optional 
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin

from app.bookings.router import router as router_bookings
from app.config import settings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.rooms.router import router as router_rooms

from app.pages.router import router as router_pages
from app.images.router import router as router_images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from sqladmin import Admin, ModelView
from app.database import engine
from app.users.models import Users

from app.admin.auth import authentication_backend

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

# Подключение роутеров с эндпоинтами
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)


# Подключение redis
@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


# Подключение админки SQLAdmin
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)

