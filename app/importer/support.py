from app.bookings.dao import BookingDAO
from app.exceptions import CannotOnvertCSVIntoBDFormat
from app.hotels.dao import HotelsDAO
from app.rooms.dao import RoomsDAO
import json
from datetime import datetime


# Конвертация данных загруженного файла в типы данных базы данных
def convert_csv_file_in_postgres_format(csv_file):
    try:
        data = []
        for line in csv_file:
            for key, value in line.items():
                if value.isdigit():
                    line[key] = int(value)
                elif key == "services":
                    line[key] = json.loads(value.replace("'", '"'))
                elif "date" in key:
                    line[key] = datetime.strptime(value, "%Y-%m-%d")       
                                                             
            data.append(line)
        return data
    except:
        raise CannotOnvertCSVIntoBDFormat