import shutil
from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


# Эндпоинт для загрузки картинок
@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"app/static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(f"app/static/images/{name}.webp")
