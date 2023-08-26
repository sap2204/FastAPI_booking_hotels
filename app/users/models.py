from sqlalchemy import Column, Integer, String
from app.database import Base

# создание модели таблицы пользователи
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

