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


# Тест добавление, чтение и удаление брони из БД
async def test_add_read_delete_booking():
    # Добавление новой брони
    new_booking = await BookingDAO.add(
        user_id = 2,
        room_id = 2,
        date_from = datetime.strptime("2023-09-26", "%Y-%m-%d"),
        date_to = datetime.strptime("2023-09-30", "%Y-%m-%d")
    )

    # Чтение последней брони
    last_booking = await BookingDAO.find_by_id(4)
        
    # Удаление добавленной брони
    last_booking = await BookingDAO.delete(id=4)

    # Получение всех броней юзера с id=2
    users_bookings = await BookingDAO.find_all(user_id=2)
        
    # После удаления добавленной брони должна остаться 1 бронь
    assert len(users_bookings) == 1
 
    

    
