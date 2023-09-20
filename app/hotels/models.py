from sqlalchemy import JSON, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


# в Base будет храниться инф-ия, что на бэкенде есть модель Hotels
class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    room = relationship("Rooms", back_populates="hotel")
    

    # Магический метод для понятного отображения отеля для пользователя
    def __str__(self):
        return f"Отель: {self.name}"
