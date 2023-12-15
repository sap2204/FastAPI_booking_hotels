from typing import Literal
from fastapi import APIRouter
from fastapi import UploadFile
import csv
import shutil

from sqlalchemy import insert, values
from app.exceptions import CannotLoadFileWithThisName, CannotOnvertCSVIntoBDFormat
from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelsDAO
import json
from datetime import datetime
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.rooms.models import Rooms



router = APIRouter(
    prefix="/import",
    tags=["Загрузка данных в БД"],
)


@router.post("/{table_name}", status_code=201)
async def import_dates_to_db(
    file: UploadFile,
    file_names: Literal['bookings', 'hotels', 'rooms']):

    # Названия таблиц в БД
    table_name = ['bookings', 'hotels', 'rooms']

    # Название файла, которое соответствует названиям таблиц в БД
    file_name = file.filename.split(".")[0]
    
    # Проверка на совпадение имени загружаемого файла с названиями таблиц в БД
    # и сохранение загружаемого файла
    if file_name not in table_name:
        raise CannotLoadFileWithThisName
    else:
        with open(f'{file.filename}', "wb") as buffer_file:
            shutil.copyfileobj(file.file, buffer_file)

    with open(f'{file.filename}', 'r', encoding="utf-8") as csv_file:
        reader = list(csv.DictReader(csv_file, delimiter=";"))
              
    try:
        data = []
        for line in reader:
            for key, value in line.items():
                if value.isdigit():
                    line[key] = int(value)
                elif key == "services":
                    line[key] = json.loads(value.replace("'", '"'))
                elif "date" in key:
                    line[key] = datetime.strptime(value, "%Y-%m-%d")       
                                                             
            data.append(line)
    except:
        raise CannotOnvertCSVIntoBDFormat
    
    for i in data:
        async with async_session_maker() as session:
            query = insert(Hotels)
            result = await session.execute(query, i)
            await session.commit()

    

    
   
  
    
    
    
    
    
     

   
        

    
        
       
        
        
    

    
   