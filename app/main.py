from datetime import date, time
from fastapi import FastAPI, Request
from typing import Optional 
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin

from app.bookings.router import router as router_bookings
from app.config import settings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.rooms.router import router as router_rooms

from app.importer.router import router as router_import

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

from app.logger import logger
import time
import sentry_sdk

from fastapi_versioning import VersionedFastAPI

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Подключение Sentry для отлова ошибок
sentry_sdk.init(
    dsn="https://b8da497be2c5c2b30b7ed709cfdaefed@o4506042285490176.ingest.sentry.io/4506042601242624",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


# Подключение роутеров с эндпоинтами
app.include_router(router_import)
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

# Версионирование API
app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    #description='Greet users with a nice message',
    #middleware=[
        #Middleware(SessionMiddleware, secret_key='mysecretkey')
    #]
)


# Подключение сбора метрики
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)

instrumentator.instrument(app).expose(app)


# Подключение админки SQLAdmin
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


# Добавление Middleware для логирования
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    responce = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return responce


# Картинки для шаблонов страниц эндпоинтов
app.mount("/static", StaticFiles(directory="app/static"), "static")