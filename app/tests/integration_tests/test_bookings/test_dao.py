from app.bookings.dao import BookingDAO
from datetime import datetime


# Тестирование функции добавления и получения брони
async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id = 2,
        room_id = 2,
        date_from = datetime.strptime("2023-09-26", "%Y-%m-%d"),
        date_to = datetime.strptime("2023-09-30", "%Y-%m-%d")
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    # Поиск новой брони по id
    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None