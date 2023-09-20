from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


# создание модели таблицы пользователи
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    booking = relationship("Bookings", back_populates="user")
    

    # Магический метод для понятного отображения информации пользователю 
    def __str__(self):
        return f"Клиент: {self.email}"

    

