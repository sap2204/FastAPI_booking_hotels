import asyncio
import json
from datetime import datetime

import pytest
from sqlalchemy import insert

# импорт моделей таблиц
from app.bookings.models import Bookings
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.users.models import Users

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app


# Создание фикстуры для создания таблиц в тестовой БД и наполнение их данными
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    # Удаление тестовых таблиц и создание новых
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Октрытие файлов с тестовыми данными
    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    # Получения данных по каждой сущности
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    # Запросы через Алхимию на вставку данных в таблицы
    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        # Отправка запросов на исполнение
        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Асинхронный клиент для тестирования эндпоинтов
@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


# Фикстура для сессии
@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session

