from sqlalchemy import JSON, Column, Integer, String
from app.database import Base 

# Создание модели таблицы
class Hotels(Base):
    __tablename__ = 'hotels' 

    # Названия стоблцов таблицы
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    location =Column(String, nullable = False)
    services =Column(JSON)
    rooms_quantity =Column(Integer, nullable = False)
    image_id = Column(Integer)