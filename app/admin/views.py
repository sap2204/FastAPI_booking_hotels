
from sqladmin import ModelView
from app.bookings.models import Bookings

from app.users.models import Users


# Модель юзеров в админке
class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


# Модель бронирований в админке
class BookingsAdmin(ModelView, model = Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    name = "Бронь"
    name_plural = "Брони"