from typing import Literal
from fastapi import APIRouter, Depends
from fastapi import UploadFile
import csv
import shutil

from sqlalchemy import insert, values
from app.bookings.models import Bookings
from app.dao.base import import_data_in_database
from app.exceptions import CannotLoadFileWithThisName
from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelsDAO
import json
from datetime import datetime
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.importer.support import convert_csv_file_in_postgres_format
from app.rooms.models import Rooms
from app.users.dependencies import get_current_user



router = APIRouter(
    prefix="/import",
    tags=["Загрузка данных в БД"],
)


@router.post("/{table_name}", 
             status_code=201,
             dependencies=[Depends(get_current_user)]
             )
async def import_dates_to_db(
    file: UploadFile,
    file_name: Literal['bookings', 'hotels', 'rooms']):

    # Названия таблиц в БД
    table_name = ['bookings', 'hotels', 'rooms']

    # Название файла, которое соответствует названиям таблиц в БД
    file_name = file.filename.split(".")[0]

    # Проверка допустимости названия файла    
    if file_name in table_name:
        # Сохранение загружаемого файла
        with open(f'{file.filename}', "wb") as buffer_file:
            shutil.copyfileobj(file.file, buffer_file)

        # Открытие загруженного csv-файла
        with open(f'{file.filename}', 'r', encoding="utf-8") as csv_file:
            csv_file = list(csv.DictReader(csv_file, delimiter=";"))
    else:
        raise CannotLoadFileWithThisName
    
    # Конвертация данных загруженного файла в формат БД
    data = convert_csv_file_in_postgres_format(csv_file)
    
    # Вставка данных в таблицу БД
    await import_data_in_database(file_name, data)
    
 
    

    
   
  
    
    
    
    
    
     

   
        

    
        
       
        
        
    

    
   